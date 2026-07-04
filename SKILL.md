---
name: une-deux-post
description: >
  Utiliser ce skill dès que Thomas demande de préparer, créer ou conformer un
  post pour une·deux (@une.deux), son média foot Instagram "le foot en deux
  touches". Couvre la production complète d'un post carrousel : script slides,
  fichier script.json prêt pour l'éditeur HTML, prompts photo style presse, et
  légende Instagram. Se déclenche sur "post pour une·deux", "on fait un post",
  "prépare un post sur [pays/joueur]", ou toute demande de contenu éditorial
  une·deux. Inclut la vérification factuelle obligatoire avant rédaction.
---

# une·deux — Production de post

## Vue d'ensemble

une·deux raconte des histoires foot méconnues en lien avec l'actu (Coupe du
Monde 2026). Posture éditoriale : **l'archiviste-conteur qui exhume**. Format
reine : carrousel narratif exporté en vidéo via l'éditeur HTML de Thomas
(toolkit qui applique l'overlay template sur des photos).

**Règle absolue : vérification web factuelle AVANT toute rédaction.** Chiffres,
citations, dates, palmarès — tout fait cité doit être vérifié. La citation de la
slide G doit être une vraie déclaration sourcée.

### Règle des 3 sources (éphémérides & faits) — OBLIGATOIRE

Tout fait proposé — en particulier chaque entrée d'éphéméride *Ce jour-là* — doit
être **confirmé par au moins 3 sources indépendantes** : trois origines
distinctes (p. ex. Wikipédia + un média + une base type RSSSF / FBref /
Britannica), pas trois reprises du même article ni trois miroirs de Wikipédia.

- Si un fait **ne peut pas** être corroboré par 3 sources différentes, il est
  **écarté** : on ne le propose pas dans le brouillon, on ne l'utilise pas dans
  un post.
- Préférer un fait moins spectaculaire mais solidement triple-sourcé à un fait
  fort mais douteux. La fiabilité prime sur le punch.
- Conserver les **liens des 3 sources** pour chaque entrée livrée (traçabilité).

## Éditeur principal : `editeurs/editeur-series.html`

L'**éditeur de référence** est `editeurs/editeur-series.html` : éditeur
conscient des **4 séries** une·deux, qui applique automatiquement la
signature visuelle de la série (couleur, virage photo, format) sur la **cover**
et la **slide CTA**. Les autres éditeurs (`post.html`, `reel.html`) restent
disponibles pour les slides intérieures et les reels.

**Modèle de données de l'éditeur (cover / CTA) :**

| Champ | Rôle |
|-------|------|
| `serie` | `cejourla` · `oublies` · `portraits` · `arretdejeu` (verrouille couleur, virage photo, format) |
| `template` | `cover` · `titre` (cover titre seul) · `corps` (cover corps seul, plein cadre — pensé pour L'arrêt de jeu) · `citation` · `cta` |
| `tag` | **auto** = `N° + nom de série` (non éditable) |
| `title` | titre de cover (MAJUSCULES, 2 lignes) — absent en template `corps` |
| `greenWord` | mot-clé du titre coloré en signature de série |
| `body` | sous-titre (cover) — `**gras**` supporté ; occupe tout le cadre en template `corps` |
| `cur` / `tot` | pagination (slide courante / total) |
| `btnlabel` | libellé du bouton (template CTA uniquement) |

Format **verrouillé par série** : `cejourla`, `oublies`, `arretdejeu` → 3:4 ;
`portraits` → 9:16 (titre vertical). Voir `exemples/*-par-serie.md` et
`planning/planning-unedeux.md` pour la déclinaison série par série (scénarios,
prompts photo, légendes) et le planning éditorial (2 posts/jour).

## Skills chaînés (utilisation automatique)

Pour toute production de texte une·deux (post carrousel ou reel), Claude
enchaîne automatiquement deux skills, sans que Thomas ait à les invoquer :

1. **`hook-writer-sms` — pour le HOOK de la cover (S1).** Avant d'écrire le hook
   de la slide 1, Claude applique le skill `hook-writer-sms` afin de générer le
   meilleur arrête-scroll possible. Le hook reste contraint par la **banque de
   hooks une·deux** (6 familles, plateforme Instagram, tutoiement, posture
   archiviste) : `hook-writer-sms` sert à optimiser la formulation, pas à
   remplacer la ligne éditoriale. Si le skill propose plusieurs variantes,
   retenir celle qui colle à l'émotion unique du post et à la famille de hook
   choisie. Le hook final doit toujours respecter le « moule commun (loi du hook
   une·deux) ».

2. **`humanizer` — pour TOUS les textes rédigés.** Une fois les textes écrits
   (titres, corps de slides, citations reformulées, légende, sous-titres de
   reel), Claude passe l'ensemble au crible du skill `humanizer` avant
   livraison, pour retirer les marqueurs d'écriture IA (symbolisme gonflé,
   langue promotionnelle, analyses en « -ing », attributions vagues, abus de
   tirets cadratins, règle de trois, vocabulaire IA, voix passive, parallélismes
   négatifs, phrases de remplissage). Le résultat doit sonner humain, direct et
   « foot », fidèle au ton « expert complice qui va à l'essentiel ».
   Anti-dérive : `humanizer` nettoie le style, il ne doit pas diluer la densité
   factuelle ni casser les hooks/relances voulus.

Ordre d'application : vérif factuelle → `hook-writer-sms` (cover) → rédaction des
slides/légende → `humanizer` (passe finale sur tout le texte) → livraison.

## Livrables par post

Dès que Thomas dit "on va faire un post pour une·deux", livrer **3 éléments** :

1. **SCRIPT SLIDES** (validé avant le reste si Thomas veut arbitrer)
2. **PROMPTS PHOTO** style presse (un par slide illustrée)
3. **LÉGENDE** complète (gabarit 5 temps + hashtags de série)

Le **Reel-promo** n'est fourni que si Thomas le demande explicitement.

Workflow v7 : Claude ne génère PAS d'images (pas d'appels Higgsfield). Claude
fournit uniquement les prompts texte ; Thomas génère les photos et les intègre
dans son éditeur.

