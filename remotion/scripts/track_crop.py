#!/usr/bin/env python3
"""Compute a smoothed horizontal "crop center" track for a landscape video,
so a 9:16 render can pan to follow the action instead of a fixed center-crop.

Signal fusion per sampled frame (editeurs/crop-focus.html's ball+person+motion
fusion):
  - ball detection (YOLOv2-COCO, "sports ball" class) -> strongest weight
  - person detection (YOLOv2-COCO, "person" class) -> dominant weight
  - motion (frame-to-frame grayscale diff) -> medium weight, fills in when
    nothing is detected (e.g. wide shots, replays)
  - edges (Sobel magnitude) -> weak weight, keeps a static single-subject
    frame from drifting back to center when nothing moves

Model: YOLOv2 (not tiny), trained on COCO -- output (1,425,13,13): 5 anchors x
(4 box + 1 objectness + 80 classes). Same box-major layout as YOLOv2-tiny/VOC
(offset 4 = objectness), just 80 classes instead of 20.

IMPORTANT preprocessing gotcha (cost a lot of debugging time): this model
expects raw 0-255 pixel values, NOT 0-1 normalized input. Verified against
the ONNX model zoo's own reference test tensors and by bit-matching cv2.dnn's
output against them. Feeding 0-1 input silently produces near-zero
objectness everywhere -- looks like "the model just doesn't work" or "domain
shift", but it's actually wrong preprocessing.

The per-frame centroid is then smoothed (EMA + max-speed clamp) so the pan
doesn't whip-pan on noise, and written out as {t, cx} keyframes (cx in
0..1, fraction of source width) for the Remotion composition to interpolate.

Usage:
    python3 track_crop.py <video.mp4> [--stride 5] [--resize-width 320] \
      [--model ../models/yolov2-coco-9.onnx] [--no-dnn] > track.json
"""
import argparse
import json
import os
import sys

import cv2
import numpy as np

BALL_WEIGHT = 60.0
PERSON_WEIGHT = 20.0
MOTION_WEIGHT = 6.0
EDGE_WEIGHT = 1.0
EMA_ALPHA = 0.15          # smoothing: higher = snappier, lower = smoother
MAX_DELTA_PER_SAMPLE = 0.05  # clamp how far cx can move between samples

DETECTION_CONF_THRESHOLD = 0.1

# YOLOv2 anchors (same for tiny and full COCO variants).
YOLOV2_ANCHORS = np.array(
    [1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52]
).reshape(5, 2)

DEFAULT_CLASS_NAMES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "models", "coco.names"
)


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -50, 50)))


def load_detector(model_path):
    if not model_path or not os.path.exists(model_path):
        print(
            f"[track_crop] no DNN model at {model_path!r}, "
            "falling back to motion/edge only",
            file=sys.stderr,
        )
        return None
    return cv2.dnn.readNetFromONNX(model_path)


def load_class_indices(names_path):
    if not os.path.exists(names_path):
        return None, None
    names = open(names_path).read().strip().split("\n")
    person = names.index("person") if "person" in names else None
    ball = names.index("sports ball") if "sports ball" in names else None
    return person, ball


def detect_boxes(net, frame, num_attrs, person_idx, ball_idx):
    """Returns list of (cx, cy, w, h, weight) in 0..1 fractions of the frame,
    weight already scaled by BALL_WEIGHT/PERSON_WEIGHT so callers can just
    sum contributions."""
    # See module docstring: raw 0-255 input, not normalized.
    blob = cv2.dnn.blobFromImage(
        frame, scalefactor=1.0, size=(416, 416), swapRB=True, crop=False
    )
    net.setInput(blob)
    out = net.forward()[0].reshape(5, num_attrs, 13, 13)

    boxes = []
    for a in range(5):
        tx, ty, tw, th, to = out[a, 0], out[a, 1], out[a, 2], out[a, 3], out[a, 4]
        class_scores = out[a, 5:num_attrs]
        conf = sigmoid(to)
        exps = np.exp(np.clip(class_scores - class_scores.max(axis=0, keepdims=True), -50, 0))
        probs = exps / exps.sum(axis=0, keepdims=True)

        for class_idx, weight in ((ball_idx, BALL_WEIGHT), (person_idx, PERSON_WEIGHT)):
            if class_idx is None:
                continue
            p = probs[class_idx] * conf
            ys, xs = np.where(p > DETECTION_CONF_THRESHOLD)
            for y, x in zip(ys, xs):
                bx = (x + sigmoid(tx[y, x])) / 13
                by = (y + sigmoid(ty[y, x])) / 13
                bw = YOLOV2_ANCHORS[a, 0] * np.exp(tw[y, x]) / 13
                bh = YOLOV2_ANCHORS[a, 1] * np.exp(th[y, x]) / 13
                boxes.append((bx, by, bw, bh, weight * float(p[y, x])))
    return boxes


def analyze(path, stride, resize_width, net, person_idx, ball_idx):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = resize_width / src_w
    resize_h = max(1, int(src_h * scale))

    num_attrs = None
    if net is not None:
        dummy = np.zeros((1, 3, 416, 416), dtype=np.float32)
        net.setInput(dummy)
        out_shape = net.forward().shape  # dry run to read the channel count
        num_attrs = out_shape[1] // 5

    prev_gray = None
    raw = []  # (frame_index, cx_raw or None)
    frame_idx = 0
    n_detect_hits = 0

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
            boxes = detect_boxes(net, frame, num_attrs, person_idx, ball_idx)
            if boxes:
                n_detect_hits += 1
            for bx, by, bw, bh, weight in boxes:
                x0 = max(0, int((bx - bw / 2) * resize_width))
                x1 = min(resize_width, int((bx + bw / 2) * resize_width))
                if x1 > x0:
                    weight_col[x0:x1] += weight

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
            f"[track_crop] person/ball detected in {n_detect_hits}/{n_samples} "
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
        os.path.dirname(os.path.abspath(__file__)), "..", "models", "yolov2-coco-9.onnx"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--stride", type=int, default=5)
    parser.add_argument("--resize-width", type=int, default=320)
    parser.add_argument("--model", default=default_model)
    parser.add_argument("--class-names", default=DEFAULT_CLASS_NAMES)
    parser.add_argument("--no-dnn", action="store_true")
    args = parser.parse_args()

    net = None if args.no_dnn else load_detector(args.model)
    person_idx, ball_idx = (None, None)
    if net is not None:
        person_idx, ball_idx = load_class_indices(args.class_names)
        if person_idx is None and ball_idx is None:
            print(
                f"[track_crop] no usable class names at {args.class_names!r}, "
                "falling back to motion/edge only",
                file=sys.stderr,
            )
            net = None

    fps, raw = analyze(args.video, args.stride, args.resize_width, net, person_idx, ball_idx)
    smoothed = smooth(raw)

    keyframes = [
        {"t": round(frame_idx / fps, 3), "cx": round(cx, 4)}
        for frame_idx, cx in smoothed
    ]
    print(json.dumps({"fps": fps, "keyframes": keyframes}, indent=2))


if __name__ == "__main__":
    main()
