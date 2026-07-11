export interface QuoteSlideProps {
  /** The verbatim, fact-checked quotation. */
  quote?: string;
  /** Substring of `quote` to render in the accent color. */
  quoteAccent?: string;
  /** Byline, e.g. "Zinédine Zidane". Leave empty to hide. */
  quoteAuthor?: string;
  /** Bottom caption chip, e.g. "L'AVEU", "LA PROMESSE", "L'ANALYSE". */
  caption?: string;
  cur?: string;
  tot?: string;
  /** Accent color for the highlighted quote segment + current-page number. Defaults to Les oubliés' vert (the source's fixed choice for this template). */
  accent?: string;
}