## Structure des 8 slides (gabarit de référence)

| # | Template | Fonction | Rôle |
|---|----------|----------|------|
| S1 | A | **HOOK** | COVER — hook interpellant (chiffre absurde / contradiction / secret nommé). Tag + titre 2 lignes avec mot-clé coloré + sous-titre accrocheur (placé dans `body`) qui crée un manque |
| S2 | A | **TRANSITION** | Fait / contexte — pose l'enjeu : gain / à éviter / légitimité. Tag + titre + corps dense avec chiffres exacts |
| S3 | H | **TEASE** | SLIDE-RESPIRATION — 3-6 mots, un mot-clé coloré, pur rythme, ni tag ni fait. Sert de relance entre deux révélations |
| S4 | A | **TEASE** | Fait historique — tag (année) + titre + corps. Une idée, une micro-boucle |
| S5 | G | **TEASE** | CITATION réelle vérifiée — mot-clé coloré + nom/rôle + légende ("L'AVEU", "LA PROMESSE", "L'AMBITION", "LE MYTHE"...) |
| S6 | A | **TEASE** | LE DÉTAIL FOU — tag + titre + corps, la relance qui ouvre la boucle finale |
| S7 | A | **CLIMAX** | 2026 / chute oralisée — tag "2026" + titre + corps qui referme la boucle de la cover (le payoff) |
| S8 | D | **ACTION** | CTA — "RESTE DANS LE JEU" · "FOLLOW" |

Ajouter une ligne **Débat : « ... »** sous le CTA (question clivante pour la
légende, pas dans le JSON).

Ton = **divertissement-info** : hook interpellant en cover, chute oralisée en
S7, tutoiement, phrases courtes, fait fort en premier, zéro remplissage, une
relance par slide qui ouvre une boucle ("Sauf que.", "Et le plus fou, c'est pas
ça."). Densité factuelle gardée. Une seule émotion par post (surprise /
nostalgie / injustice / fierté).

