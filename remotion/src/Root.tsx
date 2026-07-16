import React from 'react';
import {Composition} from 'remotion';
import {
  HighlightReel,
  HighlightReelProps,
  totalDurationInFrames,
} from './HighlightReel';
import segmentsData from './segments.json';

const FPS = 30;

const defaultProps: HighlightReelProps = {
  videoSrc: 'gaetjens_source.mp4',
  segments: segmentsData.segments,
  fps: FPS,
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="HighlightReel"
      component={HighlightReel}
      fps={FPS}
      width={1080}
      height={1920}
      durationInFrames={totalDurationInFrames(defaultProps.segments, FPS)}
      defaultProps={defaultProps}
      calculateMetadata={async ({props}) => ({
        durationInFrames: totalDurationInFrames(props.segments, props.fps),
      })}
    />
  );
};
