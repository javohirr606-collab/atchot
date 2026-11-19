#!/usr/bin/env bash
# Extracts the whole source video as 720×1280 JPEG frames at 30 fps into src/frames/NNNNN.jpg
# (frame N shows source time (N-1)/30 s). Light denoise, lanczos upscale, sharpen and grade.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf src/frames && mkdir -p src/frames
ffmpeg -hide_banner -loglevel error -y -i src/assets/source.mp4 \
  -vf "fps=30,hqdn3d=1.2:1.2:5:5,scale=720:1280:flags=lanczos,unsharp=5:5:0.75:3:3:0,eq=contrast=1.05:saturation=1.12:brightness=0.008" \
  -q:v 3 src/frames/%05d.jpg
ls src/frames | wc -l
