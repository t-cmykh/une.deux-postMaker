# Prototype — HyperFrames × Ce jour-là (reel)

Preuve de concept : produire un reel vertical 9:16 en MP4 directement via la
CLI [HyperFrames](https://hyperframes.heygen.com), en reprenant **à l'identique**
le template série `editeurs/editeur-series_2.html` (typo, layout, couleurs) —
pas une réinterprétation.

## Ce que ça reproduit

`index.html` est un port pixel-exact de deux templates de
`editeur-series_2.html` (canvas 1080px de large, mêmes constantes M/MR/safeTop
/safeBottom, mêmes tailles de police, mêmes couleurs) :

- **COVER** — header (anneau `1·2` + `une·deux` + `@UNE.DEUX`), pastille série
  `N°1 · CE JOUR LÀ …` (texte fixe — ce template n'a pas de kicker par
  slide), titre Anton 2 lignes avec un mot-clé en ocre, corps Archivo en
  `--muted-cream`. Sans corps = variante **titre seul**.
- **CTA** — fond crème + trame diagonale, bookmark ocre, chip `FOLLOW`, titre
  centré, sous-titre, footer `@UNE.DEUX`.

Structure du reel (5 scènes, 26s — sous la limite reel 90s) :

| Scène | Template | Contenu |
|---|---|---|
| S1 | **cover · titre seul** | HOOK |
| S2–S4 | **cover** (titre + corps) | montée du récit |
| S5 | **cta** | FOLLOW |

**Contenu de test** : le post "Ce jour-là" du 21 juillet 2026 (Haaland, né à
Leeds), tiré des brouillons Gmail (`POST DU JOUR — 21 juillet 2026` +
l'éphéméride source à 5 options, option 3 validée ✅). Le post original est un
format `TITRE + CORPS` en un seul bloc ; les 3 scènes centrales (S2–S4)
condensent ce paragraphe en 3 beats factuels (naissance à Leeds, record
norvégien, élimination face à l'Angleterre) — aucun fait ajouté au-delà de ce
qui est déjà sourcé dans le brouillon.

**Photos = placeholders.** Dégradé gris/sépia + léger zoom (Ken Burns) à la
place d'une vraie photo d'archive — à remplacer par `<img>` une fois les
visuels générés.

## Motion design

Volontairement sobre, pas de kinétique mot-par-mot :

- Chaque groupe (header → pastille série → bloc titre+corps) apparaît **en un
  seul bloc** (fade + léger `translateY`), pas en cascade par mot.
- Easing unique `power2.out` / `power3.out` — pas de bounce/elastic.
- Ken Burns quasi imperceptible sur la photo (`scale 1.0 → 1.035`, linéaire).
- Coupe de scène = voile encre (`#veil`, non-clip, plein cadre) qui pulse
  brièvement (~0.3s) à chaque changement de scène — évite le cut sec sans
  ajouter d'effet voyant.

## Reproduire

```bash
cd hyperframes/cejourla-reel
npx hyperframes@0.7.64 check    # lint + runtime + layout + contrast
npx hyperframes@0.7.64 render -o renders/cejourla-haaland.mp4
```

Prérequis locaux : Chrome headless (`npx hyperframes browser ensure`) et
FFmpeg (`apt install ffmpeg`). Rien de tout ça n'est committé (gros
binaires / caches) — voir `.gitignore`.

`tokens/fonts.css` (import Google Fonts Anton/Archivo/Saira Condensed) sert
uniquement d'indice pour que le compilateur HyperFrames résolve et embarque
les polices au moment du build (voir le log `check`/`render` : *"Injected
deterministic @font-face rules"*) — le rendu final n'a plus besoin du réseau.

## Généraliser à un autre post « Ce jour-là »

Le fichier est actuellement écrit à la main (scènes en dur dans `index.html`)
pour ce post précis. Pour en faire un vrai pipeline `POST DU JOUR → reel.mp4` :

1. Découper le `CORPS` du post en 2–4 beats factuels (comme fait ici à la
   main pour Haaland).
2. Générer le markup `.serietag` / `.title` / `.body` de chaque scène depuis
   ces beats au lieu de le taper à la main — le CSS/GSAP de ce prototype
   reste inchangé, un script Node de génération suffit.
3. `hyperframes render --batch scenes.json` pour sortir plusieurs reels d'un
   coup si plusieurs `POST DU JOUR` sont prêts en même temps.

## Limites de ce prototype

- Pas de vraies photos (placeholders).
- Scènes écrites à la main, pas encore de générateur automatique.
- Pas de son (voix off / musique) — HyperFrames sait faire du sous-titrage
  synchronisé à l'audio si une voix off est ajoutée un jour.
- Tailles de titre fixées à l'œil plutôt que recalculées comme l'algorithme
  `clampTitle()` de l'éditeur (qui mesure le texte pixel par pixel) — à
  affiner si les titres varient beaucoup en longueur d'un post à l'autre.
- Ne remplace pas le pipeline `remotion/` (highlight reels sur vraies images
  de match avec tracking joueur) — portée différente.
