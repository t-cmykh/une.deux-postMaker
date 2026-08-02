#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p assets

# source: 2868x1320 (post-rotation), ratio ~2.173, montage non retouché —
# ordre et longueur intacts (compilation buts Harry Kane, CM 2026), pas de
# pillarbox/watermark à exclure ici
BGW=4171   # cover-crop width for bg -> 1080x1920
FGW=1929   # cover-crop width for fg -> 1080x888

ffmpeg -y -i video_raw.mp4 -filter_complex \
  "[0:v]fps=30,split=2[z1][z2];\
[z1]scale=${BGW}:1920,crop=1080:1920,gblur=sigma=36,eq=saturation=0.4[bg];\
[z2]scale=${FGW}:888,crop=1080:888[fg];\
[bg][fg]overlay=x=0:y=420:shortest=1[outv]" \
  -map "[outv]" -c:v libx264 -crf 20 -preset fast -pix_fmt yuv420p -an assets/full.mp4 -loglevel error

ffmpeg -y -i video_raw.mp4 -vn -c:a aac -b:a 160k assets/full-audio.m4a -loglevel error

echo "full composite built"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 assets/full.mp4
