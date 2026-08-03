# une·deux — mémo projet

Voir `SKILL.md` pour la production de **posts carrousel** (skill `une-deux-post`).

Ce fichier couvre un format différent : le **reel montage vidéo "Ce jour-là"**
(images de match réelles + texte animé), construit avec HyperFrames dans
`hyperframes/`. Déclencheur : Thomas envoie un lien Drive vers une vidéo de
match et demande d'y ajouter le texte du post (sous-titres ou corps animé) —
**ou** dépose une demande via le lanceur `editeurs/lanceur-cejourla.html`
(voir ci-dessous), traitée automatiquement par une Routine.

## Lanceur automatique (`editeurs/lanceur-cejourla.html`)

Outil statique (même DA que `editeur-series.html` : panel sombre, ocre,
Saira Condensed/Anton/Archivo) où Thomas colle le lien Drive (ou, pour
« intro seule », choisit directement un fichier vidéo depuis l'appareil —
voir ci-dessous) + la date du post + la variante (reel complet / intro
seule) + des notes optionnelles. Le bouton « Lancer le montage » ouvre un
brouillon email pré-rempli (`mailto:` vers t.louisor@gmail.com, objet
`LANCER REEL — <date>`, corps au format `LIEN DRIVE: … / DATE DU POST: … /
VARIANTE: … / NOTES: …`) — une page statique ne peut pas appeler Claude Code
directement, l'email est le pont.

**Vidéo directe depuis l'appareil (intro seule uniquement)** : un toggle
« Lien Drive / Vidéo depuis l'appareil » n'apparaît que pour la variante
« intro seule » (le reel complet garde uniquement le lien Drive — source
généralement plus longue, moins adaptée à un envoi direct). En mode
fichier, le corps de l'email remplace la ligne `LIEN DRIVE: …` par
`VIDÉO: en pièce jointe de cet email (<nom du fichier>)`. `mailto:` ne peut
jamais joindre un fichier (limitation universelle des navigateurs, pas de ce
code) : le bouton tente d'abord `navigator.share({files:[...]})` (Web Share
API — fonctionne sur mobile, où Thomas utilise principalement ces outils :
le menu de partage natif s'ouvre avec la vidéo déjà jointe, il choisit
Gmail/Mail) ; si l'appareil/navigateur ne supporte pas le partage de
fichiers (desktop notamment), repli automatique sur le `mailto:` habituel
avec un avertissement visible dans l'éditeur et rappelé dans le corps de
l'email : joindre soi-même le même fichier avant d'envoyer.

Côté traitement : la Routine doit gérer les deux cas indifféremment — si le
corps de l'email contient `VIDÉO: en pièce jointe …` (pas de `LIEN DRIVE:`),
récupérer la vidéo depuis la pièce jointe Gmail du message plutôt que
tenter un téléchargement Drive.

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

## Recette figée — intro d'un reel une·deux (composite + header + titre animé)

Quand Thomas demande **"l'intro d'un reel une·deux"** (ou formulation
équivalente) et donne une vidéo courte (quelques secondes, généralement
< 7 s) : le montage de la composition (étape 2 ci-dessous, inchangée)
tourne d'abord, puis, une fois fini, l'habillage vient **en surcouche** —
**Aucun trim automatique** : le composite tourne sur toute la durée du
fichier reçu, tel quel — que la source vienne d'un lien Drive ou d'une
vidéo envoyée depuis la photothèque (§ lanceur ci-dessus). Si le fichier
fourni dépasse largement les quelques secondes attendues pour une intro,
c'est à Thomas de le pré-couper avant de l'envoyer ; ce n'est ni détecté ni
corrigé côté traitement (choix explicite — pas de complexité de découpe
auto à maintenir pour un usage marginal).
header (§3 de la recette complète, identique) **et** le titre du post animé
ligne par ligne, exactement comme le template "cover · titre seul" de
`editeur-series.html` (série `cejourla`). Référence de rendu validée :
`templates/titre-anime-intro/` sur la branche `ce-jour-là` (gabarit +
render de test, composite du 3 août 2017 réutilisé, titre "3 AOÛT 2017 :
LE PLUS GROS TRANSFERT DE L'HISTOIRE" avec "TRANSFERT DE"/"L'HISTOIRE"
encadrés) — comparer visuellement à cette référence avant de considérer un
nouvel intro conforme.

```bash
ffmpeg -y -i video_raw.mp4 -filter_complex \
"[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];[0:v]fps=30,scale=1080:-2[fg];[bg][fg]overlay=x=0:y=655:shortest=1[outv]" \
-map "[outv]" -map 0:a? -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -c:a aac -b:a 160k intro.mp4
```

- Mêmes réglages figés que la recette complète pour le composite :
  `gblur=sigma=36`, `eq=saturation=0.4`, source horizontale (~1.77)
  recentrée en 9:16. Recalculer `scale=`/`y=` si le ratio source diffère
  (voir étape 2 ci-dessous pour la formule).
