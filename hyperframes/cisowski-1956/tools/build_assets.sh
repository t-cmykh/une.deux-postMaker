#!/usr/bin/env bash
# Génère les visuels traités (duotone / trame) des trois reels à partir de sources/.
set -euo pipefail
cd "$(dirname "$0")/.."
T="python3 -I tools/treat.py"; S=sources
R1=reel-1-record/assets; R2=reel-2-destin/assets; R3=reel-3-match/assets
mkdir -p $R1 $R2 $R3

# ---------- Reel 1 — LE RECORD (plein cadre, trame sombre) ----------
# (visages posés sous le header : image 1080x1620 placée à top:300px, fondue vers l'encre en haut)
$T $S/mbappe-2018-venediktov.jpg   $R1/hook-mbappe.jpg    --size 1080x1620 --focus 0.44,0.5  --mode halftone-dark --pitch 9 --dim 0.80 --fade-top 200
$T $S/fontaine-1958-panini.jpg     $R1/hook-fontaine.jpg  --size 1080x1920 --focus 0.5,0.40  --mode halftone-dark --pitch 9 --dim 0.80
$T $S/cisowski-puskas-1956.jpg     $R1/seul-homme.jpg     --size 1080x1620 --focus 0.52,0.5  --mode halftone-dark --pitch 8 --dim 0.80 --fade-top 200
$T $S/cisowski-racing-couleur.jpg  $R1/reveal-couleur.jpg --size 1080x720  --focus 0.36,0.5  --mode color --sat 0.85
$T $S/cisowski-racing-couleur.jpg  $R1/reveal-bg.jpg      --size 1080x1920 --focus 0.30,0.5  --mode duotone --blur 26 --dim 0.42
$T $S/fra-bel-1956-but-cisowski.jpg    $R1/match-but.jpg    --size 1080x620 --crop 0,0,1,0.86 --focus 0.5,0.45 --mode halftone --pitch 8
$T $S/fra-bel-1956-action-cisowski.jpg $R1/match-action.jpg --size 1080x620 --crop 0,0,1,0.86 --focus 0.5,0.45 --mode halftone --pitch 8
$T $S/fra-bel-1956-cisowski-duel.jpg   $R1/match-duel.jpg   --size 1080x620 --crop 0,0,1,0.86 --focus 0.5,0.45 --mode halftone --pitch 8
$T $S/cisowski-racing-action.jpg   $R1/final-bg.jpg       --size 1080x1920 --focus 0.5,0.55  --mode halftone-dark --pitch 9 --dim 0.72

# ---------- Reel 2 — LE DESTIN (géométrie reel une·deux : fenêtre 1080x888 + fond flouté) ----------
win() {  # win <src> <name> <focus> <mode> [extra...]
  local src=$1 name=$2 focus=$3 mode=$4; shift 4
  $T $S/$src $R2/w-$name.jpg  --size 1080x888  --focus $focus --mode $mode "$@"
  $T $S/$src $R2/bg-$name.jpg --size 1080x1920 --focus $focus --mode duotone --blur 30 --dim 0.50 --quality 88
}
win cisowski-carte-dedicacee.jpg  portrait 0.5,0.42  halftone --crop 0.05,0.10,0.47,0.92 --pitch 7
win mine-mouriere-annees30.jpg    mine     0.55,0.55 halftone --pitch 7
win cisowski-racing-action.jpg    racing   0.5,0.42  halftone --pitch 7
win cisowski-racing-couleur.jpg   couleur  0.30,0.5  color --sat 0.85
win cisowski-puskas-1956.jpg      bleu     0.50,0.45 halftone --pitch 7
win fra-bel-1956-but-cisowski.jpg but      0.5,0.45  halftone --crop 0,0,1,0.86 --pitch 8
win fra-bel-1956-action-cisowski.jpg action 0.42,0.45 halftone --crop 0,0,1,0.86 --pitch 8
win fra-bel-1956-cisowski-duel.jpg duel    0.6,0.45  halftone --crop 0,0,1,0.86 --pitch 8
win fontaine-1958-panini.jpg      fontaine 0.5,0.36  halftone --pitch 7
win cisowski-carte-dedicacee.jpg  carte    0.5,0.5   duotone  --crop 0.0,0.0,1,1

# ---------- Reel 3 — LE MATCH (fond crème, coupures de presse tramées) ----------
clip() { $T $S/$1 $R3/clip-$2.jpg --size 880x506 --crop 0,0,1,0.86 --focus $3 --mode halftone --pitch 7; }
clip fra-bel-1956-but-cisowski.jpg    but     0.5,0.45
clip fra-bel-1956-action-cisowski.jpg action  0.5,0.45
clip fra-bel-1956-cisowski-duel.jpg   duel    0.5,0.45
clip fra-bel-1956-but-vincent.jpg     vincent 0.5,0.45
clip fra-bel-1956-but-belge.jpg       belge   0.5,0.45
clip fra-bel-1956-houf-remetter.jpg   houf    0.5,0.45
$T $S/cisowski-puskas-1956.jpg $R3/clip-cisowski.jpg --size 880x660 --focus 0.5,0.45 --mode halftone --pitch 7
echo "assets ok"
