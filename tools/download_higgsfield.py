#!/usr/bin/env python3
"""Télécharge des générations Higgsfield et, en option, les pousse dans Google
Drive en suivant le JSON d'un post (éditeur une·deux).

Deux modes
==========

1) Téléchargement simple (sans dépendance)
   Récupère des fichiers depuis leurs URLs CloudFront Higgsfield (rawUrl),
   en parallèle, avec réessais et reprise.

     python3 download_higgsfield.py                 # higgsfield_urls.txt -> ./higgsfield_downloads
     python3 download_higgsfield.py --list mes_urls.txt --out ~/Higgsfield
     python3 download_higgsfield.py --from-json generations.json
     python3 download_higgsfield.py https://.../image.png

2) Mode « post → Drive »  (--post-json)
   À partir du JSON d'un post (tableau de slides, ou {"slides":[...]}), le
   script lit dans l'ordre le champ `media` de chaque slide (ex. mbappe_01.jpg),
   associe **dans l'ordre** les images source que tu fournis (URLs Higgsfield
   ou fichiers locaux), les renomme selon le JSON, puis :
     - dérive le nom du post du préfixe des médias (mbappe_01 -> "mbappe") ;
     - crée un dossier <post> sous un dossier parent dans ton Drive ;
     - y téléverse les images.

     # URLs dans l'ordre des slides
     python3 download_higgsfield.py --post-json post.json --to-drive \\
         --drive-parent "une·deux/Posts" \\
         https://.../img1.png https://.../img2.png ...

     # ou via une liste (une URL/chemin par ligne, dans l'ordre)
     python3 download_higgsfield.py --post-json post.json --to-drive \\
         --drive-parent "une·deux/Posts" --list sources.txt

   Pré-requis Drive (mode --to-drive) : OAuth Google.
     pip install google-api-python-client google-auth-oauthlib
   Place un fichier credentials.json (OAuth client "Desktop") à côté du script
   (ou --credentials). Au 1er run, une fenêtre de consentement s'ouvre ; le
   jeton est mis en cache dans token.json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LIST = HERE / "higgsfield_urls.txt"
DEFAULT_OUT = Path.cwd() / "higgsfield_downloads"
UA = "higgsfield-downloader/1.0 (+https://higgsfield.ai)"
# Scope complet : nécessaire pour retrouver/créer un dossier parent existant
# (créé par toi dans l'UI) puis y écrire. drive.file ne verrait pas ces dossiers.
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]


# ----------------------------------------------------------------------------
# Sources d'URLs (mode simple)
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# Récupération d'un fichier (URL ou chemin local) vers une destination précise
# ----------------------------------------------------------------------------
def normalize_source(src: str) -> str:
    """Déballe les liens proxy Higgsfield (images.higgs.ai?...&url=<cloudfront>)
    pour récupérer l'URL directe pleine résolution. Laisse tout le reste tel quel.
    """
    if not src.lower().startswith(("http://", "https://")):
        return src
    try:
        p = urlparse(src)
        if p.netloc.endswith("images.higgs.ai"):
            inner = parse_qs(p.query).get("url", [None])[0]
            if inner and inner.startswith("http"):
                return inner  # parse_qs a déjà décodé le %xx
    except Exception:
        pass
    return src


def fetch_to(src: str, dest: Path, retries: int, overwrite: bool) -> tuple[str, str]:
    """src = URL http(s) ou chemin local. Retourne (statut, message)."""
    src = normalize_source(src)
    if dest.exists() and dest.stat().st_size > 0 and not overwrite:
        return "skip", dest.name

    dest.parent.mkdir(parents=True, exist_ok=True)

    # Source locale -> copie
    if not src.lower().startswith(("http://", "https://")):
        srcp = Path(src).expanduser()
        if not srcp.exists():
            return "error", f"{dest.name}: source locale introuvable ({src})"
        shutil.copyfile(srcp, dest)
        return "ok", f"{dest.name} ({dest.stat().st_size // 1024} Ko)"

    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err = ""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(src, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "wb") as fh:
                while True:
                    chunk = resp.read(1 << 16)
                    if not chunk:
                        break
                    fh.write(chunk)
            tmp.replace(dest)
            return "ok", f"{dest.name} ({dest.stat().st_size // 1024} Ko)"
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            last_err = str(exc)
            if tmp.exists():
                tmp.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(2 ** attempt)  # backoff 2s, 4s, 8s...
    return "error", f"{dest.name}: {last_err}"


def src_extension(src: str) -> str:
    base = os.path.basename(src.split("?", 1)[0])
    ext = os.path.splitext(base)[1]
    return ext or ".png"


# ----------------------------------------------------------------------------
# Mode simple : télécharge une liste d'URLs (nom = basename de l'URL)
# ----------------------------------------------------------------------------
def run_simple(urls: list[str], out_dir: Path, workers: int, retries: int, overwrite: bool) -> int:
    seen: set[str] = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]
    if not urls:
        print("Aucune URL à télécharger. Fournis --list, --from-json ou des URLs en argument.")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{len(urls)} fichier(s) -> {out_dir}\n")

    counts = {"ok": 0, "skip": 0, "error": 0}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        for u in urls:
            dest = out_dir / (os.path.basename(u.split("?", 1)[0]) or "download")
            futures[pool.submit(fetch_to, u, dest, retries, overwrite)] = u
        for fut in as_completed(futures):
            status, msg = fut.result()
            counts[status] += 1
            symbol = {"ok": "✓", "skip": "•", "error": "✗"}[status]
            print(f"  {symbol} {msg}")
    print(f"\nTerminé : {counts['ok']} téléchargé(s), {counts['skip']} ignoré(s), {counts['error']} échec(s).")
    return 0 if counts["error"] == 0 else 2


# ----------------------------------------------------------------------------
# Mode post : lecture du JSON, dérivation du nom, mapping dans l'ordre
# ----------------------------------------------------------------------------
def post_media_from_data(data) -> list[str]:
    """À partir d'un objet JSON déjà parsé : liste ordonnée des `media` non vides."""
    slides = data if isinstance(data, list) else (data.get("slides") if isinstance(data, dict) else None)
    if not isinstance(slides, list):
        raise ValueError('JSON invalide : attendu un tableau de slides ou {"slides":[...]}.')
    medias = []
    for s in slides:
        if isinstance(s, dict):
            m = s.get("media")
            if isinstance(m, str) and m.strip():
                medias.append(m.strip())
    return medias


