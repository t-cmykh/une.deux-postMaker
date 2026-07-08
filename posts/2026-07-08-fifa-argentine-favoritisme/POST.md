# L'arrêt de jeu — Pourquoi tout le monde pense que la FIFA avantage l'Argentine ?

**Série :** L'arrêt de jeu · `#arretdejeu` · Carrousel 3:4 · signature rouille / surimpression dossier
**Émotion unique :** curiosité → révélation (enquête, jamais de verdict tranché)
**Famille de hook :** question foot posée cash (signature de série) — variante autorisée sur le moule commun
**Boucle cover→climax :** « la même phrase revient depuis 1978 » → « pas un complot, un biais qui protège les stars »

Source : article fourni par Thomas, adapté au gabarit 12 slides une·deux (le contenu factuel, y compris les nuances « prouvé / non prouvé », est repris tel qu'écrit dans l'article d'origine).

**Règle de série appliquée ici (correction du 08/07) :** dans *L'arrêt de jeu*, les
slides hors cover/CTA sont des blocs de corps de texte qui **approfondissent** le
sujet façon dossier — pas des punchlines compressées comme sur *Ce jour-là* ou
*Les oubliés*. Chaque slide A reprend le paragraphe quasi complet de l'article
(chiffres secondaires, nuances, citations d'appoint), pas une phrase unique. Voir
la règle codifiée dans `SKILL.md` et `exemples/scenarios-par-serie.md`.

---

## Éditeur séries (`editeur-series.html`) — COVER & CTA

> À saisir dans l'éditeur principal (série `arretdejeu` verrouille couleur rouille, virage photo et format 3:4).

**COVER (slide 01)** — série `arretdejeu`, template `cover`
- title : `POURQUOI TOUT LE MONDE PENSE QUE LA FIFA AVANTAGE L'ARGENTINE ?`
- greenWord : `AVANTAGE`
- body : `1978. 2022. 2026. Et à chaque fois, la même phrase revient.`
- cur/tot : `01` / `12`

**CTA (slide 12)** — série `arretdejeu`, template `cta`
- title : `RESTE DANS LE JEU`
- body : `Officiellement, personne ne l'a jamais vraiment expliqué. Le foot en deux touches, tous les jours.`
- btnlabel : `FOLLOW`

Les slides intérieures (02→11) sont dans `script.json` (format `post.html`, templates A/H/G) — corps de texte denses, pas des punchlines (voir règle de série ci-dessus).

**Débat (sous le CTA, réservé à la légende, pas dans le JSON) :**
> Débat : « Alors dis-nous : biais inconscient, ou vrai favoritisme organisé ? »

---

## Structure narrative (12 slides)

| # | Template | Fonction | Contenu |
|---|----------|----------|---------|
| S1 | A | HOOK | La question posée cash + boucle « la même phrase revient » |
| S2 | A | CONSTAT | 1978 — le 6-0, la dérogation d'horaire FIFA, la protestation du Brésil, la règle instaurée après Gijón |
| S3 | H | respiration | « Le score interroge. Le calendrier, encore plus. » |
| S4 | A | ENQUÊTE | L'hypothèse opération Condor : accord non prouvé, déni des joueurs péruviens, occasions du Pérou en jeu, mais Videla au vestiaire et l'ESMA à 2 km |
| S5 | G | citation réelle | Fernández Moores, journaliste |
| S6 | A | ENQUÊTE | 2022 — les six penaltys, le penalty Messi-Croatie, la citation Infantino (2017/La Nación), Marciniak et Ibrahimović |
| S7 | G | citation réelle | Pepe, après l'élimination du Portugal |
| S8 | A | ENQUÊTE | 2026 — tirage de Washington, bascule poule I→J, règle des 48 équipes, groupe abordable et tableau « boulevard » |
| S9 | A | ENQUÊTE | Les 4 changements de leader FIFA en 3 mois + Cap-Vert (3-2) + but égyptien annulé et l'accusation de match truqué |
| S10 | H | respiration | « Le privilège est resté. La raison a disparu. » |
| S11 | A | PISTE (climax) | Balogun/Trump + la leçon transposable : pas un complot, un biais qui protège les stars |
| S12 | D | ACTION | CTA ouvert, ne referme pas la question |

---

## Photos — pas de prompts pour cette série

**Règle Thomas (ajoutée le 08/07) : plus de prompts photo livrés sur L'arrêt de
jeu.** Les noms de fichiers restent dans `script.json` (`argentine_01.PNG` à
`argentine_07.PNG`, sur S1, S2, S4, S6, S8, S9, S11) pour que l'éditeur ait ses
emplacements média, mais Thomas source/produit ces visuels lui-même — Claude ne
rédige plus de prompt texte pour cette série. Voir la règle codifiée dans
`SKILL.md` (§ Livrables par post) et `exemples/prompts-par-serie.md`.

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
| Dérogation d'horaire FIFA, Argentine-Pérou 6-0 (21/06/1978) | ✅ présenté comme fait acquis (S2/S3) |
| Hypothèse opération Condor / accord Argentine-Pérou | ⚠️ présenté explicitement comme non prouvé (S4) |
| Citation Ezequiel Fernández Moores | ✅ citée telle quelle, attribuée (S5) |
| 6 penaltys Argentine, Mondial 2022 | ✅ présenté comme fait acquis (S6) |
| Citation Infantino sur Messi (2017, La Nación) | ✅ citée telle quelle, attribuée (S6) |
| Citation Pepe après l'élimination du Portugal | ✅ citée telle quelle, attribuée (S7) |
| Tirage au sort 2026 : Argentine déplacée de poule I à J | ✅ présenté comme fait acquis, réglementaire (S8) |
| 4 changements de leader au classement FIFA (déc. 2025 → juil. 2026) | ✅ présenté comme fait acquis (S9) |
| Cap-Vert 3-2 (a.p.) en 16es, but égyptien annulé, accusation « match truqué » | ✅ présenté comme fait acquis, réaction citée en discours indirect (S9) |
| Levée de la suspension de Balogun après un appel de Trump à Infantino | ✅ présenté comme fait acquis (S11) |
| Conclusion « biais qui protège les stars » | 🧭 présentée comme piste/hypothèse, pas comme un verdict (S11), conforme à la posture éditoriale de la série |

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
