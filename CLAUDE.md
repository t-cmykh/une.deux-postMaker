# une·deux — mémo projet

Voir `SKILL.md` pour la production de **posts carrousel** (skill `une-deux-post`).

Ce fichier couvre un format différent : le **reel montage vidéo "Ce jour-là"**
(images de match réelles + texte animé), construit avec HyperFrames dans
`hyperframes/`. Déclencheur : Thomas envoie un lien Drive vers une vidéo de
match et demande d'y ajouter le texte du post (sous-titres ou corps animé).

## Recette figée — reel "Ce jour-là" à partir d'images de match

Quand Thomas dit "fait la même chose avec cette vidéo" / "on va faire un
reel une·deux" à propos d'un montage vidéo (pas un carrousel), reproduire
**à l'identique** les réglages ci-dessous, établis et validés sur les
projets `hyperframes/cejourla-uruguay-2011-textreveal*`. Ne dévier que si
Thomas donne une instruction explicite contraire pour ce reel précis — dans
ce cas, la nouvelle instruction s'applique à CE reel, mais ne remplace pas
la recette par défaut pour les suivants (sauf si Thomas dit explicitement
que c'est le nouveau standard).

### 1. Récupération de la vidéo (Drive)

```bash
curl -sL -o video_raw.mp4 "https://drive.google.com/uc?export=download&id=<ID>"
file video_raw.mp4   # si "HTML document" → page d'avertissement virus, voir ci-dessous
```

Si le téléchargement direct renvoie une page HTML d'avertissement (fichiers
volumineux) :
```bash
grep -o 'name="[a-z]*" value="[^"]*"' raw_download   # récupère confirm + uuid
curl -sL -o video_raw.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t&uuid=<UUID>"
```

**Toujours vérifier l'orientation avant de composer** — ne jamais supposer :
```bash
ffprobe -v error -show_entries stream=width,height:format=duration -of default=noprint_wrappers=1 video_raw.mp4
ffprobe -v error -show_entries stream_side_data -of default=noprint_wrappers=1 video_raw.mp4
ffmpeg -y -ss 3 -i video_raw.mp4 -frames:v 1 /tmp/check.jpg -loglevel error   # inspection visuelle via Read
```
Les vidéos fournies jusqu'ici sont horizontales (~16:9, ratio ≈1.77), avec ou
sans métadonnée de rotation trompeuse — se fier à l'image extraite, pas
seulement aux nombres.

### 2. Composite letterbox 9:16 (fond flouté + désaturé, pré-calculé ffmpeg)

**Ne jamais faire le flou en live via CSS au rendu** (coût énorme en Chrome
headless / SwiftShader — un rendu peut passer de 5 min à 30+ min). Toujours
pré-cuire le composite fond+premier plan dans un seul fichier vidéo via
ffmpeg, en amont.

Pour une source horizontale (ratio ~1.77) vers un canvas 1080×1920 :

```bash
ffmpeg -y -i video_raw.mp4 -filter_complex \
"[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];[0:v]fps=30,scale=1080:-2[fg];[bg][fg]overlay=x=0:y=655:shortest=1[outv]" \
-map "[outv]" -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -an composite.mp4

ffmpeg -y -i video_raw.mp4 -vn -c:a aac -b:a 160k audio.m4a   # si la source a du son
```

Réglages figés (dernière validation Thomas — "Super !") :
- `gblur=sigma=36` (flou fort — a été doublé une fois depuis sigma=18, la
  valeur 36 est celle validée, à réutiliser par défaut)
