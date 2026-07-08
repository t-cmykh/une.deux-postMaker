# L'arrêt de jeu — Pourquoi tout le monde pense que la FIFA avantage l'Argentine ?

**Série :** L'arrêt de jeu · `#arretdejeu` · Carrousel 3:4 · signature rouille
**Émotion unique :** curiosité → révélation (enquête, jamais de verdict tranché)
**Boucle cover→climax :** « la même phrase revient depuis 1978 » → « pas un complot, un biais qui protège les stars »

Source : article fourni par Thomas, adapté au format réel de la série (voir
correction du 08/07 ci-dessous).

---

## Pipeline — correction du 08/07 (règle de série)

**L'arrêt de jeu ne se construit PAS avec `post.html` / les templates A·H·G·D.**
Tout le post se fait dans **`editeur-series.html`**, slide par slide, avec
seulement 3 templates :

- **`titre`** (cover, S1 uniquement) — titre 2-4 lignes avec un mot-clé coloré
  (`greenWord`), média photo plein cadre. **Pas de sous-titre/body.**
- **`corps`** (toutes les slides intérieures) — **un seul champ `body`** : un
  paragraphe dense qui approfondit le fait, fond uni (pas de photo), pas de
  titre, pas de tag personnalisé par slide. Le bandeau « L'ARRÊT DE JEU » est
  automatique (fixé par la série), pas un champ à remplir.
- **`cta`** (dernière slide) — `title` + `body` + `btnlabel`.

Autrement dit : **seules la cover et le CTA ont une mise en page « titre ».
Tout le reste est du corps de texte pur**, un paragraphe complet par slide (pas
une punchline compressée — cf. la règle « densité du corps de texte » déjà
codifiée dans `SKILL.md`). Voir l'exemple fourni par Thomas (post « Pourquoi le
Brésil ne joue-t-il plus jamais en blanc ? ») : 01/08 = cover photo + titre
seul, 02→07 = fond uni + un paragraphe, 08 = CTA.

`script.json` de ce post reflète ce modèle (`template: "titre" | "corps" |
"cta"`), pas le modèle `post.html`. Il sert de référence texte à ressaisir
dans `editeur-series.html` slide par slide (l'éditeur n'a pas d'import JSON en
masse).

---

## Slides (10, à saisir dans `editeur-series.html`, série `arretdejeu`)

| # | Template | Contenu |
|---|----------|---------|
| 01 | `titre` | Cover — titre + `AVANTAGE` en rouille, photo argentine_01.PNG |
| 02 | `corps` | 1978 — la dérogation d'horaire FIFA, le 6-0, la protestation du Brésil, la règle post-Gijón |
| 03 | `corps` | L'hypothèse opération Condor : accord non prouvé, déni des joueurs, nuances sur le jeu, mais Videla au vestiaire et l'ESMA à 2 km + citation Fernández Moores |
| 04 | `corps` | 2022 — les six penaltys, le penalty Messi-Croatie, la citation d'Infantino sur Messi (2017/La Nación) |
| 05 | `corps` | Les réactions : Pepe, Ibrahimović, Marciniak — et la nuance (pas un complot, Maradona puis Messi suffisent à expliquer la fréquence) |
| 06 | `corps` | 2026 — le tirage de Washington, bascule poule I→J, règle des 48 équipes, groupe abordable et tableau « boulevard » |
| 07 | `corps` | Le classement FIFA qui bascule 4 fois en 3 mois + Cap-Vert (3-2) + but égyptien annulé |
| 08 | `corps` | La réaction égyptienne « match truqué » + la levée de la suspension de Balogun après l'appel de Trump à Infantino |
| 09 | `corps` | PISTE (climax) — pas un complot, un biais qui protège les stars ; la leçon transposable |
| 10 | `cta` | RESTE DANS LE JEU — tagline de série + FOLLOW |

Détail des champs : voir `script.json`.

**Débat (réservé à la légende, pas dans le JSON) :**
> Débat : « Alors dis-nous : biais inconscient, ou vrai favoritisme organisé ? »

---

## Photos — pas de prompts pour cette série

