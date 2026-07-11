export interface SerieButtonProps {
  /** Series display name, e.g. "Ce jour-là". */
  name: string;
  /** Short descriptor, e.g. "Éphéméride · carrousel". */
  description: string;
  /** The series' swatch color — pass --sig-* (or --swatch-portraits for Portraits). */
  swatch: string;
  active?: boolean;
  onClick?: () => void;
}
