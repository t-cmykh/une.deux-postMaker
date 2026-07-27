import React from 'react';

export interface SeriesTagProps {
  label: string;
  bg?: string;
  color?: string;
}

/**
 * Ported verbatim from design-system/components/slides/SeriesTag.jsx.
 */
export function SeriesTag({label, bg = 'var(--sig-cejourla)', color = 'var(--ink)'}: SeriesTagProps) {
  return (
    <div style={{display: 'inline-block'}}>
      <div
        style={{
          display: 'inline-block',
          background: bg,
          color,
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: 'var(--fs-label-tag)',
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          padding: '1.4cqw 2.8cqw',
        }}
      >
        {label}
      </div>
    </div>
  );
}