## Architecture narrative (Hook · Transition · Tease · Climax · Action)

C'est la **grille d'écriture** qui détermine le rôle de chaque slide dans le
récit et, surtout, **ce qui pousse le spectateur à swiper vers la suivante**.
Elle se superpose à la structure 8 slides ci-dessus : chaque slide a une
**fonction narrative** en plus de son template.

| Slide | Fonction | Mission de la slide | Règle d'écriture |
|-------|----------|---------------------|------------------|
| S1 | **HOOK** | Arrêter le scroll | Une promesse de curiosité impossible à ignorer : chiffre absurde, contradiction nommée, ou secret. Titre fort. Le `body` (sous-titre) doit créer un **manque** ("Et personne n'en parle.") |
| S2 | **TRANSITION** | Donner une raison de rester | Réponds à UNE des trois : ce que le spectateur **gagne** / ce qu'il **évite** / pourquoi le sujet est **légitime** (autorité, source, palmarès). Pose l'enjeu, pas encore la réponse |
| S3–S7 | **TEASE** | Révéler bout par bout | Une idée par slide. Tu **dévoiles l'info petit à petit** : exemples, stats, citation, détail. Chaque slide referme une micro-boucle ET en ouvre une nouvelle. Jamais tout dire d'un coup |
| S8–S9 | **CLIMAX** | Le moment « aha » | La grande révélation : la leçon, la phrase à screenshoter, le retournement qui referme la boucle de la cover. C'est le **payoff** promis au hook |
| S10 (CTA) | **ACTION** | Rendre l'étape suivante évidente | Une seule action claire (FOLLOW / commente / enregistre). Pas de nouvelle info, pas de choix multiple |

> **Mapping sur la structure une·deux 8 slides** : S1 = HOOK, S2 = TRANSITION,
> S3→S6 (H/A/G/A) = TEASE, S7 = CLIMAX (la chute 2026 qui referme la cover),
> S8 (D) = ACTION. Quand on passe à 9 ou 10 slides, étendre le TEASE
> (slides 3–7) ou dédoubler le CLIMAX (slides 8–9), jamais le HOOK ni l'ACTION.

### Banque de hooks pour la cover (S1)

