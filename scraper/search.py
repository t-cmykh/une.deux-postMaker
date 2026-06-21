import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
TIMEOUT = 15


def fetch_page(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "lxml")


def extract_media(soup: BeautifulSoup, page_url: str) -> tuple[list[str], list[str]]:
    images: list[str] = []
    videos: list[str] = []
    seen: set[str] = set()

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
                        src = urljoin(page_url, parts[0])
                        if src not in seen:
                            seen.add(src)
                            images.append(src)
            else:
                src = urljoin(page_url, val)
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
                        src = urljoin(page_url, parts[0])
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
                src = urljoin(page_url, val)
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
