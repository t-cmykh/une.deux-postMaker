import React from 'react';
import {AbsoluteFill} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {ReelBackground} from './reel/ReelBackground';
import {SlideCard} from './reel/SlideCard';
import {reelSlides, TRANSITION_FRAMES} from './reel/slides';

export const InstagramReel: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#EDDCB2'}}>
      <ReelBackground />
      <TransitionSeries>
        {reelSlides.map((slide_, i) => {
          const next = reelSlides[i + 1];
          return (
            <React.Fragment key={slide_.file}>
              <TransitionSeries.Sequence durationInFrames={slide_.durationInFrames}>
                <SlideCard
                  file={slide_.file}
                  enterFrom={slide_.enterFrom}
                  durationInFrames={slide_.durationInFrames}
                />
              </TransitionSeries.Sequence>
              {next && (
                <TransitionSeries.Transition
                  presentation={slide({direction: next.enterFrom === 'left' ? 'from-left' : 'from-right'})}
                  timing={linearTiming({durationInFrames: TRANSITION_FRAMES})}
                />
              )}
            </React.Fragment>
          );
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
