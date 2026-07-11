import React from 'react';

/**
 * BrandHeader — the fixed masthead every une·deux slide opens with:
 * a ring-monogram ("1·2"), the "une·deux" wordmark, and the "@UNE.DEUX" handle,
 * separated from the body of the slide by a single hairline.
 */
export function BrandHeader({ dark = true, ring = '1·2', handle = '@UNE.DEUX' }) {
  const fg = dark ? 'var(--cream)' : 'var(--ink)';
  return (
    <div style={{ containerType: 'inline-size' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '2.4cqw', color: fg }}>
        <div
          style={{
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
          }}
        >
          {ring}
        </div>
        <div style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--fs-display-wordmark)', letterSpacing: '0.01em' }}>
          une·deux
        </div>
        <div
          style={{
            marginLeft: 'auto',
            fontFamily: 'var(--font-label)',
            fontWeight: 600,
            fontSize: 'var(--fs-label-handle)',
            letterSpacing: '0.02em'
          }}
        >
          {handle}
        </div>
      </div>
      <div style={{ height: 2, background: fg, opacity: dark ? 1 : 1, marginTop: '3.7cqw' }} />
    </div>
  );
}
