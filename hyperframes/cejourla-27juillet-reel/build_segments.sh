#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p assets

# source: 1440x2560 pillarboxed capture, real content band = crop=1440:1132:0:714 (ratio ~1.272, same broadcast as before)
# zoom 1.4x centered crop to push the "M" watermark (top-right) out of frame
CW=1440
CH=1132
CY=714
ZW=2016
ZH=1585
BGW=2442   # cover-crop width for bg -> 1080x1920
FGW=1130   # cover-crop width for fg -> 1080x888

build_seg() {
  name=$1; in=$2; dur=$3
  ffmpeg -y -ss "$in" -i video_raw.mp4 -t "$dur" -filter_complex \
    "[0:v]crop=${CW}:${CH}:0:${CY},scale=${ZW}:${ZH},crop=${CW}:${CH},fps=30,split=2[z1][z2];\
[z1]scale=${BGW}:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];\
[z2]scale=${FGW}:888,crop=1080:888[fg];\
[bg][fg]overlay=x=0:y=420:shortest=1[outv]" \
    -map "[outv]" -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -an "assets/${name}.mp4" -loglevel error

  ffmpeg -y -ss "$in" -i video_raw.mp4 -t "$dur" -vn -c:a aac -b:a 160k "assets/${name}-audio.m4a" -loglevel error
  echo "built $name (in=$in dur=$dur)"
}

build_seg seg1 1.0  8.0
build_seg seg2 14.5 6.0
build_seg seg3 27.0 3.5
build_seg seg4 41.0 3.5
build_seg seg5 20.5 6.0
build_seg seg6 31.0 4.0
build_seg seg7 44.5 4.2

echo "all segments built"
