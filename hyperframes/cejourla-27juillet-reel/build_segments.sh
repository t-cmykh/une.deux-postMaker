#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p assets

# source displayed ratio 1680x1320 (rotation=90 auto-applied by ffmpeg)
# zoom 1.4x centered crop to push the "M" watermark (top-right) out of frame
ZW=2352
ZH=1848
BGW=2444   # cover-crop width for bg -> 1080x1920
FGW=1130   # cover-crop width for fg -> 1080x888

build_seg() {
  name=$1; in=$2; dur=$3
  ffmpeg -y -ss "$in" -i video_raw.mp4 -t "$dur" -filter_complex \
    "[0:v]scale=${ZW}:${ZH},crop=1680:1320,fps=30,split=2[z1][z2];\
[z1]scale=${BGW}:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];\
[z2]scale=${FGW}:888,crop=1080:888[fg];\
[bg][fg]overlay=x=0:y=420:shortest=1[outv]" \
    -map "[outv]" -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -an "assets/${name}.mp4" -loglevel error

  ffmpeg -y -ss "$in" -i video_raw.mp4 -t "$dur" -vn -c:a aac -b:a 160k "assets/${name}-audio.m4a" -loglevel error
  echo "built $name (in=$in dur=$dur)"
}

build_seg seg1  1.0   9.6
build_seg seg2a 20.0  4.0
build_seg seg2b 75.0  4.6
build_seg seg2c 106.0 3.9
build_seg seg3  32.0  3.6
build_seg seg4  118.0 7.6
build_seg seg5a 45.0  6.6
build_seg seg5b 90.0  6.6
build_seg seg6  58.0  6.8
build_seg seg7  100.0 5.0

echo "all segments built"
