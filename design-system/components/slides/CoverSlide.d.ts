/** Which of the 4 signature series drives color, photo grade, and locked aspect ratio. */
export type UneDeuxSerie = 'cejourla' | 'oublies' | 'portraits' | 'arretdejeu';

export interface CoverSlideProps {
  /** Locks color, photo grade, and (in the real tool) the ratio. Default 'cejourla'. */
  serie?: UneDeuxSerie;
  /** 'cover' = title + body (the opening hook slide). 'titre' = title only, larger. 'corps' = body only, full-frame (used by L'arrêt de jeu). */
  variant?: 'cover' | 'titre' | 'corps';
  /** ALWAYS UPPERCASE in the real tool; pass 2 lines separated by \n. */
  title?: string;
  /** Must match one word/segment verbatim from `title` — that word renders in the series signature color. */
  greenWord?: string;
  /** Sub-title (cover) or interior body copy. `**bold**` markers are supported by the source tool; keep plain here. */
  body?: string;
  /** Current slide number, e.g. "01". */
  cur?: string;
  /** Total slide count, e.g. "08". */
  tot?: string;
  /** Background photo URL. Leave empty to show the neutral gradient placeholder. */
  mediaUrl?: string;
  /** Shows "SWIPE →" bottom-left. Hidden automatically on 9:16. Default true. */
  showSwipe?: boolean;
  /** Shows "01/08" pagination bottom-right. Hidden automatically on 9:16. Default true. */
  showPagination?: boolean;
}
