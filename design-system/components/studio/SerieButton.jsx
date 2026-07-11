import React from 'react';

/** SerieButton — one of the 4 cards in the series-picker grid; shows a color dot + name + description. */
export function SerieButton({ name, description, swatch, active = false, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
        position: 'relative',
        textAlign: 'left',
        padding: '12px 13px 11px',
        borderRadius: 'var(--radius-md)',
        cursor: 'pointer',
        background: active ? '#2c2722' : 'var(--surface-editor-panel)',
        border: '1px solid ' + (active ? swatch : 'var(--border-editor)'),
        overflow: 'hidden',
        transition: 'all .18s'
      }}
    >
      {active && <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: 3, background: swatch }} />}
      <div style={{ position: 'absolute', top: 12, right: 12, width: 11, height: 11, borderRadius: '50%', background: swatch }} />
      <div
        style={{
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: 15,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          color: active ? swatch : 'var(--cream)',
          lineHeight: 1
        }}
      >
        {name}
      </div>
      <div style={{ fontSize: '10.5px', color: '#8b8678', marginTop: 5, lineHeight: 1.3 }}>{description}</div>
    </div>
  );
}
