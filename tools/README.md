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

## Mode « post → Drive »

À partir du JSON d'un post (éditeur une·deux), le script renomme les images
selon le champ `media` de chaque slide et les téléverse dans un dossier Drive
au nom du post.

- **Mapping** : tu fournis les images source **dans l'ordre des slides**
  (URLs Higgsfield ou chemins locaux) ; elles sont associées à `media[0]`,
  `media[1]`, … Les slides sans `media` sont ignorées.
- **Nom du dossier** : dérivé du préfixe des médias (`mbappe_01.jpg` →
  dossier `mbappe`). Forçable avec `--name`.
- **Emplacement** : sous un dossier parent (`--drive-parent`, défaut
  `une·deux/Posts`) ; mets `--drive-parent ""` pour la racine de Mon Drive.
  Plus fiable : `--drive-parent-id <ID>` pointe directement un dossier Drive
  existant (l'ID se lit dans l'URL du dossier : `.../folders/<ID>`) et a la
  priorité sur `--drive-parent`.

```bash
# URLs dans l'ordre des slides, envoi vers Drive
python3 download_higgsfield.py --post-json post.json --to-drive \
    --drive-parent "une·deux/Posts" \
    https://.../img1.png https://.../img2.png

# ou via une liste ordonnée (une URL/chemin par ligne)
python3 download_higgsfield.py --post-json post.json --to-drive --list sources.txt

# sans --to-drive : prépare juste le dossier local <post>/ renommé
python3 download_higgsfield.py --post-json post.json https://.../img1.png ...
```

> L'extension réelle de la source est conservée (`mbappe_01.png` même si le JSON
> dit `.jpg`) : l'éditeur matche par nom de base, donc ça reste compatible.

### Accès Google Drive (OAuth)

```bash
pip install google-api-python-client google-auth-oauthlib
```

1. Dans Google Cloud → API Drive activée → crée un **OAuth client « Desktop »**,
   télécharge le JSON et place-le en `credentials.json` à côté du script
   (ou `--credentials <chemin>`).
2. Au 1er run `--to-drive`, une fenêtre de consentement s'ouvre ; le jeton est
   mis en cache dans `token.json` (réutilisé ensuite).

`credentials.json` et `token.json` sont **ignorés par git** (voir `.gitignore`).
Ne les committe pas.

## Interface graphique (UI locale)

Pour ne pas taper de commandes, lance la petite UI web :

```bash
python ui.py
```

Une page s'ouvre sur `http://127.0.0.1:8765`. Tu y renseignes :
- **les liens** des images (un par ligne, dans l'ordre des slides ; cloudfront,
  lien `images.higgs.ai` ou chemin local) ;
- **le JSON du post** (collé) ;
- **le dossier Drive** (chemin `une·deux/Posts` ou ID), et un nom de post optionnel.

Clique **Lancer** : le workflow télécharge, renomme et (si la case est cochée)
téléverse dans un dossier `<post>` de ton Drive, avec le journal affiché en
direct et un lien vers le dossier. Mêmes pré-requis Drive que ci-dessus
(`credentials.json` + libs Google).

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