def post_media_list(post_json: Path) -> list[str]:
    """Retourne, dans l'ordre des slides, les noms de fichiers `media` non vides."""
    return post_media_from_data(json.loads(post_json.read_text(encoding="utf-8")))


def derive_post_name(medias: list[str]) -> str:
    """mbappe_01.jpg -> 'mbappe'. Retire l'extension puis un éventuel _<digits> final."""
    if not medias:
        return "post"
    base = os.path.splitext(os.path.basename(medias[0]))[0]
    name = re.sub(r"[ _-]?\d+$", "", base).strip(" _-")
    return name or base or "post"


def target_name(media: str, src: str) -> str:
    """Nom de fichier cible = basename du media (sans ext) + extension de la source."""
    stem = os.path.splitext(os.path.basename(media))[0]
    return stem + src_extension(src)


# ----------------------------------------------------------------------------
# Google Drive (importé seulement si --to-drive)
# ----------------------------------------------------------------------------
def drive_service(creds_path: Path, token_path: Path):
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("Libs Google manquantes. Installe : pip install google-api-python-client google-auth-oauthlib")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), DRIVE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                sys.exit(f"credentials.json introuvable ({creds_path}). Crée un OAuth client 'Desktop' dans Google Cloud.")
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), DRIVE_SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return build("drive", "v3", credentials=creds)


