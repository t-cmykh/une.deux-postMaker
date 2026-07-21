# Prototype — HyperFrames · Ce jour-là · 22 juillet 1989 (motion design)

Reel vertical 9:16 pour le brouillon Gmail `POST DU JOUR — 22 juillet 2026 ·
Canada bat le Maroc (1989)`. Le brouillon n'a pas de lien vidéo (« Pas de
lien vidéo disponible. ») — tout le reel est donc fait en motion design pur
(kinetic typography, pas d'image ni de vidéo), avec la DA "Ce jour-là"
(header ring/wordmark/handle/hairline/progress bar identique au reel
`cejourla-reel`, palette ink/cream/ocre, typo Anton/Archivo/Saira Condensed).

## Structure (29.4s)

1. **Hook** (0–4.2s) — flip-clock sur "22", titre ligne par ligne, grand
   numéro "89" fantôme en fond.
2. **Contexte** (4.2–8s) — Stade Mohammed-V, Casablanca ; trame de points
   (foule) en fond.
3. **Feuille de match** (8–17s) — ticker animé : les 4 buts canadiens
   (15′, 34′, 36′ doublé, 44′) puis le but marocain, avec score qui
   s'incrémente en direct à chaque ligne.
4. **Score punch** (17–21s) — "4-1" géant, stats (70 000 spectateurs,
   1er trophée international).
5. **Punchline** (21–24.6s) — la chute du post ("le Maroc a rempli un
   stade... le Canada est reparti avec le trophée").
6. **CTA** (24.6–29.4s) — identique au CTA du reel `cejourla-reel`
   (bookmark, chip "CE JOUR LÀ …", "CHAQUE JOUR, UNE DATE.").

## Reproduire un rendu

```bash
cd hyperframes/cejourla-canada-maroc-1989
npx hyperframes@0.7.64 check
npx hyperframes@0.7.64 render -o renders/canada-maroc-1989.mp4
```
