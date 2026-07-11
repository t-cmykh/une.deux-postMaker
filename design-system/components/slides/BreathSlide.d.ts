export interface BreathSlideProps {
  /** Short phrase, 3–6 words. Whole quote renders in Anton, all caps. */
  quote?: string;
  /** Must match a substring of `quote` verbatim — renders in the signature color. */
  quoteAccent?: string;
  /** Pass the active series' --sig-* token. */
  sig?: string;
}
