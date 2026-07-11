# une·deux — Design System

**une·deux** (@une.deux) is a French-language Instagram media brand telling little-known
football history — *"le foot en deux touches"* (football in two touches). The brand's whole
product is short-form editorial content: narrative Instagram carousels and reels about
football history, tied to the 2026 World Cup news cycle, published by Thomas at a cadence of
2 posts/day (14/week).

This design system was built from a single source: the brand's own internal content-production
tool, not a customer-facing app. There is one "product" — **Studio**, an in-browser toolkit
(plain HTML/Canvas, no framework) Thomas uses to lay out and export each Instagram slide —
plus the editorial voice/structure rules that govern what goes on those slides.

## Source material

- **GitHub repo:** [`t-cmykh/une.deux-postMaker`](https://github.com/t-cmykh/une.deux-postMaker)
  — the only resource provided. Contains:
  - `editeurs/editeur-series.html` — the reference editor (series-aware cover/CTA/quote/breath
    slide composer). This is the primary source for every visual token and component in this system.
  - `editeurs/post.html`, `reel.html`, `reel-fullbleed.html`, `monteur-mobile.html`,
    `crop-focus.html` — sibling editors for inner slides, reels, and manual cropping (not
    individually rebuilt here — `editeur-series.html` shares their drawing code for the cover/CTA/
    quote/breath templates that this system covers).
  - `SKILL.md` — the full editorial rulebook: hook-writing formulas, narrative structure (Hook ·
    Transition · Tease · Climax · Action), the 4 recurring series, caption format, fact-checking
    rules.
  - `exemples/` — reference `script.json` payloads, per-series scenario/prompt/caption examples.
  - `posts/2026-06-29-gaetjens-1950/` — one fully worked example post (script + prompts + caption
    + fact-check table).
  - `planning/planning-unedeux.md` — weekly editorial calendar across the 4 series.

  **Explore the repo further** for anything not captured here — in particular `post.html` and the
  reel editors hold the inner-slide and video-specific drawing logic this system didn't fully
  port, and `exemples/` + `posts/` hold many more worked copy examples to calibrate tone against.

No Figma file, screenshot set, or second codebase was provided — everything below is read directly
from that repo's own source, not inferred from a screenshot.

## What's in this system

- `styles.css` + `tokens/` — colors, type, spacing, effects (imports only; see below).
- `tokens/fonts.css` — Google Fonts `@import` for Anton / Archivo / Saira Condensed (see Fonts note).
- `guidelines/` — 12 foundation specimen cards (Colors, Type, Spacing, Brand groups).
- `components/slides/` — the 4 canvas slide templates rebuilt as React components: `CoverSlide`,
  `BreathSlide`, `QuoteSlide`, `CTASlide`, plus the shared `BrandHeader` and `SeriesTag` parts.
- `components/studio/` — the editor's own UI chrome as reusable primitives: `Chip`, `ToggleSwitch`,
  `RangeRow`, `SerieButton`, `StudioButton`.
- `ui_kits/studio/` — an interactive click-through recreation of `editeur-series.html`: series
  picker, template chips, live-editable fields driving a real-time slide preview.
- `assets/` — intentionally near-empty; see Iconography below.
- `SKILL.md` (this folder's own, distinct from the source repo's) — a portable skill for using
  this design system elsewhere.

## Components

- **Slides** — `BrandHeader`, `SeriesTag`, `CoverSlide`, `BreathSlide`, `QuoteSlide`, `CTASlide`
- **Studio controls** — `Chip`, `ToggleSwitch`, `RangeRow`, `SerieButton`, `StudioButton`

### Intentional additions
No component here was invented beyond what `editeur-series.html` itself draws or renders as UI
chrome — `BrandHeader` and `SeriesTag` are extracted as shared parts (the source draws them inline
inside every template function) purely to avoid duplicating the same canvas drawing code 4 times;
they carry no new visual design.

## Fonts — flag for the user

Anton, Archivo, and Saira Condensed are loaded from Google Fonts by `@import url(...)` — exactly
as the source editors do it. **No self-hosted font binaries exist in the source repo.** If you
need this system to work fully offline, download the 3 families from fonts.google.com and swap
`tokens/fonts.css`'s `@import` for local `@font-face` rules. No substitution was made — these are
the real families the brand uses today.

---

## Content fundamentals

**Posture: the archivist-storyteller who exhumes.** une·deux doesn't cover current football —
it digs up the forgotten, oblique, or absurd stories connected to it (`SKILL.md`: *"l'archiviste-conteur
qui exhume"*).

- **Person & address:** tutoiement throughout ("Tu t'apprêtes à jouer…", "Alors dis-nous :"). Direct,
  informal, never corporate "vous".
- **Sentence shape:** short, declarative, punchy. Facts stated as settled fact, full stop — never
  hedged. The brand's own house rule bans "voici", "découvre", "l'histoire incroyable de" — you
  *assert*, you don't present. Example hook: *"Le meilleur joueur de cette équipe n'a jamais joué
  une minute."*
- **The hook "mould" (S1 law):** subject + past-tense action verb + a detail that shouldn't be
  there. Often two beats: a flat statement, then a second sentence that "plants the knife" —
  *"Il a gagné le Mondial. Il a touché 2 000 francs."*
- **The swipe mechanic:** every slide must open a loop the next slide alone closes ("Sauf que…",
  "Et le plus fou, c'est pas ça."). The cover's loop never resolves before the climax slide.
  One live loop at a time — never stack cliffhangers.
- **Narrative grid:** Hook (S1) → Transition (S2, gives a reason to stay) → Tease (S3–S6, one
  idea per slide) → Climax (payoff + one transposable lesson) → Action (S8, one single ask).
- **Fact discipline:** every cited number/date/quote must be corroborated by **3 independent
  sources** before use; anything that can't be is dropped, even if it's punchier.
- **Emoji:** used sparingly and specifically — one flag emoji per caption hook (matching the
  subject's nationality), plus `⚽️` beside the handle sign-off. Never decorative or random.
- **Hashtags:** max 5, always ending in `#unedeux`; one is always the series tag
    (`#cejourla`/`#lesoubliés`/`#portraits`/`#arretdejeu`).
- **CTA:** always exactly one action, the button always says **FOLLOW** — never a second option.
- **Emotional discipline:** one emotion per post (surprise / nostalgie / injustice / fierté) —
  never mixed.
- **Vibe:** "expert complice qui va à l'essentiel" — an insider friend, not a lecturer; dense with
  real facts, zero filler, zero AI-toned hedging (the source explicitly runs a "humanizer" pass to
  strip inflated symbolism, promotional language, and vague attributions before publishing).

## Visual foundations

- **Palette:** one dark ink ground (`--ink #2C2823`) carries every cover/breath slide; one warm
  cream ground (`--cream #EDDCB2`) carries every CTA/quote slide. Each of the 4 series then locks
  its own single accent color on top (ocre / vert / rust, or ink-on-cream for Portraits) — colors
  are never mixed across series.
- **Type:** exactly 3 families, each with one job — **Anton** (display, always uppercase: titles,
  quotes, CTA) for the loud thing on the slide; **Archivo** (body, 400/500/700) for subtitles/body
  copy, `**bold**`-markup supported; **Saira Condensed** (label, 600/700, tracked-out uppercase)
  for every piece of UI chrome — tags, the wordmark ring, handle, pagination, swipe label.
- **Spacing:** editor UI spacing is small and dense (4–28px), not grid-snapped — 11px/13px/22px
  show up as often as 8px/16px. Slide-canvas margins are locked per aspect ratio (50/120px on
  square-ish ratios, 96px all around on 9:16), not proportional.
- **Backgrounds:** slides are photo-first — a full-bleed background photo (or a flat 2-stop
  gradient placeholder when none is set) with a bottom-up ink scrim for legibility. No hand-drawn
  illustration, no repeating decorative pattern on dark slides. The only "texture" anywhere is a
  faint 45° hairline hatch — on cream CTA/quote slides (very subtle ink-on-cream) and, uniquely for
  L'arrêt de jeu, a cream-on-photo "dossier" overprint hatch signaling its enquête framing.
  No gradients as a decorative device — only functional ones (the legibility scrim, Portraits'
  vignette).
- **Animation:** almost none. The one exception is Ce jour-là's cover title, which reveals
  line-by-line with a short fade/rise on load (speed adjustable in the editor) — every other
  template appears fully rendered, static, immediately (this is a static-image/video export tool,
  not an interactive product).
- **Hover/press states:** editor-only (there's no "hover" on an exported Instagram slide). Chips
  and buttons brighten (`filter:brightness(1.08)`) on hover; borders lighten from the dark line
  color to a lighter grey on hover; toggle knobs slide with a simple 0.15s ease. No shrink/scale
  press effect anywhere.
- **Borders & radius:** the brand is flat, printed-matter flat — slide *content* never has a
  border, shadow, or rounded corner. Radius (7–10px, or 20px pill, or full circle) appears only on
  editor UI chrome: inputs, chips, buttons, the canvas preview shell.
- **Shadows:** exactly one, `0 14px 50px rgba(0,0,0,.45)` under the editor's live canvas preview —
  nowhere else. No card shadows, no inner shadows, no glow.
- **Transparency & blur:** transparency is used functionally (the legibility scrim over photos,
  Portraits' semi-transparent ink caption box, the editor's disabled/dashed states) — never blur;
  there is no `backdrop-filter` anywhere in the source.
- **Imagery color grade:** each series grades its photos distinctly: Ce jour-là = warm sepia tint;
  Les oubliés = cold desaturated grey-green; Portraits = true black & white studio with a radial
  vignette; L'arrêt de jeu = rust tint plus the dossier hatch overprint. All 4 favor high-contrast,
  slightly grainy "press photography" over glossy studio imagery (see the source's own image-prompt
  language: *"cinematic grain," "vintage archival look," "Realistic photograph, not illustration"*).
- **Corner radii:** see Borders above — 7/9/10px on small controls, 20px pill on chips, full circle
  on the monogram ring / toggle knob / swipe arrow button / bookmark's rounded top corners.
- **Cards:** the editor's own UI "cards" (series-picker buttons, media dropzone) are flat panels —
  1px hairline border, no shadow, no gradient, radius 9–10px, with a 3px solid left-edge accent
  bar in the signature color when selected. There is no card pattern on the exported slides
  themselves — a slide is the whole frame, not a card within a frame.
- **Layout rules:** every slide keeps a fixed header (ring monogram + wordmark + handle + hairline)
  and, on non-vertical ratios, a fixed footer band (rule + swipe/pagination). Instagram's UI safe
  zone (avoid top ~150px / bottom ~120–200px on 9:16, per Meta's own overlay guidance) is drawn as
  an optional dashed guide in the editor, never exported.

## Iconography

There is no icon system, icon font, or SVG/PNG icon set anywhere in the source repo. The editor's
own navigation screen (`editeurs/index.html`) uses **raw Unicode glyphs** as stand-ins for icons
(★ ▦ ▮ ✎ ⌖) — this is a placeholder pattern from the tool's own internal nav, not a considered
icon language, so it isn't propagated into this system's components. The one recurring "icon" that
*is* part of the actual brand output is the **bookmark glyph** on the CTA slide (hand-drawn in
canvas as a simple filled path with a notched bottom corner) — reproduced in `CTASlide` as an
inline SVG path matching the source's exact geometry, since it's the one repeating brand mark.
Emoji appear only in captions (flags + `⚽️`), never inside a slide's visual design. If Thomas can
share a real icon set later, add it under `assets/` and wire it into `CTASlide`/`Studio` controls.

---

## Index — everything in this folder

```
readme.md                    ← this file
SKILL.md                     ← portable skill (Claude Code-compatible)
styles.css                   ← import-only entry point
tokens/
  colors.css                 ← base palette + series signatures + semantic aliases
  typography.css             ← Anton / Archivo / Saira Condensed scale
  spacing.css                ← spacing + radius scale (real editor values)
  effects.css                ← hatch textures, photo grades, cover scrim
  fonts.css                  ← Google Fonts @import (see Fonts note above)
guidelines/                  ← 12 @dsCard specimen cards — Colors (2) · Type (3) · Spacing (2) · Brand (4)
components/
  slides/                    ← BrandHeader, SeriesTag, CoverSlide, BreathSlide, QuoteSlide, CTASlide
  studio/                    ← Chip, ToggleSwitch, RangeRow, SerieButton, StudioButton
ui_kits/
  studio/                    ← interactive Studio editor recreation (index.html + StudioApp.jsx)
assets/
  README.md                  ← notes the absence of logo/icon files (see Iconography)
```


