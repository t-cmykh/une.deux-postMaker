#!/usr/bin/env python3
"""Compute a smoothed horizontal "crop center" track for a landscape video,
so a 9:16 render can pan to follow the action instead of a fixed center-crop.

Signal fusion per sampled frame (editeurs/crop-focus.html's "motion/detail"
fallback mode: this OpenCV build has no HOGDescriptor/person detector, and a
real ball detector needs a trained model we don't have offline, so this
sticks to what's left of that tool's fusion):
  - motion (frame-to-frame grayscale diff) -> dominant weight, follows where
    the action is moving
  - edges (Sobel magnitude) -> weak weight, keeps a static single-subject
    frame from drifting back to center when nothing moves

The per-frame centroid is then smoothed (EMA + max-speed clamp) so the pan
doesn't whip-pan on noise, and written out as {t, cx} keyframes (cx in
0..1, fraction of source width) for the Remotion composition to interpolate.

Usage:
    python3 track_crop.py <video.mp4> [--stride 5] [--resize-width 320] > track.json
"""
import argparse
import json

import cv2
import numpy as np

MOTION_WEIGHT = 6.0
EDGE_WEIGHT = 1.0
EMA_ALPHA = 0.15          # smoothing: higher = snappier, lower = smoother
MAX_DELTA_PER_SAMPLE = 0.05  # clamp how far cx can move between samples


def analyze(path, stride, resize_width):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = resize_width / src_w
    resize_h = max(1, int(src_h * scale))

    prev_gray = None
    raw = []  # (frame_index, cx_raw or None)
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx % stride != 0:
            frame_idx += 1
            continue

        small = cv2.resize(frame, (resize_width, resize_h), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        weight_col = np.zeros(resize_width, dtype=np.float64)

        if prev_gray is not None:
            motion = np.abs(gray.astype(np.int16) - prev_gray.astype(np.int16)).sum(axis=0)
            m_max = motion.max()
            if m_max > 0:
                weight_col += MOTION_WEIGHT * (motion / m_max)

        sobel = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        edge = np.abs(sobel).sum(axis=0)
        e_max = edge.max()
        if e_max > 0:
            weight_col += EDGE_WEIGHT * (edge / e_max)

        total = weight_col.sum()
        if total > 1e-6:
            idx = np.arange(resize_width)
            cx = float((idx * weight_col).sum() / total) / resize_width
        else:
            cx = None

        raw.append((frame_idx, cx))
        prev_gray = gray
        frame_idx += 1

    cap.release()
    return fps, raw


def smooth(raw):
    smoothed = []
    current = 0.5
    have_signal = False
    for frame_idx, cx in raw:
        if cx is None:
            smoothed.append((frame_idx, current))
            continue
        if not have_signal:
            current = cx
            have_signal = True
        else:
            delta = cx - current
            delta = max(-MAX_DELTA_PER_SAMPLE, min(MAX_DELTA_PER_SAMPLE, delta))
            current = current + EMA_ALPHA * delta
        smoothed.append((frame_idx, current))
    return smoothed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--stride", type=int, default=5)
    parser.add_argument("--resize-width", type=int, default=320)
    args = parser.parse_args()

    fps, raw = analyze(args.video, args.stride, args.resize_width)
    smoothed = smooth(raw)

    keyframes = [
        {"t": round(frame_idx / fps, 3), "cx": round(cx, 4)}
        for frame_idx, cx in smoothed
    ]
    print(json.dumps({"fps": fps, "keyframes": keyframes}, indent=2))


if __name__ == "__main__":
    main()
