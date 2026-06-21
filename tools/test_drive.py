#!/usr/bin/env python3
"""Test rapide de l'accès Google Drive (OAuth).

Se connecte, crée un dossier de test dans ton Drive et affiche son lien.
À lancer sur TA machine, dans le dossier tools/ (avec credentials.json à côté).

    python3 test_drive.py
    python3 test_drive.py --parent-id <ID>     # créer le test sous un dossier précis
    python3 test_drive.py --parent "une·deux/Posts"

Si ça marche, l'OAuth est bon : tu peux utiliser download_higgsfield.py --to-drive.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Réutilise la logique Drive du script principal.
from download_higgsfield import (
    drive_service,
    drive_ensure_folder,
    drive_ensure_path,
    HERE,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Teste la connexion Google Drive (OAuth).")
    ap.add_argument("--name", default="postmaker_test", help="Nom du dossier de test à créer.")
    ap.add_argument("--parent", default="", help="Dossier parent par chemin (ex. 'une·deux/Posts').")
    ap.add_argument("--parent-id", default="", help="ID d'un dossier parent (prioritaire).")
    ap.add_argument("--credentials", type=Path, default=HERE / "credentials.json")
    ap.add_argument("--token", type=Path, default=HERE / "token.json")
    args = ap.parse_args()

    print("Connexion à Google Drive (une fenêtre de consentement peut s'ouvrir au 1er run)…")
    svc = drive_service(args.credentials, args.token)
    print("✓ Authentifié.")

    if args.parent_id:
        parent_id = args.parent_id
    elif args.parent:
        parent_id = drive_ensure_path(svc, args.parent)
        print(f"✓ Dossier parent prêt : {args.parent}")
    else:
        parent_id = None  # racine de Mon Drive

    folder_id = drive_ensure_folder(svc, args.name, parent_id)
    print(f"✓ Dossier de test créé/retrouvé : « {args.name} »")
    print(f"  ID   : {folder_id}")
    print(f"  Lien : https://drive.google.com/drive/folders/{folder_id}")
    print("\nTout est bon ✅ — l'upload via download_higgsfield.py --to-drive fonctionnera.")
    print("(Tu peux supprimer ce dossier de test dans ton Drive.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
