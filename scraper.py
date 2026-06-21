#!/usr/bin/env python3
"""Scrape images (jpg, png) and videos (mp4) from a given web page."""

import argparse
import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_media_urls(page_url: str) -> list[str]:
    resp = requests.get(page_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    urls = set()

    for img in soup.find_all("img", src=True):
        urls.add(urljoin(page_url, img["src"]))
    for source in soup.find_all("source", src=True):
        urls.add(urljoin(page_url, source["src"]))
    for video in soup.find_all("video", src=True):
        urls.add(urljoin(page_url, video["src"]))
    for a in soup.find_all("a", href=True):
        urls.add(urljoin(page_url, a["href"]))

    # srcset
    for tag in soup.find_all(attrs={"srcset": True}):
        for entry in tag["srcset"].split(","):
            url_part = entry.strip().split()[0]
            urls.add(urljoin(page_url, url_part))

    # og:image / og:video meta tags
    for meta in soup.find_all("meta", attrs={"property": re.compile(r"og:(image|video)")}):
        content = meta.get("content")
        if content:
            urls.add(urljoin(page_url, content))

    return [u for u in urls if has_valid_extension(u)]


def has_valid_extension(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in EXTENSIONS)


def download(url: str, dest_dir: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ✗ {url} — {e}")
        return None

    filename = os.path.basename(urlparse(url).path)
    if not filename:
        return None

    filepath = os.path.join(dest_dir, filename)
    counter = 1
    base, ext = os.path.splitext(filepath)
    while os.path.exists(filepath):
        filepath = f"{base}_{counter}{ext}"
        counter += 1

    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    size_kb = os.path.getsize(filepath) / 1024
    print(f"  ✓ {filename} ({size_kb:.1f} KB)")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Download images and videos from a web page.")
    parser.add_argument("url", help="URL of the page to scrape")
    parser.add_argument("-o", "--output", default="./downloads", help="Output directory (default: ./downloads)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    print(f"Scanning {args.url} ...")
    media_urls = get_media_urls(args.url)
    print(f"Found {len(media_urls)} media file(s) (jpg/png/mp4)\n")

    downloaded = 0
    for url in sorted(media_urls):
        result = download(url, args.output)
        if result:
            downloaded += 1

    print(f"\nDone — {downloaded}/{len(media_urls)} files saved to {args.output}")


if __name__ == "__main__":
    main()
