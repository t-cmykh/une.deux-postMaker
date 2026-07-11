The core carousel slide — cover (hook) and interior fact slides, one per series signature.

```jsx
<CoverSlide
  serie="cejourla"
  variant="cover"
  title={"ILS ONT INVENTÉ LE FOOT\nILS L'ONT GAGNÉ UNE FOIS"}
  greenWord="UNE FOIS"
  body="Et c'était il y a 60 ans."
  cur="01" tot="08"
  mediaUrl="/assets/placeholder-sepia.jpg"
/>
```

Variants:
- `cover` — title + body, the S1 hook slide.
- `titre` — title only, larger, no body (Ce jour-là animates it in line-by-line in the live tool).
- `corps` — body only, full-frame, tinted panel behind the text. Built for L'arrêt de jeu's enquête format.

Always pair with the matching `serie` — color, photo grade and tag label are locked together in the real product; never hand-pick a signature color that doesn't belong to the chosen series.
