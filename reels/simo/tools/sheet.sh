#!/usr/bin/env bash
# Contact sheet of review stills: tools/sheet.sh reel out.jpg 1.2 5 9.5 …
set -euo pipefail
cd "$(dirname "$0")/.."
page=$1; out=$2; shift 2
node tools/shoot.mjs "$page" "$@"
args=(); f=""; i=0
for t in "$@"; do args+=(-i "build/shots/${page}_${t}.jpg"); f+="[$i]scale=$([ "$page" = wide ] && echo 640:360 || echo 360:640),drawtext=text='$t':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6[v$i];"; i=$((i+1)); done
n=$#; cols=$([ "$page" = wide ] && echo 3 || echo 6); rows=$(( (n + cols - 1) / cols ))
for ((k=0;k<n;k++)); do f+="[v$k]"; done
ffmpeg -hide_banner -loglevel error -y "${args[@]}" -filter_complex "${f}xstack=inputs=$n:layout=$(python3 -c "
c=$cols;n=$n;w=$([ "$page" = wide ] && echo 640 || echo 360);h=$([ "$page" = wide ] && echo 360 || echo 640)
print('|'.join(f'{(i%c)*w}_{(i//c)*h}' for i in range(n)))"):fill=black" "$out"
