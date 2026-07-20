import React from 'react';
import {Composition} from 'remotion';
import {
  HighlightReel,
  HighlightReelProps,
  totalDurationInFrames,
} from './HighlightReel';
import {Outro, OUTRO_DURATION_IN_FRAMES} from './Outro';
import {OutroPresse, OUTRO_PRESSE_DURATION_IN_FRAMES} from './OutroPresse';
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
    <>
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
    <Composition
      id="Outro"
      component={Outro}
      fps={FPS}
      width={1080}
      height={1920}
      durationInFrames={OUTRO_DURATION_IN_FRAMES}
      defaultProps={{
        tagline: 'LE FOOT EN DEUX TOUCHES',
        handle: '@UNE.DEUX',
      }}
    />
    <Composition
      id="OutroPresse"
      component={OutroPresse}
      fps={FPS}
      width={1080}
      height={1920}
      durationInFrames={OUTRO_PRESSE_DURATION_IN_FRAMES}
      defaultProps={{
        tagline: 'LE FOOT EN DEUX TOUCHES',
        handle: '@UNE.DEUX',
      }}
    />
    </>
  );
};