- `eq=saturation=0.4` (fond nettement désaturé, ~40% de la saturation
  d'origine)
- `overlay=x=0:y=655` — recentre le premier plan net verticalement sur tout
  le canvas 1920 (pour une source ratio 1.77 → fg height≈610 → y=(1920-610)/2)
- Si le ratio de la source diffère de 1.77, recalculer `scale=3400:1920`
  (fond, cover-crop) et `y=` (centrage vertical) en conséquence — ne pas
  réutiliser les chiffres bruts tels quels.
- `fps=30` partout (aligne sur `data-fps="30"` de la composition)

### 3. Header — repris à l'identique de `editeurs/editeur-series.html`

Valeurs pixel exactes (ratio 9:16, série `cejourla`), à ne jamais
approximer — ce sont les vraies constantes de l'éditeur de série :

```css
/* M = MR = 96 (marges), safeTop() = 150 pour le ratio 9:16 */
.ring     { left:96px;  top:216px; width:92px; height:92px; border:4px solid var(--cream); border-radius:50%; }
           /* "1·2", Saira Condensed 600 38px, centré dans le ring */
.wordmark { left:214px; top:262px; transform:translateY(-50%); font:58px 'Anton'; color:var(--cream); }
           /* "une·deux" */
.handle   { right:96px; top:262px; transform:translateY(-50%); font:32px 'Saira Condensed'; font-weight:600; color:var(--cream); }
           /* "@UNE.DEUX" */
.hairline { left:96px; right:96px; top:318px; height:4px; background:var(--cream); }
.tag      { left:96px; top:350px; height:58px; background:var(--ocre); color:var(--ink);
            font:32px 'Saira Condensed'; font-weight:600; padding:0 15px; display:flex; align-items:center; }
           /* "CE JOUR LÀ …" */
```

Ne PAS ajouter de dégradé d'assombrissement en bas du cadre (`scrim-bottom`)
— règle permanente pour ce format, sauf demande contraire explicite.

### 4. Texte — corps du post, animé, découpé en unités de sens

- Utiliser le texte du **CORPS** du brouillon Gmail tel quel (ne pas le
  réécrire) — chercher le brouillon "POST DU JOUR — <date>" correspondant à
  la date demandée ("le post de demain" etc.) via `search_threads`/
  `list_drafts`, section `CORPS`.
- Découper en unités de sens (phrases ou propositions), chacune son propre
  bloc qui apparaît en fondu puis disparaît avant le suivant (même mécanique
  que les sous-titres établis dans ce projet : `fromTo(opacity 0→1)` puis
  `to(opacity→0)` + `tl.set(opacity:0)` hard-kill en fin de fenêtre).
- Mots-clés importants en **gras et/ou ocre** (`<b>` pour gras crème,
  `<b class="ocre">` pour gras + couleur ocre) — chiffres, scores, noms
  propres, faits marquants. Ne pas surcharger : un ou deux par phrase.
- **Texte centré**, y compris sur les blocs à plusieurs lignes
  (`text-align:center` sur la zone ET sur chaque bloc) — pas d'alignement à
  gauche.
- Police Archivo (corps de texte, pas Anton tout-capitales — c'est de la
  prose, pas un sous-titre condensé), ~38px, line-height 1.38, couleur
  crème, `text-shadow: 0 2px 16px rgba(0,0,0,.65), 0 1px 4px rgba(0,0,0,.8)`
  pour la lisibilité (remplace tout scrim, puisque le bas ne doit pas être
  assombri).
- Position : `top:1560px` avec `transform:translateY(-50%)`, zone
  `left:96px; right:96px`, dans la bande floutée basse (sous la vidéo nette
  letterboxée).

### 5. Calcul du rythme (formule établie, réutiliser systématiquement)

```
durée_brute_ligne = nombre_de_mots × 0.27 + 0.35   (secondes)
facteur = (durée_vidéo_disponible − Σ pauses) / Σ durée_brute_toutes_lignes
durée_ligne = durée_brute_ligne × facteur
```

- Pauses entre blocs : 0.15s (vidéo courte, rythme serré) à 0.5s (vidéo
  longue, rythme posé) selon la marge disponible.
- Si `facteur < 1` (vidéo plus courte que le texte au rythme naturel) :
  compresser quand même plutôt que couper le texte — ne jamais réduire le
  contenu du corps sans demande explicite.
- Démarrer le premier bloc à `t≈0.3s` (pas de délai d'intro/titre sauf
  demande contraire).
- `tl.fromTo(..., {opacity:0}, {opacity:1, duration:0.2-0.35, ease:'power2.out'})`
  puis `tl.to(..., {opacity:0, duration:0.18-0.3, ease:'sine.in'})` puis
  `tl.set(..., {opacity:0}, start+dur)` (hard-kill obligatoire, sinon lint
  `gsap_exit_missing_hard_kill`).

### 6. Piège GSAP à ne jamais reproduire

Un élément avec un `transform: translateY(-50%)` **statique** en CSS (pour
le centrage vertical) ne doit **jamais** recevoir de tween GSAP incluant la
propriété `y` — ça entre en conflit avec le transform géré par le CSS.
Utiliser des tweens **opacity uniquement** sur ces éléments.

### 7. Scaffolding projet

Chaque reel = un nouveau dossier `hyperframes/<slug>/` avec
`hyperframes.json`, `meta.json`, `package.json` (copier depuis un projet
`cejourla-uruguay-2011-textreveal*` existant et adapter `name`/`id`),
`.gitignore` (`node_modules/`, `renders/`, `snapshots/`, `.debug/`),
`tokens/fonts.css` + `tokens/colors.css` copiés tels quels (source de
vérité : palette `--ocre`/`--ink`/`--cream`/`--muted-cream` de
`editeurs/editeur-series.html`).

Vidéo et audio en enfants directs de `#root`, vidéo mutée
(`muted playsinline`), son porté par un `<audio>` séparé avec sa propre
`data-duration` (contrainte HyperFrames — jamais de son sur `<video>`).

### 8. Check → render → vérif → livraison

```bash
npm run check     # 0 erreur attendu ; le warning StaticGuard "data-end
                   # without data-duration" et le timeout Runtime sont des
                   # flakes connus, non bloquants si le Lint affiche 0 erreur
npm run render     # tourne en tâche de fond (>2 min) — laisser tourner,
                   # ne pas sonder, attendre la notification
```

Après rendu : extraire des frames à quelques instants clés (ballon officiel/
date, but, scoreboard, célébration finale) via `ffmpeg -ss <t> -frames:v 1`
et les lire avec l'outil Read pour vérifier visuellement le calage texte/
image, la lisibilité et le header — ne jamais livrer sans ce contrôle.

Si le rendu dépasse 30 Mo (limite `SendUserFile`), recompresser :
```bash
ffmpeg -y -i render.mp4 -c:v libx264 -crf 25-26 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k compressed.mp4
```

Committer le dossier du projet (assets compris — seuls `renders/`,
`node_modules/`, `snapshots/`, `.debug/` sont ignorés) et pousser sur la
branche de travail en cours.