6 familles de hooks qui arrêtent le scroll, adaptées au foot. Le HOOK de la
cover doit toujours sortir d'une de ces familles. `X` = le sujet du post
(joueur, équipe, match, époque). Tutoiement, MAJUSCULES dans le `title`,
phrase courte. Le `body` (sous-titre) ajoute le **manque** ("Et ce n'est pas
une blague.").

**Moule commun (loi du hook une·deux) :** sujet + verbe d'action au passé
composé + **détail qui ne devrait pas être là**. Phrase déclarative assenée
comme un fait acquis, point final sec, zéro adjectif de remplissage. Souvent
en deux temps ("X a fait Y. Et Z.") où le second segment plante le couteau.
Jamais de "voici", "découvre", "l'histoire incroyable de" : on **affirme**, on
ne présente pas. Le hook cache toujours la moitié (le "comment"), résolue
seulement au CLIMAX.

**1. Autorité / révélation oubliée** — injustice, oubli
- "Le meilleur joueur de cette équipe n'a jamais joué une minute."
- "On a effacé X de l'histoire. Volontairement."
- "X a changé le foot. Son nom a disparu en 10 ans."
- "Le geste le plus copié du foot a été inventé par un type que personne ne cite."
- "Cette finale a été truquée. Tout le monde le sait, personne ne le dit."

**2. Polarisants** — fierté, débat
- "X n'a jamais été un génie. Il a juste eu de la chance pendant 90 minutes."
- "Le plus grand exploit de X, c'est les autres qui l'ont fait."
- "Cette équipe légendaire ? Elle a gagné par accident."
- "Le but du siècle n'aurait jamais dû compter."
- "Ton joueur préféré a volé sa place à un meilleur que lui."

**3. Storytelling** — nostalgie
- "X a dormi dans sa voiture. Six mois plus tard, il gagnait le Mondial."
- "Une blessure de rien du tout a fait basculer toute une carrière."
- "Il a raté son bus. Ça lui a coûté une Coupe du Monde."
- "X a signé son contrat sur une nappe de restaurant."
- "On l'a refusé partout. Il est devenu champion du monde."

**4. Curiosité** — on annonce le secret sans le livrer
- "X a gagné un match qu'il n'a jamais joué."
- "Il y a une raison pour laquelle on ne montre jamais cette finale en entier."
- "Le vrai héros de ce match n'est même pas sur la feuille de match."
- "Ce match a duré 90 minutes. Une seule seconde a tout décidé."
- "Personne ne sait ce qui s'est dit à la mi-temps. Sauf que ça a tout changé."

**5. Contrariants** — le fait qui semble impossible
- "Champion du monde. Jamais sélectionné. Vraie histoire."
- "X a marqué le but le plus important du foot. Il a fini ouvrier."
- "Cette équipe a perdu tous ses matchs. Et elle est entrée dans la légende."
- "Il a gagné la Coupe du Monde sans toucher le ballon."
- "Le plus grand gardien de l'histoire mesurait 1m68."

**6. Chiffre absurde / contradiction nommée** — signature une·deux (la plus forte)
- "Le premier buteur de l'histoire du Mondial était coursier chez Peugeot."
- "L'Angleterre a gagné la Coupe du Monde grâce à un chien."
- "Il a gagné le Mondial. Il a touché 2 000 francs."
- "Footballeur le week-end, ouvrier à l'usine la semaine. Et champion du monde."
- "Une équipe entière a disparu dans un crash. Le club existe encore grâce à ça."

> Choisir la famille selon l'émotion unique du post : autorité/révélation pour
> l'injustice et l'oubli ; storytelling pour la nostalgie ; contrariant et
> chiffre absurde pour la surprise ; polarisant pour la fierté/débat. Le hook
> doit promettre une **curiosité précise** (un fait nommé), jamais un teasing
> vague ("une histoire incroyable"). La famille 6 est la plus efficace pour
> une·deux : c'est d'elle que sortent les covers Laurent et Pickles.

### La mécanique du swipe (règle reine)

**Chaque slide doit créer une tension qui ne se résout qu'à la slide suivante.**
C'est le seul moteur du taux de complétion. Trois leviers, à alterner :

- **Boucle ouverte** : annoncer sans révéler. "Sauf qu'un détail change tout."
  → le détail est sur la slide d'après.
- **Compte à rebours / liste** : "3 raisons", "le pire arrive en dernier" →
  le spectateur swipe pour fermer la liste.
- **Contradiction suspendue** : poser un fait qui semble impossible, ne
  l'expliquer qu'ensuite. "Champion du monde. Jamais sélectionné. Comment ?"

Anti-règles : ne **jamais** résoudre la boucle de la cover avant le CLIMAX ;
ne jamais finir une slide TEASE sur une phrase qui se suffit à elle-même
(sinon le spectateur sort) ; une seule boucle vivante à la fois (ne pas
empiler 3 cliffhangers non tenus).

### Le « Teach a framework » (leçon transposable, juste avant l'ACTION)

S'ajoute par-dessus la grille ci-dessus, **sans la remplacer**. La formule de
référence des carrousels qui se sauvegardent est en **4 temps** :
**Hook curiosity → Tell a story → Teach a framework → End with action.**

Mapping sur une·deux :
- **Hook curiosity** = HOOK (S1)
- **Tell a story** = TRANSITION + TEASE (S2→S6) — le cœur narratif inchangé
- **Teach a framework** = un **principe à emporter**, glissé dans le CLIMAX (S7)
  ou juste avant l'ACTION
- **End with action** = ACTION (S8 / template S)

**Règle :** après le payoff de la cover, le CLIMAX doit livrer **une leçon
généralisable** que le spectateur peut réutiliser — pas seulement refermer la
boucle. C'est ce qui transforme une belle histoire foot en contenu qu'on
**sauvegarde pour s'en servir** (métrique reine = sauvegardes).

Forme : une phrase courte, sentencieuse, détachable de l'anecdote. Elle tire
de l'histoire une règle valable au-delà du cas raconté.
- Laurent → *« Les pionniers ne sont pas oubliés parce qu'ils sont petits, mais parce qu'ils ne se racontent pas. »*
- Pickles → *« Parfois, c'est le détail qu'on ne contrôle pas qui sauve tout. »*

Où la placer concrètement :
- soit en **dernière phrase du `body` du CLIMAX** (S7 / template A ou X),
  juste avant la phrase qui referme la cover ;
- soit, sur un post à 9 slides, sur une **slide dédiée** entre le CLIMAX et le
  CTA (template H « respiration » ou X « révélation »).

Anti-dérive : la leçon reste **tirée du fait vérifié**, jamais un proverbe
plaqué. Une seule leçon par post. Ne pas moraliser ni sur-jouer ; rester dans
la posture archiviste (on constate, on ne sermonne pas).

### Checklist avant livraison du script
- [ ] Le HOOK promet une curiosité précise (pas un titre vague)
- [ ] Le HOOK s'appuie sur une des 6 familles de la banque de hooks
- [ ] La boucle ouverte en S1 n'est refermée qu'au CLIMAX
- [ ] Chaque slide TEASE finit sur une relance qui appelle la suivante
- [ ] Le CLIMAX tient explicitement la promesse du HOOK
- [ ] Le CLIMAX (ou la slide juste avant l'ACTION) livre UNE leçon transposable
- [ ] L'ACTION ne propose qu'UNE seule étape suivante

## Format script.json (post carrousel — référence `script_post.json`)

Tableau d'objets, 1 objet par slide, 8 slides dans l'ordre : A, A, H, A, G, A, A, D.

**Accents :** autorisés partout (`title`, `greenWord`, `tag`, `body`, `quote`,
`quoteAuthor`, `caption`). Pas de mise en majuscules sans accents.

### Template A (cover + faits)
```json
{
  "template": "A",
  "tag": "LE PARADOXE",
  "title": "ILS ONT INVENTÉ LE FOOT. ILS L'ONT GAGNÉ UNE FOIS.",
  "greenWord": "UNE FOIS",
  "body": "Et c'était il y a 60 ans.",
  "media": "pays_01.PNG"
}
```
- `greenWord` : mot/segment du titre à colorer (sans balise, doit apparaître tel quel dans le title)
- Cover (S1) : le sous-titre va dans `body`
- `media` : nom de fichier exact, .PNG par défaut

### Template H (slide-respiration)
```json
{
  "template": "H",
  "quote": "Sauf que non.",
  "quoteAccent": "non.",
  "quoteAuthor": "",
  "caption": ""
}
```
- `quoteAccent` : segment de la quote à colorer
- `quoteAuthor` et `caption` vides
- PAS de champ `media`

### Template G (citation réelle)
```json
{
  "template": "G",
  "quote": "Trois lions sur un maillot, et le foot qui rentre à la maison.",
  "quoteAccent": "à la maison.",
  "quoteAuthor": "Three Lions, l'hymne de 1996",
  "caption": "LE MYTHE"
}
```
- PAS de champ `media`

### Template D (CTA final — INCLUS dans le JSON)
```json
{
  "template": "D",
  "tag": "LE RECAP",
  "title": "RESTE DANS LE JEU",
  "body": "Le foot en deux touches, tous les jours.",
  "btnlabel": "FOLLOW"
}
```
- PAS de `greenWord`, PAS de `media`
- `btnlabel` toujours "FOLLOW"

### Clés INTERDITES
Ne JAMAIS utiliser : `subtitle`, `button`, `legend`, `ocreWord`, `citedName`.

### Validation
Toujours valider le JSON (parse) avant livraison. Un dossier par post :
`pays/script.json` + médias nommés.

## Format prompts photo (style presse, Workflow v7)

Un prompt par slide illustrée (S1, S2, S4, S6, S7 — pas H ni G). Format :
```
nom_NN (LABEL) : Press photography. [sujet nommé / maillot précis] [action/émotion],
[lumière], [ambiance stade], cinematic grain. Portrait 4:5. No text.
```

**Règle nommage (obligatoire) :** chaque prompt doit identifier explicitement
- **le joueur** par son nom complet + nationalité (`Kylian Mbappé, french player`),
- **l'équipe / le maillot** précis (`with a PSG match kit`),
- **l'année** de la scène (`in 2020`).

Exemple : pour Mbappé au PSG en 2020 →
`Kylian Mbappé, french player with a PSG match kit in 2020`.

Pour les slides "archive" (fait historique), ajouter un look vintage :
`2014 vintage archival look, retro grainy film aesthetic, faded colors` +
`Realistic photograph, not illustration.`

Nom de fichier = exactement celui du champ `media` du JSON (`pays_01.PNG`, etc.).

### Visuels & droits d'image (règle)

Les livrables d'un post fournissent les **prompts photo** (texte), pas des photos
d'archive récupérées sur le web. Raison : pour les faits anciens (surtout la série
*Ce jour-là*), il n'existe quasiment **aucune vraie photo libre de droits** ; les
archives du moment sont chez Getty / AP / Wikipedia (fair use) = **copyright**,
donc **risquées à republier** sur le compte.

- **Par défaut** : livrer les prompts photo « façon presse » — Thomas génère
  lui-même les visuels dans son outil. Zéro problème de droits, visuels sur-mesure.
- **Images web** : n'intégrer que des images **réellement libres** (Wikimedia
  Commons PD/CC0/CC-BY) et seulement pour l'**ambiance/contexte** ; jamais une
  archive copyrightée dans un post publié. Toujours indiquer la licence.
