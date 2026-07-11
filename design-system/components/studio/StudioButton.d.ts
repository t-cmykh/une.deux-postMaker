export interface StudioButtonProps {
  children?: any;
  /** 'primary' = filled with the signature color (Exporter). 'ghost' = outlined (Réinit.). Default 'primary'. */
  variant?: 'primary' | 'ghost';
  onClick?: () => void;
}
