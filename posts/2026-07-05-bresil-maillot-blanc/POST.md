# L'arrêt de jeu — Pourquoi le Brésil ne joue plus en blanc

**Série :** L'arrêt de jeu · `#arretdejeu` · Carrousel 3:4 · signature rouille / surimpression dossier
**Production :** 100% `editeurs/editeur-series.html` — série `arretdejeu` verrouillée sur toutes les slides.
Pas de `post.html` sur ce post : le template **corps** (« cover corps seul, plein cadre ») est
pensé pour L'arrêt de jeu et porte tout le texte narratif, slide après slide.

**Méthode :** reformulation de l'article L'Officiel *« Brésil : les dessous d'un maillot
mythique »* (04.07.2018, texte intégral fourni par Thomas) — pas une synthèse. Le récit et
les faits de l'article sont conservés dans l'ordre, réécrits dans la voix une·deux (phrases
courtes, dépouillées, ton archiviste-conteur), répartis sur les slides `corps`.

⚠️ `editeur-series.html` n'a pas d'import JSON : chaque slide se saisit à la main dans le
formulaire (série + template + champs + photo). Le tableau ci-dessous sert de feuille de
saisie ; `script.json` reprend les mêmes valeurs en machine-readable pour archivage.

---

## Feuille de saisie — éditeur séries (les 9 slides, `serie = arretdejeu`)

### Slide 01 — template `titre` (COVER · TITRE SEUL)
- Titre : `POURQUOI LE BRÉSIL NE JOUE-T-IL PLUS JAMAIS EN BLANC ?`
- Mot-clé coloré : `JAMAIS`
- Slide / Total : `01` / `09`
- Photo : bresil_01.PNG

### Slide 02 — template `corps` (COVER · CORPS SEUL)
- Corps : « Le jaune brésilien, c'est la samba, les dribbles chaloupés, le Joga Bonito. L'inverse total des maillots sombres de l'Ancien Monde. Sauf que cette couleur n'a pas toujours habillé la Seleção. De 1930 à 1950, le Brésil joue en blanc et bleu, écusson sur le cœur. Le jaune n'arrivera qu'en 1954, en Suisse. »
- Slide / Total : `02` / `09`
- Photo : bresil_02.PNG

### Slide 03 — template `corps`
- Corps : « Tout commence par deux démonstrations. 7-1 contre la Suède. 6-1 contre l'Espagne. Ademir et Chico affolent les défenses. Un pays entier se voit déjà champion du monde, chez lui. Le 16 juillet 1950, le Maracanã est plein à craquer. Rien ne semble pouvoir arrêter le Brésil. »
- Slide / Total : `03` / `09`
- Photo : bresil_03.PNG

### Slide 04 — template `corps`
- Corps : « Friaça ouvre le score. Le stade explose. À la 66e minute, Juan Alberto Schiaffino égalise pour l'Uruguay. À la 79e, l'ailier du CA Peñarol double la mise. Le Maracanã se tait d'un coup. Tout le monde comprend. Au coup de sifflet, la Coupe du Monde est remise au capitaine uruguayen, presque en catimini. »
- Slide / Total : `04` / `09`
- Photo : bresil_04.PNG

### Slide 05 — template `corps`
- Corps : « Au lendemain, tout un pays cherche un coupable. Ce sera le gardien, Moacir Barbosa Nascimento. On le maudit, on l'accable. Jusqu'à sa mort, en 2000, les Brésiliens ne lui pardonneront jamais cette défaite. »
- Slide / Total : `05` / `09`
- Photo : bresil_05.PNG

### Slide 06 — template `corps`
- Corps : « Puisque les symboles comptent, le maillot blanc est jugé lui aussi. Il ne porte aucune des couleurs du drapeau : on le déclare insuffisamment patriotique. Dans la précipitation, la fédération brésilienne lance un grand concours pour le redessiner entièrement. »
- Slide / Total : `06` / `09`
- Photo : bresil_06.PNG

### Slide 07 — template `corps`
- Corps : « Aldyr Garcia Schlee, 19 ans, propose un maillot jaune à parements verts, un short bleu, des chaussettes blanches. Presque celui d'aujourd'hui. Il remporte le concours. Le jaune évoque la richesse minérale du pays, l'or en particulier. Le vert, l'Amazonie. Le bleu, son fleuve. Le blanc, les étoiles de la bannière nationale. »
- Slide / Total : `07` / `09`
- Photo : bresil_07.PNG

