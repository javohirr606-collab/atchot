#!/bin/sh
# Extracts the two phone clips into 30 fps JPEG frames used by the page (src/frames/v1, src/frames/v2).
# Usage: sh tools/frames.sh path/to/IMG_5831.MOV path/to/IMG_5838.MOV
set -e
cd "$(dirname "$0")/.."
mkdir -p src/frames/v1 src/frames/v2
ffmpeg -hide_banner -loglevel error -y -i "$1" -vf fps=30 -q:v 2 src/frames/v1/%04d.jpg
ffmpeg -hide_banner -loglevel error -y -i "$2" -vf fps=30 -q:v 2 src/frames/v2/%04d.jpg
