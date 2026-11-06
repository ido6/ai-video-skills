"""Swap pace-matched parts into a film: each part colour-matched to the shot it replaces, the film's own audio kept,
every frame kept, written to a NEW file.

  python splice_parts.py --film final.mp4 --out final_v2.mp4 --part 0:3:partA_paced.mp4 --part 9:15:partB_paced.mp4

A part must already have exactly the frames of the span it replaces (run pace_match.py first); anything else stops
with the counts, because filling the gap by picking nearest frames is what makes a splice stutter.
--no-colour skips the colour match (for parts that are meant to look different).
"""
import argparse, subprocess
import numpy as np
import cv2


def read(path):
    cap, out = cv2.VideoCapture(path), []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(f)
    return out


def cuts(frames):
    g = [cv2.cvtColor(cv2.resize(f, (120, 214)), cv2.COLOR_BGR2GRAY).astype(np.float32) for f in frames]
    d = np.array([np.mean(np.abs(g[i + 1] - g[i])) for i in range(len(g) - 1)])
    return [int(i) + 1 for i in np.flatnonzero(d > max(25.0, 8 * np.median(d)))]


def colour_match(orig, part, reset):
    """LAB mean and spread of each part frame moved onto the original's, calm over time, fresh at every cut."""
    out, cm = [], None
    for i, (a, b) in enumerate(zip(orig, part)):
        if i in reset:
            cm = None
        if b.shape != a.shape:
            b = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_LANCZOS4)
        la = cv2.cvtColor(a, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
        lb = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32)
        cur = np.concatenate([la.mean(0), la.std(0), lb.reshape(-1, 3).mean(0), lb.reshape(-1, 3).std(0)])
        cm = cur if cm is None else 0.8 * cm + 0.2 * cur
        m = np.clip((lb - cm[6:9]) * (cm[3:6] / (cm[9:12] + 1e-3)) + cm[0:3], 0, 255).astype(np.uint8)
        out.append(cv2.cvtColor(m, cv2.COLOR_LAB2BGR))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--part", action="append", required=True, help="start_s:end_s:paced_part.mp4")
    ap.add_argument("--no-colour", action="store_true")
    a = ap.parse_args()
    if a.out == a.film:
        raise SystemExit("write to a new file; the film stays as it is")
    film = read(a.film)
    fps = cv2.VideoCapture(a.film).get(cv2.CAP_PROP_FPS) or 24
    for spec in a.part:
        s, e, path = spec.split(":", 2)
        f0, f1 = round(float(s) * fps), round(float(e) * fps)
        orig, part = film[f0:f1], read(path)
        oc, pc = cuts(orig), cuts(part)
        if len(part) != len(orig) or oc != pc:
            raise SystemExit(f"{path}: {len(part)} frames, cuts {pc}; the span {s}-{e} s has {len(orig)} frames, "
                             f"cuts {oc}. Pace-match it first (pace_match.py --ref).")
        film[f0:f1] = part if a.no_colour else colour_match(orig, part, set(oc))
        print(f"part {s}-{e} s: {len(part)} frames swapped in, cuts {oc}")
    h, w = film[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
                          "-r", f"{fps:g}", "-i", "-", "-i", a.film, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                          "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-profile:v", "high",
                          "-movflags", "+faststart", "-c:a", "copy", a.out], stdin=subprocess.PIPE)
    for f in film:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()
    print("RESULT", a.out, len(film), "frames")


if __name__ == "__main__":
    main()