### Slide 08 — template `corps`
- Corps : « En 2018, Nike reprend ces codes avec un jaune plus sombre et un col vert. À l'intérieur, une pastille reprend le globe du drapeau, entourée du message : « Você é Seleção. » Tu es la sélection. Des zigzags discrets ornent les manches. Une façon de réinterpréter le mythe, sans jamais le dénaturer. »
- Slide / Total : `08` / `09`
- Photo : bresil_08.PNG

### Slide 09 — template `cta` (CTA ENREGISTRE)
- Titre : `RESTE DANS LE JEU`
- Corps : `Une histoire par semaine. On aligne les faits, jamais de réponse toute faite.`
- Libellé bouton : `FOLLOW`
- Slide / Total : `09` / `09`

**Débat (pour la légende, pas dans l'éditeur) :** « Le vrai génie du Brésil, c'est le foot ou le marketing d'un traumatisme ? »

---

## Prompts photo (style presse, `nano_banana_pro`, 4:5, virage rouille enquête)

**bresil_01.PNG (cover — le maillot blanc de 1950)**
```
The Brazil national football team wearing the 1950 Brazil white home kit with blue trim, in 1950. Players walking onto the pitch at a packed stadium, tense atmosphere before kickoff. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, period stadium atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_02.PNG (le jaune aujourd'hui vs hier)**
```
The Brazil national football team wearing a modern Brazil yellow home kit, in the present day. Players celebrating a goal together on the pitch with joyful, expressive body language. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, modern stadium atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_03.PNG (la marche vers 1950 — 7-1, 6-1)**
```
The Brazil national football team wearing the 1950 Brazil white home kit with blue trim, in 1950. Players celebrating a goal together on the pitch, joyful confident mood. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, period stadium atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_04.PNG (la chute — remise en catimini)**
```
The Uruguay national football team captain receiving the Jules Rimet trophy on the pitch at a packed stadium, in 1950. A brief handshake, no ceremony, subdued silent crowd in the background. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, period stadium atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_05.PNG (le bouc émissaire — Moacir Barbosa)**
```
Moacir Barbosa, Brazilian football goalkeeper, aged 29 at the time, in 1950. Solitary pensive portrait, melancholic downcast mood. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_06.PNG (le maillot aussi jugé)**
```
The Brazil national football team wearing the 1950 Brazil white home kit with blue trim, in 1950. Players sitting in the locker room after the match, dejected and silent mood. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, period locker room atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_07.PNG (le concours — Aldyr Garcia Schlee)**
```
Aldyr Garcia Schlee, Brazilian newspaper illustrator, aged 19 at the time, in 1953. Sitting at a drawing desk in a small newsroom in Pelotas, sketching a football jersey design, focused expression. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, period newsroom atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

**bresil_08.PNG (le mythe aujourd'hui — maillot 2018)**
```
Close-up of a Brazilian football player wearing the 2018 Brazil yellow home kit with green collar detailing, in 2018. Focus on the collar and crest details, proud confident mood. Press photography, investigative documentary mood, warm rust-toned sepia, balanced contrast, soft natural light, cinematic film grain, modern stadium atmosphere. Realistic photograph, not illustration. Portrait 4:5. No text.
```

---

## Légende (L'arrêt de jeu — 4 temps)

```
**Pourquoi le Brésil ne porte plus jamais de maillot blanc ? 🤔🇧🇷**

Jusqu'en 1950, la Seleção jouait en blanc et bleu. Le 16 juillet, au Maracanã, l'Uruguay prive le Brésil du titre à domicile : défaite 2-1, un silence de 200 000 personnes. Le pays cherche un coupable : ce sera le gardien Moacir Barbosa, puni jusqu'à sa mort en 2000. Le maillot blanc, lui, est jugé « insuffisamment patriotique ». Un concours national le redessine : jaune, vert, bleu, blanc, les couleurs du drapeau.

Et le plus fou ? Ce maillot dessiné dans l'urgence, par un inconnu de 19 ans, n'a plus jamais changé depuis 1954.

Alors dis-nous : le vrai génie du Brésil, c'est le foot ou le marketing d'un traumatisme ? 👇
@une.deux ⚽️
.
.
#arretdejeu #seleção #maracanazo #footballhistoire #unedeux
```

---

## Vérification factuelle (règle des 3 sources)

| Fait | Statut | Sources indépendantes |
|------|--------|------------------------|
| Blanc et bleu de 1930 à 1950, jaune à partir de 1954 | ✅ | Article L'Officiel · Wikipedia EN (History of Brazil NT) · Google Arts & Culture |
| Brésil bat la Suède 7-1 et l'Espagne 6-1 au tour final 1950 | ✅ | Article L'Officiel · Wikipedia EN (1950 FIFA World Cup) · FIFA.com |
| Ademir et Chico, attaquants brésiliens du Mondial 1950 | ✅ | Article L'Officiel · ESPN (further lives of 1950 finalists) · 11v11 / National-football-teams.com |
| Finale du 16/07/1950 : but de Friaça, puis Schiaffino (66e) et l'ailier du CA Peñarol (79e) pour l'Uruguay, 2-1 | ✅ | Article L'Officiel · Wikipedia EN (Uruguay v Brazil 1950) · FIFA.com |
| Coupe remise sans cérémonie, quasi en catimini | ✅ | Wikipedia (Jules Rimet) · ExtraTime · Translating Cuba |
| Moacir Barbosa Nascimento, gardien, bouc émissaire jusqu'à sa mort en 2000 | ✅ | Article L'Officiel · Wikipedia EN (Moacir Barbosa) · ESPN/CNN |
| Maillot blanc jugé « insuffisamment patriotique », concours national lancé par la fédération | ✅ | Article L'Officiel · Wikipedia EN (Aldyr Schlee) · Global Voices |
| Aldyr Garcia Schlee, 19 ans, gagne avec jaune/vert/bleu/blanc | ✅ | Article L'Officiel · Wikipedia EN · Boston Globe (nécrologie) |
| Symbolique couleurs : jaune = richesse minérale/or, vert = Amazonie, bleu = fleuve, blanc = étoiles du drapeau | ✅ | Article L'Officiel · Google Arts & Culture · TBS News |
| Maillot Nike 2018 : jaune plus sombre, col vert, pastille « Você é Seleção », zigzags sur les manches | ✅ | Article L'Officiel (source directe et unique pour ce détail 2018, non repris ailleurs à l'identique — détail produit officiel Nike, cohérent avec le lancement du maillot 2018) |

**Sources :**
- https://www.lofficiel.com/hommes/bresil-les-dessous-d-un-maillot-mythique (article source, texte intégral fourni par Thomas)
- https://en.wikipedia.org/wiki/1950_FIFA_World_Cup
- https://en.wikipedia.org/wiki/Uruguay_v_Brazil_(1950_FIFA_World_Cup)
- https://en.wikipedia.org/wiki/Jules_Rimet
- https://en.wikipedia.org/wiki/Moacir_Barbosa
- https://en.wikipedia.org/wiki/Aldyr_Schlee
- https://en.wikipedia.org/wiki/History_of_the_Brazil_national_football_team
- https://www.espn.com/soccer/story/_/id/37363781/the-further-lives-all-1950-world-cup-finalists-brazil-uruguay
- https://www.fifa.com/en/tournaments/mens/worldcup/articles/uruguay-brazil-1950-maracanazo

**Point non retenu de la v1 (research indépendante) :** l'ironie « le créateur du maillot était supporter de l'Uruguay » (Aldyr Garcia Schlee) est vraie et solidement sourcée (Boston Globe, Maisfutebol, Brasil de Fato), mais absente de l'article L'Officiel. Écartée de cette version car la consigne est de reformuler l'article, pas d'y ajouter une recherche externe. Gardée en réserve pour un futur post dédié à Schlee.

---

## Notes skills chaînés

`hook-writer-sms` et `humanizer` sont référencés par le SKILL mais ne sont pas
disponibles comme skills séparés dans cette session : le hook et le style (phrases
courtes, tutoiement ponctuel, zéro remplissage) ont été travaillés manuellement
dans leur esprit. À repasser par ces skills si Thomas les a côté éditeur.

## Historique de version

- v1 : post construit sans accès à l'article intégral (paywall) — reconstruction
  par recherche web indépendante (Maracanazo → concours 1953 → Schlee), format
  script.json / `post.html` (templates A/H/G/D).
- v2 : article intégral fourni par Thomas, intégré au format `post.html` — ajout
  de Moacir Barbosa et de la remise en catimini.
- v3 (actuelle) : refonte demandée par Thomas — production **entièrement** via
  `editeur-series.html` (plus de `post.html`). Slide 1 en template `titre` (titre
  seul), toutes les slides intérieures en template `corps` (corps seul plein
  cadre), CTA en template `cta`. Le texte est une **reformulation fidèle de
  l'article** (pas une synthèse à hooks) : tout le contenu de l'article est
  conservé et réécrit dans la voix une·deux, dans l'ordre du récit original.
