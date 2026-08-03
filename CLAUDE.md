# une·deux — mémo projet

Voir `SKILL.md` pour la production de **posts carrousel** (skill `une-deux-post`).

Ce fichier couvre un format différent : le **reel montage vidéo "Ce jour-là"**
(images de match réelles + texte animé), construit avec HyperFrames sur la
branche dédiée **`ce-jour-là`** (jamais `main` — voir §7). Déclencheur :
Thomas envoie un lien Drive vers une vidéo de
match et demande d'y ajouter le texte du post (sous-titres ou corps animé) —
**ou** dépose une demande via le lanceur `editeurs/lanceur-cejourla.html`
(voir ci-dessous), traitée automatiquement par une Routine.

## Lanceur automatique (`editeurs/lanceur-cejourla.html`)

Outil statique (même DA que `editeur-series.html` : panel sombre, ocre,
Saira Condensed/Anton/Archivo) où Thomas colle le lien Drive + la date du
post + la variante (reel complet / intro seule) + des notes optionnelles.
Le bouton « Lancer le montage » ouvre un brouillon email pré-rempli
(`mailto:` vers t.louisor@gmail.com, objet `LANCER REEL — <date>`, corps au
format `LIEN DRIVE: … / DATE DU POST: … / VARIANTE: … / NOTES: …`) — une
page statique ne peut pas appeler Claude Code directement, l'email est le
pont.

Une **Routine** ("Lanceur reels Ce jour-là", trig_01CJMco7Azm8WwCSEpM8dhvX)
tourne une fois par jour à 14h heure de Paris (créée via l'interface Routines
de claude.ai, connecteurs Gmail + Google Drive attachés explicitement — la
création via l'outil `create_trigger` en session échoue silencieusement sur
les connecteurs pour cette organisation, toujours passer par l'interface web
pour ce genre de Routine). Liée à une session existante (pas une session
fraîche : le connecteur Gmail ne s'y transmet pas de façon fiable sur cette
org). Elle cherche un brouillon/thread Gmail `subject:LANCER REEL` non marqué
`[TRAITÉ]`/label `reel-traite`, construit le reel selon la recette figée de
ce fichier, livre, committe/pousse, puis marque la demande traitée. Si rien
n'est en attente, elle ne fait rien.

Pour un montage immédiat, demander directement dans le chat reste plus
rapide (pas d'attente jusqu'à 14h) — le lanceur sert pour poser une demande à
traiter en tâche de fond.

## Recette figée — intro d'un reel une·deux (fond plein cadre, sans texte)

Quand Thomas demande **"l'intro d'un reel une·deux"** (ou formulation
équivalente : juste le traitement visuel de la vidéo, sans habillage), livrer
**uniquement** le composite letterbox — pas de header, pas de tag, pas de
texte, rien d'autre. C'est un sous-ensemble de la recette complète
ci-dessous : seulement l'étape 2 (composite letterbox), sans les étapes
3-4 (header, texte).

```bash
ffmpeg -y -i video_raw.mp4 -filter_complex \
"[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];[0:v]fps=30,scale=1080:-2[fg];[bg][fg]overlay=x=0:y=655:shortest=1[outv]" \
-map "[outv]" -map 0:a? -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -c:a aac -b:a 160k intro.mp4
```

- Mêmes réglages figés que la recette complète : `gblur=sigma=36`,
  `eq=saturation=0.4`, source horizontale (~1.77) recentrée en 9:16.
  Recalculer `scale=`/`y=` si le ratio source diffère (voir étape 2
  ci-dessous pour la formule).
- Simple opération ffmpeg, **pas besoin d'un projet HyperFrames** (pas
  d'animation, pas de composition) — traiter directement dans un dossier de
  travail, livrer le fichier obtenu.
- Si Thomas demande seulement "le fond plein cadre" (sans "derrière" /
  sans vidéo nette dessus), livrer juste la couche flou/désaturé plein cadre
  (`[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4`
  seule, sans overlay du premier plan net).

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

### 1bis. Sélection des plans (montage multi-plans)

Règles figées, validées par Thomas sur `cejourla-25juillet-reel` — à
appliquer par défaut dès que le reel est un montage découpé (plusieurs
segments coupés dans une vidéo source, cf. §2bis/§8), sauf demande contraire :

- **Aucun plan de moins de 3.5s.** Repérer des fenêtres source d'au moins
  ~3.5-4s par segment ; ne jamais garder un plan de 1-2s même si le contenu
  est pertinent — l'étendre ou le remplacer par un autre passage.
- **Uniquement des images filmées réelles** (plan de caméra, photo
  d'époque) — aucun carton graphique/infographie généré (habillage
  chaîne : stats, cartes de score animées, etc.), même si la source en
  contient et que ça illustrerait bien le texte. Scanner la vidéo source
  dans son ensemble (contact-sheets ffmpeg à différentes fenêtres/grilles)
  pour repérer les passages réellement filmés avant de choisir les plans.
