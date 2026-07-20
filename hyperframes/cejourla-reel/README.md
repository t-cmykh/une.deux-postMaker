# Prototype — HyperFrames × Ce jour-là (reel)

Preuve de concept : produire un reel vertical 9:16 en MP4 directement via la
CLI [HyperFrames](https://hyperframes.heygen.com), avec la DA du template
série `editeurs/editeur-series_2.html` (typo, couleurs) — layout retravaillé
pour le format vidéo au fil des itérations (voir `git log -- index.html`).

**Contenu de test** : le post "Ce jour-là" du 21 juillet 2026 (Haaland, né à
Leeds), tiré des brouillons Gmail (`POST DU JOUR — 21 juillet 2026` +
l'éphéméride source à 5 options, option 3 validée ✅). Toutes les infos du
`CORPS` sont reprises (père à Leeds United, mère championne d'heptathlon,
retour à Bryne, 62 buts/54 sélections, quarts 2026 contre Irak/Sénégal/
Côte d'Ivoire/Brésil, élimination 2-1 face à l'Angleterre).

## État actuel (dernière itération)

- **Titre d'ouverture** en Anton, dès la 1re frame, reveal ligne par ligne,
  gros dans le cadre, calé à gauche.
- **Tampon de date en flip-clock** (split-flap) qui atterrit sur "21" —
  illustre le thème de la série (une date, ce jour-là).
- **Sous-titres** = le `CORPS` du post découpé en phrases courtes, simple
  fondu d'apparition (pas d'encadré), typo Anton.
- **Coupes franches** entre chapitres — plus de fondu enchaîné.
- **Chapitre "Mondial 2026"** : 5 vrais rushs envoyés par Thomas
  (`cadrage_auto.mp4`, déjà cadrés 1080×1920), un plan par sous-titre, coupés
  sans son.
- **Chiffres clés** (compteur d'années 0→26, "62 BUTS · 54 SÉLECTIONS", score
  "2-1") en gros, sur fond encre plein (pattern-interrupt).
- **Barre de progression** ocre sous le header, remplit sur toute la durée.
- Tout le contenu reste dans la zone sûre Instagram (T=150, B=H-200,
  L/R=96 — valeurs exactes des éditeurs une·deux).

## Reproduire un rendu

```bash
cd hyperframes/cejourla-reel
npx hyperframes@0.7.64 check    # lint + runtime + layout + contrast
npx hyperframes@0.7.64 render -o renders/cejourla-haaland.mp4
npx hyperframes@0.7.64 snapshot --at 0.5,15,30,55   # aperçus PNG en secondes, pour itérer vite
```

Prérequis locaux : Chrome headless (`npx hyperframes browser ensure`) et
FFmpeg (`apt install ffmpeg`). Rien de tout ça n'est committé (gros
binaires / caches) — voir `.gitignore`. Les 5 rushs vidéo vont dans
`assets/haaland-0N.mp4` (non versionnés, à resourcer depuis le Drive de
Thomas si le dossier est vide).

`tokens/fonts.css` (import Google Fonts) sert uniquement d'indice pour que le
compilateur HyperFrames résolve et embarque les polices au moment du build —
le rendu final n'a plus besoin du réseau.

## Aperçu interactif (`preview/`)

`npx hyperframes preview` lance un studio de prévisualisation, mais son
`localhost` n'est joignable que depuis cette session — pas depuis le
navigateur de Thomas. `preview/build.py` construit à la place une version
**autonome et scrubbable** de `index.html` : polices, GSAP et les 5 clips
vidéo (recompressés en VP9/WebM basse résolution, ~2,4 Mo au total) sont tous
embarqués en base64 dans un seul fichier HTML, avec une mini-timeline
(lecture/pause/scrub) qui réimplémente à la main la logique de visibilité des
clips HyperFrames (le runtime officiel n'existe que dans le CLI). Publié via
l'outil Artifact de Claude, ça donne une URL que Thomas peut ouvrir
directement, indépendamment de la session.

```bash
cd hyperframes/cejourla-reel/preview
python3 build.py   # régénère studio-preview.html après une modif d'index.html
```

Notes :
- VP9/WebM plutôt que H.264 : certains builds Chromium (dont les navigateurs
  headless de test) n'ont pas le décodage H.264 — VP9 est universellement
  supporté.
- Vidéos en `blob:` URL (décodées depuis une constante JS en base64) plutôt
  qu'en `data:` URI directe sur `src=` — bien plus fiable pour le
  seek/décodage dans Chromium.
- Fichiers générés (`preview/*.webm`, `*.woff2`, `gsap.min.js`,
  `studio-preview.html`...) non versionnés — voir `.gitignore`. Seul
  `build.py` est committé.

## Limites de ce prototype

- Pas de son (voix off / musique) — HyperFrames sait faire du sous-titrage
  synchronisé à l'audio si une voix off est ajoutée un jour.
- Tailles de titre fixées à l'œil plutôt que recalculées comme l'algorithme
  `clampTitle()` de l'éditeur (qui mesure le texte pixel par pixel) — à
  affiner si les titres varient beaucoup en longueur d'un post à l'autre.
- Scènes écrites à la main dans `index.html`, pas encore de générateur
  `POST DU JOUR → reel.mp4` automatique.
- Ne remplace pas le pipeline `remotion/` (highlight reels sur vraies images
  de match avec tracking joueur) — portée différente.