- **Contrairement à la recette complète, ce composite EST un projet
  HyperFrames** (§7 scaffolding) dès qu'un titre animé est ajouté par-dessus
  — le `<video>` composite passe en simple `<div class="video-full">
  inset:0</div>` plein cadre (le composite déjà cuit par ffmpeg fait tout le
  travail visuel, la vidéo HTML ne fait qu'occuper tout le canvas), header
  en HTML/CSS statique par-dessus (§3, valeurs pixel identiques), titre en
  divs absolus animés par GSAP.
- **Source du titre** : champ `TITRE` du brouillon Gmail "POST DU JOUR —
  <date>" correspondant (pas `CORPS` — c'est le champ court/percutant,
  distinct du texte long utilisé en §4 pour le reel complet). Repris tel
  quel, mis en capitales par le CSS (`text-transform:uppercase`).
- **Découpage en lignes** : à la main (pas d'auto-wrap côté HTML/HyperFrames
  contrairement au canvas de l'éditeur) — composer au jugé puis corriger
  après vérification par extraction de frame (§8) si une ligne déborde des
  marges (`left:96px; right:96px`, soit 888px de large utile).
- **Mots-clés encadrés** : dernière(s) ligne(s) ou fait(s) marquant(s)
  (chiffres, nom propre, verdict) — un carré fusionné derrière chaque
  groupe de mots consécutifs accentués, même mécanique que
  `drawWordLine`/§4 : couleur du carré = teinte de la série (`--ocre` pour
  `cejourla`), texte toujours crème (pas d'inversion de couleur de texte).
  Ne pas surcharger, une ligne ou deux au maximum.
- **CSS/HTML/GSAP à reproduire à l'identique** (`Anton`, aligné à **gauche**
  — pas centré, contrairement au corps de texte du §4, et **sans ombre
  portée** — contrairement au corps de texte du §4 qui en a besoin faute de
  carré plein derrière, la lisibilité du titre vient du carré ocre sur les
  mots-clés) :
  ```css
  .t-line { position:absolute; left:96px; right:96px; font-family:'Anton',sans-serif;
            font-size:140px; line-height:1; text-transform:uppercase; color:var(--cream);
            opacity:0; }
  .kw-box { background:var(--ocre); padding:10px; margin:-10px; display:inline-block; }
  ```
  (la marge négative égale au padding annule le décalage de layout — le
  texte encadré reste aligné avec les lignes non encadrées)
  **`font-size` : ~140px est le point de départ validé sur le titre-test
  4 lignes de `templates/titre-anime-intro/` (branche `ce-jour-là`), mais ce
  n'est PAS une constante universelle à réutiliser telle quelle** — un
  canvas 130px (éditeur) et un texte CSS 130px n'ont pas le même corps de
  casse apparent une fois rendus par HyperFrames (chargement de police
  différent), et le nombre/longueur des lignes change la marge disponible
  dans la boîte de 888px (`left:96px; right:96px`) avant renvoi à la ligne.
  Pour chaque nouveau titre : partir de 140px, **comparer la hauteur de
  casse par extraction de frame** face à une vidéo de référence si
  disponible (sinon au jugé), et si une ligne déborde/revient à la ligne
  dans la boîte de 888px, réduire la taille (jamais laisser une ligne se
  scinder en deux — ça fait chevaucher la ligne suivante).
  ```js
  const start = 0.3, revealMs = 0.62, fadeMs = 0.22;   // vitesse par défaut (×1)
  lines.forEach((sel, i) => {
    tl.fromTo(sel, {opacity:0, y:8}, {opacity:1, y:0, duration:fadeMs, ease:'none'}, start + i*revealMs);
  });
  ```
  Formule exacte de l'éditeur : `revealMs = 620/vitesse`,
  `fadeMs = clamp(80, 220, revealMs*0.6)` — rampe **linéaire** (`ease:'none'`),
  pas d'easing, avec un léger décalage vertical 8px→0px qui accompagne le
  fondu. Le texte reste affiché jusqu'à la fin du clip (pas de fondu de
  sortie, contrairement aux blocs de corps du §4 — pas de hard-kill requis
  ici puisque l'opacité finale est 1, pas 0).
- **Positionnement vertical** : ancrer par le bas, `top` de chaque ligne =
  baseline − ascent avec baseline la plus basse ≈ 1690-1730px (juste
  au-dessus de la zone de sécurité basse) et un écart entre lignes de
  `tSize*0.92` ≈ 120px — recalculer précisément pour chaque titre (nombre de
  lignes différent) plutôt que de réutiliser les pixels bruts du gabarit de
  référence, qui ne valent que pour son titre à 4 lignes.
- Si Thomas demande explicitement **"juste le composite, sans habillage"**
  (aucun header, aucun titre — juste le traitement visuel de la vidéo),
  revenir à l'ancien comportement : livrer uniquement le fichier
  `intro.mp4` produit par la commande ffmpeg ci-dessus, sans projet
  HyperFrames.
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
