import React from 'react';

/**
 * SeriesTag — the small filled label pill that names the active series + slide number
 * ("N°1 CE JOUR LÀ …"), drawn in the series' signature color. Absent on Portraits covers
 * (which use a vertical rotated label instead — see CoverSlide).
 */
export function SeriesTag({ label, bg = 'var(--sig-cejourla)', color = 'var(--ink)' }) {
  return (
    <div style={{ containerType: 'inline-size', display: 'inline-block' }}>
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
          padding: '1.4cqw 2.8cqw'
        }}
      >
        {label}
      </div>
    </div>
  );
}
