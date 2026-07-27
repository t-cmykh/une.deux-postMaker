import React from 'react';
import {BrandHeader} from './BrandHeader';

export interface QuoteSlideProps {
  quote?: string;
  quoteAccent?: string;
  quoteAuthor?: string;
  caption?: string;
  cur?: string;
  tot?: string;
  accent?: string;
}

/**
 * Ported verbatim from design-system/components/slides/QuoteSlide.jsx (canvas template "G").
 */
export function QuoteSlide({
  quote = 'Sur le terrain, tout s’est joué en deux passes.',
  quoteAccent = "tout s'est joué en deux passes.",
  quoteAuthor = '',
  caption = "L'ANALYSE",
  cur = '05',
  tot = '08',
  accent = 'var(--vert)',
}: QuoteSlideProps) {
  const idx = quoteAccent ? quote.toLowerCase().indexOf(quoteAccent.toLowerCase()) : -1;
  const before = idx >= 0 ? quote.slice(0, idx) : quote;
  const acc = idx >= 0 ? quote.slice(idx, idx + quoteAccent.length) : '';
  const after = idx >= 0 ? quote.slice(idx + quoteAccent.length) : '';

  return (
    <div
      style={{
        containerType: 'inline-size',
        width: '100%',
        height: '100%',
        aspectRatio: '3 / 4',
        position: 'relative',
        background: 'var(--surface-light)',
        backgroundImage: 'var(--hatch-on-cream-faint)',
        color: 'var(--ink)',
        display: 'flex',
        flexDirection: 'column',
        padding: '6.1cqw 11.1cqw 6.5cqw 4.6cqw',
        boxSizing: 'border-box',
      }}
    >
      <BrandHeader dark={false} handle="@UNE.DEUX" />

      <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <div style={{fontFamily: 'var(--font-display)', fontSize: 'var(--fs-display-quote)', lineHeight: 'var(--lh-display)'}}>
          &ldquo;{before.toUpperCase()}
          <span style={{color: accent}}>{acc.toUpperCase()}</span>
          {after.toUpperCase()}&rdquo;
        </div>
        {quoteAuthor && (
          <div style={{marginTop: '2.2cqw', fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: '3.5cqw'}}>
            — {quoteAuthor.toUpperCase()}
          </div>
        )}
      </div>

      {caption && (
        <div style={{display: 'flex', alignItems: 'center', gap: '1.5cqw', marginBottom: '2cqw'}}>
          <div style={{width: '4cqw', height: 3, background: 'var(--ink)'}} />
          <div style={{fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: '2.8cqw', letterSpacing: '0.05em'}}>
            {caption.toUpperCase()}
          </div>
        </div>
      )}

      <div style={{height: 3, background: 'var(--ink)'}} />
      <div style={{display: 'flex', justifyContent: 'flex-end', marginTop: '3.5cqw', fontFamily: 'var(--font-display)', fontSize: '5.6cqw'}}>
        <span style={{color: accent}}>{cur}</span>
        <span>/{tot}</span>
      </div>
    </div>
  );
}
