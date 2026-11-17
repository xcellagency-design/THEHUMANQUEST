#!/usr/bin/env bash
# One-time setup for a fresh checkout. Safe to re-run.
set -e
cd "$(dirname "$0")"
python3 -c "import kokoro_onnx, soundfile, cv2, PIL, scipy, numpy" 2>/dev/null || pip install --break-system-packages -q kokoro-onnx soundfile opencv-python-headless pillow scipy numpy
python3 -c "import faster_whisper" 2>/dev/null || pip install --break-system-packages -q faster-whisper
python3 -c "import pytest" 2>/dev/null || pip install --break-system-packages -q pytest
mkdir -p engine/models out/shorts work
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s engine/models/kokoro-v1.0.onnx ] || curl -fsSL "$B/kokoro-v1.0.onnx" -o engine/models/kokoro-v1.0.onnx
[ -s engine/models/voices-v1.0.bin ] || curl -fsSL "$B/voices-v1.0.bin" -o engine/models/voices-v1.0.bin
which ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
python3 -m pytest -q tests | tail -1
python3 -m studio.cli status
