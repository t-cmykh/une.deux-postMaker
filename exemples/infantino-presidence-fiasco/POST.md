# L'arrêt de jeu — « Infantino, entre pouvoir et argent, comment sa présidence tourne au fiasco »

Post carrousel, série **L'arrêt de jeu** (`#arretdejeu`), 10 slides, ratio 3:4.
Gabarits utilisés : ceux déjà codés dans `editeurs/editeur-series.html`, aucun
nouveau template créé. Mapping validé sur les 4 captures de référence fournies
par Thomas (Bosman, Mbappé salaire/transfert, citation écho) :

| Réf. fournie | Gabarit réel (chip / fonction JS) |
|---|---|
| « LE JOUR OÙ LA JUSTICE A CASSÉ LE MARCHÉ » (Bosman, footer 3 colonnes) | **ENQUÊTE · TÉMOIN** (`drawEnqueteTemoin`) |
| « LE VRAI SALAIRE DE MBAPPÉ » (titre géant en découpe sur la photo) | **ENQUÊTE · DUO PHOTO** (`drawEnqueteDuo`) |
| « LE VRAI PRIX D'UN TRANSFERT LIBRE » (byline, photo à part) | **ENQUÊTE · TITRE XXL** (`drawEnqueteTitre`) |
| Citation « Un salaire n'est presque jamais... » | **CITATION · ÉCHO** (`drawEnqueteEcho`) |

Vérification factuelle faite par recherche web, le sujet couvre juillet-août
2026, postérieur à la base de connaissances (sources en bas de fichier).
Ton : registre journalistique, articles au conditionnel ou attribués là où le
fait est rapporté et non établi, jamais d'accusation pénale non prouvée.
Conforme à la doctrine de la série (`exemples/scenarios-par-serie.md`) : on
aligne les faits, on ne referme pas la boucle par un verdict. La dernière
slide avant le CTA relance plutôt qu'elle ne tranche.

Tag fixe sur toutes les slides : **L'ARRÊT DE JEU** (rouille). Pagination :
`cur` de `01` à `10`, `tot` = `10` (les captures de réf affichent `01/09` par
défaut de l'éditeur : à ignorer, ce n'est pas la vraie pagination de ce post).

---

## S1 — HOOK — gabarit ENQUÊTE · DUO PHOTO

- **tag** : L'ARRÊT DE JEU
- **title** : `IL A FAILLI VENDRE LA COUPE DU MONDE`
- **mot-clé coloré (accent)** : `VENDRE`
- **intro (chapô italique)** : Gianni Infantino a pris la tête de la FIFA en 2016 en promettant de la nettoyer après le scandale Blatter. Dix ans plus tard, il a manqué de la privatiser.
- **body (corps à lettrine)** : Fin juillet 2026, la FIFA propose de céder 20 % des droits commerciaux de ses compétitions, Coupe du Monde comprise, à des investisseurs privés, via une filiale baptisée FIFA Forward Enterprise. Le projet porte la signature de son président. Il ne tiendra que quelques jours.

**Photo (prompt)** :
```
gianni_infantino_01 (S1) : Press photography. Gianni Infantino, FIFA president,
at a press conference podium, dark suit, serious expression, microphones in
foreground, press-room lighting, in 2026. Warm rust-toned sepia, balanced
contrast, cinematic film grain, investigative documentary mood. Realistic
photograph, not illustration. Portrait 4:5. No text.
```

---

## S2 — CONSTAT — gabarit ENQUÊTE · TÉMOIN

- **tag** : L'ARRÊT DE JEU
- **title** : `DIX ANS AU POUVOIR. UN EMPIRE À 15 MILLIARDS.`
- **intro (chapô)** : Depuis 2016, un seul homme dirige le football mondial. Le chiffre d'affaires de la FIFA a explosé. La confiance, elle, s'est nettement dégradée.
- **body (lettrine)** : Sur le cycle 2023-2026, porté par le Mondial nord-américain, la FIFA a engrangé environ 15 milliards de dollars de revenus, un record, largement au-dessus des 11 milliards initialement prévus. Dans le même temps, son président a tenté de vendre une part du tournoi à des fonds privés, vu son salaire grimper au-delà de 6 millions de dollars par an, et fait valider une lecture des statuts qui repousse la limite de son propre mandat.
- **qaRaw (3 colonnes)** :
  1. Q : Le vrai enjeu, c'était quoi ?
     A : Une FIFA transparente, promise après la chute de Sepp Blatter en 2015.
  2. Q : Qui a payé le prix fort ?
     A : Les supporters, sur des billets de finale passés de 1 550 à 5 785 dollars.
  3. Q : Et aujourd'hui ?
     A : Un mandat qui peut légalement courir jusqu'en 2031.

