# Prototype — HyperFrames × Ce jour-là (reel)

Preuve de concept : transformer le carrousel `posts/2026-06-29-gaetjens-1950/`
(série **Ce jour-là**) en reel vertical 9:16, rendu en MP4 directement via la
CLI [HyperFrames](https://hyperframes.heygen.com), sans passer par
`editeurs/reel.html`.

## Ce que ça reproduit

Le habillage reprend telle quelle la DA de `design-system/` (tokens
`colors.css` / `typography.css` / `effects.css`, copiés dans `tokens/` pour un
projet autonome) : header `1·2 · une·deux · @UNE.DEUX`, pastille kicker ocre,
titre Anton 2 lignes avec un mot-clé coloré, sous-titre Archivo, pagination
`N / 6`. La slide finale reprend `CTASlide.jsx` (fond crème + trame,
bookmark, chip FOLLOW).

Contenu : les 8 slides du carrousel condensées en **6 scènes** (règle reel
« 90s max », ici 30,5s) — HOOK → TRANSITION → 2 TEASE → CLIMAX → ACTION —
avec le texte déjà vérifié du `script.json` d'origine, pas de nouveau
contenu inventé.

**Photos = placeholders.** Aucune image réelle n'existe pour ce post (les
prompts photo dans `POST.md` n'ont jamais été générés). Chaque scène affiche
un dégradé sépia avec un léger zoom (Ken Burns) à la place de la photo — à
remplacer par `<img>` une fois les visuels générés (voir
`variables-and-media.md` du skill HyperFrames pour le binding média).

## Reproduire

```bash
cd hyperframes/cejourla-reel
npx hyperframes@0.7.64 check    # lint + runtime + layout + contrast
npx hyperframes@0.7.64 render -o renders/cejourla-gaetjens.mp4
```

Prérequis locaux : Chrome headless (`npx hyperframes browser ensure`) et
FFmpeg (`apt install ffmpeg`). Rien de tout ça n'est committé (gros
binaires / caches) — voir `.gitignore`.

## Généraliser à un autre post « Ce jour-là »

Le fichier est actuellement écrit à la main (scènes en dur dans `index.html`)
pour ce post précis. Pour en faire un vrai pipeline `script.json → reel.mp4` :

1. Extraire les 6 scènes (`tag`, titre 2 lignes, `greenWord`, `subs`) d'un
   `script.json` existant selon les mêmes règles de condensation que ci-dessus.
2. Générer le markup des scènes (`.scene` + `.title .w` par mot) depuis ce
   JSON au lieu de le taper à la main — un script Node de ~50 lignes suffit,
   le CSS/GSAP de ce prototype reste inchangé.
3. `hyperframes render --batch scenes.json` permet de sortir plusieurs reels
   d'un coup si plusieurs posts sont prêts en même temps.

## Limites de ce prototype

- Pas de vraies photos (placeholders sépia).
- Scènes écrites à la main, pas encore de générateur `script.json → HTML`.
- Pas de son (voix off / musique) — HyperFrames sait faire du sous-titrage
  synchronisé à l'audio si une voix off est ajoutée un jour.
- Ne remplace pas le pipeline `remotion/` (highlight reels sur vraies images
  de match avec tracking joueur) — portée différente.
