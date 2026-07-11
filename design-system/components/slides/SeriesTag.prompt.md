The filled series-name tag pill that anchors every non-Portraits cover slide.

```jsx
<SeriesTag label="N°1 CE JOUR LÀ …" bg="var(--sig-cejourla)" color="var(--on-sig-cejourla)" />
```

Each of the 4 series has a fixed tag/text-color pair — never mix them:
- Ce jour-là: bg `--sig-cejourla` (ocre), text `--on-sig-cejourla` (ink)
- Les oubliés: bg `--sig-oublies` (vert), text `--on-sig-oublies` (cream)
- L'arrêt de jeu: bg `--sig-arretdejeu` (rouille), text `--on-sig-arretdejeu` (cream)
- Portraits doesn't use this component — see CoverSlide's vertical label.
