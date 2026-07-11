import React from 'react';

/**
 * BreathSlide — the "slide-respiration" (canvas template H). Pure rhythm: no header, no tag,
 * no media — just a short quote (3–6 words) with one accented segment, dead center on ink.
 * Used as a pacing beat between two revelation slides.
 */
export function BreathSlide({ quote = 'Sauf que non.', quoteAccent = 'non.', sig = 'var(--sig-cejourla)' }) {
  const idx = quoteAccent ? quote.toLowerCase().indexOf(quoteAccent.toLowerCase()) : -1;
  const before = idx >= 0 ? quote.slice(0, idx) : quote;
  const accent = idx >= 0 ? quote.slice(idx, idx + quoteAccent.length) : '';
  const after = idx >= 0 ? quote.slice(idx + quoteAccent.length) : '';

  return (
    <div
      style={{
        containerType: 'inline-size',
        width: '100%',
        aspectRatio: '3 / 4',
        background: 'var(--surface-dark)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '10cqw'
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '8cqw',
          lineHeight: 'var(--lh-display)',
          textAlign: 'center',
          color: 'var(--cream)'
        }}
      >
        {before.toUpperCase()}
        <span style={{ color: sig }}>{accent.toUpperCase()}</span>
        {after.toUpperCase()}
      </div>
    </div>
  );
}
