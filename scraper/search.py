import re
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse, quote
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
TIMEOUT = 15


@dataclass
class PageResult:
    url: str
    title: str
    score: int
    snippet: str
    images: list[str] = field(default_factory=list)
    videos: list[str] = field(default_factory=list)


def _fetch(url: str, verbose: bool = False) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        return BeautifulSoup(resp.content, "lxml")
    except Exception as e:
        if verbose:
            print(f"    [!] Erreur fetch {url}: {e}")
        return None


def _fetch_raw(url: str, verbose: bool = False) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        if verbose:
            print(f"    [!] Erreur fetch {url}: {e}")
        return None


def _get_sitemap_urls(site_url: str, keywords: list[str], max_sitemap_urls: int = 500, verbose: bool = False) -> list[str]:
    urls = []
    parsed = urlparse(site_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    kw_lower = [kw.lower() for kw in keywords]

    sitemap_candidates = [
        f"{base}/sitemap.xml",
        f"{base}/sitemap_index.xml",
        f"{base}/sitemap/sitemap.xml",
    ]

    robots_sitemaps = []
    robots_url = f"{base}/robots.txt"
    robots_text = _fetch_raw(robots_url, verbose)
    if robots_text:
        for line in robots_text.splitlines():
            if line.lower().startswith("sitemap:"):
                sm_url = line.split(":", 1)[1].strip()
                if sm_url:
                    robots_sitemaps.append(sm_url)
                    if verbose:
                        print(f"    [sitemap] trouvé dans robots.txt: {sm_url}")

    all_candidates = robots_sitemaps + sitemap_candidates

    for sm_url in all_candidates:
        if verbose:
            print(f"    [sitemap] chargement de {sm_url[:70]}...")
        xml_text = _fetch_raw(sm_url, verbose)
        if not xml_text:
            continue
        try:
            xml_text_clean = re.sub(r'\sxmlns="[^"]+"', '', xml_text, count=1)
            root = ET.fromstring(xml_text_clean)

            sub_sitemaps = root.findall(".//sitemap/loc")
            if sub_sitemaps:
                relevant_subs = []
                other_subs = []
                for sitemap_tag in sub_sitemaps:
                    if not sitemap_tag.text:
                        continue
                    sub_url = sitemap_tag.text.strip()
                    if any(kw in sub_url.lower() for kw in kw_lower):
                        relevant_subs.append(sub_url)
                    else:
                        other_subs.append(sub_url)

                ordered_subs = relevant_subs + other_subs[:5]
                if verbose:
                    print(f"    [sitemap] {len(sub_sitemaps)} sous-sitemaps, scan de {len(ordered_subs)}...")

                for sub_url in ordered_subs:
                    if len(urls) >= max_sitemap_urls:
                        break
                    if verbose:
                        print(f"    [sitemap]   -> {sub_url[:70]}...")
                    sub_xml = _fetch_raw(sub_url, verbose)
                    if not sub_xml:
                        continue
                    sub_clean = re.sub(r'\sxmlns="[^"]+"', '', sub_xml, count=1)
                    try:
                        sub_root = ET.fromstring(sub_clean)
                        for loc in sub_root.findall(".//url/loc"):
                            if loc.text:
                                urls.append(loc.text.strip())
                                if len(urls) >= max_sitemap_urls:
                                    break
                    except ET.ParseError:
                        pass

            for loc in root.findall(".//url/loc"):
                if loc.text:
                    urls.append(loc.text.strip())
                    if len(urls) >= max_sitemap_urls:
                        break

            if urls:
                if verbose:
                    print(f"    [sitemap] {len(urls)} URLs collectées")
                break
        except ET.ParseError:
            continue

    return urls


def _extract_links(soup: BeautifulSoup, base_url: str, site_root: str) -> list[str]:
    links = set()
    parsed_root = urlparse(site_root)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.netloc == parsed_root.netloc:
            clean = parsed._replace(fragment="").geturl()
            links.add(clean)
    return list(links)


def _score_page(soup: BeautifulSoup, keywords: list[str]) -> tuple[int, str]:
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    og_title = ""
    og_tag = soup.find("meta", attrs={"property": "og:title"})
    if og_tag and og_tag.get("content"):
        og_title = og_tag["content"].strip()

    text = soup.get_text(separator=" ", strip=True).lower()
    searchable = f"{title} {meta_desc} {og_title} {text}".lower()

    score = 0
    snippet_parts = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title.lower():
            score += 10
        if kw_lower in meta_desc.lower():
            score += 5
        if kw_lower in og_title.lower():
            score += 5
        count = searchable.count(kw_lower)
        score += count
        match = re.search(
            rf".{{0,60}}{re.escape(kw_lower)}.{{0,60}}",
            searchable,
        )
        if match:
            snippet_parts.append("…" + match.group() + "…")

    snippet = " | ".join(snippet_parts[:3]) if snippet_parts else (meta_desc or title)[:120]
    return score, snippet


def _extract_media(soup: BeautifulSoup, base_url: str) -> tuple[list[str], list[str]]:
    images: list[str] = []
    videos: list[str] = []
    seen = set()

    img_attrs = ["src", "data-src", "data-lazy-src", "data-original", "srcset"]
    for img in soup.find_all("img"):
        for attr in img_attrs:
            val = img.get(attr)
            if not val:
                continue
            if attr == "srcset":
                for entry in val.split(","):
                    parts = entry.strip().split()
                    if parts:
                        src = urljoin(base_url, parts[0])
                        if src not in seen:
                            seen.add(src)
                            images.append(src)
            else:
                src = urljoin(base_url, val)
                if src not in seen:
                    seen.add(src)
                    images.append(src)

    for pic in soup.find_all("picture"):
        for source in pic.find_all("source"):
            srcset = source.get("srcset")
            if srcset:
                for entry in srcset.split(","):
                    parts = entry.strip().split()
                    if parts:
                        src = urljoin(base_url, parts[0])
                        if src not in seen:
                            seen.add(src)
                            images.append(src)

    css_bg = re.findall(r'url\(["\']?(https?://[^"\')\s]+)["\']?\)', str(soup))
    for src in css_bg:
        if any(src.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif")):
            if src not in seen:
                seen.add(src)
                images.append(src)

    video_exts = (".mp4", ".webm", ".ogg", ".mov", ".m4v")
    for tag in soup.find_all(["video", "source"]):
        for attr in ["src", "data-src"]:
            val = tag.get(attr)
            if val:
                src = urljoin(base_url, val)
                if src not in seen and any(src.lower().endswith(ext) for ext in video_exts):
                    seen.add(src)
                    videos.append(src)

    for iframe in soup.find_all("iframe", src=True):
        src = iframe["src"]
        if any(domain in src for domain in ("youtube.com", "vimeo.com", "dailymotion.com")):
            if src not in seen:
                seen.add(src)
                videos.append(src)

    return images, videos


def search_site(site_url: str, keywords: list[str], max_pages: int = 30, verbose: bool = True) -> list[PageResult]:
    results: list[PageResult] = []
    visited: set[str] = set()
    to_visit: list[str] = [site_url]

    if verbose:
        print(f"    [1/3] Recherche du sitemap...")

    sitemap_urls = _get_sitemap_urls(site_url, keywords, verbose=verbose)
    if sitemap_urls:
        if verbose:
            print(f"    [sitemap] {len(sitemap_urls)} pages découvertes")
        kw_lower = [kw.lower() for kw in keywords]
        prioritized = []
        others = []
        for url in sitemap_urls:
            if any(kw in url.lower() for kw in kw_lower):
                prioritized.append(url)
            else:
                others.append(url)
        to_visit = prioritized + [site_url] + others
    else:
        if verbose:
            print(f"    [sitemap] Aucun sitemap trouvé, crawl classique...")

    if verbose:
        print(f"    [2/3] Scan des pages (max {max_pages})...")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        if verbose:
            print(f"    [{len(visited)}/{max_pages}] {url[:70]}...", end="")

        soup = _fetch(url, verbose)
        if soup is None:
            if verbose:
                print(" ERREUR")
            continue

        score, snippet = _score_page(soup, keywords)
        if verbose:
            print(f" score={score}")

        if score > 0:
            images, videos = _extract_media(soup, url)
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            if not title:
                title = url
            results.append(PageResult(
                url=url,
                title=title,
                score=score,
                snippet=snippet,
                images=images,
                videos=videos,
            ))

        if not sitemap_urls:
            new_links = _extract_links(soup, url, site_url)
            for link in new_links:
                if link not in visited:
                    to_visit.append(link)

    if verbose:
        print(f"    [3/3] {len(results)} résultat(s) avec correspondance")

    results.sort(key=lambda r: r.score, reverse=True)
    return results