def _q(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def drive_ensure_folder(svc, name: str, parent_id: str | None) -> str:
    q = (f"name='{_q(name)}' and mimeType='application/vnd.google-apps.folder' "
         f"and trashed=false")
    if parent_id:
        q += f" and '{parent_id}' in parents"
    res = svc.files().list(q=q, fields="files(id,name)", spaces="drive").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        meta["parents"] = [parent_id]
    return svc.files().create(body=meta, fields="id").execute()["id"]


def drive_ensure_path(svc, path: str) -> str | None:
    """Crée/retrouve l'arborescence 'a/b/c' à partir de la racine. None -> racine."""
    parent = None
    for seg in [p for p in path.split("/") if p.strip()]:
        parent = drive_ensure_folder(svc, seg.strip(), parent)
    return parent


def drive_upload(svc, local_path: Path, folder_id: str) -> str:
    from googleapiclient.http import MediaFileUpload
    name = local_path.name
    q = f"name='{_q(name)}' and '{folder_id}' in parents and trashed=false"
    res = svc.files().list(q=q, fields="files(id)", spaces="drive").execute()
    media = MediaFileUpload(str(local_path), resumable=True)
    if res.get("files"):
        fid = res["files"][0]["id"]
        svc.files().update(fileId=fid, media_body=media).execute()
        return "updated"
    meta = {"name": name, "parents": [folder_id]}
    svc.files().create(body=meta, media_body=media, fields="id").execute()
    return "created"


def run_post(args, sources: list[str]) -> int:
    medias = post_media_list(args.post_json)
    if not medias:
        print("Aucun champ 'media' trouvé dans le JSON du post.")
        return 1
    if not sources:
        print("Aucune source fournie. Donne des URLs/chemins (dans l'ordre) en argument ou via --list.")
        return 1

    post_name = args.name or derive_post_name(medias)
    n = min(len(sources), len(medias))
    if len(sources) != len(medias):
        print(f"⚠️  {len(sources)} source(s) vs {len(medias)} média(s) dans le JSON — "
              f"on associe les {n} premiers, dans l'ordre.")

    out_dir = args.out / post_name
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Post « {post_name} » — {n} fichier(s) -> {out_dir}\n")

    pairs = []  # (src, dest_path)
    for i in range(n):
        src = sources[i]
        dest = out_dir / target_name(medias[i], src)
        pairs.append((src, dest))

    counts = {"ok": 0, "skip": 0, "error": 0}
    local_ready: list[Path] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch_to, s, d, args.retries, args.overwrite): d for s, d in pairs}
        for fut in as_completed(futures):
            status, msg = fut.result()
            counts[status] += 1
            print(f"  {'✓' if status=='ok' else '•' if status=='skip' else '✗'} {msg}")
            if status in ("ok", "skip"):
                local_ready.append(futures[fut])
    print(f"\nLocal : {counts['ok']} récupéré(s), {counts['skip']} déjà présent(s), {counts['error']} échec(s).")

    if not args.to_drive:
        print("(--to-drive non demandé : pas d'envoi vers Drive.)")
        return 0 if counts["error"] == 0 else 2

    where = args.drive_parent_id if args.drive_parent_id else (args.drive_parent or "racine")
    print(f"\nDrive : dossier '{post_name}' sous {where} …")
    svc = drive_service(args.credentials, args.token)
    if args.drive_parent_id:
        parent_id = args.drive_parent_id            # ID fourni : pas de résolution de chemin
    elif args.drive_parent:
        parent_id = drive_ensure_path(svc, args.drive_parent)
    else:
        parent_id = None                            # racine de Mon Drive
    folder_id = drive_ensure_folder(svc, post_name, parent_id)
    up = {"created": 0, "updated": 0, "error": 0}
    for path in sorted(local_ready):
        try:
            res = drive_upload(svc, path, folder_id)
            up[res] += 1
            print(f"  ↑ {path.name} ({res})")
        except Exception as exc:  # noqa: BLE001
            up["error"] += 1
            print(f"  ✗ {path.name}: {exc}")
    print(f"\nDrive terminé : {up['created']} créé(s), {up['updated']} mis à jour, {up['error']} échec(s).")
    return 0 if (counts["error"] == 0 and up["error"] == 0) else 2


# ----------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Télécharge des générations Higgsfield ; option post → Drive.")
    ap.add_argument("sources", nargs="*", help="URLs (mode simple) ou URLs/chemins dans l'ordre (mode post).")
    ap.add_argument("--list", type=Path, help="Fichier de sources (une par ligne, dans l'ordre).")
    ap.add_argument("--from-json", type=Path, action="append", default=[],
                    help="Export JSON show_generations (extrait les rawUrl). Mode simple. Répétable.")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"Dossier de sortie local (défaut: {DEFAULT_OUT}).")
    ap.add_argument("--workers", type=int, default=5, help="Téléchargements parallèles (défaut: 5).")
    ap.add_argument("--retries", type=int, default=4, help="Réessais par fichier (défaut: 4).")
    ap.add_argument("--overwrite", action="store_true", help="Re-télécharger même si le fichier existe.")
    # --- mode post ---
    ap.add_argument("--post-json", type=Path, help="JSON du post : active le mode post (mapping dans l'ordre).")
    ap.add_argument("--name", help="Force le nom du post (sinon dérivé du préfixe des médias).")
    ap.add_argument("--to-drive", action="store_true", help="Téléverse le dossier du post dans Google Drive.")
    ap.add_argument("--drive-parent", default="une·deux/Posts",
                    help="Dossier parent Drive (par chemin) sous lequel créer <post> (défaut: 'une·deux/Posts'). '' = racine.")
    ap.add_argument("--drive-parent-id", default="",
                    help="ID d'un dossier Drive existant comme parent (prioritaire sur --drive-parent).")
    ap.add_argument("--credentials", type=Path, default=HERE / "credentials.json",
                    help="OAuth client 'Desktop' (défaut: credentials.json à côté du script).")
    ap.add_argument("--token", type=Path, default=HERE / "token.json",
                    help="Jeton OAuth mis en cache (défaut: token.json).")
    args = ap.parse_args()

    # Sources ordonnées : positionnels puis --list (l'ordre compte en mode post).
    sources: list[str] = list(args.sources)
    if args.list:
        sources += urls_from_text(args.list)
    # Déballe les liens proxy images.higgs.ai -> URL cloudfront pleine résolution.
    sources = [normalize_source(s) for s in sources]

    if args.post_json:
        return run_post(args, sources)

    # Mode simple
    urls = list(sources)
    for jpath in args.from_json:
        urls += urls_from_json(jpath)
    if not urls and not args.from_json and DEFAULT_LIST.exists():
        urls += [normalize_source(u) for u in urls_from_text(DEFAULT_LIST)]
    return run_simple(urls, args.out, args.workers, args.retries, args.overwrite)


if __name__ == "__main__":
    sys.exit(main())
