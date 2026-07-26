import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';

const MARGIN_X = 56;
const CARD_ASPECT = 3 / 4; // slides are 1080x1440 (width / height)

export const SlideCard: React.FC<{
  file: string;
  enterFrom: 'left' | 'right';
  durationInFrames: number;
}> = ({file, enterFrom, durationInFrames}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const settleScale = interpolate(frame, [0, 16], [0.96, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  const settleRotate = interpolate(frame, [0, 16], [enterFrom === 'left' ? -3 : 3, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  const kenBurnsScale = interpolate(frame, [0, Math.max(durationInFrames - 1, 1)], [1, 1.045]);

  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div
        style={{
          width: `calc(100% - ${MARGIN_X * 2}px)`,
          aspectRatio: `${CARD_ASPECT}`,
          borderRadius: 22,
          overflow: 'hidden',
          boxShadow: '0 40px 80px rgba(44,40,35,0.35), 0 10px 24px rgba(44,40,35,0.25)',
          opacity,
          transform: `scale(${settleScale * kenBurnsScale}) rotate(${settleRotate}deg)`,
        }}
      >
        <Img
          src={staticFile(`slides/${file}`)}
          style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}}
        />
      </div>
    </AbsoluteFill>
  );
};
