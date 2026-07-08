# une·deux — Templates de scénario par série

Grille narrative commune : **HOOK → TRANSITION → TEASE (libre) → CLIMAX → ACTION**.
Règles prioritaires appliquées partout :
- **Hook ultra-catchy** (familles curiosité / contrariant / chiffre absurde).
- **Carrousel sans limite de slides** : le TEASE s'étend autant que le récit l'exige.
- **CTA ouvert « série »** : la dernière slide annonce explicitement une suite.
- **Reel : 90 secondes max.**
- Une seule émotion par post. Métriques reines : sauvegardes + complétion.

---

## Ce jour-là — `#cejourla` · Carrousel 3:4

| Slide | Fonction | Contenu |
|-------|----------|---------|
| S1 | HOOK | Date + fait impossible. Ex : « [DATE]. [Joueur] avait [âge] ans. Et il a [exploit improbable]. » + sous-titre qui crée le manque. |
| S2 | TRANSITION | Le contexte de la date : enjeu, adversaire, ce qui était en jeu. Chiffres exacts. |
| S3…Sn | TEASE | Le déroulé minute par minute / étape par étape. Une idée par slide, chaque slide ouvre une boucle (« Sauf que. », « Et le plus fou, c'est pas ça. »). Étendre autant que nécessaire. |
| S(n-1) | CLIMAX | Le payoff qui referme la cover : ce que la date a vraiment changé. |
| Sn | ACTION | CTA ouvert : « Ce jour-là n'est qu'un début. Demain, un autre. » → FOLLOW. |

> **CTA ouvert type** : « Chaque jour, une date. Reste pour ne pas rater la prochaine. »

---

## Les oubliés — `#lesoubliés` · Carrousel 3:4

| Slide | Fonction | Contenu |
|-------|----------|---------|
| S1 | HOOK | Révélation d'injustice nommée. Ex : « Le meilleur joueur de cette équipe n'a jamais joué une minute. » + sous-titre « Et personne n'en parle. » |
| S2 | TRANSITION | Qui il était, sa légitimité (palmarès, témoignages), pourquoi on devrait le connaître. |
| S3…Sn | TEASE | Le récit de l'effacement, étape par étape : ce qu'il a fait, comment l'histoire l'a écrasé. Chaque slide une preuve. |
| S(n-1) | CLIMAX | L'injustice nommée, sans moraliser : le fait brut qui révèle l'oubli. |
| Sn | ACTION | CTA ouvert : « Il y en a d'autres qu'on a effacés. On les sort un par un. » → FOLLOW. |

> **CTA ouvert type** : « Ce nom, tu ne l'oublieras plus. Et il y en a d'autres. À suivre. »

---

## Portraits — `#portraits` · Reel 9:16 (90 s max)

Structure reel (scènes), pas un carrousel. Chaque scène = 1 media + subs (2 lignes max).

| Scène | Fonction | Contenu |
|-------|----------|---------|
| 1 | HOOK | Accroche sur l'angle méconnu, pas la gloire évidente. Ex : « Tout le monde connaît [joueur]. Personne ne connaît [le détail]. » |
| 2 | CONTEXTE | Qui il est, situé rapidement, mais par l'angle choisi. |
| 3 | EXPLOIT/RÉVÉLATION | Le moment ou le trait qui change le regard sur lui. |
| 4 | DÉTAIL FOU | La relance : le fait que personne ne formule. |
| 5 | CHUTE | Le payoff : ce qui fait sa singularité. CTA ouvert oralisé. |

> **Durée** : ~5 scènes, viser 60–90 s. Ne jamais dépasser 1 min 30.
> **CTA ouvert type (oralisé sur la dernière scène)** : « Et c'est pas le seul portrait. Le prochain arrive. »
> Le reel a une valeur autonome — il ne recopie pas un carrousel.

---

## L'arrêt de jeu — `#arretdejeu` · Carrousel 3:4 (enquête/hypothèse)

Ton mini-enquête, jamais de résolution nette : on pose la question et on aligne
les faits, mais on ne referme pas la boucle par un « voici pourquoi » définitif.
La dernière slide relance ou expose la piste la plus solide sans trancher —
c'est ce suspense non résolu qui fait discuter en commentaires.

**Pipeline (spécifique à cette série) :** L'arrêt de jeu ne se construit **pas**
avec `post.html` (pas de templates A/H/G/D). Tout se fait dans
`editeur-series.html`, slide par slide, avec 3 templates seulement : `titre`
(cover), `corps` (toutes les slides intérieures), `cta` (dernière slide). Voir
`SKILL.md` § « Densité du corps de texte par série » et
`posts/2026-07-08-fifa-argentine-favoritisme/` pour un exemple complet.

**Densité du corps de texte :** contrairement à *Ce jour-là* ou *Les oubliés*,
les slides intérieures ne sont pas des punchlines compressées avec tag/titre.
Ce sont des blocs `corps` (un seul champ `body`, fond uni, pas de photo) qui
approfondissent le sujet façon dossier : on reprend le paragraphe quasi complet
de la source (chiffres secondaires, nuances, citations d'appoint intégrées au
texte courant), pas une phrase unique. S'il y a trop de matière pour une seule
slide, on en ajoute une plutôt que de compresser.

| Slide | Template | Fonction | Contenu |
|-------|----------|----------|---------|
| S1 | `titre` | HOOK | Cover — la question foot posée cash, sans détour. Ex : « Mais pourquoi l'équipe de France ne joue-t-elle plus jamais en rouge ? » Titre + mot-clé coloré + photo. Pas de sous-titre. |
| S2 | `corps` | CONSTAT | Le fait qui rend la question légitime — un chiffre, une asymétrie, une récurrence qui interpelle. Paragraphe dense. |
| S3…S(n-1) | `corps` | ENQUÊTE | Les indices s'accumulent étape par étape (dates, chiffres, déclarations, citations réelles intégrées au texte) — sans jamais les relier en une explication officielle unique. Un paragraphe dense par slide, autant de slides que la matière l'exige. |
| S(n-1) | `corps` | PISTE | La piste la plus solide qu'on ait trouvée, présentée comme hypothèse — pas comme un verdict. |
| Sn | `cta` | ACTION | CTA ouvert qui relance la question plutôt que de la refermer. → FOLLOW. |

> **CTA ouvert type** : « Une histoire par semaine. On aligne les faits, jamais de réponse toute faite. »

---

## Rappels transverses
- **Hook** : toujours passé par `hook-writer-sms` + banque de hooks. Jamais tiède.
- **Mécanique du swipe** : chaque slide TEASE finit sur une relance qui appelle la suivante. Ne jamais résoudre la boucle de la cover avant le CLIMAX.
- **Une leçon transposable** glissée au CLIMAX (ce qui fait sauvegarder).
- **Humanizer** : passe finale sur tous les textes avant livraison.
- **Vérif factuelle** obligatoire avant rédaction (chiffres, citations, dates).
