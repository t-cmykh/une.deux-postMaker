#!/usr/bin/env python3
"""Télécharge en local des générations Higgsfield à partir de leurs URLs.

Higgsfield expose chaque résultat via une URL CloudFront directe (rawUrl).
Ce script récupère ces fichiers (images ou vidéos), en parallèle, avec
réessais et reprise (les fichiers déjà présents sont ignorés).

Sources d'URLs (au choix, cumulables) :
  - un fichier texte (une URL par ligne, '#' = commentaire) ;
  - un ou plusieurs exports JSON de l'outil `show_generations`
    (le script en extrait automatiquement tous les `rawUrl`) ;
  - des URLs passées directement en argument.

Exemples
--------
  # Liste par défaut (higgsfield_urls.txt à côté du script)
  python3 download_higgsfield.py

  # Liste personnalisée + dossier de sortie
  python3 download_higgsfield.py --list mes_urls.txt --out ~/Higgsfield

  # Depuis un export JSON de show_generations
  python3 download_higgsfield.py --from-json generations.json

  # Une ou plusieurs URLs directes
  python3 download_higgsfield.py https://.../image.png https://.../video.mp4
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LIST = HERE / "higgsfield_urls.txt"
DEFAULT_OUT = Path.cwd() / "higgsfield_downloads"
UA = "higgsfield-downloader/1.0 (+https://higgsfield.ai)"


def urls_from_text(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def urls_from_json(path: Path) -> list[str]:
    """Extrait récursivement toutes les valeurs `rawUrl` d'un export JSON."""
    data = json.loads(path.read_text(encoding="utf-8"))
    found: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "rawUrl" and isinstance(v, str) and v.startswith("http"):
                    found.append(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return found


def download_one(url: str, out_dir: Path, retries: int, overwrite: bool) -> tuple[str, str]:
    """Retourne (statut, message). statut ∈ {ok, skip, error}."""
    name = os.path.basename(url.split("?", 1)[0]) or "download"
    dest = out_dir / name
    if dest.exists() and dest.stat().st_size > 0 and not overwrite:
        return "skip", name

    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err = ""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "wb") as fh:
                while True:
                    chunk = resp.read(1 << 16)
                    if not chunk:
                        break
                    fh.write(chunk)
            tmp.replace(dest)
            return "ok", f"{name} ({dest.stat().st_size // 1024} Ko)"
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            last_err = str(exc)
            if tmp.exists():
                tmp.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(2 ** attempt)  # backoff 2s, 4s, 8s...
    return "error", f"{name}: {last_err}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Télécharge des générations Higgsfield.")
    ap.add_argument("urls", nargs="*", help="URLs à télécharger directement.")
    ap.add_argument("--list", type=Path, help=f"Fichier d'URLs (défaut: {DEFAULT_LIST.name} s'il existe).")
    ap.add_argument("--from-json", type=Path, action="append", default=[],
                    help="Export JSON de show_generations (extrait les rawUrl). Répétable.")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"Dossier de sortie (défaut: {DEFAULT_OUT}).")
    ap.add_argument("--workers", type=int, default=5, help="Téléchargements parallèles (défaut: 5).")
    ap.add_argument("--retries", type=int, default=4, help="Réessais par fichier (défaut: 4).")
    ap.add_argument("--overwrite", action="store_true", help="Re-télécharger même si le fichier existe.")
    args = ap.parse_args()

    urls: list[str] = list(args.urls)
    for jpath in args.from_json:
        urls += urls_from_json(jpath)
    if args.list:
        urls += urls_from_text(args.list)
    elif not urls and not args.from_json and DEFAULT_LIST.exists():
        urls += urls_from_text(DEFAULT_LIST)

    # Déduplique en gardant l'ordre.
    seen: set[str] = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]

    if not urls:
        print("Aucune URL à télécharger. Fournis --list, --from-json ou des URLs en argument.")
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"{len(urls)} fichier(s) -> {args.out}\n")

    counts = {"ok": 0, "skip": 0, "error": 0}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(download_one, u, args.out, args.retries, args.overwrite): u for u in urls}
        for fut in as_completed(futures):
            status, msg = fut.result()
            counts[status] += 1
            symbol = {"ok": "✓", "skip": "•", "error": "✗"}[status]
            print(f"  {symbol} {msg}")
            if status == "error":
                errors.append(msg)

    print(f"\nTerminé : {counts['ok']} téléchargé(s), {counts['skip']} ignoré(s), {counts['error']} échec(s).")
    if errors:
        print("Échecs :")
        for e in errors:
            print(f"  - {e}")
    return 0 if counts["error"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