**Photo (prompt)** :
```
gianni_infantino_02 (S2) : Press photography. Gianni Infantino speaking on
stage at the FIFA Congress in Vancouver, podium and FIFA banner in the
background, rows of delegates, in April 2026. Warm rust-toned sepia,
institutional lighting, cinematic film grain. Realistic photograph, not
illustration. Portrait 4:5. No text.
```

---

## S3 — ENQUÊTE #1 — gabarit ENQUÊTE · TITRE XXL

- **tag** : L'ARRÊT DE JEU
- **title** : `TROIS MANDATS. QUINZE ANS DE RÈGNE.`
- **byline** : PAR UNE·DEUX — DOSSIER FIFA
- **body (corps flow-around-photo)** : Les statuts de la FIFA plafonnent la présidence à trois mandats de quatre ans. Sauf que le Conseil de la FIFA a tranché : les trente-neuf premiers mois d'Infantino, de février 2016 à 2019, où il achevait le mandat laissé vacant par Sepp Blatter, ne comptent pas dans ce total. Réélu en 2019 puis en 2023, il a confirmé au Congrès de Vancouver, le 30 avril 2026, qu'il briguerait un nouveau mandat en 2027. Sur le papier, la règle des trois mandats reste intacte. Dans les faits, elle l'autorise à diriger la FIFA jusqu'en 2031.

**Photo (prompt)** :
```
gianni_infantino_03 (S3) : Press photography. Gianni Infantino at a FIFA
Congress vote, raising his hand or standing at the podium, large FIFA screens
in the background, modern congress hall, in 2026. Warm rust-toned sepia,
balanced contrast, cinematic film grain, institutional atmosphere. Realistic
photograph, not illustration. Portrait 4:5. No text.
```

---

## S4 — ENQUÊTE #2 — gabarit ENQUÊTE · DUO PHOTO

