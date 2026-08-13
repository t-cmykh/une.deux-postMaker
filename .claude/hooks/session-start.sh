#!/bin/bash
# SessionStart hook — preinstalls ffmpeg so it's already available when a
# session starts, instead of being reinstalled from scratch on every run.
# Motivated by the "Ce jour-là" reel-fabrication Routine (see CLAUDE.md),
# whose delivery reports repeatedly logged ffmpeg missing from the
# container at the start of each daily run (first signalled 5 août 2026,
# still recurring as of 13 août 2026) — a real, avoidable chunk of the
# ~15min gap observed before the video pipeline itself even starts.
set -euo pipefail

# Only relevant for Claude Code on the web / remote sessions — a local
# dev machine already has its own toolchain.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg already present: $(ffmpeg -version | head -1)"
  exit 0
fi

echo "ffmpeg not found — installing..."
if command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq ffmpeg
elif command -v apk >/dev/null 2>&1; then
  apk add --no-cache ffmpeg
else
  echo "No supported package manager found (apt-get/apk) — could not install ffmpeg" >&2
  exit 1
fi

ffmpeg -version | head -1
