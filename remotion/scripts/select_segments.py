#!/usr/bin/env python3
"""Pick the most 'interesting' seconds of a video combining visual scene-change
score (ffmpeg lavfi.scene_score, one value per frame) and audio loudness
(ffmpeg astats RMS_level in dB, one value per second).

On real, grainy archival footage the visual scene score has very low dynamic
range (film grain dominates), so audio energy (crowd noise) turns out to be
the stronger signal for "exciting moment" -- this combines both, normalized,
with audio weighted higher.

Usage:
    ffmpeg -i in.mp4 -vf "scale=160:90,select='gte(scene\,0)',metadata=print" \
      -an -f null - 2>&1 | grep -o 'lavfi.scene_score=[0-9.]*' | cut -d= -f2 \
      > scene_scores.txt

    ffmpeg -i in.mp4 -af "asetnsamples=n=44100,astats=metadata=1:reset=1,\
ametadata=print:key=lavfi.astats.Overall.RMS_level" -f null - 2>&1 \
      | grep RMS_level | sed -E 's/.*RMS_level=(.*)/\1/' > audio_rms.txt

    python3 select_segments.py scene_scores.txt audio_rms.txt <source_fps> <target_seconds>
"""
import json
import sys

WINDOW_S = 1.0
MIN_GAP_S = 0.0       # merge picks separated by <= this many seconds
MIN_SEGMENT_S = 2.0
PAD_S = 0.5
AUDIO_WEIGHT = 0.65
VISUAL_WEIGHT = 0.35
TOP_FRACTION = 0.25    # keep the top X% of seconds by combined score

def load_floats(path):
    with open(path) as f:
        return [float(l.strip()) for l in f if l.strip()]

def bucket_visual(scores, fps, window_s):
    per_window = int(window_s * fps)
    buckets = []
    for i in range(0, len(scores), per_window):
        chunk = scores[i:i + per_window]
        if chunk:
            buckets.append(sum(chunk) / len(chunk))
    return buckets

def normalize(values):
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]

def main():
    visual_path, audio_path, fps_s, target_s = sys.argv[1:5]
    fps = float(fps_s)
    target = float(target_s)

    visual_raw = load_floats(visual_path)
    audio_raw = load_floats(audio_path)  # dB, higher (less negative) = louder

    visual_buckets = bucket_visual(visual_raw, fps, WINDOW_S)
    n = min(len(visual_buckets), len(audio_raw))
    visual_buckets = visual_buckets[:n]
    audio_raw = audio_raw[:n]

    visual_n = normalize(visual_buckets)
    audio_n = normalize(audio_raw)  # min dB -> 0, max dB (loudest) -> 1
    combined = [VISUAL_WEIGHT * v + AUDIO_WEIGHT * a for v, a in zip(visual_n, audio_n)]

    ranked_idx = sorted(range(n), key=lambda i: -combined[i])
    keep_count = max(1, int(n * TOP_FRACTION))
    kept_idx = set(ranked_idx[:keep_count])

    # merge kept seconds into contiguous segments, bridging small gaps
    segments = []
    sorted_idx = sorted(kept_idx)
    start = prev = sorted_idx[0]
    for i in sorted_idx[1:]:
        if i - prev <= MIN_GAP_S:
            prev = i
            continue
        segments.append((start, prev + 1))
        start = prev = i
    segments.append((start, prev + 1))

    scored_segments = []
    for s, e in segments:
        seg_vals = combined[s:e]
        avg = sum(seg_vals) / len(seg_vals)
        dur = (e - s) * WINDOW_S
        if dur < MIN_SEGMENT_S:
            extra = (MIN_SEGMENT_S - dur) / 2
            s = max(0, s - extra)
            e = e + extra
            dur = MIN_SEGMENT_S
        scored_segments.append({"start": s * WINDOW_S, "end": e * WINDOW_S, "score": avg})

    ranked = sorted(scored_segments, key=lambda x: -x["score"])
    kept, total = [], 0.0
    for seg in ranked:
        if total >= target:
            break
        kept.append(seg)
        total += seg["end"] - seg["start"]
    kept.sort(key=lambda x: x["start"])

    padded = [
        {
            "start": max(0, seg["start"] - PAD_S),
            "end": seg["end"] + PAD_S,
            "score": seg["score"],
        }
        for seg in kept
    ]

    # padding can make neighboring picks touch or overlap; merge those so
    # the render never repeats the same source frames twice.
    merged = []
    for seg in padded:
        if merged and seg["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], seg["end"])
            merged[-1]["score"] = max(merged[-1]["score"], seg["score"])
        else:
            merged.append(dict(seg))

    result = [
        {"start": round(s["start"], 2), "end": round(s["end"], 2), "score": round(s["score"], 4)}
        for s in merged
    ]
    total_final = sum(s["end"] - s["start"] for s in result)
    print(json.dumps({"segments": result, "totalDuration": round(total_final, 2)}, indent=2))

if __name__ == "__main__":
    main()
