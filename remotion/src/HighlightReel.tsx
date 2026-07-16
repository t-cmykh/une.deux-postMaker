import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export type Segment = {start: number; end: number};
export type TrackKeyframe = {t: number; cx: number};

export type HighlightReelProps = {
  videoSrc: string;
  segments: Segment[];
  fps: number;
  sourceWidth: number;
  sourceHeight: number;
  // Optional smoothed horizontal "region of interest" track (cx in 0..1,
  // fraction of source width), indexed by absolute time in the *source*
  // video. When omitted, falls back to a fixed center-crop.
  track?: TrackKeyframe[];
};

export const segmentFrameLengths = (segments: Segment[], fps: number) =>
  segments.map((s) => Math.max(1, Math.round((s.end - s.start) * fps)));

export const totalDurationInFrames = (segments: Segment[], fps: number) =>
  segmentFrameLengths(segments, fps).reduce((a, b) => a + b, 0);

const TrackedSegment: React.FC<{
  videoSrc: string;
  segment: Segment;
  sourceWidth: number;
  sourceHeight: number;
  track?: TrackKeyframe[];
}> = ({videoSrc, segment, sourceWidth, sourceHeight, track}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  const absoluteSourceTime = segment.start + frame / fps;

  const cx =
    track && track.length > 0
      ? interpolate(
          absoluteSourceTime,
          track.map((k) => k.t),
          track.map((k) => k.cx),
          {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
        )
      : 0.5;

  const renderedWidth = (sourceWidth / sourceHeight) * height;
  const maxOffset = Math.max(0, renderedWidth - width);
  const offsetLeft = Math.min(maxOffset, Math.max(0, cx * renderedWidth - width / 2));

  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <OffthreadVideo
        src={staticFile(videoSrc)}
        trimBefore={Math.round(segment.start * fps)}
        trimAfter={Math.round(segment.end * fps)}
        style={{
          position: 'absolute',
          top: 0,
          left: -offsetLeft,
          height,
          width: renderedWidth,
        }}
      />
    </AbsoluteFill>
  );
};

// No text/overlay yet: segments follow the tracked horizontal region of
// interest (or a fixed center-crop if no track is given), one after another.
export const HighlightReel: React.FC<HighlightReelProps> = ({
  videoSrc,
  segments,
  fps,
  sourceWidth,
  sourceHeight,
  track,
}) => {
  const lengths = segmentFrameLengths(segments, fps);
  let cursor = 0;

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {segments.map((seg, i) => {
        const from = cursor;
        const durationInFrames = lengths[i];
        cursor += durationInFrames;
        return (
          <Sequence key={i} from={from} durationInFrames={durationInFrames}>
            <TrackedSegment
              videoSrc={videoSrc}
              segment={seg}
              sourceWidth={sourceWidth}
              sourceHeight={sourceHeight}
              track={track}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
