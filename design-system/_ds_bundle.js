/* @ds-bundle: {"format":4,"namespace":"UneDeuxDesignSystem_8067cc","components":[{"name":"BrandHeader","sourcePath":"components/slides/BrandHeader.jsx"},{"name":"BreathSlide","sourcePath":"components/slides/BreathSlide.jsx"},{"name":"CTASlide","sourcePath":"components/slides/CTASlide.jsx"},{"name":"CoverSlide","sourcePath":"components/slides/CoverSlide.jsx"},{"name":"QuoteSlide","sourcePath":"components/slides/QuoteSlide.jsx"},{"name":"SeriesTag","sourcePath":"components/slides/SeriesTag.jsx"},{"name":"Chip","sourcePath":"components/studio/Chip.jsx"},{"name":"RangeRow","sourcePath":"components/studio/RangeRow.jsx"},{"name":"SerieButton","sourcePath":"components/studio/SerieButton.jsx"},{"name":"StudioButton","sourcePath":"components/studio/StudioButton.jsx"},{"name":"ToggleSwitch","sourcePath":"components/studio/ToggleSwitch.jsx"}],"sourceHashes":{"components/slides/BrandHeader.jsx":"8bf90d2ab11c","components/slides/BreathSlide.jsx":"1adcc9bb74f1","components/slides/CTASlide.jsx":"eefce9b769b1","components/slides/CoverSlide.jsx":"9bb07e25cfcf","components/slides/QuoteSlide.jsx":"03b2b6470f7a","components/slides/SeriesTag.jsx":"5a69d85349cc","components/studio/Chip.jsx":"213e34f2f8d4","components/studio/RangeRow.jsx":"d405f5b48f44","components/studio/SerieButton.jsx":"71ad31eb66d6","components/studio/StudioButton.jsx":"013e459e1439","components/studio/ToggleSwitch.jsx":"6a5b85202a1d","ui_kits/studio/StudioApp.jsx":"62032450a386"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.UneDeuxDesignSystem_8067cc = window.UneDeuxDesignSystem_8067cc || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/slides/BrandHeader.jsx
try { (() => {
/**
 * BrandHeader — the fixed masthead every une·deux slide opens with:
 * a ring-monogram ("1·2"), the "une·deux" wordmark, and the "@UNE.DEUX" handle,
 * separated from the body of the slide by a single hairline.
 */
