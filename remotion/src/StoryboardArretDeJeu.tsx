import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {BrandFonts} from './brand/Theme';
import {CoverSlide} from './brand/CoverSlide';
import {BreathSlide} from './brand/BreathSlide';
import {QuoteSlide} from './brand/QuoteSlide';
import {CTASlide} from './brand/CTASlide';

export const FPS = 30;
const TOT = '17';

type Scene =
  | {kind: 'cover'; seconds: number; cur: string; props: React.ComponentProps<typeof CoverSlide>}
  | {kind: 'breath'; seconds: number; props: React.ComponentProps<typeof BreathSlide>}
  | {kind: 'quote'; seconds: number; cur: string; props: React.ComponentProps<typeof QuoteSlide>}
  | {kind: 'cta'; seconds: number; props: React.ComponentProps<typeof CTASlide>};

/**
 * Scene-by-scene prototype of the "Les clubs-états ont-ils cassé l'équité
 * sportive du foot ?" storyboard, restyled with L'arrêt de jeu's locked DA
 * (rust/rouille signature, enquête photo grade + dossier hatch, 3:4 ratio) —
 * reusing the design-system's CoverSlide/BreathSlide/QuoteSlide/CTASlide
 * components as-is.
 */
export const SCENES: Scene[] = [
  {
    kind: 'cover',
    seconds: 7,
    cur: '01',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '11 TITRES\nSUR 13',
      greenWord: '11',
      body: 'Depuis le rachat qatari de 2011.',
      cur: '01',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'breath',
    seconds: 6,
    props: {quote: 'DEUX. EN UN SIÈCLE.', quoteAccent: 'EN UN SIÈCLE.', sig: 'var(--sig-arretdejeu)'},
  },
  {
    kind: 'cover',
    seconds: 7,
    cur: '03',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '8 TITRES\nPREMIER LEAGUE',
      greenWord: '8',
      body: "Manchester City, racheté par Abu Dhabi en 2008.",
      cur: '03',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'breath',
    seconds: 4,
    props: {quote: 'DU. JAMAIS. VU.', quoteAccent: 'JAMAIS.', sig: 'var(--sig-arretdejeu)'},
  },
  {
    kind: 'cover',
    seconds: 8,
    cur: '05',
    props: {
      serie: 'arretdejeu',
      variant: 'corps',
      body:
        "Un club classique vit de sa billetterie, ses droits TV, ses sponsors.\nUn club-État peut signer avec des entités liées à cet État, à des montants qu'aucun investisseur ne proposerait.",
      cur: '05',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 7,
    cur: '06',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '200M€\nRÉDUITS DE MOITIÉ',
      greenWord: '200M€',
      body: "Le sponsoring qatari du PSG, ramené à 100M€ par l'UEFA en 2014.",
      cur: '06',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 7,
    cur: '07',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '222M€\nPOUR NEYMAR',
      greenWord: '222M€',
      body: "3 août 2017. Le double du record précédent.",
      cur: '07',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 7,
    cur: '08',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: 'TOUJOURS\nLE RECORD',
      greenWord: 'TOUJOURS',
      body: "Neuf ans plus tard, en 2026. Aucun club n'a fait plus.",
      cur: '08',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'quote',
    seconds: 8,
    cur: '09',
    props: {
      quote: "Ce n'est plus du sport. C'est devenu le jouet d'un État.",
      quoteAccent: "le jouet d'un État.",
      quoteAuthor: 'Javier Tebas, président de LaLiga, 2019',
      caption: "L'AVEU",
      accent: 'var(--rouille)',
      cur: '09',
      tot: TOT,
    },
  },
  {
    kind: 'cover',
    seconds: 7,
    cur: '10',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: 'FAIR-PLAY\nFINANCIER',
      greenWord: 'FAIR-PLAY',
      body: "Créé par l'UEFA en 2010, contre ce scénario précis.",
      cur: '10',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 8,
    cur: '11',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '115\nACCUSATIONS',
      greenWord: '115',
      body: 'Contre Manchester City, depuis 2023. Toujours sans verdict trois ans après.',
      cur: '11',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 8,
    cur: '12',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '-10 POINTS\nEN QUELQUES MOIS',
      greenWord: '-10',
      body: 'Everton et Nottingham Forest sanctionnés. Manchester City attend toujours.',
      cur: '12',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 8,
    cur: '13',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: '12 CLUBS\n1 PROPRIÉTAIRE',
      greenWord: '12',
      body: "Le City Football Group. City et Girona, tous deux en Ligue des champions 2024-25.",
      cur: '13',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cover',
    seconds: 5,
    cur: '14',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: 'UN FIDUCIAIRE\nINDÉPENDANT',
      greenWord: 'FIDUCIAIRE',
      body: "Pour éviter l'exclusion de l'un des deux clubs, sous supervision de l'UEFA.",
      cur: '14',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'breath',
    seconds: 6,
    props: {quote: 'ÇA SANCTIONNE. TROP LENTEMENT.', quoteAccent: 'TROP LENTEMENT.', sig: 'var(--sig-arretdejeu)'},
  },
  {
    kind: 'cover',
    seconds: 8,
    cur: '16',
    props: {
      serie: 'arretdejeu',
      variant: 'cover',
      title: "LE FOOT N'A\nPAS PERDU SES RÈGLES",
      greenWord: 'RÈGLES',
      body: "Il a perdu le temps d'arriver à temps.",
      cur: '16',
      tot: TOT,
      showSwipe: false,
    },
  },
  {
    kind: 'cta',
    seconds: 5,
    props: {
      title: 'RESTE DANS\nLE JEU',
      greenWord: 'JEU',
      body: 'On parle encore du même sport ? Débat en commentaire.',
      btnlabel: 'FOLLOW',
      sig: 'var(--sig-arretdejeu)',
      onSig: 'var(--on-sig-arretdejeu)',
    },
  },
];

export function totalDurationInFrames(): number {
  return SCENES.reduce((acc, s) => acc + Math.round(s.seconds * FPS), 0);
}

function SceneRenderer({scene}: {scene: Scene}) {
  if (scene.kind === 'cover') return <CoverSlide {...scene.props} />;
  if (scene.kind === 'breath') return <BreathSlide {...scene.props} />;
  if (scene.kind === 'quote') return <QuoteSlide {...scene.props} />;
  return <CTASlide {...scene.props} />;
}

export const StoryboardArretDeJeu: React.FC = () => {
  let frame = 0;
  return (
    <AbsoluteFill style={{background: 'var(--ink)'}}>
      <BrandFonts />
      {SCENES.map((scene, i) => {
        const durationInFrames = Math.round(scene.seconds * FPS);
        const from = frame;
        frame += durationInFrames;
        return (
          <Sequence key={i} from={from} durationInFrames={durationInFrames}>
            <SceneRenderer scene={scene} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
