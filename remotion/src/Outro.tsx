import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

// Brand tokens, copied 1:1 from design-system/tokens/*.css (source of truth:
// t-cmykh/une.deux-postMaker editeurs/editeur-series.html). No new colors invented.
const INK = '#2C2823';
const CREAM = '#EDDCB2';
const VERT = '#27543C';
const FONT_DISPLAY = "'Anton', 'Arial Narrow', sans-serif";
const FONT_LABEL = "'Saira Condensed', system-ui, sans-serif";

const GOOGLE_FONTS_IMPORT =
  "@import url('https://fonts.googleapis.com/css2?family=Anton&family=Saira+Condensed:wght@600;700&display=swap');";

const ease = (t: number) => 1 - Math.pow(1 - t, 3); // cubic ease-out, no overshoot

export type OutroProps = {
  tagline?: string;
  handle?: string;
};

/**
 * Outro — end-card motion design: the ring monogram + wordmark drawn as a
 * football pitch diagram (center circle sitting on the halfway line), the
 * "·" between "une" and "deux" popping twice like a ball's two touches,
 * then the handle/tagline settling underneath. Sober, no bounce/blur/shadow
 * beyond what the brand already uses elsewhere.
 */
export const Outro: React.FC<OutroProps> = ({
  tagline = 'LE FOOT EN DEUX TOUCHES',
  handle = '@UNE.DEUX',
}) => {
  const frame = useCurrentFrame();

  // Phase 1 — halfway line draws outward from center.
  const lineProgress = ease(interpolate(frame, [0, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));

  // Phase 2 — ring "kicks off": scales/fades in on top of the line.
  const ringProgress = ease(interpolate(frame, [8, 28], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const ringScale = interpolate(ringProgress, [0, 1], [0.72, 1]);

  // Phase 3 — wordmark rises + fades in underneath.
  const wordProgress = ease(interpolate(frame, [26, 46], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const wordY = interpolate(wordProgress, [0, 1], [16, 0]);

  // Phase 4 — the middot "kicks" twice, like the ball's two touches.
  const touch1 = interpolate(frame, [44, 48, 52], [1, 1.22, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const touch2 = interpolate(frame, [52, 56, 60], [1, 1.16, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dotScale = frame < 52 ? touch1 : touch2;

  // Phase 5 — handle + tagline settle in.
  const footerProgress = ease(interpolate(frame, [58, 76], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const footerY = interpolate(footerProgress, [0, 1], [12, 0]);

  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <style>{GOOGLE_FONTS_IMPORT}</style>
      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
        }}
      >
        {/* halfway line + center circle, drawn like a pitch diagram */}
        <div style={{position: 'relative', width: 560, height: 168, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div
            style={{
              position: 'absolute',
              left: '50%',
              top: '50%',
              width: `${lineProgress * 560}px`,
              height: 2,
              background: CREAM,
              transform: 'translate(-50%, -50%)',
            }}
          />
          <div
            style={{
              width: 168,
              height: 168,
              borderRadius: '50%',
              border: `3px solid ${CREAM}`,
              background: INK,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: ringProgress,
              transform: `scale(${ringScale})`,
              fontFamily: FONT_LABEL,
              fontWeight: 700,
              fontSize: 44,
              color: CREAM,
            }}
          >
            1·2
          </div>
        </div>

        {/* wordmark */}
        <div
          style={{
            marginTop: 56,
            opacity: wordProgress,
            transform: `translateY(${wordY}px)`,
            fontFamily: FONT_DISPLAY,
            fontSize: 108,
            letterSpacing: '0.01em',
            color: CREAM,
            display: 'flex',
          }}
        >
          <span>une</span>
          <span style={{color: VERT, display: 'inline-block', transform: `scale(${dotScale})`}}>·</span>
          <span>deux</span>
        </div>

        {/* handle + tagline */}
        <div
          style={{
            marginTop: 40,
            opacity: footerProgress,
            transform: `translateY(${footerY}px)`,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 10,
            fontFamily: FONT_LABEL,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: CREAM,
          }}
        >
          <div style={{fontWeight: 700, fontSize: 30}}>{handle}</div>
          <div style={{fontWeight: 600, fontSize: 22, color: '#D1C1A3'}}>{tagline}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const OUTRO_DURATION_IN_FRAMES = 120;