function BrandHeader({
  dark = true,
  ring = '1·2',
  handle = '@UNE.DEUX'
}) {
  const fg = dark ? 'var(--cream)' : 'var(--ink)';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '2.4cqw',
      color: fg
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '8.52cqw',
      height: '8.52cqw',
      minWidth: 28,
      minHeight: 28,
      borderRadius: '50%',
      border: '0.37cqw solid ' + fg,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 'var(--fs-label-monogram)',
      flex: '0 0 auto',
      boxSizing: 'border-box'
    }
  }, ring), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-display-wordmark)',
      letterSpacing: '0.01em'
    }
  }, "une\xB7deux"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto',
      fontFamily: 'var(--font-label)',
      fontWeight: 600,
      fontSize: 'var(--fs-label-handle)',
      letterSpacing: '0.02em'
    }
  }, handle)), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 2,
      background: fg,
      opacity: dark ? 1 : 1,
      marginTop: '3.7cqw'
    }
  }));
}
Object.assign(__ds_scope, { BrandHeader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/BrandHeader.jsx", error: String((e && e.message) || e) }); }

// components/slides/BreathSlide.jsx
try { (() => {
/**
 * BreathSlide — the "slide-respiration" (canvas template H). Pure rhythm: no header, no tag,
 * no media — just a short quote (3–6 words) with one accented segment, dead center on ink.
 * Used as a pacing beat between two revelation slides.
 */
function BreathSlide({
  quote = 'Sauf que non.',
  quoteAccent = 'non.',
  sig = 'var(--sig-cejourla)'
}) {
  const idx = quoteAccent ? quote.toLowerCase().indexOf(quoteAccent.toLowerCase()) : -1;
  const before = idx >= 0 ? quote.slice(0, idx) : quote;
  const accent = idx >= 0 ? quote.slice(idx, idx + quoteAccent.length) : '';
  const after = idx >= 0 ? quote.slice(idx + quoteAccent.length) : '';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size',
      width: '100%',
      aspectRatio: '3 / 4',
      background: 'var(--surface-dark)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '10cqw'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: '8cqw',
      lineHeight: 'var(--lh-display)',
      textAlign: 'center',
      color: 'var(--cream)'
    }
  }, before.toUpperCase(), /*#__PURE__*/React.createElement("span", {
    style: {
      color: sig
    }
  }, accent.toUpperCase()), after.toUpperCase()));
}
Object.assign(__ds_scope, { BreathSlide });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/BreathSlide.jsx", error: String((e && e.message) || e) }); }

// components/slides/CTASlide.jsx
try { (() => {
/**
 * CTASlide — the final "follow / save" slide (canvas templates "D"/"S"). Cream ground with the
 * diagonal hatch, a bookmark glyph in the series signature color, a labeled action chip,
 * centered 2-line title with one colored keyword, and a subtitle.
 */
function CTASlide({
  title = 'RESTE DANS LE JEU',
  greenWord = '',
  body = 'Le foot en deux touches, tous les jours.',
  btnlabel = 'FOLLOW',
  sig = 'var(--sig-cejourla)',
  onSig = 'var(--on-sig-cejourla)'
}) {
  const words = title.trim().split(/\s+/);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size',
      width: '100%',
      aspectRatio: '3 / 4',
      position: 'relative',
      background: 'var(--surface-light)',
      backgroundImage: 'var(--hatch-on-cream)',
      color: 'var(--ink)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '6.1cqw 11.1cqw 5.2cqw',
      boxSizing: 'border-box',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      alignSelf: 'stretch'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.BrandHeader, {
    dark: false,
    handle: "@UNE.DEUX"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement("svg", {
    width: "14%",
    viewBox: "0 0 120 156",
    style: {
      fill: sig
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14 0h92a14 14 0 0 1 14 14v142L60 98 0 156V14A14 14 0 0 1 14 0Z"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: '3.7cqw',
      background: sig,
      color: onSig,
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: '3.15cqw',
      letterSpacing: '0.03em',
      padding: '1.5cqw 3cqw'
    }
  }, btnlabel.toUpperCase()), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: '2.8cqw',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-display-cta-title)',
      lineHeight: 'var(--lh-display)',
      overflowWrap: 'break-word'
    }
  }, words.map((w, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      color: greenWord && w.toUpperCase() === greenWord.toUpperCase() ? sig : 'var(--ink)'
    }
  }, w.toUpperCase(), i < words.length - 1 ? ' ' : ''))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: '2.2cqw',
      fontFamily: 'var(--font-body)',
      fontSize: '3.7cqw',
      maxWidth: '86%'
    }
  }, body), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      alignSelf: 'stretch',
      height: 3,
      background: 'var(--ink)',
      marginBottom: '2.8cqw'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      alignSelf: 'flex-start',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: '2.96cqw'
    }
  }, "@UNE.DEUX"));
}
Object.assign(__ds_scope, { CTASlide });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/CTASlide.jsx", error: String((e && e.message) || e) }); }

