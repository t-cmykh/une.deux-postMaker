import React from 'react';
import { BrandHeader } from './BrandHeader';

/**
 * CTASlide — the final "follow / save" slide (canvas templates "D"/"S"). Cream ground with the
 * diagonal hatch, a bookmark glyph in the series signature color, a labeled action chip,
 * centered 2-line title with one colored keyword, and a subtitle.
 */
export function CTASlide({
  title = 'RESTE DANS LE JEU',
  greenWord = '',
  body = 'Le foot en deux touches, tous les jours.',
  btnlabel = 'FOLLOW',
  sig = 'var(--sig-cejourla)',
  onSig = 'var(--on-sig-cejourla)'
}) {
  const words = title.trim().split(/\s+/);
  return (
    <div
      style={{
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
      }}
    >
      <div style={{ alignSelf: 'stretch' }}>
        <BrandHeader dark={false} handle="@UNE.DEUX" />
      </div>

      <div style={{ flex: 1 }} />

      {/* bookmark glyph */}
      <svg width="14%" viewBox="0 0 120 156" style={{ fill: sig }}>
        <path d="M14 0h92a14 14 0 0 1 14 14v142L60 98 0 156V14A14 14 0 0 1 14 0Z" />
      </svg>

      <div
        style={{
          marginTop: '3.7cqw',
          background: sig,
          color: onSig,
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: '3.15cqw',
          letterSpacing: '0.03em',
          padding: '1.5cqw 3cqw'
        }}
      >
        {btnlabel.toUpperCase()}
      </div>

      <div
        style={{
          marginTop: '2.8cqw',
          fontFamily: 'var(--font-display)',
          fontSize: 'var(--fs-display-cta-title)',
          lineHeight: 'var(--lh-display)',
          overflowWrap: 'break-word'
        }}
      >
        {words.map((w, i) => (
          <span key={i} style={{ color: greenWord && w.toUpperCase() === greenWord.toUpperCase() ? sig : 'var(--ink)' }}>
            {w.toUpperCase()}{i < words.length - 1 ? ' ' : ''}
          </span>
        ))}
      </div>

      <div style={{ marginTop: '2.2cqw', fontFamily: 'var(--font-body)', fontSize: '3.7cqw', maxWidth: '86%' }}>
        {body}
      </div>

      <div style={{ flex: 1 }} />
      <div style={{ alignSelf: 'stretch', height: 3, background: 'var(--ink)', marginBottom: '2.8cqw' }} />
      <div style={{ alignSelf: 'flex-start', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: '2.96cqw' }}>
        @UNE.DEUX
      </div>
    </div>
  );
}
