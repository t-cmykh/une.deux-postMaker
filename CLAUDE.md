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
Saira Condensed/Anton/Archivo) où Thomas colle le lien Drive (ou choisit
directement un fichier vidéo depuis l'appareil — voir ci-dessous) + la date
du post + le style de sous-titres (voir ci-dessous) + des notes optionnelles.
**Une seule variante de montage** (voir section recette ci-dessous — l'ancien
choix "reel complet / intro seule" a été fusionné, il n'y a plus de champ
VARIANTE ; le seul choix qui reste est le style des sous-titres). Le bouton
« Lancer le montage » ouvre un brouillon email pré-rempli (`mailto:` vers
t.louisor@gmail.com, objet `LANCER REEL — <date>`, corps au format `LIEN
DRIVE: … / DATE DU POST: … / STYLE SOUS-TITRES: … / NOTES: …`) — une page
statique ne peut pas appeler Claude Code directement, l'email est le pont.

**Style des sous-titres** : un sélecteur à deux chips dans le lanceur —
« FIXE » (par défaut, coché à l'ouverture) ou « KARAOKÉ ». Le choix est
écrit dans le corps de l'email en `STYLE SOUS-TITRES: fixe` ou
`STYLE SOUS-TITRES: karaoké`. Côté traitement, la Routine lit cette ligne
et applique la variante correspondante du §4 (Corps de texte) ci-dessous —
absence de la ligne (anciennes demandes envoyées avant cet ajout, ou
anciennes valeurs `actuel`/`tiktok` d'avant le renommage) = traiter comme
`fixe`.

**Vidéo directe depuis l'appareil** : un toggle « Lien Drive / Vidéo depuis
l'appareil » permet de choisir un fichier vidéo directement dans la
photothèque plutôt que de coller un lien. En mode fichier, le corps de
l'email remplace la ligne `LIEN DRIVE: …` par `VIDÉO: en pièce jointe de
cet email (<nom du fichier>)`. `mailto:` ne peut jamais joindre un fichier
(limitation universelle des navigateurs, pas de ce code) : le bouton tente
d'abord `navigator.share({files:[...]})` (Web Share API — fonctionne sur
mobile, où Thomas utilise principalement ces outils : le menu de partage
natif s'ouvre avec la vidéo déjà jointe, il choisit Gmail/Mail) ; si
l'appareil/navigateur ne supporte pas le partage de fichiers (desktop
notamment), repli automatique sur le `mailto:` habituel avec un
avertissement visible dans l'éditeur et rappelé dans le corps de l'email :
joindre soi-même le même fichier avant d'envoyer.

Côté traitement : la Routine doit gérer les deux cas indifféremment — si le
corps de l'email contient `VIDÉO: en pièce jointe …` (pas de `LIEN DRIVE:`),
récupérer la vidéo depuis la pièce jointe Gmail du message plutôt que
tenter un téléchargement Drive.

**Plusieurs jours en un seul email** : le lanceur permet d'ajouter des
« jours » répétables (bouton « + Ajouter un jour », un jour = source vidéo +
date + style sous-titres + notes, chacun indépendant) avant de cliquer
« Lancer le montage » — un seul email part, avec un bloc par jour. Format du
corps sur un seul jour (identique à l'historique, sans en-tête) :

```
LIEN DRIVE: …
DATE DU POST: …
STYLE SOUS-TITRES: …
NOTES: …
```

Sur plusieurs jours, chaque bloc est précédé d'un en-tête `JOUR N` et les
blocs sont séparés par une ligne vide :

```
JOUR 1
LIEN DRIVE: …
DATE DU POST: …
STYLE SOUS-TITRES: …
NOTES: …

JOUR 2
VIDÉO: en pièce jointe de cet email (nom-du-fichier.mp4)
DATE DU POST: …
STYLE SOUS-TITRES: …
NOTES: …
```

L'objet passe de `LANCER REEL — <date>` (un seul jour, inchangé) à
`LANCER REEL — MULTI (<n> jours)` (plusieurs jours) — dans les deux cas
l'objet contient toujours `LANCER REEL`, donc la recherche Gmail
`subject:LANCER REEL` de la Routine (ci-dessous) n'a pas besoin de changer.
Si des vidéos par pièce jointe sont mêlées à des liens Drive dans le même
lot, le partage natif (`navigator.share`) joint toutes les vidéos-fichiers
du lot en une fois ; si l'appareil ne le supporte pas, repli mailto habituel
avec la liste des fichiers à joindre soi-même.

**Côté traitement d'un email multi-jours** : découper le corps sur les
lignes `^JOUR \d+` ; l'absence de tout marqueur `JOUR N` (anciens emails,
ou nouveaux emails à un seul jour) veut dire un unique bloc implicite —
comportement inchangé. Traiter chaque bloc comme un reel indépendant, dans
l'ordre, selon la recette figée ci-dessous ; livrer (commit/push) chaque
reel séparément sur la branche `ce-jour-là`, puis ne marquer l'email/thread
entier comme traité qu'une fois **tous** les blocs livrés (un échec sur un
seul jour ne doit pas faire perdre le suivi des autres — livrer ce qui
fonctionne, signaler explicitement le(s) jour(s) en échec plutôt que de
marquer l'email traité en silence).

Une **Routine** ("Lanceur reels Ce jour-là", trig_01CJMco7Azm8WwCSEpM8dhvX)
tourne une fois par jour à 14h heure de Paris (créée via l'interface Routines
de claude.ai, connecteurs Gmail + Google Drive attachés explicitement — la
création via l'outil `create_trigger` en session échoue silencieusement sur
les connecteurs pour cette organisation, toujours passer par l'interface web
pour ce genre de Routine). Liée à une session existante (pas une session
fraîche : le connecteur Gmail ne s'y transmet pas de façon fiable sur cette
org). Elle cherche un brouillon/thread Gmail `subject:LANCER REEL` non marqué
`[TRAITÉ]`/label `reel-traite`, construit le ou les reels selon la recette
figée de ce fichier (un par jour listé dans l'email, cf. ci-dessus), livre,
committe/pousse, puis marque la demande traitée. Si rien n'est en attente,
elle ne fait rien.

**Important — cette Routine travaille sur la branche `ce-jour-là`, qui n'est
jamais fusionnée dans `main` : toute correction qu'elle découvre en cours de
production (bug de cadrage, couleur, etc.) doit être reportée MANUELLEMENT
dans la copie de `CLAUDE.md` sur `main` (via une session normale, PR) pour
ne pas rester bloquée sur une branche qui ne remonte jamais.** C'est arrivé
une fois (3 correctifs découverts le 4 août 2026 sur `cejourla-4aout-reel`,
fusionnés ici avec le reste de la recette) — vérifier périodiquement que les
deux copies n'ont pas divergé.

Pour un montage immédiat, demander directement dans le chat reste plus
rapide (pas d'attente jusqu'à 14h) — le lanceur sert pour poser une demande à
traiter en tâche de fond.

## Recette figée — reel "Ce jour-là" (intro + corps + CTA de fin, une seule vidéo)

Quand Thomas dit "fait la même chose avec cette vidéo" / "on va faire un
reel une·deux" à propos d'un montage vidéo (pas un carrousel), ou déclenche
via le lanceur ci-dessus, reproduire **à l'identique** les réglages
ci-dessous. Ne dévier que si Thomas donne une instruction explicite
contraire pour ce reel précis — dans ce cas, la nouvelle instruction
s'applique à CE reel, mais ne remplace pas la recette par défaut pour les
suivants (sauf si Thomas dit explicitement que c'est le nouveau standard).

**Vue d'ensemble** : à partir d'**une seule vidéo source, gardée intégrale**
(§1bis), un **unique composite continu** (§2, même géométrie du début à la
fin) est habillé de deux couches de texte qui se relaient dans le temps —
titre animé de l'intro (§4bis) sur les premières secondes, puis corps de
texte façon sous-titres (§4) sur le reste — dans une seule composition
HyperFrames. Un CTA de fin est ajouté en post-traitement (§8).

Il n'y a plus de choix "intro seule / reel complet" à faire : une vidéo
donnée produit toujours ce montage complet en une fois.

### 1. Récupération de la vidéo (Drive ou pièce jointe)

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

Si la demande contient `VIDÉO: en pièce jointe …` (pas de `LIEN DRIVE:`),
récupérer la vidéo depuis la pièce jointe Gmail du message plutôt que
télécharger depuis Drive (voir § lanceur ci-dessus).

**Aucun trim automatique** : la vidéo reçue est utilisée telle quelle, sur
toute sa durée — que la source vienne d'un lien Drive ou d'une vidéo envoyée
depuis la photothèque. Ce n'est ni détecté ni corrigé côté traitement (choix
explicite — pas de complexité de découpe auto à maintenir).

**Toujours vérifier l'orientation avant de composer** — ne jamais supposer :
```bash
ffprobe -v error -show_entries stream=width,height:format=duration -of default=noprint_wrappers=1 video_raw.mp4
ffprobe -v error -show_entries stream_side_data -of default=noprint_wrappers=1 video_raw.mp4
ffmpeg -y -ss 3 -i video_raw.mp4 -frames:v 1 /tmp/check.jpg -loglevel error   # inspection visuelle via Read
```
Les vidéos fournies jusqu'ici sont horizontales (~16:9, ratio ≈1.77), avec ou
sans métadonnée de rotation trompeuse — se fier à l'image extraite, pas
seulement aux nombres.

### 1bis. Vidéo intégrale par défaut — pas de sélection de plans

**Par défaut, garder la vidéo source intégrale, sans découpage ni sélection
de plans** : le composite (§2) et les overlays (titre puis corps) s'appliquent
à toute la vidéo, du début à la fin, durée inchangée. Les vidéos fournies par
Thomas sont en général déjà des montages propres (highlights, pas du brut de
captation) — il n'y a rien à curer.

Erreur commise sur `cejourla-4aout-reel` (Copa Confederaciones 1999, routine
du 3 août 2026) : une sélection de "6 meilleurs plans ≥3.5s" a été appliquée
à tort à une vidéo déjà montée, livrant 37s au lieu des ~50s réels de la
source. Corrigée après retour explicite de Thomas : « GARDE LA VIDÉO DU
DRIVE TEL QUEL ». **C'est la consigne par défaut.**

Le titre animé (§4bis) joue sur les premières secondes de cette même vidéo
continue, le corps de texte (§4) prend le relais sur le reste — aucune
découpe ni sélection n'intervient pour distinguer "l'intro" du "corps", ce
sont deux fenêtres temporelles d'overlay sur le **même** fichier vidéo composité
une seule fois (§2), jamais deux composites à géométries différentes.

**Ne sélectionner/curer des plans que si** : Thomas le demande explicitement
pour ce reel précis, OU la source est manifestement du brut mélangé à des
cartons graphiques/infographie qu'il faut exclure (repérable par
contact-sheets ffmpeg à différentes fenêtres/grilles). Dans ce cas
seulement, appliquer les règles ci-dessous (validées par Thomas sur
`cejourla-25juillet-reel`) :

- **Aucun plan de moins de 3.5s.** Repérer des fenêtres source d'au moins
  ~3.5-4s par segment ; ne jamais garder un plan de 1-2s même si le contenu
  est pertinent — l'étendre ou le remplacer par un autre passage.
- **Uniquement des images filmées réelles** (plan de caméra, photo
  d'époque) — aucun carton graphique/infographie généré (habillage
  chaîne : stats, cartes de score animées, etc.), même si la source en
  contient et que ça illustrerait bien le texte.
- **Vérifier la cohérence factuelle plan/texte** : un même passage source
  peut illustrer deux événements différents (ex. verdict initial vs verdict
  en appel, deux dates distinctes) — ne jamais réutiliser un plan/carton
  dont le contenu contredirait la phrase du corps qu'il est censé
  illustrer ; en cas de doute, préférer un plan neutre (lieu, ambiance,
  personne concernée) à un plan trop spécifique mais potentiellement faux.
- Dans ce mode curé, un seul composite continu s'applique quand même (§2)
  sur la vidéo reconstituée à partir des plans retenus, mis bout à bout —
  jamais un composite séparé par plan avec des géométries différentes.

### 2. Composite unique (fond flouté + désaturé, même géométrie du début à la fin)

**Ne jamais faire le flou en live via CSS au rendu** (coût énorme en Chrome
headless / SwiftShader — un rendu peut passer de 5 min à 30+ min). Toujours
pré-cuire le composite en un seul fichier vidéo via ffmpeg, en amont.

**Un seul passage ffmpeg sur la vidéo entière, une seule géométrie, y
compris sous le titre animé de l'intro.** Ne PAS composer l'intro
séparément avec une géométrie plein-canvas puis le corps avec une géométrie
différente : le plan net ne démarrerait alors pas à la même hauteur dans
les deux composites, ce qui crée un décalage de cadrage visible à la coupe
titre→texte (bug identifié par Thomas sur `cejourla-4aout-reel` via une
capture annotée comparant les deux frames — corps net dès juste sous le
header, intro net nettement plus bas). Un seul fichier vidéo continu, un
seul `<video>` dans la composition ; seuls les overlays de texte (titre
puis corps) changent dans le temps, jamais le cadrage vidéo.

Géométrie figée (validée par Thomas via capture d'écran de rendu) — plan net
occupant l'espace entre le bas du tag (§3, tag bottom ≈408) et la zone de
texte (§4), plein cadre horizontalement :

```bash
ffmpeg -y -i video_raw.mp4 -filter_complex \
"[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];[0:v]fps=30,scale=<cover_w2>:888,crop=1080:888:<centerX>:0[fg];[bg][fg]overlay=x=0:y=420:shortest=1[outv]" \
-map "[outv]" -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -g 30 -keyint_min 30 -sc_threshold 0 -an composite.mp4

ffmpeg -y -i video_raw.mp4 -vn -c:a aac -b:a 160k audio.m4a   # si la source a du son
```

- `gblur=sigma=36` (flou fort — a été doublé une fois depuis sigma=18, la
  valeur 36 est celle validée) / `eq=saturation=0.4` (fond nettement
  désaturé, ~40% de la saturation d'origine).
- `overlay=x=0:y=420` — plan net plein cadre horizontal (`x=0`, pas de marge
  96px type header/texte), hauteur **888px fixe**, donc du haut à `y=420`
  jusqu'à `y=1308`.
- **`-g 30 -keyint_min 30 -sc_threshold 0` obligatoires sur chaque composite**
  (intervalle de keyframes = 1s à 30fps) — un intervalle trop large cause des
  sauts/figeages perceptibles à la lecture ("séquences" au lieu d'un plan
  continu), signalés par le compilateur HyperFrames au check
  (`sparse keyframes... causes seek failures and frame freezing`) mais
  **à tort ignorables comme non-bloquants** : ce warning-là DOIT être
  corrigé avant de livrer, contrairement aux flakes listés en §9.
- Si la source a son propre habillage à exclure (logo de la chaîne d'origine,
  bouton d'interface, etc.), zoomer la source ~25% (`scale=W*1.25:H*1.25` puis
  `crop=W:H` centré) **avant** ce calcul de cover-crop, sur le fond ET le
  plan net — recadre juste assez pour sortir les éléments de bord sans
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
- Référence de rendu pour l'habillage titre animé (header + `.t-line`,
  géométrie à part, prototype antérieur à cette unification) :
  `templates/titre-anime-intro/` sur la branche `ce-jour-là` — utile pour le
  texte/l'animation du titre, **pas** pour le cadrage vidéo (qui utilisait
  encore l'ancienne géométrie plein-canvas y=655, corrigée depuis).

**Cas à part — "juste le composite, sans habillage" :** si Thomas demande
explicitement uniquement le traitement visuel de la vidéo (pas de header,
pas de titre, pas de texte, rien d'autre), c'est un livrable différent, pas
un sous-ensemble de la recette ci-dessus : géométrie plein-canvas
recentrée (`overlay=x=0:y=655`, pas de zone de texte réservée puisqu'il n'y
a pas de texte), pas de projet HyperFrames, livrer directement le fichier
ffmpeg obtenu.
```bash
ffmpeg -y -i video_raw.mp4 -filter_complex \
"[0:v]fps=30,scale=3400:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];[0:v]fps=30,scale=1080:-2[fg];[bg][fg]overlay=x=0:y=655:shortest=1[outv]" \
-map "[outv]" -map 0:a? -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -g 30 -keyint_min 30 -sc_threshold 0 -c:a aac -b:a 160k intro.mp4
```
Si Thomas demande seulement "le fond plein cadre" (sans vidéo nette
dessus), livrer juste la couche flou/désaturé seule, sans overlay.

### 3. Header — repris à l'identique de `editeurs/editeur-series.html`, persistant sur tout le reel

Valeurs pixel exactes (ratio 9:16, série `cejourla`), à ne jamais
approximer — ce sont les vraies constantes de l'éditeur de série. Le header
(ring/wordmark/handle/hairline/tag) reste affiché en continu du début à la
fin du reel — intro **et** corps — il n'est jamais ré-animé ni masqué entre
les deux parties :

```css
/* M = MR = 96 (marges), safeTop() = 150 pour le ratio 9:16 */
.ring     { left:96px;  top:216px; width:92px; height:92px; border:4px solid var(--cream); border-radius:50%; }
           /* "1·2", Saira Condensed 600 38px, centré dans le ring */
.wordmark { left:214px; top:262px; transform:translateY(-50%); font:58px 'Anton'; color:var(--cream); }
           /* "une·deux" */
.handle   { right:96px; top:262px; transform:translateY(-50%); font:32px 'Saira Condensed'; font-weight:600; color:var(--cream); }
           /* "@UNE.DEUX" */
.hairline { left:96px; right:96px; top:318px; height:4px; background:var(--cream); }
.tag      { left:96px; top:350px; height:58px; background:var(--ocre-render); color:var(--ink);
            font:32px 'Saira Condensed'; font-weight:600; padding:0 15px; display:flex; align-items:center; }
           /* "CE JOUR LÀ …" */
```

Ne PAS ajouter de dégradé d'assombrissement en bas du cadre (`scrim-bottom`)
— règle permanente pour ce format, sauf demande contraire explicite.

**Compensation couleur ocre pour le rendu vidéo** (`--ocre-render`, utilisé
ci-dessus sur `.tag` et référencé en §4/§4bis) : le pipeline de render
HyperFrames (capture écran → encodage vidéo H.264) décale légèrement les
couleurs — `var(--ocre)` (#C2A04E) ressort visiblement plus terne/décalé
dans une vidéo rendue que dans l'éditeur web (confirmé par pixel-sampling
sur un rendu réel et par un test isolé, aplat de couleur seul). Pour tout
élément dont l'ocre doit apparaître correct **dans la vidéo rendue** (`.tag`,
`.kw-box` du titre §4bis, mots-clés `b.ocre` du corps §4), déclarer une
variable locale compensée dans la composition :
```css
:root { --ocre-render: #B9A456; }  /* compense le décalage du pipeline de
                                       render — quasi pixel-exact sur la
                                       référence validée par Thomas */
```
**Ne pas modifier `tokens/colors.css`** — le token `--ocre` doit rester
fidèle à `editeur-series.html` (l'éditeur web n'a pas ce problème, propre au
pipeline de render vidéo) ; `--ocre-render` est une compensation locale à
déclarer dans chaque composition qui affiche de l'ocre à l'écran dans un
rendu final. Si un nouveau rendu montre encore un écart visible face à une
référence validée, recalibrer cette valeur par pixel-sampling plutôt que de
supposer qu'elle reste universelle indéfiniment (le pipeline de render peut
évoluer).

### 4. Corps de texte — sous-titres animés, découpés en unités de sens

**Deux styles au choix, sélectionnés par Thomas dans le lanceur
(`editeurs/lanceur-cejourla.html`, champ « Style des sous-titres ») ou
donnés en instruction explicite dans le chat** — la ligne `STYLE
SOUS-TITRES: …` du brouillon "LANCER REEL" fait foi (absence de la ligne,
ou anciennes valeurs `actuel`/`tiktok` d'avant le renommage, = demandes
envoyées avant l'ajout/le renommage de ce champ = traiter comme §4.A
Fixe). Les deux styles partagent : la source du texte (CORPS du brouillon,
utilisé tel quel), la mécanique de fondu par bloc (`fromTo(opacity 0→1)`
puis `to(opacity→0)` + `tl.set(opacity:0)` hard-kill), et le centrage
horizontal du texte. **Tout le reste diffère** — découpage en unités,
position verticale, présence ou non d'un titre animé séparé, démarrage
dans la timeline — voir chaque sous-section, ne pas supposer qu'une valeur
d'un style s'applique à l'autre.

- Utiliser le texte du **CORPS** du brouillon Gmail tel quel (ne pas le
  réécrire) — chercher le brouillon "POST DU JOUR — <date>" correspondant à
  la date demandée ("le post de demain" etc.) via `search_threads`/
  `list_drafts`, section `CORPS`.

#### 4.A — Style fixe (défaut, `STYLE SOUS-TITRES: fixe`)

- Position : `top:1420px` avec `transform:translateY(-50%)`, zone
  `left:96px; right:96px`, dans la bande floutée basse (sous le plan net —
  valeur calibrée pour la géométrie §2, où le plan net s'arrête à `y=1308`).
  Garder une marge d'environ 100-115px entre le bas du plan net et `top`.
- **Le corps démarre juste après la fin de l'intro** (§4bis, titre animé —
  présent uniquement dans ce style) dans la timeline globale de la
  composition — décaler tous les `start` calculés en §5 de `introEnd`
  (durée totale de l'intro, cf. §4bis), pas de `t=0`.
- **Découpage en unités : phrases/propositions** du CORPS, chacune son
  propre bloc (peut tenir sur 2-3 lignes, cf. règle una-seule-ligne propre
  à 4.B ci-dessous qui ne s'applique pas ici).

- Mots-clés importants en **gras et/ou ocre** (`<b>` pour gras crème,
  `<b class="ocre">` pour gras + couleur `var(--ocre-render)`, cf. §3) —
  chiffres, scores, noms propres, faits marquants. Ne pas surcharger : un ou
  deux par phrase.
- Police Archivo (corps de texte, pas Anton tout-capitales — c'est de la
  prose, pas un sous-titre condensé), ~38px, line-height 1.38, couleur
  crème, `text-shadow: 0 2px 16px rgba(0,0,0,.65), 0 1px 4px rgba(0,0,0,.8)`
  pour la lisibilité (remplace tout scrim, puisque le bas ne doit pas être
  assombri).
- Bloc entier en fondu (fromTo/to opacity, cf. ci-dessus) — pas de
  surlignage mot par mot, tout le bloc a la même couleur en même temps
  (hors `<b class="ocre">` ponctuel).

#### 4.B — Style karaoké (`STYLE SOUS-TITRES: karaoké`)

Refondu le 11 août 2026 après un test grandeur nature (branche
`claude/reels-video-storytelling-structure-cdpnoy`, reel 11 août 1984)
inspiré d'une référence externe (compte paris sportifs) que Thomas a
validée ("Ok ok pas mal"). **Remplace entièrement l'ancienne mécanique
"TikTok"** (surlignage mot par mot par encadré ocre mobile, police
Archivo 700, une ligne assemblée par contrainte de largeur) — cette
ancienne mécanique est abandonnée, ne pas la réintroduire. Le style
karaoké n'a **pas** de titre animé séparé (§4bis ne s'applique pas à ce
style, cf. note en tête de §4bis) : le corps couvre tout le reel, de
juste après le header jusqu'au CTA.

- **Source du texte : le champ `CORPS (karaoké)` du brouillon "POST DU
  JOUR — <date>" (skill `une-deux-post`, SKILL.md § « Livrable quotidien »)
  — PAS le champ `CORPS` générique**, qui reste la source du style Fixe
  (§4.A). Le brouillon quotidien contient les deux champs côte à côte
  depuis leur ajout au workflow (11 août 2026) : `CORPS` (paragraphes,
  utilisé aussi par le carrousel et la légende) et `CORPS (karaoké)`
  (lignes courtes, storytelling, écrit spécifiquement pour ce style — voir
  SKILL.md pour les règles de rédaction). Ne jamais utiliser `CORPS` pour
  ce style même si `CORPS (karaoké)` semble absent avant d'avoir relu le
  brouillon en entier — c'est un champ séparé, pas une section du `CORPS`.
  **Une ligne de `CORPS (karaoké)` = un carton affiché à l'écran,
  verbatim.** Contrairement à 4.A (découpage algorithmique en
  phrases/propositions) ou à l'ancienne mécanique 4.B (regroupement par
  contrainte de largeur), ici il n'y a **aucun re-découpage côté
  traitement** — chaque saut de ligne devient directement un carton, dans
  l'ordre. La responsabilité de la brièveté (viser ~3 mots par ligne,
  jamais une phrase entière) revient à qui rédige `CORPS (karaoké)`, pas à
  la Routine.
  **Si le brouillon ne contient pas de champ `CORPS (karaoké)`** (brouillon
  produit avant l'ajout de ce champ, ou rédigé à la main sans le suivre) :
  ne pas re-découper soi-même le `CORPS` générique en silence — signaler le
  manque à Thomas et proposer soit de réécrire `CORPS (karaoké)` à partir
  des mêmes faits déjà vérifiés du `CORPS` (mêmes règles que SKILL.md :
  accroche sans spoiler, boucle qui se referme, ~3 mots/ligne), soit de
  traiter ce reel en style Fixe à la place.
- **Police Anton** (pas Archivo — contrairement à l'ancienne mécanique
  4.B), `text-transform:uppercase`, mais **le texte doit être écrit
  directement en MAJUSCULES dans le HTML source**, jamais compter sur la
  transformation CSS seule : le compilateur HyperFrames fait du
  subsetting de police sur les caractères littéraux du HTML, pas sur le
  résultat visuel de `text-transform` — un mot dont la version minuscule
  seule apparaît dans le source (ex. `Brisson ouvre le score` avec un `v`
  minuscule mais jamais de `V` majuscule ailleurs) se retrouve avec un
  glyphe manquant pour le `V` majuscule affiché (rendu en signe cassé,
  bug identifié et corrigé sur ce test — toujours écrire le texte des
  `.story-line` déjà en capitales dans le HTML, `text-transform:uppercase`
  reste en CSS comme filet de sécurité mais ne doit jamais être la seule
  source des majuscules).
- **Taille bien plus grande que 4.A, mais FIXE — jamais de réduction selon
  la longueur de la carte.** Corrigé le 12 août 2026 : la première version
  de ce style avait deux paliers (108px courtes / 80px longues) qui
  faisaient visiblement "rétrécir" le texte sur les cartes à 2-3 mots —
  Thomas a explicitement demandé une taille similaire quel que soit le
  nombre de mots par ligne. **`font-size:80px` fixe** (`line-height:1.1`)
  pour toutes les cartes, sans exception ni classe de taille alternative —
  cette taille tient déjà sur une seule ligne dans les 888px utiles pour
  une carte de ~18 caractères (validé par extraction de frame sur le test
  du 11 août 1984).
  Si un cas dépasse malgré la règle "~3 mots/ligne" de SKILL.md, **wrap
  sur 2 lignes plutôt que de réduire la taille** — ne jamais réintroduire
  de palier de taille par longueur.
- **Aucune ombre portée** — la lisibilité vient de la taille/graisse
  d'Anton, pas d'un effet flou. **Léger contour semi-transparent** sur le
  texte (ajouté le 12 août 2026, demande explicite de Thomas — l'ancienne
  consigne "aucun contour" de la version précédente de ce style est
  remplacée par celle-ci) :
  ```css
  -webkit-text-stroke: 1.5px rgba(44,40,35,.35);
  ```
  (`rgba(44,40,35,…)` = `--ink` en RGB, à faible opacité — un contour
  sombre discret pour détacher le texte crème du fond sans reproduire
  l'effet "contour noir" épais façon sous-titre générique ; ajuster
  l'opacité/l'épaisseur au jugé si le texte semble flou ou si le contour
  devient trop visible en extraction de frame, mais rester sur un ink
  semi-transparent, pas un noir ou un crème plein comme testé et écarté
  précédemment). Couleur du texte crème (`var(--cream)`) par défaut, tout
  le carton change d'état en même temps (fondu bloc entier, cf. mécanique
  commune du §4) — **pas de surlignage mot par mot animé dans le temps**
  (l'ancienne mécanique "TikTok" à encadré ocre mobile reste abandonnée,
  cf. tête de §4.B) ; la seule exception à la couleur crème par défaut est
  statique, cf. règle ci-dessous.
- **Mot-clé en ocre via `**mot**`** (ajoutée le 13 août 2026, demande
  explicite de Thomas) : si une ligne de `CORPS (karaoké)` contient un ou
  plusieurs mots encadrés par des astérisques doubles (`**mot**`), retirer
  les `**` et afficher ce(s) mot(s) en couleur ocre (`var(--ocre-render)`,
  cf. §3) au lieu du crème par défaut — même principe d'extraction par
  position que les mots-clés du titre animé (§4bis, `extractGreenWords`) :
  pas de sélection "au jugé" côté traitement, uniquement les mots que la
  rédaction de `CORPS (karaoké)` a explicitement marqués (voir SKILL.md §
  « Livrable quotidien », champ `Corps (karaoké)`). Implémentation : envelopper
  chaque mot marqué dans `<b class="ocre">` (même convention que le
  `<b class="ocre">` du corps en style Fixe, §4.A) à l'intérieur du
  `.story-line`, avec :
  ```css
  .story-line b.ocre { color:var(--ocre-render); font-weight:inherit; }
  ```
  Contrairement au `kw-box` du §4bis (carré ocre plein derrière le mot),
  ici pas de fond ni de padding — seule la couleur du texte change, tout le
  reste du carton (police, taille, contour) reste identique. Une ligne peut
  mélanger mots crème et mots ocre ; le fondu du bloc entier (§4/§4.B) reste
  la seule animation, aucun tween supplémentaire par mot. Si une ligne de
  `CORPS (karaoké)` ne contient aucun `**…**`, elle reste entièrement crème
  comme avant cette règle.
- **Position : centré verticalement dans le cadre** (pas dans la bande
  basse comme 4.A) — le texte est superposé directement sur le plan net,
  au milieu de l'écran, comme sur la référence externe. CSS :
  ```css
  .story-zone { position:absolute; left:96px; right:96px; z-index:20; text-align:center; }
  .story-line {
    position:absolute; left:0; right:0;
    top:50%; transform:translateY(-50%);
    font-family:'Anton', sans-serif; font-size:80px; line-height:1.1;
    color:var(--cream); opacity:0;
    -webkit-text-stroke: 1.5px rgba(44,40,35,.35);
  }
  ```
  `.story-zone` n'a pas besoin de `top`/`height` explicites si elle est un
  enfant direct de `#root` (elle hérite de sa hauteur 1920px) — chaque
  `.story-line` se centre indépendamment via son propre
  `top:50%; transform:translateY(-50%)`, donc toutes les cartes (1 ou
  plusieurs lignes) se superposent bien au même centre vertical quel que
  soit leur nombre de lignes.
- **Piège §6 applicable ici** : `.story-line` porte un `transform:
  translateY(-50%)` **statique** pour ce centrage — ne **jamais** animer
  `y` dessus avec GSAP (contrairement au léger `y:10→0` utilisé par le
  fondu commun du §4/§5 sur d'autres styles). Pour le style karaoké,
  utiliser des tweens **opacity uniquement** :
  ```js
  function fadeBlockKaraoke(sel, start, dur) {
    tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.10, ease: 'power2.out' }, start);
    tl.to(sel, { opacity: 0, duration: 0.08, ease: 'sine.in' }, start + dur - 0.08);
    tl.set(sel, { opacity: 0 }, start + dur);
  }
  ```
- **Il doit toujours y avoir un sous-titre à l'écran, sans exception** —
  aucun trou, y compris pendant les moments forts (but, célébration) :
  contrairement à 4.A où une pause de 0.15-0.5s sépare les blocs (cf. §5),
  ici les cartes sont **contiguës** (`start` de la carte N+1 = `start +
  dur` de la carte N, zéro pause). S'il n'y a plus de ligne de CORPS
  disponible pour combler un moment fort, répéter/reformuler brièvement un
  fait déjà énoncé (ex. le score) plutôt que de laisser l'écran sans texte
  — jamais inventer un fait non sourcé pour combler.
- **Aucun ralenti sur la vidéo source** — règle générale du pipeline (cf.
  §2), rappelée ici car explicitement demandée par Thomas sur ce style :
  le réencodage/rééchantillonnage de frame rate ne doit jamais s'accompagner
  d'un `setpts`/ralenti, la vidéo doit rester à sa vitesse native du début
  à la fin.
- Style validé le 11 août 2026 — reste un choix explicite de Thomas par
  reel (par défaut le style 4.A Fixe si rien n'est précisé), ni l'un ni
  l'autre ne devient le nouveau standard implicite sans qu'il le dise.

### 4bis. Titre animé de l'intro

**Ne s'applique qu'au style Fixe (§4.A).** Le style Karaoké (§4.B) n'a pas
de titre animé séparé — sauter entièrement cette section pour ce style, le
champ `TITRE` du brouillon n'est pas utilisé pour l'habillage vidéo (il
reste utile ailleurs, ex. légende Instagram), et le corps (§4.B) démarre
directement après le header, cf. §5.

- **Source du titre** : champ `TITRE` du brouillon Gmail "POST DU JOUR —
  <date>" correspondant (pas `CORPS` — c'est le champ court/percutant,
  distinct du texte long utilisé en §4 pour le corps). Repris tel quel, mis
  en capitales par le CSS (`text-transform:uppercase`).
- **Mots-clés encadrés : uniquement ceux marqués `**entre étoiles**`** dans
  le champ TITRE — même mécanisme d'extraction par position que le mode
  batch de `editeur-series.html` (`extractGreenWords`) : retirer les `**`,
  garder la position des mots qu'ils entouraient, et n'encadrer que ces
  mots-là. Pas de sélection "au jugé" — c'est Thomas qui marque explicitement
  le(s) mot(s)/la ou les lignes à encadrer en écrivant le brouillon.
  Un carré fusionné derrière chaque groupe de mots consécutifs marqués,
  couleur `var(--ocre-render)` (cf. §3), texte toujours crème (pas
  d'inversion de couleur).
- **Découpage en lignes** : à la main (pas d'auto-wrap côté HTML/HyperFrames
  contrairement au canvas de l'éditeur) — composer au jugé puis corriger
  après vérification par extraction de frame (§9) si une ligne déborde des
  marges (`left:96px; right:96px`, soit 888px de large utile).
- **CSS/HTML/GSAP à reproduire à l'identique** (`Anton`, aligné à **gauche**
  — pas centré, contrairement au corps de texte du §4, et **sans ombre
  portée** — contrairement au corps de texte du §4 qui en a besoin faute de
  carré plein derrière, la lisibilité du titre vient du carré ocre sur les
  mots-clés) :
  ```css
  .t-line { position:absolute; left:96px; right:96px; font-family:'Anton',sans-serif;
            font-size:140px; line-height:1; text-transform:uppercase; color:var(--cream);
            opacity:0; }
  .kw-box { background:var(--ocre-render); padding:10px; margin:-10px; display:inline-block; }
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
- **Vitesse d'apparition fixée à 1.0×** (pas de variation) :
  ```js
  const start = 0.3, revealMs = 0.62, fadeMs = 0.22;   // vitesse figée ×1
  lines.forEach((sel, i) => {
    tl.fromTo(sel, {opacity:0, y:8}, {opacity:1, y:0, duration:fadeMs, ease:'none'}, start + i*revealMs);
  });
  ```
  Formule : `revealMs = 620/1 = 0.62s`, `fadeMs = clamp(80,220,revealMs*0.6) = 0.22s`
  (capé) — rampe **linéaire** (`ease:'none'`), pas d'easing, avec un léger
  décalage vertical 8px→0px qui accompagne le fondu.
- **Une fois toutes les lignes affichées, le titre reste figé à l'écran
  1 seconde avant la coupe vers le corps.** Durée totale de l'intro (à
  utiliser comme offset de démarrage du corps, cf. §4) :
  ```
  introEnd = start + (nombreDeLignes - 1) × revealMs + fadeMs + 1.0
           = 0.3 + (n-1) × 0.62 + 0.22 + 1.0   (secondes)
  ```
  À `introEnd`, **masquer les lignes de titre** (`tl.set('.t-line', {opacity:0}, introEnd)`,
  hard-kill sur toutes les lignes en une fois) — le header (ring/wordmark/
  handle/hairline/tag) reste affiché, seul le titre disparaît avant que le
  corps de texte (§4) ne commence. Le plan vidéo, lui, ne change pas : c'est
  le même composite continu (§2) qui continue de jouer sous les deux
  couches de texte successives.
- **Positionnement vertical** : ancrer par le bas, `top` de chaque ligne =
  baseline − ascent avec baseline la plus basse ≈ 1690-1730px (juste
  au-dessus de la zone de sécurité basse) et un écart entre lignes de
  `tSize*0.92` ≈ 120px — recalculer précisément pour chaque titre (nombre de
  lignes différent) plutôt que de réutiliser les pixels bruts du gabarit de
  référence, qui ne valent que pour son titre à 4 lignes.

### 5. Calcul du rythme du corps (formule établie, réutiliser systématiquement)

```
durée_brute_ligne = nombre_de_mots × 0.27 + 0.35   (secondes)
facteur = (durée_vidéo_disponible − Σ pauses) / Σ durée_brute_toutes_lignes
durée_ligne = durée_brute_ligne × facteur
```

Cette formule sert de base au **style Fixe**. Le style Karaoké a sa propre
logique de rythme (mesurée directement sur la vidéo de référence, pas une
formule proportionnelle au nombre de mots) — voir ci-dessous, ne pas
appliquer la formule mots×durée à ce style.

**Style Fixe (§4.A)** :
- Pauses entre blocs : 0.15s (vidéo courte, rythme serré) à 0.5s (vidéo
  longue, rythme posé) selon la marge disponible.
- Démarrer le premier bloc du corps à `introEnd + 0.3s` (§4bis) — pas de
  `t≈0.3s` absolu comme avant la fusion, le corps commence après l'intro.
  `durée_vidéo_disponible` = durée totale de la vidéo moins `introEnd`.
- `tl.fromTo(..., {opacity:0}, {opacity:1, duration:0.2-0.35, ease:'power2.out'})`
  puis `tl.to(..., {opacity:0, duration:0.18-0.3, ease:'sine.in'})` puis
  `tl.set(..., {opacity:0}, start+dur)` (hard-kill obligatoire, sinon lint
  `gsap_exit_missing_hard_kill`).

**Style Karaoké (§4.B)** :
- **Rythme mesuré directement sur la vidéo de référence** (compte paris
  sportifs, cf. §4.B), le 12 août 2026 : échantillonnage vidéo à 0.25s sur
  un segment dense de mots ("L'ANGLETERRE" → "VA GAGNER" → "LA COUPE" →
  "DU MONDE" → "C'EST" → "UN PRONOSTIC" → "QUI CIRCULE" → "DEPUIS" → "LE
  DÉBUT" → "DE LA" → "COMPÉTITION"). Durée de tenue observée par carte :
  **0.25 à 0.75s, moyenne ≈ 0.35-0.4s** — sans corrélation nette au nombre
  de mots (des cartes à 1 mot et à 2-3 mots tiennent dans la même
  fourchette). **Ne pas utiliser la formule mots×durée du style Fixe** —
  une durée de base quasi fixe, pas proportionnelle à la longueur de la
  carte :
  ```
  durée_carte_brute ≈ 0.35s   (fixe, indépendante du nombre de mots)
  facteur = durée_vidéo_disponible / (n_cartes × 0.35)
  durée_carte = 0.35 × facteur
  ```
  - Si `facteur > 1` (pas assez de lignes de `CORPS (karaoké)` pour
    couvrir toute la vidéo à 0.35s/carte) : étirer chaque carte par ce
    facteur plutôt que laisser un trou (règle "toujours un sous-titre à
    l'écran" du §4.B) — le rythme sera alors un peu plus lent que la
    référence, compromis acceptable.
  - Si `facteur < 1` (plus de lignes que la vidéo ne peut en tenir à
    0.35s/carte) : compresser, mais **ne jamais descendre sous ~0.2s/carte**
    (proche du rythme le plus rapide observé). En dessous, signaler à
    Thomas qu'il y a trop de lignes de `CORPS (karaoké)` pour la durée de
    la vidéo plutôt que de produire un rendu illisible.
- **Zéro pause entre blocs** — cartes contiguës (`start` de la carte N+1 =
  `start + dur` de la carte N), cf. règle "toujours un sous-titre à
  l'écran" du §4.B. Ne pas utiliser la fourchette 0.15-0.5s du style Fixe.
- Démarrer le premier bloc à `~0.2-0.3s` absolu (pas d'`introEnd`, pas de
  §4bis pour ce style) — `durée_vidéo_disponible` = durée totale de la
  vidéo (moins ce petit offset de départ).
- Fondu plus rapide que le style Fixe (cf. `fadeBlockKaraoke` du §4.B,
  `inDur:0.10` / `outDur:0.08`) — cohérent avec des cartes de 0.2-0.5s, pas
  la place pour un fondu plus long.

### 6. Piège GSAP à ne jamais reproduire

Un élément avec un `transform: translateY(-50%)` **statique** en CSS (pour
le centrage vertical) ne doit **jamais** recevoir de tween GSAP incluant la
propriété `y` — ça entre en conflit avec le transform géré par le CSS.
Utiliser des tweens **opacity uniquement** sur ces éléments (le titre de
l'intro, qui anime `y:8→0`, est une exception volontaire : `.t-line` n'a
**pas** de `transform` statique, donc pas de conflit).

### 7. Scaffolding projet

Chaque reel = un nouveau dossier `<date-ISO>/` (ex. `2026-08-05/`) **à la
racine de la branche `ce-jour-là`** — pas de préfixe `hyperframes/`, pas de
slug descriptif — avec `hyperframes.json`, `meta.json`, `package.json`
(copier depuis un projet existant et adapter `name`/`id`), `.gitignore`
(`node_modules/`, `renders/`, `snapshots/`, `.debug/`, `assets/` — ajouté le
12 août 2026, voir §9 pour la justification), `tokens/fonts.css` +
`tokens/colors.css` copiés tels quels (source de vérité : palette
`--ocre`/`--ink`/`--cream`/`--muted-cream` de `editeurs/editeur-series.html`
— `--ocre-render`, lui, se déclare localement dans `index.html`, cf. §3).

**Paralléliser le scaffold avec le bake ffmpeg §2** (optimisation du
12 août 2026) : écrire `index.html` (header, textes, timeline GSAP) et
copier les fichiers de scaffold ci-dessus ne dépend que de la **durée** de
la vidéo, connue dès l'inspection d'orientation du §1 — pas du fichier
`composite.mp4` fini. Lancer le composite ffmpeg du §2 en tâche de fond
(`run_in_background`) et rédiger le scaffold + `index.html` pendant qu'il
tourne, plutôt que d'attendre la fin de l'encodage pour commencer à écrire
la composition — ça sort ce poste du chemin critique séquentiel.
`npm run check` (§9), lui, doit attendre que `composite.mp4`/`audio.m4a`
existent réellement sur disque avant de tourner.

Toujours un projet HyperFrames (le titre animé de l'intro est désormais
systématique — il n'y a plus de cas "composite ffmpeg seul, sans
HyperFrames", sauf le cas à part §2 "juste le composite, sans habillage").

Vidéo et audio en enfants directs de `#root`, vidéo mutée
(`muted playsinline`), son porté par un `<audio>` séparé avec sa propre
`data-duration` (contrainte HyperFrames — jamais de son sur `<video>`).
**Un seul élément `<video>`** pour toute la composition (le composite
continu de §2) — pas d'élément par plan/segment sauf si le mode curé
(§1bis, opt-in) a explicitement recomposé la vidéo à partir de plusieurs
plans mis bout à bout, auquel cas ils restent quand même mergés en un seul
fichier composite avant d'entrer dans HyperFrames, jamais plusieurs
`<video>` séquencés par `data-start`/`data-duration`.

### 8. CTA de fin — carte "RDV DEMAIN", ajoutée systématiquement

**Tous les montages se terminent par le même CTA générique** — pas de
personnalisation par date, pas de re-rendu à chaque fois. Le rendu final
validé est committé en tant qu'asset réutilisable :
`templates/rdvdemain-intro/cta-final.mp4` (branche `ce-jour-là`, 3.0s,
1080×1920, h264/yuv420p/30fps, pas de piste audio). Le gabarit HyperFrames
source (`templates/rdvdemain-intro/index.html`) n'a besoin d'être modifié
et re-rendu que si le CTA lui-même doit changer un jour — sinon, toujours
réutiliser `cta-final.mp4` tel quel.

Une fois le rendu HyperFrames de l'intro+corps obtenu (§9), le concaténer
avec le CTA via le filtre `concat` (pas le démuxeur `-f concat`, qui exige
des flux strictement identiques — le CTA n'a pas de piste audio, le reel
peut en avoir une) :

```bash
ffmpeg -y -i reel-intro-corps.mp4 -i templates/rdvdemain-intro/cta-final.mp4 -filter_complex \
"[0:v]setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[outv]" \
-map "[outv]" -map 0:a? -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p -c:a aac reel-final.mp4
```

**`-preset veryfast` (pas `fast`) sur ce ré-encodage précis** — optimisation
du 12 août 2026. Ce concat est déjà le **3ᵉ encodage complet** de la même
vidéo (bake §2 → capture/encodage interne du render HyperFrames → ce
ré-encodage de raccord) : la qualité perçue est verrouillée par les deux
passages précédents, ce raccord ne fait que recoller deux fichiers déjà
définitifs au même CRF — un preset plus rapide n'introduit pas de perte
visible supplémentaire à CRF constant. **Ne pas confondre avec les presets
du §2** (bake principal du composite) ni ceux internes au render
HyperFrames, qui restent `fast` et inchangés — cette optimisation ne
s'applique qu'à cette seule commande de raccord CTA. Le contrôle visuel du
§9 (extraction de frames à la coupe reel→CTA) reste obligatoire et
suffirait de toute façon à détecter un problème d'encodage si ce
raisonnement s'avérait faux sur un cas réel.

Le CTA s'ajoute donc en coupe franche (pas de fondu-enchaîné) — c'est
attendu, c'est une carte de fin sur fond clair complètement différente du
composite sombre du reel, pas une continuité visuelle.

### 9. Check → render → concat CTA → vérif → livraison

```bash
npm run check     # 0 erreur attendu ; le warning StaticGuard "data-end
                   # without data-duration" et le timeout Runtime sont des
                   # flakes connus, non bloquants si le Lint affiche 0 erreur —
                   # MAIS le warning "sparse keyframes" (§2) doit lui être
                   # corrigé avant de livrer, ce n'est pas un flake
npm run render     # tourne en tâche de fond (>2 min) — laisser tourner,
                   # ne pas sonder, attendre la notification
```

**`package.json` doit passer `-w 4`** (`"render": "npx --yes hyperframes@0.7.64 render -w 4"`, à reprendre dans tous les nouveaux scaffolds §7) — le mode par défaut (`-w auto`) sous-estime souvent les workers disponibles (mesuré : 2 workers choisis sur une machine à 4 cœurs). Passer explicitement à 4 workers a réduit le temps de rendu de 43% sur un test contrôlé (67s → 38s, même composition, même machine) sans rien changer d'autre. Adapter le chiffre au nombre de cœurs réels si la machine de rendu diffère, mais ne jamais laisser `auto` deviner sans l'avoir vérifié au moins une fois.

Puis concaténer le CTA (§8) sur le fichier obtenu dans `renders/`.

Après concat : extraire des frames à quelques instants clés (titre de
l'intro à mi-révélation et pleinement révélé, coupe intro→corps — **vérifier
qu'il n'y a aucun saut de cadrage visible à cette coupe, cf. §2**, quelques
plans du corps, carte CTA finale) via `ffmpeg -ss <t> -frames:v 1` — **lancer
ces extractions en parallèle** (optimisation du 12 août 2026 : chaque
commande en tâche de fond avec `&`, puis `wait` — chacune ré-ouvre/décode le
fichier indépendamment, donc les paralléliser ne coûte rien et évite
d'attendre N fois le coût de décodage d'un enchaînement séquentiel) — puis
les lire avec l'outil Read pour vérifier visuellement le calage texte/image,
la lisibilité, le header, la couleur ocre (cf. §3) et la coupe propre vers
le CTA — ne jamais livrer sans ce contrôle.

**INTERDIT de livrer un fichier depuis `assets/`** (sources brutes du
composite, sans header ni texte) — le seul livrable valide est le fichier
issu de `npm run render` (dans `renders/`) **après concat du CTA**. Si le
render n'a pas tourné ou a échoué, ne rien livrer et signaler le blocage.

**Livraison : uniquement par commit/push Git sur `ce-jour-là`, plus de
Google Drive.** Retiré le 12 août 2026 (demande explicite de Thomas — le
chemin d'upload Drive échouait de façon récurrente : limite de taille sur
`create_file` en base64 sans téléversement résumable, puis plus
récemment des refus d'autorisation systématiques sur le connecteur pour
cette session). L'ancienne double-livraison Drive + Git (avec Git en
repli si Drive échouait) est abandonnée — **Git est désormais le seul
canal, pas un repli** : ne plus tenter d'upload Drive du tout pour ce
livrable, ne plus recompresser de version dégradée pour l'upload (le
fichier committé reste la version pleine qualité issue du render).

Committer le dossier du projet — **`assets/` exclu depuis le 12 août
2026** (seuls `assets/`, `renders/`, `node_modules/`, `snapshots/`,
`.debug/` sont ignorés, cf. §7) — et pousser sur la branche `ce-jour-là`
(jamais fusionnée dans `main`). Le message de livraison à Thomas doit
pointer vers le chemin du fichier sur cette branche (ex. « Reel livré :
`<date>/reel-final.mp4` sur la branche ce-jour-là »).

**Pourquoi exclure `assets/`** : `composite.mp4`/`audio.m4a` (§2) sont des
fichiers intermédiaires reproductibles, jamais le livrable (rappel
ci-dessus) — ils pesaient à eux seuls autant que `reel-final.mp4` (~30 Mo
chacun sur les reels déjà livrés), doublant le poids poussé chaque jour
sur une branche qui n'est jamais purgée ni fusionnée : ce poids ne fait
que s'accumuler indéfiniment et ralentit chaque `git fetch`/`push`/`pull`
que la Routine fait sur cette branche, jour après jour.
**Contrepartie à connaître** : si Thomas redemande une retouche sur un
reel déjà livré (texte, timing), la vidéo source n'est plus dans le
dossier une fois committé — retélécharger depuis le lien Drive ou la
pièce jointe d'origine (§1) avant de pouvoir relancer le bake §2 ; si le
lien Drive a expiré entre-temps, le signaler à Thomas plutôt que
d'improviser une source de remplacement.

**Ne jamais se fier à la seule présence de `assets/` dans `.gitignore` —
vérifier explicitement avant chaque commit.** Incident du 13 août 2026 :
la règle d'exclusion ci-dessus existait dans `.gitignore` depuis le
12 août mais n'a en pratique **jamais fonctionné sur aucun des 10 dossiers
livrés entre le 5 et le 13 août** — `assets/` (composite.mp4 + audio.m4a)
s'est retrouvé committé à chaque fois malgré la règle, faisant grossir la
branche à plus d'1,3 Go et provoquant des `git fetch` en timeout (jusqu'à
11 minutes avant même de commencer le pipeline sur un run mesuré). Purgé
rétroactivement par réécriture d'historique (`git filter-repo`, branche
retombée à ~360 Mo) — mais la cause n'a pas été identifiée avec certitude
(probablement `git add` sur des fichiers déjà indexés avant l'écriture du
`.gitignore` du jour, ou un ordre d'opérations qui contourne l'exclusion),
donc rien ne garantit que ça ne se reproduise pas silencieusement.
**Avant tout commit du dossier de projet, vérifier explicitement les
fichiers réellement mis en index** (`git status --short` ou
`git add -n .` sur le dossier du jour) et confirmer qu'aucun chemin
`assets/` n'apparaît dans la liste — si c'en est un, `git reset` ce
chemin avant de committer plutôt que de faire confiance au `.gitignore`
seul. Ce contrôle est obligatoire à chaque livraison, pas seulement en cas
de doute.
