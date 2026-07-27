import React from 'react';
import {
  anton400,
  archivoVar,
  saira400,
  saira500,
  saira600,
  saira700,
} from './fontData.generated';

/**
 * une·deux design tokens, ported verbatim from design-system/tokens/*.css
 * (colors.css, typography.css, spacing.css, effects.css) with the Google
 * Fonts @import swapped for local base64 @font-face rules so the video
 * renders identically with no network access.
 */
const CSS = `
@font-face{font-family:'Anton';font-style:normal;font-weight:400;src:url(data:font/woff2;base64,${anton400}) format('woff2');}
@font-face{font-family:'Archivo';font-style:normal;font-weight:400 700;src:url(data:font/woff2;base64,${archivoVar}) format('woff2');}
@font-face{font-family:'Saira Condensed';font-style:normal;font-weight:400;src:url(data:font/woff2;base64,${saira400}) format('woff2');}
@font-face{font-family:'Saira Condensed';font-style:normal;font-weight:500;src:url(data:font/woff2;base64,${saira500}) format('woff2');}
@font-face{font-family:'Saira Condensed';font-style:normal;font-weight:600;src:url(data:font/woff2;base64,${saira600}) format('woff2');}
@font-face{font-family:'Saira Condensed';font-style:normal;font-weight:700;src:url(data:font/woff2;base64,${saira700}) format('woff2');}

:root{
  --ink: #2C2823;
  --paper: #F1ECE1;
  --cream: #EDDCB2;
  --muted-cream: #D1C1A3;

  --ocre: #C2A04E;
  --vert: #27543C;
  --vert-deep: #1F4430;
  --rouille: #A8452B;

  --surface-dark: var(--ink);
  --surface-light: var(--cream);

  --sig-cejourla: var(--ocre);
  --on-sig-cejourla: var(--ink);
  --sig-oublies: var(--vert);
  --on-sig-oublies: var(--cream);
  --sig-arretdejeu: var(--rouille);
  --on-sig-arretdejeu: var(--cream);
  --sig-portraits: var(--cream);

  --font-display: 'Anton', 'Arial Narrow', sans-serif;
  --font-body: 'Archivo', system-ui, sans-serif;
  --font-label: 'Saira Condensed', system-ui, sans-serif;

  --fs-display-cover-title: 8.5cqw;
  --fs-display-cta-title: 9.63cqw;
  --fs-display-quote: 9.63cqw;
  --fs-display-pagination: 6.30cqw;
  --fs-display-wordmark: 5.37cqw;

  --fs-body-slide: 3.70cqw;
  --fs-body-slide-sm: 2.78cqw;

  --fs-label-tag: 2.96cqw;
  --fs-label-handle: 2.96cqw;
  --fs-label-monogram: 3.52cqw;
  --fs-label-swipe: 3.33cqw;

  --lh-display: 0.92;
  --lh-body: 1.32;

  --hatch-on-cream: repeating-linear-gradient(-45deg, rgba(44,40,35,0.06) 0px, rgba(44,40,35,0.06) 2px, transparent 2px, transparent 46px);
  --hatch-on-cream-faint: repeating-linear-gradient(-45deg, rgba(44,40,35,0.05) 0px, rgba(44,40,35,0.05) 2px, transparent 2px, transparent 46px);
  --hatch-enquete: repeating-linear-gradient(-45deg, rgba(241,236,225,0.06) 0px, rgba(241,236,225,0.06) 1.5px, transparent 1.5px, transparent 38px);

  --scrim-cover: linear-gradient(to bottom, rgba(44,40,35,0) 0%, rgba(44,40,35,0) 42%, rgba(44,40,35,0.78) 80%, rgba(44,40,35,0.78) 100%);

  --grade-arretdejeu: rgba(150,62,40,0.22);
}
* { box-sizing: border-box; }
`;

export function BrandFonts() {
  return <style dangerouslySetInnerHTML={{__html: CSS}} />;
}
