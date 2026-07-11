import React from 'react';

/** Chip — pill-shaped selectable tag, used for template pickers, green-word/accent pickers. */
export function Chip({ children, active = false, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
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
      }}
    >
      {children}
    </div>
  );
}
