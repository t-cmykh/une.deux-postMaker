export type ReelSlide = {
  file: string;
  durationInFrames: number;
  enterFrom: 'left' | 'right';
};

export const REEL_FPS = 30;
export const TRANSITION_FRAMES = 24;

// Order matches the carousel: cover, context, Mediapro, CVC, quote, TV rights
// collapse, Bordeaux/Lyon. Durations are longer on paragraph-heavy slides so
// there's time to actually read them.
export const reelSlides: ReelSlide[] = [
  {file: '01-cover.png', durationInFrames: 180, enterFrom: 'left'},
  {file: '02-bordeaux-exception.png', durationInFrames: 330, enterFrom: 'right'},
  {file: '03-mediapro.png', durationInFrames: 330, enterFrom: 'left'},
  {file: '04-cvc.png', durationInFrames: 330, enterFrom: 'right'},
  {file: '05-quote-labrune.png', durationInFrames: 210, enterFrom: 'left'},
  {file: '06-droits-tv-chute.png', durationInFrames: 330, enterFrom: 'right'},
  {file: '07-bordeaux-lyon.png', durationInFrames: 300, enterFrom: 'left'},
];

export const reelTotalDurationInFrames = () =>
  reelSlides.reduce((sum, s) => sum + s.durationInFrames, 0) -
  TRANSITION_FRAMES * (reelSlides.length - 1);
