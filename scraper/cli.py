import os
import sys

from scraper.sites import add_site, remove_site, list_sites
from scraper.search import search_site, PageResult
from scraper.export import export_media


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 60)
    print("  une·deux — Web Scraper & Media Export")
    print("=" * 60)


def menu_principal():
    print("\n  [1] Gérer les sites sources")
    print("  [2] Rechercher par mots-clés")
    print("  [3] Quitter")
    return input("\n  Choix > ").strip()


def menu_sites():
    while True:
        sites = list_sites()
        print(f"\n--- Sites enregistrés ({len(sites)}) ---")
        if sites:
            for i, s in enumerate(sites, 1):
                print(f"  {i}. {s}")
        else:
            print("  (aucun)")

        print("\n  [a] Ajouter un site")
        print("  [s] Supprimer un site")
        print("  [r] Retour")
        choix = input("\n  Choix > ").strip().lower()

        if choix == "a":
            url = input("  URL du site > ").strip()
            if url:
                print(f"  {add_site(url)}")
        elif choix == "s":
            if not sites:
                print("  Aucun site à supprimer.")
                continue
            idx = input(f"  Numéro du site (1-{len(sites)}) > ").strip()
            try:
                idx_int = int(idx) - 1
                if 0 <= idx_int < len(sites):
                    print(f"  {remove_site(sites[idx_int])}")
                else:
                    print("  Numéro invalide.")
            except ValueError:
                print("  Entrée invalide.")
        elif choix == "r":
            break


def afficher_resultats(results: list[PageResult]) -> list[PageResult]:
    print(f"\n--- {len(results)} page(s) trouvée(s) ---\n")
    for i, r in enumerate(results, 1):
        media_count = len(r.images) + len(r.videos)
        print(f"  {i}. [{r.score} pts] {r.title}")
        print(f"     {r.url}")
        print(f"     {r.snippet[:100]}")
        print(f"     Médias : {len(r.images)} images, {len(r.videos)} vidéos")
        print()
    return results


def menu_export(results: list[PageResult]):
    while True:
        print("  [num] Voir/exporter les médias d'une page (ex: 1)")
        print("  [all] Exporter tous les médias de toutes les pages")
        print("  [r]   Retour")
        choix = input("\n  Choix > ").strip().lower()

        if choix == "r":
            break
        elif choix == "all":
            all_images = []
            all_videos = []
            for r in results:
                all_images.extend(r.images)
                all_videos.extend(r.videos)
            exporter_selection(all_images, all_videos)
        else:
            try:
                idx = int(choix) - 1
                if 0 <= idx < len(results):
                    page = results[idx]
                    print(f"\n  Page : {page.title}")
                    print(f"  URL  : {page.url}")
                    exporter_selection(page.images, page.videos)
                else:
                    print("  Numéro invalide.")
            except ValueError:
                print("  Entrée invalide.")


def exporter_selection(images: list[str], videos: list[str]):
    print(f"\n  Images disponibles : {len(images)}")
    for i, img in enumerate(images[:20], 1):
        print(f"    {i}. {img[:90]}")
    if len(images) > 20:
        print(f"    ... et {len(images) - 20} de plus")

    print(f"\n  Vidéos disponibles : {len(videos)}")
    for i, vid in enumerate(videos[:10], 1):
        print(f"    {i}. {vid[:90]}")
    if len(videos) > 10:
        print(f"    ... et {len(videos) - 10} de plus")

    if not images and not videos:
        print("  Aucun média trouvé sur cette page.")
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


def menu_recherche():
    sites = list_sites()
    if not sites:
        print("\n  Aucun site enregistré. Ajoutez d'abord des sites sources.")
        return

    keywords_input = input("\n  Mots-clés (séparés par des espaces) > ").strip()
    if not keywords_input:
        return
    keywords = keywords_input.split()

    max_pages_input = input("  Pages max par site [30] > ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else 30

    all_results: list[PageResult] = []

    for site in sites:
        print(f"\n  Scan de {site}...")
        results = search_site(site, keywords, max_pages=max_pages)
        print(f"  -> {len(results)} résultat(s)")
        all_results.extend(results)

    all_results.sort(key=lambda r: r.score, reverse=True)

    if not all_results:
        print("\n  Aucun résultat trouvé pour ces mots-clés.")
        return

    afficher_resultats(all_results)
    menu_export(all_results)


def main():
    clear()
    print_header()

    while True:
        choix = menu_principal()
        if choix == "1":
            menu_sites()
        elif choix == "2":
            menu_recherche()
        elif choix == "3":
            print("\n  À bientôt !")
            sys.exit(0)
        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    main()
