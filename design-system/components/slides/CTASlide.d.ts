export interface CTASlideProps {
  /** Always 2 short lines, e.g. "RESTE DANS LE JEU". */
  title?: string;
  /** Word/segment of `title` to render in the signature color. Optional. */
  greenWord?: string;
  /** One-line subtitle under the title. */
  body?: string;
  /** Action chip label. The source product hard-locks this to "FOLLOW" — only "ENREGISTRE" is used as a fallback default. */
  btnlabel?: string;
  /** Series signature color driving the bookmark + chip. */
  sig?: string;
  /** Text color that sits on `sig` (ink for ocre bg, cream for vert/rouille bg). */
  onSig?: string;
}
