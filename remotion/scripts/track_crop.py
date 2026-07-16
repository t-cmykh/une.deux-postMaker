#!/usr/bin/env python3
"""Compute a smoothed horizontal "crop center" track for a landscape video,
so a 9:16 render can pan to follow the action instead of a fixed center-crop.

Signal fusion per sampled frame (editeurs/crop-focus.html's ball+person+motion
fusion, minus the ball detector which needs a model we don't have offline):
  - person detection (YOLOv2-tiny ONNX, VOC "person" class) -> dominant weight
  - motion (frame-to-frame grayscale diff) -> medium weight, fills in when
    no person is detected (e.g. wide shots, replays)
  - edges (Sobel magnitude) -> weak weight, keeps a static single-subject
    frame from drifting back to center when nothing moves

Note: on 1950s black-and-white archival footage the person detector was
tested and found useless (near-zero, near-constant confidence regardless of
content -- a classic domain-shift failure: the model was trained on modern
color photography). It's expected to do much better on modern color footage.

The per-frame centroid is then smoothed (EMA + max-speed clamp) so the pan
doesn't whip-pan on noise, and written out as {t, cx} keyframes (cx in
0..1, fraction of source width) for the Remotion composition to interpolate.

Usage:
    python3 track_crop.py <video.mp4> [--stride 5] [--resize-width 320] \
      [--model ../models/tinyyolov2-8.onnx] [--no-dnn] > track.json
"""
import argparse
import json
import os
import sys

import cv2
import numpy as np

PERSON_WEIGHT = 30.0
MOTION_WEIGHT = 6.0
EDGE_WEIGHT = 1.0
EMA_ALPHA = 0.15          # smoothing: higher = snappier, lower = smoother
MAX_DELTA_PER_SAMPLE = 0.05  # clamp how far cx can move between samples

PERSON_CONF_THRESHOLD = 0.1

# YOLOv2-tiny (VOC) anchors and class list; "person" is class index 14.
YOLOV2_TINY_VOC_ANCHORS = np.array(
    [1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52]
).reshape(5, 2)
PERSON_CLASS_INDEX = 14


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def load_person_detector(model_path):
    if not model_path or not os.path.exists(model_path):
        print(
            f"[track_crop] no DNN model at {model_path!r}, "
            "falling back to motion/edge only",
            file=sys.stderr,
        )
        return None
    return cv2.dnn.readNetFromONNX(model_path)


def detect_person_boxes(net, frame):
    """Returns list of (cx, cy, w, h, conf) in 0..1 fractions of the frame."""
    blob = cv2.dnn.blobFromImage(
        frame, scalefactor=1 / 255.0, size=(416, 416), swapRB=True, crop=False
    )
    net.setInput(blob)
    out = net.forward()[0].reshape(5, 25, 13, 13)

    boxes = []
    for a in range(5):
        tx, ty, tw, th, to = out[a, 0], out[a, 1], out[a, 2], out[a, 3], out[a, 4]
        class_scores = out[a, 5:25]
        conf = sigmoid(to)
        exps = np.exp(class_scores - class_scores.max(axis=0, keepdims=True))
        probs = exps / exps.sum(axis=0, keepdims=True)
        person_prob = probs[PERSON_CLASS_INDEX] * conf
        ys, xs = np.where(person_prob > PERSON_CONF_THRESHOLD)
        for y, x in zip(ys, xs):
            bx = (x + sigmoid(tx[y, x])) / 13
            by = (y + sigmoid(ty[y, x])) / 13
            bw = YOLOV2_TINY_VOC_ANCHORS[a, 0] * np.exp(tw[y, x]) / 13
            bh = YOLOV2_TINY_VOC_ANCHORS[a, 1] * np.exp(th[y, x]) / 13
            boxes.append((bx, by, bw, bh, float(person_prob[y, x])))
    return boxes


def analyze(path, stride, resize_width, net):
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
    n_person_hits = 0

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

        if net is not None:
            boxes = detect_person_boxes(net, frame)
            if boxes:
                n_person_hits += 1
            for bx, by, bw, bh, conf in boxes:
                x0 = max(0, int((bx - bw / 2) * resize_width))
                x1 = min(resize_width, int((bx + bw / 2) * resize_width))
                if x1 > x0:
                    weight_col[x0:x1] += PERSON_WEIGHT * conf

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
    if net is not None:
        n_samples = len(raw)
        print(
            f"[track_crop] person detected in {n_person_hits}/{n_samples} "
            "sampled frames",
            file=sys.stderr,
        )
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
    default_model = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "models", "tinyyolov2-8.onnx"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--stride", type=int, default=5)
    parser.add_argument("--resize-width", type=int, default=320)
    parser.add_argument("--model", default=default_model)
    parser.add_argument("--no-dnn", action="store_true")
    args = parser.parse_args()

    net = None if args.no_dnn else load_person_detector(args.model)

    fps, raw = analyze(args.video, args.stride, args.resize_width, net)
    smoothed = smooth(raw)

    keyframes = [
        {"t": round(frame_idx / fps, 3), "cx": round(cx, 4)}
        for frame_idx, cx in smoothed
    ]
    print(json.dumps({"fps": fps, "keyframes": keyframes}, indent=2))


if __name__ == "__main__":
    main()
