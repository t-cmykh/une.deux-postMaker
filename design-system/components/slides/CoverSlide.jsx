import React from 'react';
import { BrandHeader } from './BrandHeader';
import { SeriesTag } from './SeriesTag';

const SERIES = {
  cejourla:   { label: 'CE JOUR LÀ …', sig: 'var(--sig-cejourla)',   onSig: 'var(--on-sig-cejourla)',   grade: 'var(--grade-cejourla)',   ratio: '3:4' },
  oublies:    { label: 'LES OUBLIÉS',  sig: 'var(--sig-oublies)',    onSig: 'var(--on-sig-oublies)',    grade: 'var(--grade-oublies)',    ratio: '3:4' },
  portraits:  { label: 'PORTRAITS',    sig: 'var(--sig-portraits)',  onSig: 'var(--ink)',                grade: null,                        ratio: '9:16', vertical: true },
  arretdejeu: { label: "L'ARRÊT DE JEU", sig: 'var(--sig-arretdejeu)', onSig: 'var(--on-sig-arretdejeu)', grade: 'var(--grade-arretdejeu)', ratio: '3:4' }
};

const RATIO_BOX = { '3:4': '3 / 4', '4:5': '4 / 5', '9:16': '9 / 16', '1:1': '1 / 1' };

function TitleLine({ text, greenWord, sig }) {
  const words = text.trim().split(/\s+/);
  return (
    <>
      {words.map((w, i) => (
        <span key={i} style={{ color: greenWord && w.toUpperCase() === greenWord.toUpperCase() ? sig : 'var(--cream)' }}>
          {w.toUpperCase()}{i < words.length - 1 ? ' ' : ''}
        </span>
      ))}
    </>
  );
}

/**
 * CoverSlide — the workhorse: opening/interior slide of a carousel (canvas template "A"/"K"/"X",
 * plus the "titre" and "corps" cover variants). Dark photo ground, bottom-up scrim, brand header,
 * series tag, 2-line Anton title with one colored keyword, Archivo body, swipe/pagination footer.
 */
export function CoverSlide({
  serie = 'cejourla',
  variant = 'cover',           // 'cover' | 'titre' | 'corps'
  title = 'TITRE DE LA SLIDE EN DEUX LIGNES',
  greenWord = '',
  body = 'Le sous-titre qui crée le manque.',
  cur = '01',
  tot = '08',
  mediaUrl = '',
  showSwipe = true,
  showPagination = true
}) {
  const s = SERIES[serie] || SERIES.cejourla;
  const isVert = s.ratio === '9:16';
  const noTag = s.vertical;

  return (
    <div
      style={{
        containerType: 'inline-size',
        width: '100%',
        aspectRatio: RATIO_BOX[s.ratio],
        position: 'relative',
        overflow: 'hidden',
        background: mediaUrl
          ? `${'var(--grade-portraits, none)'}`
          : 'linear-gradient(180deg, #9a968c, #4f4c44)',
        color: 'var(--cream)',
        fontFamily: 'var(--font-body)'
      }}
    >
      {mediaUrl && (
        <img
          src={mediaUrl}
          alt=""
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }}
        />
      )}
      {s.grade && <div style={{ position: 'absolute', inset: 0, background: s.grade }} />}
      {s.vertical && <div style={{ position: 'absolute', inset: 0, background: 'var(--grade-portraits)' }} />}
      <div style={{ position: 'absolute', inset: 0, background: 'var(--scrim-cover)' }} />

      <div
        style={{
          position: 'absolute',
          inset: 0,
          padding: isVert ? '13.9cqw 8.9cqw' : '6.1cqw 11.1cqw 5.6cqw 4.6cqw',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <BrandHeader dark handle="@UNE.DEUX" />

        {!noTag && (
          <div style={{ marginTop: '3cqw' }}>
            <SeriesTag label={s.label} bg={s.sig} color={s.onSig} />
          </div>
        )}

        <div style={{ flex: 1 }} />

        {variant !== 'corps' ? (
          <div
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'var(--fs-display-cover-title)',
              lineHeight: 'var(--lh-display)',
              marginBottom: '1.8cqw',
              overflowWrap: 'break-word'
            }}
          >
            <div><TitleLine text={title.split('\n')[0] || title} greenWord={greenWord} sig={s.sig} /></div>
            {title.split('\n')[1] && <div><TitleLine text={title.split('\n')[1]} greenWord={greenWord} sig={s.sig} /></div>}
          </div>
        ) : (
          <div
            style={{
              fontFamily: 'var(--font-body)',
              fontWeight: 500,
              fontSize: 'var(--fs-body-slide)',
              lineHeight: 'var(--lh-body)',
              color: s.onSig === 'var(--ink)' ? 'var(--ink)' : 'var(--cream)',
              background: 'rgba(194,160,78,0.55)',
              padding: '2cqw 2.4cqw',
              whiteSpace: 'pre-line'
            }}
          >
            {body}
          </div>
        )}

        {variant === 'cover' && (
          <div
            style={{
              fontFamily: 'var(--font-body)',
              fontWeight: 500,
              fontSize: 'var(--fs-body-slide)',
              lineHeight: 'var(--lh-body)',
              color: 'var(--muted-cream)',
              whiteSpace: 'pre-line'
            }}
          >
            {body}
          </div>
        )}

        {!isVert && (
          <>
            <div style={{ height: 3, background: 'var(--cream)', marginTop: '4.3cqw', opacity: 0.9 }} />
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '4.2cqw' }}>
              {showSwipe ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '2.6cqw', color: s.sig }}>
                  <span style={{ fontFamily: 'var(--font-label)', fontWeight: 700, fontSize: 'var(--fs-label-swipe)' }}>SWIPE</span>
                  <div
                    style={{
                      width: '7.04cqw',
                      height: '7.04cqw',
                      borderRadius: '50%',
                      background: s.sig,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'var(--cream)',
                      fontSize: '3.2cqw'
                    }}
                  >
                    →
                  </div>
                </div>
              ) : <span />}
              {showPagination && (
                <div style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--fs-display-pagination)' }}>
                  <span style={{ color: s.sig }}>{cur}</span>
                  <span style={{ color: 'var(--cream)' }}>/{tot}</span>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
