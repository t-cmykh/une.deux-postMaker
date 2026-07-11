import React from 'react';

/** RangeRow — labeled slider with a live numeric readout (zoom, position, darken, etc). */
export function RangeRow({ label, value, min = 0, max = 100, step = 1, onChange, display }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 11, marginBottom: 11 }}>
      <label
        style={{
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: 11,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          color: '#9a968c',
          minWidth: 74
        }}
      >
        {label}
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange && onChange(+e.target.value)}
        style={{ flex: 1, accentColor: 'var(--sig-cejourla)' }}
      />
      <span
        style={{
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: 12,
          color: 'var(--cream)',
          minWidth: 34,
          textAlign: 'right'
        }}
      >
        {display != null ? display : value}
      </span>
    </div>
  );
}
