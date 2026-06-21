import re
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
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


def _fetch(url: str) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.content, "lxml")
    except Exception:
        return None


def _extract_links(soup: BeautifulSoup, base_url: str, site_root: str) -> list[str]:
    links = set()
    parsed_root = urlparse(site_root)
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        parsed = urlparse(href)
        if parsed.netloc == parsed_root.netloc:
            clean = parsed._replace(fragment="").geturl()
            links.add(clean)
    return list(links)


def _score_page(soup: BeautifulSoup, keywords: list[str]) -> tuple[int, str]:
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    text = soup.get_text(separator=" ", strip=True).lower()

    score = 0
    snippet_parts = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title.lower():
            score += 10
        count = text.count(kw_lower)
        score += count
        match = re.search(
            rf".{{0,60}}{re.escape(kw_lower)}.{{0,60}}",
            text,
        )
        if match:
            snippet_parts.append("…" + match.group() + "…")

    snippet = " | ".join(snippet_parts[:3]) if snippet_parts else title[:120]
    return score, snippet


def _extract_media(soup: BeautifulSoup, base_url: str) -> tuple[list[str], list[str]]:
    images: list[str] = []
    videos: list[str] = []

    for img in soup.find_all("img", src=True):
        src = urljoin(base_url, img["src"])
        if src not in images:
            images.append(src)
    for source in soup.find_all("source", src=True):
        src = urljoin(base_url, source["src"])
        if any(src.lower().endswith(ext) for ext in (".mp4", ".webm", ".ogg", ".mov")):
            if src not in videos:
                videos.append(src)
    for video in soup.find_all("video", src=True):
        src = urljoin(base_url, video["src"])
        if src not in videos:
            videos.append(src)

    for tag in soup.find_all(["img", "source", "video"], attrs={"data-src": True}):
        src = urljoin(base_url, tag["data-src"])
        if any(src.lower().endswith(ext) for ext in (".mp4", ".webm", ".ogg", ".mov")):
            if src not in videos:
                videos.append(src)
        elif src not in images:
            images.append(src)

    return images, videos


def search_site(site_url: str, keywords: list[str], max_pages: int = 30) -> list[PageResult]:
    results: list[PageResult] = []
    visited: set[str] = set()
    to_visit: list[str] = [site_url]

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        soup = _fetch(url)
        if soup is None:
            continue

        score, snippet = _score_page(soup, keywords)
        if score > 0:
            images, videos = _extract_media(soup, url)
            title = soup.title.string.strip() if soup.title and soup.title.string else url
            results.append(PageResult(
                url=url,
                title=title,
                score=score,
                snippet=snippet,
                images=images,
                videos=videos,
            ))

        new_links = _extract_links(soup, url, site_url)
        for link in new_links:
            if link not in visited:
                to_visit.append(link)

    results.sort(key=lambda r: r.score, reverse=True)
    return results
