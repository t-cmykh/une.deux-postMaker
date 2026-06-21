import os
import sys

from scraper.search import fetch_page, extract_media
from scraper.export import export_media


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 60)
    print("  une·deux — Media Export")
    print("=" * 60)


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def exporter_selection(images: list[str], videos: list[str]):
    print(f"\n  --- Images ({len(images)}) ---")
    for i, img in enumerate(images, 1):
        print(f"    {i}. {img[:90]}")

    print(f"\n  --- Vidéos ({len(videos)}) ---")
    if videos:
        for i, vid in enumerate(videos, 1):
            print(f"    {i}. {vid[:90]}")
    else:
        print("    (aucune)")

    if not images and not videos:
        print("\n  Aucun média trouvé sur cette page.")
        return

    print("\n  Que voulez-vous exporter ?")
    print("  [i] Images seulement")
    print("  [v] Vidéos seulement")
    print("  [t] Tout (images + vidéos)")
    print("  [r] Annuler")
    choix = input("\n  Choix > ").strip().lower()

    if choix == "r":
        return

    urls_to_export = []
    if choix in ("i", "t"):
        urls_to_export.extend(images)
    if choix in ("v", "t"):
        urls_to_export.extend(videos)

    if not urls_to_export:
        print("  Rien à exporter.")
        return

    default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "une-deux-export")
    dest = input(f"\n  Dossier de destination [{default_dir}] > ").strip()
    if not dest:
        dest = default_dir

    print(f"\n  Export de {len(urls_to_export)} fichier(s) vers {dest}...\n")
    downloaded = export_media(urls_to_export, dest)
    print(f"\n  Terminé ! {len(downloaded)}/{len(urls_to_export)} fichier(s) téléchargé(s).")


def main():
    clear()
    print_header()

    while True:
        print("\n  Colle un lien de page web (ou 'q' pour quitter)")
        url = input("\n  URL > ").strip()

        if url.lower() == "q":
            print("\n  À bientôt !")
            sys.exit(0)

        if not url:
            continue

        url = normalize_url(url)
        print(f"\n  Chargement de {url}...")

        try:
            soup = fetch_page(url)
        except Exception as e:
            print(f"\n  Erreur : impossible de charger la page.\n  {e}")
            continue

        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        if title:
            print(f"  Page : {title}")

        images, videos = extract_media(soup, url)
        print(f"  Trouvé : {len(images)} images, {len(videos)} vidéos")

        exporter_selection(images, videos)


if __name__ == "__main__":
    main()
