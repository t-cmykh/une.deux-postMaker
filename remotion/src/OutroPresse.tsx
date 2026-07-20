import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

// Brand tokens, copied 1:1 from design-system/tokens/*.css and the real
// CTASlide/BrandHeader components (source of truth: editeurs/editeur-series.html).
// Nothing invented — this variation reuses the brand's actual header lockup,
// its one recurring icon (the bookmark), and the "dossier" hatch that L'arrêt
// de jeu already uses to signal football-history enquête framing.
const INK = '#2C2823';
const CREAM = '#EDDCB2';
const MUTED_CREAM = '#D1C1A3';
const ROUILLE = '#A8452B'; // L'arrêt de jeu signature — football "dossier" accent
const FONT_DISPLAY = "'Anton', 'Arial Narrow', sans-serif";
const FONT_LABEL = "'Saira Condensed', system-ui, sans-serif";

const GOOGLE_FONTS_IMPORT =
  "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Saira+Condensed:wght@600;700&display=swap');";

// --hatch-enquete, tinted cream-on-ink, exactly as effects.css defines it.
const HATCH_ENQUETE =
  'repeating-linear-gradient(-45deg, rgba(241,236,225,0.06) 0px, rgba(241,236,225,0.06) 1.5px, transparent 1.5px, transparent 38px)';

const ease = (t: number) => 1 - Math.pow(1 - t, 3);

export type OutroPresseProps = {
  tagline?: string;
  handle?: string;
};

/**
 * OutroPresse — end-card built from the brand's own real parts instead of an
 * invented motif: the fixed BrandHeader lockup, the dossier hatch overprint,
 * and the bookmark glyph (the one true recurring icon) in the rouille
 * "enquête" accent — the same visual signal L'arrêt de jeu already uses for
 * football-history digging. Fade/rise only, matching the one documented
 * brand animation (Ce jour-là's cover-title reveal).
 */
export const OutroPresse: React.FC<OutroPresseProps> = ({
  tagline = 'LE FOOT EN DEUX TOUCHES',
  handle = '@UNE.DEUX',
}) => {
  const frame = useCurrentFrame();

  const headerProgress = ease(interpolate(frame, [0, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const headerY = interpolate(headerProgress, [0, 1], [14, 0]);

  const touch1 = interpolate(frame, [16, 20, 24], [1, 1.22, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const touch2 = interpolate(frame, [24, 28, 32], [1, 1.16, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dotScale = frame < 24 ? touch1 : touch2;

  const hatchOpacity = interpolate(frame, [10, 44], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  const bookmarkProgress = ease(interpolate(frame, [36, 58], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const bookmarkScale = interpolate(bookmarkProgress, [0, 1], [0.85, 1]);

  const tagProgress = ease(interpolate(frame, [54, 72], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const tagY = interpolate(tagProgress, [0, 1], [10, 0]);

  const footerProgress = ease(interpolate(frame, [66, 84], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));

  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <style>{GOOGLE_FONTS_IMPORT}</style>

      {/* dossier hatch overprint, fading in — L'arrêt de jeu's enquête texture */}
      <AbsoluteFill style={{backgroundImage: HATCH_ENQUETE, opacity: hatchOpacity}} />

      <AbsoluteFill style={{padding: 96, boxSizing: 'border-box', display: 'flex', flexDirection: 'column'}}>
        {/* fixed header lockup, identical proportions to BrandHeader */}
        <div
          style={{
            opacity: headerProgress,
            transform: `translateY(${headerY}px)`,
          }}
        >
          <div style={{display: 'flex', alignItems: 'center', gap: 26, color: CREAM}}>
            <div
              style={{
                width: 92,
                height: 92,
                borderRadius: '50%',
                border: `4px solid ${CREAM}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: FONT_LABEL,
                fontWeight: 700,
                fontSize: 38,
                flex: '0 0 auto',
                boxSizing: 'border-box',
              }}
            >
              1·2
            </div>
            <div style={{fontFamily: FONT_DISPLAY, fontSize: 58, letterSpacing: '0.01em', display: 'flex'}}>
              <span>une</span>
              <span style={{color: ROUILLE, display: 'inline-block', transform: `scale(${dotScale})`}}>·</span>
              <span>deux</span>
            </div>
            <div style={{marginLeft: 'auto', fontFamily: FONT_LABEL, fontWeight: 600, fontSize: 32, letterSpacing: '0.02em'}}>
              {handle}
            </div>
          </div>
          <div style={{height: 2, background: CREAM, marginTop: 40}} />
        </div>

        <div style={{flex: 1}} />

        {/* bookmark glyph — the brand's one recurring icon, in the enquête accent */}
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
          <svg
            width={132}
            viewBox="0 0 120 156"
            style={{
              fill: ROUILLE,
              opacity: bookmarkProgress,
              transform: `scale(${bookmarkScale})`,
            }}
          >
            <path d="M14 0h92a14 14 0 0 1 14 14v142L60 98 0 156V14A14 14 0 0 1 14 0Z" />
          </svg>

          <div
            style={{
              opacity: tagProgress,
              transform: `translateY(${tagY}px)`,
              fontFamily: FONT_LABEL,
              fontWeight: 600,
              fontSize: 26,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              color: MUTED_CREAM,
            }}
          >
            {tagline}
          </div>
        </div>

        <div style={{flex: 1}} />

        {/* fixed footer band, mirroring CTASlide's bottom rule + handle */}
        <div style={{opacity: footerProgress}}>
          <div style={{height: 3, background: CREAM, marginBottom: 28}} />
          <div style={{fontFamily: FONT_LABEL, fontWeight: 700, fontSize: 32, color: CREAM}}>{handle}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const OUTRO_PRESSE_DURATION_IN_FRAMES = 120;
