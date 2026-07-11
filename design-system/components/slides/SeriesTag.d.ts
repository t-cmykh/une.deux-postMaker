export interface SeriesTagProps {
  /** Tag text, e.g. "N°1 CE JOUR LÀ …". Auto-generated from series + slide number in the real tool. */
  label: string;
  /** Fill color — pass one of the --sig-* series tokens. */
  bg?: string;
  /** Text color — ink on ocre/cream tags, cream on vert/rouille tags. */
  color?: string;
}
