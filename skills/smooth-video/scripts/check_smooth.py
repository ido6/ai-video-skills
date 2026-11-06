"""Measure how smoothly a clip plays: cuts, frozen frames, jumps, evenness, and how closely it follows a reference.

  python check_smooth.py clip.mp4
  python check_smooth.py new_film.mp4 --ref original_film.mp4 --ranges 0-3,9-12,12-15

A frozen frame is one that barely changes from the frame before (under 25% of the range's median change); a jump is
one that changes more than 2.2x the median without being a cut. "follows" is the correlation of frame-to-frame motion
with the reference over the same range (1.00 = moves exactly like the reference); "motion" is the range's median
frame-to-frame change. Read every number against the reference: a still moment (someone holding a pose) shows as
frozen frames in the reference too, and in a near-still range (motion under about 2) the scores are noise.
"""
import argparse
import numpy as np
import cv2


def motion(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    prev, d = None, []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(f, (270, 480)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            d.append(float(np.mean(np.abs(g - prev))))
        prev = g
    return np.array(d), fps


def cut_frames(d):
    """Frame indices that start a new shot: a jump far above the clip's normal change."""
    return [int(i) + 1 for i in np.flatnonzero(d > max(25.0, 8 * np.median(d)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--ref")
    ap.add_argument("--ranges", default="", help="seconds, e.g. 0-3,9-12; default: the whole clip")
    a = ap.parse_args()
    d, fps = motion(a.clip)
    cuts = cut_frames(d)
    print(f"{a.clip}: {len(d) + 1} frames, {fps:g} fps, {(len(d) + 1) / fps:.3f} s, cuts at {[round(float(c) / fps, 3) for c in cuts]} s"
          " (very fast motion can read as a cut too)")
    r = motion(a.ref)[0] if a.ref else None
    ranges = [tuple(float(v) for v in s.split("-")) for s in a.ranges.split(",") if s] or [(0, len(d) / fps)]
    for t0, t1 in ranges:
        i0, i1 = int(round(t0 * fps)), min(len(d), int(round(t1 * fps)) - 1)
        s = d[i0:i1]
        idx = np.arange(i0, i1)
        keep = ~np.isin(idx + 1, cuts)                       # a cut is not a jump
        med = np.median(s[keep])
        frozen = idx[(s < 0.25 * med) & keep] + 1
        jumps = idx[(s > 2.2 * med) & keep] + 1
        line = (f"  {t0:g}-{t1:g} s: frozen {len(frozen)} at {[round(float(f) / fps, 2) for f in frozen]}"
                f" | jumps {len(jumps)} at {[round(float(f) / fps, 2) for f in jumps]}"
                f" | evenness {np.std(s[keep]) / med:.2f} | motion {med:.1f}")
        if r is not None and len(r) >= i1:
            line += f" | follows ref {np.corrcoef(s, r[i0:i1])[0, 1]:.2f}"
        print(line)


if __name__ == "__main__":
    main()