// components/slides/QuoteSlide.jsx
try { (() => {
/**
 * QuoteSlide — the real, sourced-quote slide (canvas template "G"). Cream ground, diagonal
 * hairline hatch, big Anton quotation with one accented segment, author byline, bottom caption.
 */
function QuoteSlide({
  quote = 'Sur le terrain, tout s\u2019est joué en deux passes.',
  quoteAccent = "tout s'est joué en deux passes.",
  quoteAuthor = '',
  caption = "L'ANALYSE",
  cur = '05',
  tot = '08',
  accent = 'var(--vert)'
}) {
  const idx = quoteAccent ? quote.toLowerCase().indexOf(quoteAccent.toLowerCase()) : -1;
  const before = idx >= 0 ? quote.slice(0, idx) : quote;
  const acc = idx >= 0 ? quote.slice(idx, idx + quoteAccent.length) : '';
  const after = idx >= 0 ? quote.slice(idx + quoteAccent.length) : '';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size',
      width: '100%',
      aspectRatio: '3 / 4',
      position: 'relative',
      background: 'var(--surface-light)',
      backgroundImage: 'var(--hatch-on-cream-faint)',
      color: 'var(--ink)',
      display: 'flex',
      flexDirection: 'column',
      padding: '6.1cqw 11.1cqw 6.5cqw 4.6cqw',
      boxSizing: 'border-box'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.BrandHeader, {
    dark: false,
    handle: "@UNE.DEUX"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-display-quote)',
      lineHeight: 'var(--lh-display)'
    }
  }, "\u201C", before.toUpperCase(), /*#__PURE__*/React.createElement("span", {
    style: {
      color: accent
    }
  }, acc.toUpperCase()), after.toUpperCase(), "\u201D"), quoteAuthor && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: '2.2cqw',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: '3.5cqw'
    }
  }, "\u2014 ", quoteAuthor.toUpperCase())), caption && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '1.5cqw',
      marginBottom: '2cqw'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '4cqw',
      height: 3,
      background: 'var(--ink)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: '2.8cqw',
      letterSpacing: '0.05em'
    }
  }, caption.toUpperCase())), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 3,
      background: 'var(--ink)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end',
      marginTop: '3.5cqw',
      fontFamily: 'var(--font-display)',
      fontSize: '5.6cqw'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: accent
    }
  }, cur), /*#__PURE__*/React.createElement("span", null, "/", tot)));
}
Object.assign(__ds_scope, { QuoteSlide });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/QuoteSlide.jsx", error: String((e && e.message) || e) }); }

