import React from 'react';

/** StudioButton — the two footer actions in the Studio panel: primary (signature-filled) and ghost. */
export function StudioButton({ children, variant = 'primary', onClick }) {
  const primary = variant === 'primary';
  return (
    <button
      onClick={onClick}
      style={{
        flex: 1,
        fontFamily: 'var(--font-label)',
        fontWeight: 700,
        fontSize: 14,
        letterSpacing: '0.03em',
        textTransform: 'uppercase',
        padding: 13,
        borderRadius: 'var(--radius-md)',
        border: primary ? 'none' : '1px solid var(--border-editor)',
        background: primary ? 'var(--sig-cejourla)' : 'transparent',
        color: primary ? 'var(--ink)' : '#9a9588',
        cursor: 'pointer'
      }}
    >
      {children}
    </button>
  );
}