- Ne pas lancer de génération d'images (Higgsfield) sans demande explicite de
  Thomas.
- Séries à faits récents (*Portraits*, *L'arrêt de jeu* quand l'hypothèse porte sur un sujet actuel) :
  davantage de sources visuelles disponibles, mais la même règle de droits
  s'applique.

## Livrable quotidien de la routine « post du jour »

Le brouillon Gmail produit chaque jour par la routine (à partir du sujet validé
en vert dans l'éphéméride) contient, **en tête et pour le sujet retenu** :

1. **Titre** au format EXACT : `JJ MOIS AAAA : <phrase percutante>`
   — la date de l'événement, deux-points, puis **une phrase courte qui claque**
   (ton une·deux : affirmation, pas de « voici / découvre »).
2. **Corps** : un paragraphe qui **explique l'événement** (faits vérifiés, règle
   des 3 sources), et dont la **dernière phrase est une punchline sentie** sur
   l'événement (elle referme, elle marque).
3. **Lien vidéo** de l'événement si un existe (match, but, reportage — YouTube ou
   archive vérifiée). Si aucune vidéo fiable n'est trouvée, écrire explicitement :
   **« Pas de lien vidéo disponible. »**
4. **Légende Instagram** prête à publier, au format de la série (voir
   `exemples/legendes-par-serie.md`).