- **tag** : L'ARRÊT DE JEU
- **title** : `UN SEUL CANDIDAT POUR TOUT UN MONDIAL`
- **mot-clé coloré (accent)** : `UN`  *(ou reformuler pour isoler un mot unique net si le mécanisme de coloration ne prend qu'un seul mot exact, voir note technique en bas de fichier)*
- **intro (chapô)** : En décembre 2023, la FIFA attribue le Mondial 2034 à l'Arabie saoudite. Un seul pays est encore en course ce jour-là.
- **body (lettrine)** : L'Australie, un temps candidate, retire son dossier faute de temps : la fenêtre de candidature n'a duré que 26 jours. Au terme d'un processus de quinze mois jugé opaque, orchestré par Infantino sans qu'aucune question ne soit prise en salle, le Congrès de la FIFA entérine le choix saoudien à l'applaudimètre. Un an plus tard, Aramco, la compagnie pétrolière publique du royaume, signe un partenariat de quatre ans avec la FIFA. Des organisations de défense des droits humains alertent sur le sort des travailleurs migrants du chantier.

**Photo (prompt)** :
```
gianni_infantino_04 (S4) : Press photography. Gianni Infantino shaking hands
with Saudi Crown Prince Mohammed bin Salman at an official visit, FIFA and
Saudi flags in the background, formal diplomatic setting, in 2023. Warm
rust-toned sepia, formal lighting, cinematic film grain. Realistic
photograph, not illustration. Portrait 4:5. No text.
```

---

## S5 — ENQUÊTE #3 — gabarit ENQUÊTE · TÉMOIN

- **tag** : L'ARRÊT DE JEU
- **title** : `UN COUP DE FIL. UN CARTON ROUGE EFFACÉ.`
- **intro (chapô)** : Lors de la victoire du Team USA face à la Bosnie-Herzégovine, début juillet 2026, l'attaquant Folarin Balogun reçoit un carton rouge. Une sanction qui doit l'écarter du match suivant, contre la Belgique.
- **body (lettrine)** : Donald Trump appelle alors Gianni Infantino pour contester la décision de l'arbitre, jugeant qu'il n'y avait pas faute. Le 5 juillet, dans une décision presque sans précédent, la FIFA suspend la sanction de Balogun pour une période probatoire d'un an. Le joueur est aligné dès le match suivant, perdu 4-1 face à la Belgique. Interrogé, Trump reconnaît l'appel tout en assurant qu'il ne peut « rien dicter » à Infantino ; la FIFA renvoie la décision à un organe judiciaire qu'elle dit indépendant.
- **qaRaw (3 colonnes)** :
  1. Q : Le vrai enjeu, c'était quoi ?
     A : L'indépendance des décisions arbitrales, censée être hors de portée politique.
  2. Q : Qui a payé le prix fort ?
     A : L'intégrité du tableau, selon l'UEFA, qui dénonce la décision.
  3. Q : Et aujourd'hui ?
     A : Deux plaintes formelles visent la proximité d'Infantino avec Trump.

**Photo (prompt)** :
```
gianni_infantino_05 (S5) : Press photography. Donald Trump and Gianni
Infantino standing together at a public World Cup event, smiling, FIFA
branding and flags in the background, in 2026. Warm rust-toned sepia, event
lighting, cinematic film grain, investigative documentary mood. Realistic
photograph, not illustration. Portrait 4:5. No text.
```

---

## S6 — CITATION (renforce S5) — gabarit CITATION · ÉCHO

- **tag** : L'ARRÊT DE JEU
- **quote** : « Une décision sans précédent, incompréhensible et injustifiable. La FIFA a franchi une ligne rouge. »
- **mots accentués (quoteWords)** : `ligne`, `rouge`
- **quoteAuthor** : UEFA, COMMUNIQUÉ, JUILLET 2026

**Photo (prompt)** :
```
gianni_infantino_06 (S6) : Press photography. Gianni Infantino with a grave
expression at a press briefing following a contested refereeing decision,
FIFA conference room, in 2026. Warm rust-toned sepia, dramatic press-room
lighting, cinematic film grain. Realistic photograph, not illustration.
Portrait 4:5. No text.
```

---

## S7 — ENQUÊTE #4 — gabarit ENQUÊTE · TITRE XXL

- **tag** : L'ARRÊT DE JEU
- **title** : `20 % DE LA COUPE DU MONDE, À VENDRE`
- **byline** : PAR UNE·DEUX — DOSSIER FIFA
- **body (corps flow-around-photo)** : Le projet FIFA Forward Enterprise, présenté fin juillet 2026, prévoit de céder environ 20 % d'une nouvelle entité commerciale (celle qui détient les droits du Mondial et de la Coupe du Monde des clubs) à des investisseurs privés, dont Thrive Capital, le fonds de Joshua Kushner, frère du gendre de Donald Trump. Le montage aurait rapporté jusqu'à 4,2 milliards de dollars à la FIFA, et, selon le Times, plus de 30 millions d'euros de rémunération annuelle à son président, contre environ 6 millions aujourd'hui. Pour convaincre les fédérations, Infantino promet jusqu'à 40 millions de dollars à celles qui voteront pour, avant une échéance fixée au 19 septembre. Il lui faut 106 voix sur 211.

**Photo (prompt)** :
```
gianni_infantino_07 (S7) : Press photography. Gianni Infantino announcing a
new commercial project at a FIFA press conference, presentation screen with
financial charts in the background, in 2026. Warm rust-toned sepia,
boardroom lighting, cinematic film grain. Realistic photograph, not
illustration. Portrait 4:5. No text.
```

---

## S8 — CITATION (renforce S7) — gabarit CITATION · ÉCHO

- **tag** : L'ARRÊT DE JEU
- **quote** : « Un mauvais deal pour le foot. »
- **mot accentué (quoteWords)** : `deal`
- **quoteAuthor** : CARLOS CORDEIRO, EX-CONSEILLER D'INFANTINO, DÉMISSION EN JUILLET 2026

**Photo (prompt)** :
```
gianni_infantino_08 (S8) : Press photography. An empty chair at a FIFA
Zurich meeting table, files and a FIFA logo visible, dim moody lighting,
symbolic of a resignation, in 2026. Warm rust-toned sepia, moody indoor
lighting, cinematic film grain, investigative documentary mood. Realistic
photograph, not illustration. Portrait 4:5. No text.
```

---

## S9 — PISTE (hypothèse, pas un verdict) — gabarit ENQUÊTE · DUO PHOTO

- **tag** : L'ARRÊT DE JEU
- **title** : `LE POUVOIR TIENT DANS UNE SEULE MAIN`
- **mot-clé coloré (accent)** : `POUVOIR`
- **intro (chapô)** : Un mandat prolongé jusqu'en 2031. Un Mondial donné sans adversaire à l'Arabie saoudite. Un carton rouge annulé après un appel de la Maison-Blanche. Une Coupe du Monde presque vendue à des fonds privés.
- **body (lettrine)** : Officiellement, chaque dossier a sa propre justification statutaire ou sportive. Mis bout à bout, ils dessinent un même mouvement : toujours plus de pouvoir, toujours plus longtemps, entre toujours moins de mains. La FIFA assure appliquer ses textes à la lettre. La question, elle, reste ouverte : jusqu'où ces textes peuvent-ils encore s'étirer ?

**Photo (prompt)** :
```
gianni_infantino_09 (S9) : Press photography. Gianni Infantino seen from
behind or in profile, alone, leaving an empty FIFA conference room, isolated
silhouette, long institutional corridor perspective, in 2026. Warm
rust-toned sepia, low dramatic lighting, cinematic film grain, investigative
documentary mood. Realistic photograph, not illustration. Portrait 4:5. No
text.
```

---

## S10 — ACTION — gabarit D (CTA standard)

- **tag** : L'ARRÊT DE JEU
- **title** : `RESTE DANS LE JEU`
- **body** : L'enquête continue. Le foot en deux touches, tous les jours.
- **btnlabel** : FOLLOW

*(Débat, à mettre dans la légende, pas dans le JSON ou l'éditeur, voir légende
ci-dessous.)*

---

## Légende Instagram

```
🚨 Il devait sauver la FIFA. Il a failli la vendre.

Dix ans après avoir promis de nettoyer la FIFA, Gianni Infantino cumule les
polémiques : mandat prolongé jusqu'en 2031 malgré la limite des trois
mandats, Mondial 2034 offert sans concurrent à l'Arabie saoudite, carton
rouge annulé au Mondial 2026 après un appel de Donald Trump, et une
tentative de céder 20 % de la Coupe du Monde à des investisseurs privés,
retirée en catastrophe fin juillet.

La piste la plus solide qu'on ait trouvée n'est pas un scandale isolé.
C'est un même mouvement qui revient à chaque fois : plus de pouvoir, plus
longtemps, entre moins de mains.

Alors dis-nous : un homme peut-il encore réformer une institution qu'il
contrôle à ce point ? 👇
@une.deux ⚽️
.
.
#arretdejeu #infantino #fifa #footballhistoire #lefootendeuxtouches #unedeux
```

---

## Note technique — mots-clés colorés sur les titres DUO PHOTO

Le moteur de coloration (`state.greenWords` / `greenWordIndices`) matche un
mot **exact** du titre (casse + ponctuation collée comprises). Sur S4
(« UN SEUL CANDIDAT POUR TOUT UN MONDIAL »), le mot `UN` apparaît deux fois.
Soit on accepte que les deux occurrences se colorent, soit on reformule le
titre pour isoler un mot unique sans ambiguïté, par ex. `UN SEUL PAYS
CANDIDAT AU MONDIAL` avec accent sur `SEUL`. À trancher dans l'éditeur au
moment du
remplissage, selon le rendu réel.

---

## Sources vérifiées (recherche web, juillet-août 2026)

- Plan de privatisation « FIFA Forward Enterprise », opposition de l'UEFA,
  démission de Carlos Cordeiro, abandon du projet :
  [NPR](https://www.npr.org/2026/07/31/nx-s1-5915820/fifa-world-cup-gianni-infantino),
  [TIME](https://time.com/article/2026/08/01/fifa-s-infantino-scraps-world-cup-investment-plan-but-is-it-too-little-too-late-/),
  [Euronews](https://www.euronews.com/my-europe/2026/07/31/a-history-of-own-goals-gianni-infantinos-timeline-of-fifa-controversies),
  [TIME (Kushner/Thrive Capital)](https://time.com/article/2026/07/29/fifa-forward-enterprise-world-cup-commercial-invest-infantino-trump-kushner/)
- Salaire d'Infantino et rémunération projetée via le plan FFE :
  [Sportbible](https://www.sportbible.com/football/football-news/fifa-world-cup/gianni-infantino-fifa-pay-salary-wages-124263-20260624),
  [Goal.com](https://www.goal.com/en/news/the-times-reveal-the-mega-salary-that-infantino-had-in-mind-for-himself/blt4f96806c3c3d3d5e)
- Limite des trois mandats et « faille » des 39 premiers mois non comptabilisés,
  Congrès de Vancouver (30 avril 2026) :
  [Yahoo Sports](https://sports.yahoo.com/articles/gianni-infantino-might-found-loophole-084217147.html),
  [Inside the Games](https://www.insidethegames.biz/articles/infantino-term-limits)
- Carton rouge de Folarin Balogun suspendu après l'appel de Donald Trump,
  réaction de l'UEFA :
  [Snopes](https://www.snopes.com/news/2026/07/06/trump-fifa-red-card/),
  [CNBC](https://www.cnbc.com/2026/07/05/trump-fifa-balogun-world-cup-red-card-suspension.html),
  [CNBC (suite)](https://www.cnbc.com/2026/07/06/trump-balogun-fifa-world-cup-us-belgium.html)
- Plaintes formelles sur la proximité Infantino-Trump après le Mondial :
  [Yahoo Sports](https://sports.yahoo.com/articles/two-formal-complaints-gianni-infantino-104223022.html),
  [Al Jazeera](https://www.aljazeera.com/sports/2026/8/4/fifa-deny-infantino-sought-trump-backing-after-failed-world-cup-sell-off)
- Prix des billets, promesse initiale à 1 550 $, pic à 5 785 $, enquête des
  procureurs de New York et du New Jersey :
  [Fortune](https://fortune.com/2026/06/02/fifa-dynamic-pricing-backfiring-soccer-fans-world-cup-ticket-costs/),
  [ESPN](https://www.espn.com/soccer/story/_/id/47325927/fifa-2026-world-cup-ticket-prices-supporter-tier),
  [The Conversation](https://theconversation.com/the-ticket-price-fiasco-for-the-mens-fifa-world-cup-has-been-a-spectacular-own-goal-282532)
- Attribution du Mondial 2034 à l'Arabie saoudite (vote sans concurrent,
  fenêtre de candidature de 26 jours, partenariat Aramco) :
  [Front Office Sports](https://frontofficesports.com/saudi-arabia-2034-fifa-world-cup/),
  [World Soccer Talk](https://worldsoccertalk.com/news/why-saudi-arabia-will-host-the-2034-world-cup-gianni-infantino-under-fire-after-poor-human-rights-record/)
- Revenus FIFA du cycle 2023-2026 (~15 milliards de dollars, contre 11
  milliards initialement prévus) :
  [Sportcal](https://www.sportcal.com/financial/fifa-to-net-15bn-revenue-for-2023-26-cycle-afa-partners-with-faraday/),
  [Yahoo Sports](https://sports.yahoo.com/articles/interpreting-infantino-15b-world-cup-195259357.html)
- UEFA menace d'action légale et demande la conservation des documents liés
  au plan FFE (3 août 2026) :
  [Free Malaysia Today](https://www.freemalaysiatoday.com/category/highlight/2026/08/03/uefa-threatens-legal-action-demands-infantino-preserve-records)

Toute citation traduite de l'anglais l'a été fidèlement, sans reformulation
du sens. Les faits contestés ou niés par une partie (ex. FIFA dément
qu'Infantino ait sollicité le soutien de Trump après l'échec du plan FFE)
sont présentés comme tels, pas comme établis.
