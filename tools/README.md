# Téléchargeur de générations Higgsfield

`download_higgsfield.py` récupère en local tes générations Higgsfield
(images/vidéos) depuis leurs URLs CloudFront directes. Python 3, **aucune
dépendance** à installer.

## Utilisation

```bash
# Télécharge tout ce qui est listé dans higgsfield_urls.txt
python3 download_higgsfield.py

# Dossier de sortie personnalisé
python3 download_higgsfield.py --out ~/Higgsfield

# Depuis un export JSON de l'outil show_generations (extrait les rawUrl)
python3 download_higgsfield.py --from-json generations.json

# Une ou plusieurs URLs directes
python3 download_higgsfield.py https://.../image.png
```

Options : `--list <fichier>`, `--out <dossier>`, `--workers N` (parallélisme),
`--retries N`, `--overwrite`.

## La liste d'URLs

`higgsfield_urls.txt` contient une URL par ligne (`#` = commentaire). Elle est
pré-remplie avec les générations récentes. Pour la rafraîchir ou l'étendre :

- ajoute simplement des lignes (n'importe quelle `rawUrl` Higgsfield), ou
- demande à Claude de régénérer la liste via l'outil `show_generations`, ou
- sauvegarde un export JSON `show_generations` et passe-le avec `--from-json`.

## Notes

- Les fichiers déjà téléchargés (taille > 0) sont **ignorés** : relancer le
  script ne refait que ce qui manque.
- Les noms de fichiers reprennent ceux de Higgsfield
  (`hf_<date>_<id>.png`), donc pas de collision entre générations.
