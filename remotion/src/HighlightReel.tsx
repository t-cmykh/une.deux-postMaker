import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile} from 'remotion';

export type Segment = {start: number; end: number};

export type HighlightReelProps = {
  videoSrc: string;
  segments: Segment[];
  fps: number;
};

export const segmentFrameLengths = (segments: Segment[], fps: number) =>
  segments.map((s) => Math.max(1, Math.round((s.end - s.start) * fps)));

export const totalDurationInFrames = (segments: Segment[], fps: number) =>
  segmentFrameLengths(segments, fps).reduce((a, b) => a + b, 0);

// No overlay/text yet: just a straight center-crop of the 16:9 source into
// a 9:16 canvas, one segment after another.
export const HighlightReel: React.FC<HighlightReelProps> = ({
  videoSrc,
  segments,
  fps,
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
            <AbsoluteFill style={{overflow: 'hidden'}}>
              <OffthreadVideo
                src={staticFile(videoSrc)}
                trimBefore={Math.round(seg.start * fps)}
                trimAfter={Math.round(seg.end * fps)}
                style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  height: '100%',
                  width: 'auto',
                  transform: 'translate(-50%, -50%)',
                }}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
