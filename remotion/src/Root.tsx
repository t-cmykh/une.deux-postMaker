import React from 'react';
import {Composition} from 'remotion';
import {
  HighlightReel,
  HighlightReelProps,
  totalDurationInFrames,
} from './HighlightReel';
import segmentsData from './segments.json';
import trackData from './track.json';

const FPS = 30;

const defaultProps: HighlightReelProps = {
  videoSrc: 'color_source.mp4',
  segments: segmentsData.segments,
  fps: FPS,
  sourceWidth: 2868,
  sourceHeight: 1320,
  track: trackData.keyframes,
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
