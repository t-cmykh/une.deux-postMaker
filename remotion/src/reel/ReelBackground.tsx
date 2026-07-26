import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

const HATCH_ON_CREAM =
  'repeating-linear-gradient(-45deg, rgba(44,40,35,0.06) 0px, rgba(44,40,35,0.06) 2px, transparent 2px, transparent 46px)';

const INK = '#2C2823';
const ROUILLE = '#A8452B';
const CREAM = '#EDDCB2';

// Brand-only backdrop that sits behind every slide: the same diagonal hatch
// used on the cream slides (drifting slowly for a bit of life) plus a soft
// rouille ribbon that keeps sweeping across, echoing the swoosh motion from
// the reference reel without borrowing any of its actual colors/shapes.
export const ReelBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const hatchShift = (frame * 0.35) % 46;

  const ribbonLoopFrames = 260;
  const ribbonProgress = (frame % ribbonLoopFrames) / ribbonLoopFrames;
  const ribbonOffset = ribbonProgress * 2600 - 900;

  const arcSpin = (frame / durationInFrames) * 40;

  return (
    <AbsoluteFill style={{backgroundColor: CREAM, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          backgroundImage: HATCH_ON_CREAM,
          backgroundPosition: `${hatchShift}px ${hatchShift}px`,
        }}
      />

      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1080 1920"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          transform: `rotate(${arcSpin}deg)`,
          transformOrigin: '1080px 0px',
        }}
      >
        {Array.from({length: 9}).map((_, i) => (
          <circle
            key={i}
            cx={1080}
            cy={0}
            r={220 + i * 130}
            fill="none"
            stroke={INK}
            strokeOpacity={0.07}
            strokeWidth={2}
          />
        ))}
      </svg>

      <div
        style={{
          position: 'absolute',
          top: -400,
          left: ribbonOffset,
          width: 340,
          height: 2700,
          background: `linear-gradient(90deg, transparent, ${ROUILLE}22 35%, ${ROUILLE}33 50%, ${ROUILLE}22 65%, transparent)`,
          transform: 'rotate(18deg)',
        }}
      />
    </AbsoluteFill>
  );
};