// components/slides/SeriesTag.jsx
try { (() => {
/**
 * SeriesTag — the small filled label pill that names the active series + slide number
 * ("N°1 CE JOUR LÀ …"), drawn in the series' signature color. Absent on Portraits covers
 * (which use a vertical rotated label instead — see CoverSlide).
 */
function SeriesTag({
  label,
  bg = 'var(--sig-cejourla)',
  color = 'var(--ink)'
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size',
      display: 'inline-block'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-block',
      background: bg,
      color,
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 'var(--fs-label-tag)',
      letterSpacing: '0.02em',
      textTransform: 'uppercase',
      padding: '1.4cqw 2.8cqw'
    }
  }, label));
}
Object.assign(__ds_scope, { SeriesTag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/SeriesTag.jsx", error: String((e && e.message) || e) }); }

// components/slides/CoverSlide.jsx
try { (() => {
const SERIES = {
  cejourla: {
    label: 'CE JOUR LÀ …',
    sig: 'var(--sig-cejourla)',
    onSig: 'var(--on-sig-cejourla)',
    grade: 'var(--grade-cejourla)',
    ratio: '3:4'
  },
  oublies: {
    label: 'LES OUBLIÉS',
    sig: 'var(--sig-oublies)',
    onSig: 'var(--on-sig-oublies)',
    grade: 'var(--grade-oublies)',
    ratio: '3:4'
  },
  portraits: {
    label: 'PORTRAITS',
    sig: 'var(--sig-portraits)',
    onSig: 'var(--ink)',
    grade: null,
    ratio: '9:16',
    vertical: true
  },
  arretdejeu: {
    label: "L'ARRÊT DE JEU",
    sig: 'var(--sig-arretdejeu)',
    onSig: 'var(--on-sig-arretdejeu)',
    grade: 'var(--grade-arretdejeu)',
    ratio: '3:4'
  }
};
const RATIO_BOX = {
  '3:4': '3 / 4',
  '4:5': '4 / 5',
  '9:16': '9 / 16',
  '1:1': '1 / 1'
};
function TitleLine({
  text,
  greenWord,
  sig
}) {
  const words = text.trim().split(/\s+/);
  return /*#__PURE__*/React.createElement(React.Fragment, null, words.map((w, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      color: greenWord && w.toUpperCase() === greenWord.toUpperCase() ? sig : 'var(--cream)'
    }
  }, w.toUpperCase(), i < words.length - 1 ? ' ' : '')));
}

/**
 * CoverSlide — the workhorse: opening/interior slide of a carousel (canvas template "A"/"K"/"X",
 * plus the "titre" and "corps" cover variants). Dark photo ground, bottom-up scrim, brand header,
 * series tag, 2-line Anton title with one colored keyword, Archivo body, swipe/pagination footer.
 */
function CoverSlide({
  serie = 'cejourla',
  variant = 'cover',
  // 'cover' | 'titre' | 'corps'
  title = 'TITRE DE LA SLIDE EN DEUX LIGNES',
  greenWord = '',
  body = 'Le sous-titre qui crée le manque.',
  cur = '01',
  tot = '08',
  mediaUrl = '',
  showSwipe = true,
  showPagination = true
}) {
  const s = SERIES[serie] || SERIES.cejourla;
  const isVert = s.ratio === '9:16';
  const noTag = s.vertical;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      containerType: 'inline-size',
      width: '100%',
      aspectRatio: RATIO_BOX[s.ratio],
      position: 'relative',
      overflow: 'hidden',
      background: mediaUrl ? `${'var(--grade-portraits, none)'}` : 'linear-gradient(180deg, #9a968c, #4f4c44)',
      color: 'var(--cream)',
      fontFamily: 'var(--font-body)'
    }
  }, mediaUrl && /*#__PURE__*/React.createElement("img", {
    src: mediaUrl,
    alt: "",
    style: {
      position: 'absolute',
      inset: 0,
      width: '100%',
      height: '100%',
      objectFit: 'cover'
    }
  }), s.grade && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: s.grade
    }
  }), s.vertical && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'var(--grade-portraits)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'var(--scrim-cover)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      padding: isVert ? '13.9cqw 8.9cqw' : '6.1cqw 11.1cqw 5.6cqw 4.6cqw',
      display: 'flex',
      flexDirection: 'column'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.BrandHeader, {
    dark: true,
    handle: "@UNE.DEUX"
  }), !noTag && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: '3cqw'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.SeriesTag, {
    label: s.label,
    bg: s.sig,
    color: s.onSig
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }), variant !== 'corps' ? /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-display-cover-title)',
      lineHeight: 'var(--lh-display)',
      marginBottom: '1.8cqw',
      overflowWrap: 'break-word'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(TitleLine, {
    text: title.split('\n')[0] || title,
    greenWord: greenWord,
    sig: s.sig
  })), title.split('\n')[1] && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(TitleLine, {
    text: title.split('\n')[1],
    greenWord: greenWord,
    sig: s.sig
  }))) : /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-body)',
      fontWeight: 500,
      fontSize: 'var(--fs-body-slide)',
      lineHeight: 'var(--lh-body)',
      color: s.onSig === 'var(--ink)' ? 'var(--ink)' : 'var(--cream)',
      background: 'rgba(194,160,78,0.55)',
      padding: '2cqw 2.4cqw',
      whiteSpace: 'pre-line'
    }
  }, body), variant === 'cover' && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-body)',
      fontWeight: 500,
      fontSize: 'var(--fs-body-slide)',
      lineHeight: 'var(--lh-body)',
      color: 'var(--muted-cream)',
      whiteSpace: 'pre-line'
    }
  }, body), !isVert && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 3,
      background: 'var(--cream)',
      marginTop: '4.3cqw',
      opacity: 0.9
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginTop: '4.2cqw'
    }
  }, showSwipe ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '2.6cqw',
      color: s.sig
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 'var(--fs-label-swipe)'
    }
  }, "SWIPE"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: '7.04cqw',
      height: '7.04cqw',
      borderRadius: '50%',
      background: s.sig,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'var(--cream)',
      fontSize: '3.2cqw'
    }
  }, "\u2192")) : /*#__PURE__*/React.createElement("span", null), showPagination && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-display-pagination)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: s.sig
    }
  }, cur), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--cream)'
    }
  }, "/", tot))))));
}
Object.assign(__ds_scope, { CoverSlide });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/slides/CoverSlide.jsx", error: String((e && e.message) || e) }); }

