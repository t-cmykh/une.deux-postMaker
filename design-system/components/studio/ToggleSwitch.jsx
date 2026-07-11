import React from 'react';

/** ToggleSwitch — labeled on/off row (safe-zone guide, pagination visibility, etc). */
export function ToggleSwitch({ label, on = false, onChange }) {
  return (
    <div
      onClick={() => onChange && onChange(!on)}
      style={{ display: 'flex', alignItems: 'center', gap: 9, cursor: 'pointer', userSelect: 'none' }}
    >
      <div
        style={{
          width: 40,
          height: 22,
          borderRadius: 12,
          background: on ? 'var(--sig-cejourla)' : 'var(--surface-editor-panel)',
          border: '1px solid ' + (on ? 'var(--sig-cejourla)' : 'var(--border-editor)'),
          position: 'relative',
          transition: 'all .15s',
          flex: '0 0 auto'
        }}
      >
        <div
          style={{
            position: 'absolute',
            top: 2,
            left: on ? 20 : 2,
            width: 16,
            height: 16,
            borderRadius: '50%',
            background: on ? 'var(--ink)' : '#9a9588',
            transition: 'all .15s'
          }}
        />
      </div>
      <span
        style={{
          fontFamily: 'var(--font-label)',
          fontWeight: 700,
          fontSize: 12,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          color: '#9a968c'
        }}
      >
        {label}
      </span>
    </div>
  );
}
