import json
import os
from urllib.parse import urlparse

SITES_FILE = os.path.join(os.path.dirname(__file__), "..", "sites.json")


def _load() -> list[str]:
    if not os.path.exists(SITES_FILE):
        return []
    with open(SITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(sites: list[str]) -> None:
    with open(SITES_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)


def _normalize(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def add_site(url: str) -> str:
    url = _normalize(url)
    parsed = urlparse(url)
    if not parsed.netloc:
        return f"URL invalide : {url}"
    sites = _load()
    if url in sites:
        return f"Déjà enregistré : {url}"
    sites.append(url)
    _save(sites)
    return f"Ajouté : {url}"


def remove_site(url: str) -> str:
    url = _normalize(url)
    sites = _load()
    if url not in sites:
        return f"Non trouvé : {url}"
    sites.remove(url)
    _save(sites)
    return f"Supprimé : {url}"


def list_sites() -> list[str]:
    return _load()
