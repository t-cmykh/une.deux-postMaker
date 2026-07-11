export interface RangeRowProps {
  label: string;
  value: number;
  min?: number;
  max?: number;
  step?: number;
  onChange?: (next: number) => void;
  /** Override the raw value's display text, e.g. "1.4×". */
  display?: string;
}