**Règle Thomas (rappel du 08/07) : plus de prompts photo sur L'arrêt de jeu.**
Seule la cover (S1) a besoin d'un visuel (`argentine_01.PNG`) ; toutes les
slides `corps` et la slide `cta` sont en fond uni, sans photo. Thomas
source/produit ce visuel de cover lui-même — aucun prompt texte n'est fourni.

---

## Légende (L'arrêt de jeu — 4 temps)

```
**La FIFA avantage-t-elle vraiment l'Argentine ? 🤔🇦🇷**

1978 : pour aller en finale, l'Argentine doit battre le Pérou par 4 buts d'écart. La FIFA lui accorde une dérogation d'horaire, elle joue en connaissant déjà le score du Brésil. Résultat : 6-0. Des années plus tard, des documents liés à l'opération Condor évoquent un accord entre les deux dictatures. Rien n'est prouvé, mais Videla est entré dans le vestiaire péruvien avant le match.

2022 : six penaltys en sept matchs, dont un très discuté contre la Croatie. Cinq ans plus tôt, Infantino avait dit qu'il serait « injuste » que Messi finisse sa carrière sans Coupe du monde. 2026 : l'Argentine change de poule en plein tirage au sort et hérite d'un tableau dégagé, alors que le classement qui justifiait ce privilège a changé quatre fois en trois mois.

Et le plus fou ? Aucun accord organisé n'a jamais été prouvé. Mais une institution qui protège ses stars finit toujours par ressembler à une institution qui triche, même quand elle ne triche pas.

Alors dis-nous : biais inconscient, ou vrai favoritisme organisé ? 👇
@une.deux ⚽️
.
.
#arretdejeu #messi #coupedumonde #argentine #unedeux
```

---

## Vérification factuelle (règle des 3 sources)

Le contenu de ce post reprend l'article fourni par Thomas, déjà rédigé avec un souci
de distinction explicite entre faits documentés et hypothèses non prouvées. Cette
distinction est conservée sans être aplatie dans le carrousel :

| Fait | Statut dans le post |
|------|----------------------|
| Dérogation d'horaire FIFA, Argentine-Pérou 6-0 (21/06/1978) | ✅ présenté comme fait acquis (S02) |
| Hypothèse opération Condor / accord Argentine-Pérou | ⚠️ présenté explicitement comme non prouvé (S03) |
| Citation Ezequiel Fernández Moores | ✅ citée telle quelle, attribuée (S03) |
| 6 penaltys Argentine, Mondial 2022 | ✅ présenté comme fait acquis (S04) |
| Citation Infantino sur Messi (2017, La Nación) | ✅ citée telle quelle, attribuée (S04) |
| Citations Pepe / Ibrahimović après l'élimination du Portugal | ✅ citées telles quelles, attribuées (S05) |
| Tirage au sort 2026 : Argentine déplacée de poule I à J | ✅ présenté comme fait acquis, réglementaire (S06) |
| 4 changements de leader au classement FIFA (déc. 2025 → juil. 2026) | ✅ présenté comme fait acquis (S07) |
| Cap-Vert 3-2 (a.p.) en 16es, but égyptien annulé, accusation « match truqué » | ✅ présenté comme fait acquis, réaction citée en discours indirect (S07/S08) |
| Levée de la suspension de Balogun après un appel de Trump à Infantino | ✅ présenté comme fait acquis (S08) |
| Conclusion « biais qui protège les stars » | 🧭 présentée comme piste/hypothèse, pas comme un verdict (S09), conforme à la posture éditoriale de la série |

**Recommandation avant publication :** si ce post doit sortir avec la même rigueur que
*Ce jour-là*, refaire une passe de vérification à 3 sources indépendantes sur chaque
ligne ci-dessus (FIFA, Wikipedia, presse) avant mise en ligne — cette étape n'a pas
été relancée ici puisque le texte source était déjà fourni comme rédigé/vérifié par
Thomas.

## Notes skills chaînés
`hook-writer-sms` et `humanizer` ne sont pas disponibles comme skills séparés dans
cette session : le hook (question cash, signature `arretdejeu`) et le style (phrases
courtes, ton complice, zéro remplissage, distinction fait/hypothèse conservée) ont été
travaillés manuellement dans leur esprit.