- **Vérifier la cohérence factuelle plan/texte** : un même passage source
  peut illustrer deux événements différents (ex. verdict initial vs verdict
  en appel, deux dates distinctes) — ne jamais réutiliser un plan/carton
  dont le contenu contredirait la phrase du corps qu'il est censé
  illustrer ; en cas de doute, préférer un plan neutre (lieu, ambiance,
  personne concernée) à un plan trop spécifique mais potentiellement faux.

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

### 2bis. Variante montage multi-plans (plusieurs segments, header + texte présents)

Quand le reel est un montage découpé en plusieurs plans (1 segment ≈ 1 phrase,
cf. §8 scaffolding), le plan net ne doit pas recentrer sur tout le canvas
1920 comme en §2 (qui suppose un habillage sans header/texte) : il doit
occuper exactement l'espace entre le bas du tag (§3, tag bottom ≈408) et le
haut de la zone de texte (§4), plein cadre horizontalement. Réglages figés
(validés par Thomas via capture d'écran de rendu) :

- `overlay=x=0:y=420` — plan net plein cadre horizontal (`x=0`, pas de marge
  96px type header/texte), hauteur **888px fixe**, donc du haut à
  `y=420` jusqu'à `y=1308`.
- Fond (flouté/désaturé, mêmes réglages `gblur=sigma=36`/`eq=saturation=0.4`)
  toujours plein canvas 1080×1920 derrière.
- Si la source a son propre habillage à exclure (logo de la chaîne d'origine,
  bouton d'interface, etc.), zoomer la source ~25% (`scale=W*1.25:H*1.25` puis
  `crop=W:H` centré) **avant** ce calcul de cover-crop, sur le fond ET le
  premier plan — recadre juste assez pour sortir les éléments de bord sans
  perdre le sujet ; ajuster le facteur au cas par cas si un élément déborde
  encore (ex. logo en coin déjà recadré à ×1.25 mais toujours visible → passer
  à ×1.35 et vérifier par extraction de frame).
- Exemple filter-graph complet (source zoomée ×1.25, cover-crop bg vers
  1080×1920, plan net cover-crop vers 1080×888) :
  ```
  [0:v]scale=W*1.25:H*1.25,crop=W:H:offX:offY,fps=30,split=2[z1][z2];
  [z1]scale=<cover_w>:1920,crop=1080:1920[bg-crop],gblur=sigma=36,eq=saturation=0.4[bg];
  [z2]scale=<cover_w2>:888,crop=1080:888:<centerX>:0[fg];
  [bg][fg]overlay=x=0:y=420:shortest=1[outv]
  ```
  (recalculer `cover_w`/`cover_w2`/`centerX` selon le ratio réel de la
  source zoomée, cover-crop classique : facteur = max(target_w/src_w,
  target_h/src_h))

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
- Position : `top:1420px` avec `transform:translateY(-50%)`, zone
  `left:96px; right:96px`, dans la bande floutée basse (sous le plan net —
  valeur calibrée pour la variante §2bis, où le plan net s'arrête à
  `y=1308` ; remonté depuis `top:1560px` à la demande de Thomas pour
  rapprocher le texte du plan net). Si le plan net occupe un espace
  différent (variante §2 plein-centrage), ajuster en conséquence — garder
  une marge d'environ 100-115px entre le bas du plan net et `top`.

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

**Branche dédiée `ce-jour-là`, jamais `main` ni une branche de session
quelconque.** Se placer sur cette branche (la créer depuis `main` si elle
n'existe pas encore localement) avant de committer quoi que ce soit. Cette
branche n'est **jamais fusionnée vers `main`** — elle reste la seule source
de vérité pour les reels "Ce jour-là", indépendamment de `main` (qui resterait
sinon alourdi par les vidéos).

Chaque reel = un nouveau dossier **à la racine de cette branche**, nommé par
la date ISO du post (`AAAA-MM-JJ/`, ex. `2026-08-05/` — pas de slug
descriptif, pas de préfixe `hyperframes/`). Contenu du dossier :
`hyperframes.json`, `meta.json`, `package.json` (copier depuis un projet
existant de cette branche et adapter `name`/`id`), `.gitignore`
(`node_modules/`, `renders/`, `snapshots/`, `.debug/`), `tokens/fonts.css` +
`tokens/colors.css` copiés tels quels (source de vérité : palette
`--ocre`/`--ink`/`--cream`/`--muted-cream` de `editeurs/editeur-series.html`).

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
branche `ce-jour-là`.

**INTERDIT de livrer un fichier depuis `assets/`** (ce sont les sources
brutes du composite ffmpeg — fond flouté + plan net, sans header ni texte —
jamais le résultat final). Le seul livrable valide pour `SendUserFile` est le
fichier produit par `npm run render`, dans `renders/` (jamais committé,
gitignored). Si le render n'a pas encore tourné ou a échoué, ne rien
livrer — relancer `npm run render` et attendre, ou signaler le blocage
plutôt que de livrer le composite brut par erreur.