// components/studio/Chip.jsx
try { (() => {
/** Chip — pill-shaped selectable tag, used for template pickers, green-word/accent pickers. */
function Chip({
  children,
  active = false,
  onClick
}) {
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClick,
    style: {
      display: 'inline-block',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: '12.5px',
      letterSpacing: '0.02em',
      textTransform: 'uppercase',
      padding: '7px 13px',
      borderRadius: 'var(--radius-pill)',
      border: '1px solid ' + (active ? 'var(--sig-cejourla)' : 'var(--border-editor)'),
      background: active ? 'var(--sig-cejourla)' : 'var(--surface-editor-panel)',
      color: active ? 'var(--ink)' : 'var(--cream)',
      cursor: 'pointer',
      userSelect: 'none',
      transition: 'all .15s'
    }
  }, children);
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/studio/Chip.jsx", error: String((e && e.message) || e) }); }

// components/studio/RangeRow.jsx
try { (() => {
/** RangeRow — labeled slider with a live numeric readout (zoom, position, darken, etc). */
function RangeRow({
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  onChange,
  display
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 11,
      marginBottom: 11
    }
  }, /*#__PURE__*/React.createElement("label", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 11,
      letterSpacing: '0.02em',
      textTransform: 'uppercase',
      color: '#9a968c',
      minWidth: 74
    }
  }, label), /*#__PURE__*/React.createElement("input", {
    type: "range",
    min: min,
    max: max,
    step: step,
    value: value,
    onChange: e => onChange && onChange(+e.target.value),
    style: {
      flex: 1,
      accentColor: 'var(--sig-cejourla)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 12,
      color: 'var(--cream)',
      minWidth: 34,
      textAlign: 'right'
    }
  }, display != null ? display : value));
}
Object.assign(__ds_scope, { RangeRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/studio/RangeRow.jsx", error: String((e && e.message) || e) }); }

// components/studio/SerieButton.jsx
try { (() => {
/** SerieButton — one of the 4 cards in the series-picker grid; shows a color dot + name + description. */
function SerieButton({
  name,
  description,
  swatch,
  active = false,
  onClick
}) {
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClick,
    style: {
      position: 'relative',
      textAlign: 'left',
      padding: '12px 13px 11px',
      borderRadius: 'var(--radius-md)',
      cursor: 'pointer',
      background: active ? '#2c2722' : 'var(--surface-editor-panel)',
      border: '1px solid ' + (active ? swatch : 'var(--border-editor)'),
      overflow: 'hidden',
      transition: 'all .18s'
    }
  }, active && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 0,
      top: 0,
      bottom: 0,
      width: 3,
      background: swatch
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 12,
      right: 12,
      width: 11,
      height: 11,
      borderRadius: '50%',
      background: swatch
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 15,
      letterSpacing: '0.02em',
      textTransform: 'uppercase',
      color: active ? swatch : 'var(--cream)',
      lineHeight: 1
    }
  }, name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: '10.5px',
      color: '#8b8678',
      marginTop: 5,
      lineHeight: 1.3
    }
  }, description));
}
Object.assign(__ds_scope, { SerieButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/studio/SerieButton.jsx", error: String((e && e.message) || e) }); }

// components/studio/StudioButton.jsx
try { (() => {
/** StudioButton — the two footer actions in the Studio panel: primary (signature-filled) and ghost. */
function StudioButton({
  children,
  variant = 'primary',
  onClick
}) {
  const primary = variant === 'primary';
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      flex: 1,
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 14,
      letterSpacing: '0.03em',
      textTransform: 'uppercase',
      padding: 13,
      borderRadius: 'var(--radius-md)',
      border: primary ? 'none' : '1px solid var(--border-editor)',
      background: primary ? 'var(--sig-cejourla)' : 'transparent',
      color: primary ? 'var(--ink)' : '#9a9588',
      cursor: 'pointer'
    }
  }, children);
}
Object.assign(__ds_scope, { StudioButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/studio/StudioButton.jsx", error: String((e && e.message) || e) }); }

// components/studio/ToggleSwitch.jsx
try { (() => {
/** ToggleSwitch — labeled on/off row (safe-zone guide, pagination visibility, etc). */
function ToggleSwitch({
  label,
  on = false,
  onChange
}) {
  return /*#__PURE__*/React.createElement("div", {
    onClick: () => onChange && onChange(!on),
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 9,
      cursor: 'pointer',
      userSelect: 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 40,
      height: 22,
      borderRadius: 12,
      background: on ? 'var(--sig-cejourla)' : 'var(--surface-editor-panel)',
      border: '1px solid ' + (on ? 'var(--sig-cejourla)' : 'var(--border-editor)'),
      position: 'relative',
      transition: 'all .15s',
      flex: '0 0 auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 2,
      left: on ? 20 : 2,
      width: 16,
      height: 16,
      borderRadius: '50%',
      background: on ? 'var(--ink)' : '#9a9588',
      transition: 'all .15s'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 12,
      letterSpacing: '0.02em',
      textTransform: 'uppercase',
      color: '#9a968c'
    }
  }, label));
}
Object.assign(__ds_scope, { ToggleSwitch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/studio/ToggleSwitch.jsx", error: String((e && e.message) || e) }); }

// ui_kits/studio/StudioApp.jsx
try { (() => {
const {
  SerieButton,
  Chip,
  RangeRow,
  ToggleSwitch,
  StudioButton,
  CoverSlide,
  QuoteSlide,
  CTASlide
} = window.UneDeuxDesignSystem_8067cc;
const SERIES = {
  cejourla: {
    name: 'Ce jour-là',
    description: 'Éphéméride · carrousel',
    swatch: 'var(--sig-cejourla)',
    onSig: 'var(--on-sig-cejourla)',
    label: 'N°1 · CE JOUR LÀ …',
    ratio: '3:4'
  },
  oublies: {
    name: 'Les oubliés',
    description: 'Injustices · carrousel',
    swatch: 'var(--sig-oublies)',
    onSig: 'var(--on-sig-oublies)',
    label: 'N°1 · LES OUBLIÉS',
    ratio: '3:4'
  },
  portraits: {
    name: 'Portraits',
    description: 'Visages · reel',
    swatch: 'var(--swatch-portraits)',
    onSig: 'var(--ink)',
    label: 'PORTRAITS',
    ratio: '9:16'
  },
  arretdejeu: {
    name: "L'arrêt de jeu",
    description: 'Enquête · carrousel',
    swatch: 'var(--sig-arretdejeu)',
    onSig: 'var(--on-sig-arretdejeu)',
    label: "N°1 · L'ARRÊT DE JEU",
    ratio: '3:4'
  }
};
const TEMPLATES = ['cover', 'titre', 'corps', 'citation', 'cta'];
function StudioApp() {
  const [serie, setSerie] = React.useState('cejourla');
  const [tpl, setTpl] = React.useState('cover');
  const [title, setTitle] = React.useState('28 JUIN 1958 IMAGINE TU AS 17 ANS');
  const [greenWord, setGreenWord] = React.useState('IMAGINE');
  const [body, setBody] = React.useState("Tu t'apprêtes à jouer une demi-finale de Coupe du monde.\nEt à la fin du match…");
  const [cur, setCur] = React.useState('01');
  const [tot, setTot] = React.useState('09');
  const [zoom, setZoom] = React.useState(100);
  const [dark, setDark] = React.useState(78);
  const [safeOn, setSafeOn] = React.useState(true);
  const [quote, setQuote] = React.useState("Sur le terrain, tout s'est joué en deux passes.");
  const [quoteAccent, setQuoteAccent] = React.useState("tout s'est joué en deux passes.");
  const [quoteAuthor, setQuoteAuthor] = React.useState('');
  const [caption, setCaption] = React.useState("L'ANALYSE");
  const [btnlabel, setBtnlabel] = React.useState('ENREGISTRE');
  const s = SERIES[serie];
  const words = [...new Set(title.trim().split(/\s+/).filter(Boolean))];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      minHeight: '100vh',
      background: 'var(--ink)',
      color: 'var(--cream)',
      fontFamily: 'var(--font-body)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 420,
      flex: '0 0 420px',
      padding: '22px 22px 60px',
      borderRight: '1px solid var(--border-editor)',
      overflowY: 'auto',
      maxHeight: '100vh',
      boxSizing: 'border-box'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 11,
      paddingBottom: 16,
      marginBottom: 18,
      borderBottom: '1px solid var(--border-editor)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 30,
      height: 30,
      border: '2px solid var(--cream)',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 14
    }
  }, "1\xB72"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 22
    }
  }, "une", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--sig-oublies)'
    }
  }, "\xB7"), "deux"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 11,
      letterSpacing: '0.1em',
      color: s.swatch
    }
  }, s.name.toUpperCase())), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 8,
      marginBottom: 20
    }
  }, Object.keys(SERIES).map(k => /*#__PURE__*/React.createElement(SerieButton, {
    key: k,
    name: SERIES[k].name,
    description: SERIES[k].description,
    swatch: SERIES[k].swatch,
    active: serie === k,
    onClick: () => setSerie(k)
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 13
    }
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Type de slide"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 7
    }
  }, TEMPLATES.map(t => /*#__PURE__*/React.createElement(Chip, {
    key: t,
    active: tpl === t,
    onClick: () => setTpl(t)
  }, t)))), /*#__PURE__*/React.createElement("div", {
    style: sectionHeadStyle
  }, "Contenu de la cover"), (tpl === 'cover' || tpl === 'titre') && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Titre"), /*#__PURE__*/React.createElement("textarea", {
    value: title,
    onChange: e => setTitle(e.target.value),
    style: textareaStyle
  })), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Mot-cl\xE9 color\xE9"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 7
    }
  }, /*#__PURE__*/React.createElement(Chip, {
    active: greenWord === '',
    onClick: () => setGreenWord('')
  }, "Aucun"), words.map(w => /*#__PURE__*/React.createElement(Chip, {
    key: w,
    active: w.toUpperCase() === greenWord.toUpperCase(),
    onClick: () => setGreenWord(w)
  }, w))))), (tpl === 'cover' || tpl === 'corps') && /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, tpl === 'corps' ? 'Corps (plein cadre)' : 'Sous-titre (corps)'), /*#__PURE__*/React.createElement("textarea", {
    value: body,
    onChange: e => setBody(e.target.value),
    style: textareaStyle
  })), tpl === 'citation' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Citation"), /*#__PURE__*/React.createElement("textarea", {
    value: quote,
    onChange: e => setQuote(e.target.value),
    style: textareaStyle
  })), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Segment color\xE9"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 7
    }
  }, /*#__PURE__*/React.createElement(Chip, {
    active: !quoteAccent,
    onClick: () => setQuoteAccent('')
  }, "Aucun"), [...new Set(quote.trim().split(/\s+/).filter(Boolean))].map(w => /*#__PURE__*/React.createElement(Chip, {
    key: w,
    active: quoteAccent.trim().toLowerCase() === w.toLowerCase(),
    onClick: () => setQuoteAccent(w)
  }, w)))), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Auteur"), /*#__PURE__*/React.createElement("input", {
    value: quoteAuthor,
    onChange: e => setQuoteAuthor(e.target.value),
    style: inputStyle,
    placeholder: "Ex : Zin\xE9dine Zidane"
  })), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "L\xE9gende bas"), /*#__PURE__*/React.createElement("input", {
    value: caption,
    onChange: e => setCaption(e.target.value),
    style: inputStyle
  }))), tpl === 'cta' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Titre"), /*#__PURE__*/React.createElement("textarea", {
    value: title,
    onChange: e => setTitle(e.target.value),
    style: textareaStyle
  })), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Sous-titre"), /*#__PURE__*/React.createElement("textarea", {
    value: body,
    onChange: e => setBody(e.target.value),
    style: textareaStyle
  })), /*#__PURE__*/React.createElement("div", {
    style: fieldWrapStyle
  }, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Libell\xE9 du bouton"), /*#__PURE__*/React.createElement("input", {
    value: btnlabel,
    onChange: e => setBtnlabel(e.target.value),
    style: inputStyle
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 11,
      marginBottom: 13
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Slide"), /*#__PURE__*/React.createElement("input", {
    value: cur,
    onChange: e => setCur(e.target.value),
    style: inputStyle
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
    style: fieldLabelStyle
  }, "Total"), /*#__PURE__*/React.createElement("input", {
    value: tot,
    onChange: e => setTot(e.target.value),
    style: inputStyle
  }))), /*#__PURE__*/React.createElement("div", {
    style: sectionHeadStyle
  }, "Photo de fond"), /*#__PURE__*/React.createElement("div", {
    style: {
      border: '1px dashed var(--border-editor)',
      borderRadius: 10,
      padding: '18px 14px',
      textAlign: 'center',
      background: 'var(--surface-editor-panel)',
      marginBottom: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 13,
      letterSpacing: '0.03em',
      color: '#9a9588'
    }
  }, "CLIQUE OU GLISSE UNE PHOTO"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: '#776f60',
      marginTop: 5
    }
  }, "aucune image \u2014 d\xE9grad\xE9 par d\xE9faut")), /*#__PURE__*/React.createElement(RangeRow, {
    label: "Zoom",
    value: zoom,
    min: 100,
    max: 260,
    onChange: setZoom,
    display: (zoom / 100).toFixed(1)
  }), /*#__PURE__*/React.createElement(RangeRow, {
    label: "Assombrir",
    value: dark,
    min: 20,
    max: 95,
    onChange: setDark
  }), /*#__PURE__*/React.createElement(ToggleSwitch, {
    label: "Zone s\xFBre Instagram",
    on: safeOn,
    onChange: setSafeOn
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement(StudioButton, null, "Exporter PNG"), /*#__PURE__*/React.createElement(StudioButton, {
    variant: "ghost",
    onClick: () => {
      setZoom(100);
      setDark(78);
    }
  }, "R\xE9init."))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '28px 22px',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      maxWidth: 420,
      display: 'flex',
      justifyContent: 'space-between',
      fontFamily: 'var(--font-label)',
      fontWeight: 700,
      fontSize: 13,
      letterSpacing: '0.06em',
      color: '#8b8678'
    }
  }, /*#__PURE__*/React.createElement("span", null, "APER\xC7U \u2014 ", s.name.toUpperCase()), /*#__PURE__*/React.createElement("span", null, s.ratio)), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 420,
      width: '100%',
      borderRadius: 10,
      overflow: 'hidden',
      background: '#1a1714'
    }
  }, tpl === 'citation' ? /*#__PURE__*/React.createElement(QuoteSlide, {
    quote: quote,
    quoteAccent: quoteAccent,
    quoteAuthor: quoteAuthor,
    caption: caption,
    cur: cur,
    tot: tot
  }) : tpl === 'cta' ? /*#__PURE__*/React.createElement(CTASlide, {
    title: title,
    greenWord: greenWord,
    body: body,
    btnlabel: btnlabel,
    sig: s.swatch,
    onSig: s.onSig
  }) : /*#__PURE__*/React.createElement(CoverSlide, {
    serie: serie,
    variant: tpl,
    title: title,
    greenWord: greenWord,
    body: body,
    cur: cur,
    tot: tot
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      maxWidth: 420,
      fontSize: '11.5px',
      color: '#776f60',
      lineHeight: 1.5,
      textAlign: 'center'
    }
  }, "Recreation for design reference only \u2014 not wired to real export/upload.")));
}
const fieldLabelStyle = {
  display: 'block',
  fontFamily: 'var(--font-label)',
  fontWeight: 700,
  fontSize: 12,
  letterSpacing: '0.02em',
  color: '#9a968c',
  marginBottom: 6,
  textTransform: 'uppercase'
};
const sectionHeadStyle = {
  fontFamily: 'var(--font-label)',
  fontWeight: 700,
  fontSize: 12,
  letterSpacing: '0.1em',
  color: 'var(--sig-cejourla)',
  margin: '22px 0 12px',
  textTransform: 'uppercase'
};
const fieldWrapStyle = {
  marginBottom: 13
};
const inputStyle = {
  width: '100%',
  background: 'var(--surface-editor-panel)',
  border: '1px solid var(--border-editor)',
  borderRadius: 8,
  color: 'var(--cream)',
  fontFamily: 'var(--font-body)',
  fontSize: 15,
  padding: '11px 13px',
  outline: 'none',
  boxSizing: 'border-box'
};
const textareaStyle = {
  ...inputStyle,
  resize: 'vertical',
  minHeight: 60,
  lineHeight: 1.4
};
window.StudioApp = StudioApp;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/studio/StudioApp.jsx", error: String((e && e.message) || e) }); }

__ds_ns.BrandHeader = __ds_scope.BrandHeader;

__ds_ns.BreathSlide = __ds_scope.BreathSlide;

__ds_ns.CTASlide = __ds_scope.CTASlide;

__ds_ns.CoverSlide = __ds_scope.CoverSlide;

__ds_ns.QuoteSlide = __ds_scope.QuoteSlide;

__ds_ns.SeriesTag = __ds_scope.SeriesTag;

__ds_ns.Chip = __ds_scope.Chip;

__ds_ns.RangeRow = __ds_scope.RangeRow;

__ds_ns.SerieButton = __ds_scope.SerieButton;

__ds_ns.StudioButton = __ds_scope.StudioButton;

__ds_ns.ToggleSwitch = __ds_scope.ToggleSwitch;

})();