**Le livrable quotidien s'arrête là : PAS de `script.json`, PAS de prompts photo.**
Ces éléments (cover/CTA éditeur séries, script.json, prompts) ne sont produits que
sur demande explicite de Thomas (« on fait le post complet »).

**Exemple (29 juin 1950) :**
> **29 JUIN 1950 : des amateurs américains ont giflé les rois du foot.**
>
> À Belo Horizonte, les États-Unis — un prof, un chauffeur de corbillard, un
> plongeur, donnés à 500 contre 1 — battent l'Angleterre 1-0. But de Joe
> Gaetjens, né en Haïti, à la 37e minute. Rentré au pays, il disparaît en 1964,
> arrêté par le régime Duvalier. *L'homme du but le plus improbable du foot, son
> propre pays l'a effacé.*
>
> 🎥 Vidéo : https://www.youtube.com/watch?v=-vqQWrrzNWU

## Format légende (4 temps)

1. Accroche en gras + emoji drapeau
2. Résumé en deux touches (le récit condensé)
3. Punchline / relance ("Et le plus fou ?")
4. Question débat + `@une.deux ⚽️` + hashtags

**Règle : ne JAMAIS écrire "story à la une" ni aucun renvoi vers la story
dans la légende.**

Hashtags : série (#lesouscotés, #undestinparjour, #lachutedesgéants, #ledébat)
+ thématiques + `#lefootendeuxtouches #unedeux`.

## Séries récurrentes

### Les 4 séries (modèle éditeur — voir `planning/planning-unedeux.md`)
- **Ce jour-là** · `#cejourla` — éphéméride calendaire (socle quotidien). Carrousel 3:4, ocre / sépia chaud.
- **Les oubliés** · `#lesoubliés` — effacés de l'histoire, injustices. Carrousel 3:4, vert / N&B froid.
- **Portraits** · `#portraits` — parcours d'un joueur par l'angle méconnu. Reel 9:16, N&B studio.
- **L'arrêt de jeu** · `#arretdejeu` — mode enquête/hypothèse : on pose une question foot (« pourquoi les Bleus ne rejouent plus en rouge ? ») et on aligne les faits, sans jamais donner de réponse tranchée — on relance plutôt qu'on referme. Carrousel 3:4, rouille / légère surimpression sur les médias importés.

Scénarios, prompts photo et légendes déclinés par série dans
`exemples/scenarios-par-serie.md`, `exemples/prompts-par-serie.md`,
`exemples/legendes-par-serie.md`.

### Hashtags thématiques (transverses)
- **#lesouscotés** — équipes sous-estimées
- **#undestinparjour** — portraits joueurs
- **#lachutedesgéants** — grands qui s'effondrent
- **#ledébat** — questions clivantes

## Règles permanentes
- Pas de comparaisons avec les USA (France / Europe uniquement)
- Bouton CTA toujours `FOLLOW`, rien d'autre
- Métriques reines : sauvegardes + taux de complétion (pas les vues)
- Publication du carrousel 1-3h avant le coup d'envoi de l'équipe concernée

## Fichiers de référence

Deux JSON de référence dans `exemples/`, à copier pour tout nouveau contenu :

- **`exemples/script_post.json`** — modèle canonique des **posts carrousel**
  (quand Thomas dit "on fait un post"). Structure : 8 slides A/A/H/A/G/A/A/D,
  clés par template. Fait foi pour tout doute sur une clé ou un format de post.
- **`exemples/script_reel.json`** — modèle canonique des **reels** (quand Thomas
  dit "on fait un reel"). Structure : `meta` + 5 scènes narratives. Fait foi
  pour tout doute sur le format reel.

### Posts produits (cas concrets, pas des gabarits)

Sous `exemples/<slug>/`, chaque post livré sert d'exemple complet (application
réelle des règles narratives + ton + vérif factuelle). À consulter comme modèle
de raisonnement, pas à copier tel quel.

- **`exemples/lucien-laurent-1930/`** — premier buteur de l'histoire du Mondial,
  footballeur-ouvrier oublié 60 ans. Montre : choix de templates par fonction
  (K/A/H/C/G/A/X/S, pas le gabarit par défaut A/A/H/A/G/A/A/D), mécanique de
  boucle cover→climax, et retrait d'un détail non vérifiable. Contient
  `script.json` (prêt éditeur) + `POST.md` (structure, prompts photo, légende,
  ton, vérif factuelle).

### Format reel (`script_reel.json`)

`meta` porte les réglages verrouillés :
- `cadence_subs` : **2** (sous-titres toutes les 2 sec)
- `parallaxe` : **2.4**
- `vitesse_animation` : **4**
- `ratio` : `9:16`, `duree_par_scene` : 8

`scenes` : 5 scènes (accroche → contexte → exploit → détail fou → chute 2026).
Par scène : `media`, `titre`, `slideTitle`, `titleAccent` (sous-chaîne littérale
du slideTitle à colorer), `kicker`, `subs`, `mix`, `duo` (palette 2 couleurs).

**Règle subs : maximum 2 lignes par scène.** Le `subs` est le cœur narratif —
garder les 2 phrases les plus fortes.
