import os
import re
from urllib.parse import urlparse, unquote

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}
TIMEOUT = 30


def _safe_filename(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(unquote(parsed.path))
    if not name or name == "/":
        name = parsed.netloc.replace(".", "_")
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    if not os.path.splitext(name)[1]:
        name += ".jpg"
    return name


def download_file(url: str, dest_dir: str) -> str | None:
    os.makedirs(dest_dir, exist_ok=True)
    filename = _safe_filename(url)
    filepath = os.path.join(dest_dir, filename)

    counter = 1
    base, ext = os.path.splitext(filepath)
    while os.path.exists(filepath):
        filepath = f"{base}_{counter}{ext}"
        counter += 1

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return filepath
    except Exception as e:
        print(f"  Erreur téléchargement {url}: {e}")
        return None


def export_media(urls: list[str], dest_dir: str) -> list[str]:
    downloaded = []
    total = len(urls)
    for i, url in enumerate(urls, 1):
        print(f"  [{i}/{total}] {url[:80]}...")
        path = download_file(url, dest_dir)
        if path:
            downloaded.append(path)
            print(f"    -> {path}")
    return downloaded
