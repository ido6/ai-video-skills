"""Pace-match a clip: every output frame is a source frame or an optical-flow in-between, never a skipped or repeated one.

With a reference (the shot the clip replaces): for every reference frame, find the moment in the clip that looks most
like it (a fraction between two frames, from a parabola through the best match), smooth that mapping, keep it moving
forward, and draw the frame at that moment. The clip then moves exactly like the reference.
Without a reference: drop the clip's frozen frames and respace what is left evenly over --frames frames.
Works shot by shot (cuts found in both clips; or give --shots) so each cut lands on its exact frame.
Frames are compared with brightness and contrast evened out, so a change of light is not mistaken for motion or a freeze.
A clip with no reference and no frozen frames is copied through unchanged (--force redraws it anyway).
The sound of --audio-from (default: --ref, else --edit) goes under the result, trimmed or padded to the exact frame count.

  python pace_match.py --edit ai.mp4 --ref original_part.mp4 --out paced.mp4
  python pace_match.py --edit ai.mp4 --frames 96 --out paced.mp4                 (no reference: 96 frames per shot)
  python pace_match.py ... --shots "0-72:0-69,72-144:69-137"                       (ref range:edit range, frame indices)
  python pace_match.py ... --engine rife --rife C:/tools/rife-ncnn-vulkan.exe --gpu 1   (sharper, needs rife-ncnn-vulkan)
"""
import argparse, os, subprocess, tempfile
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


def small(f):
    """Small blurred grey frame with brightness and contrast evened out, so a light change does not read as motion."""
    g = cv2.cvtColor(cv2.resize(f, (135, 240), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 1.0)
    return (g - g.mean()) / (g.std() + 1e-3) * 40.0 + 128.0


def changes(frames):
    s = [small(f) for f in frames]
    return np.array([np.mean(np.abs(s[i + 1] - s[i])) for i in range(len(s) - 1)])


def cuts(frames):
    d = changes(frames)
    return [int(i) + 1 for i in np.flatnonzero(d > max(25.0, 8 * np.median(d)))]


def unfrozen(frames, ratio):
    """Indices of the frames to keep: a frame that barely differs from the one before it is a freeze and is dropped."""
    if len(frames) < 3:
        return list(range(len(frames)))
    d = changes(frames)
    med = np.median(d)
    return [0] + [i + 1 for i, v in enumerate(d) if v >= ratio * med]


def match_mapping(ref, clip):
    """Fractional clip index for every reference frame: best match, sub-frame refined, smoothed, monotonic."""
    sr, sc = [small(f) for f in ref], [small(f) for f in clip]
    raw = []
    for g in sr:
        err = np.array([np.mean((g - h) ** 2) for h in sc])
        j = int(np.argmin(err))
        if 0 < j < len(err) - 1:
            a, b, c = err[j - 1], err[j], err[j + 1]
            den = a - 2 * b + c
            j = j + (0.5 * (a - c) / den if den > 1e-6 else 0.0)
        raw.append(float(j))
    raw = np.array(raw)
    k = 5                                                    # smooth out matching noise, keep real changes of pace
    sm = np.convolve(np.pad(raw, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
    sm[0], sm[-1] = raw[0], raw[-1]
    return np.maximum.accumulate(np.clip(sm, 0, len(clip) - 1))


def between_opencv(fa, fb, alpha, dis):
    h, w = fa.shape[:2]
    ga = cv2.cvtColor(cv2.resize(fa, (w // 2, h // 2)), cv2.COLOR_BGR2GRAY)
    gb = cv2.cvtColor(cv2.resize(fb, (w // 2, h // 2)), cv2.COLOR_BGR2GRAY)
    fab = cv2.resize(dis.calc(ga, gb, None), (w, h)) * 2
    fba = cv2.resize(dis.calc(gb, ga, None), (w, h)) * 2
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    al = np.float32(alpha)
    wa = cv2.remap(fa, xs - al * fab[..., 0], ys - al * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    wb = cv2.remap(fb, xs - (1 - al) * fba[..., 0], ys - (1 - al) * fba[..., 1], cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT)
    return cv2.addWeighted(wa, float(1 - alpha), wb, float(alpha), 0)


def between_rife(fa, fb, alpha, exe, model, gpu, work):
    pa, pb, po = (os.path.join(work, n) for n in ("a.png", "b.png", "o.png"))
    cv2.imwrite(pa, fa, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    cv2.imwrite(pb, fb, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    subprocess.run([exe, "-0", pa, "-1", pb, "-o", po, "-m", model, "-s", f"{alpha:.4f}", "-g", str(gpu)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return cv2.imread(po)


def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0",
                        path], capture_output=True, text=True)
    return bool(r.stdout.strip())


def frame_count(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", path], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def add_audio(video, source, out, frames, fps):
    """Mux the source's sound under the new video. Padded with silence or trimmed to the video's exact length, never
    with -shortest, which drops the last frames when the audio track ends early."""
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-i", source, "-map", "0:v", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", f"{frames / fps:.6f}", out],
                   check=True)


def shot_pairs(ref, clip, spec):
    if spec:
        return [tuple(tuple(int(v) for v in part.split("-")) for part in s.split(":")) for s in spec.split(",")]
    rc, cc = cuts(ref), cuts(clip)
    if len(rc) != len(cc):
        raise SystemExit(f"cuts differ (reference {rc}, clip {cc}): pass --shots")
    rb, cb = [0] + rc + [len(ref)], [0] + cc + [len(clip)]
    return list(zip(zip(rb, rb[1:]), zip(cb, cb[1:])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edit", required=True, help="the clip to fix")
    ap.add_argument("--ref", help="the shot(s) it must move like; omit to respace evenly")
    ap.add_argument("--frames", default="", help="no reference: frames per shot, one number or a comma list")
    ap.add_argument("--shots", default="", help="ref_from-ref_to:clip_from-clip_to,... (frame indices)")
    ap.add_argument("--freeze", type=float, default=0.25, help="a change under this share of the median is a freeze")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=0, help="output fps (default: the reference's, else the clip's)")
    ap.add_argument("--engine", choices=("opencv", "rife"), default="opencv")
    ap.add_argument("--rife", help="path to rife-ncnn-vulkan.exe")
    ap.add_argument("--rife-model", default="rife-v4.6")
    ap.add_argument("--gpu", type=int, default=0, help="Vulkan GPU id for RIFE (rife-ncnn-vulkan -v lists them)")
    ap.add_argument("--audio-from", help="file whose sound goes under the result (default: --ref, else --edit)")
    ap.add_argument("--no-audio", action="store_true", help="write the video without sound")
    ap.add_argument("--force", action="store_true", help="redraw even a clip that has nothing to fix")
    a = ap.parse_args()

    clip = read(a.edit)
    ref = read(a.ref) if a.ref else None
    fps = a.fps or cv2.VideoCapture(a.ref or a.edit).get(cv2.CAP_PROP_FPS) or 24
    if ref is not None and clip[0].shape != ref[0].shape:
        clip = [cv2.resize(f, (ref[0].shape[1], ref[0].shape[0]), interpolation=cv2.INTER_LANCZOS4) for f in clip]
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    work = tempfile.mkdtemp(prefix="pace_")
    model = os.path.join(os.path.dirname(a.rife or ""), a.rife_model)

    def draw(fa, fb, al):
        if al < 0.02:
            return fa
        if al > 0.98:
            return fb
        return between_rife(fa, fb, al, a.rife, model, a.gpu, work) if a.engine == "rife" else between_opencv(fa, fb, al, dis)

    if ref is not None:
        pairs = shot_pairs(ref, clip, a.shots)
    else:
        cb = [0] + cuts(clip) + [len(clip)]
        pairs = [(None, c) for c in zip(cb, cb[1:])]
    targets = [int(v) for v in a.frames.split(",") if v]
    if ref is None and not targets and not a.force and all(
            len(unfrozen(clip[c0:c1], a.freeze)) == c1 - c0 for _, (c0, c1) in pairs):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.edit, "-map", "0", "-c", "copy", a.out], check=True)
        print(f"already smooth: no frozen frames to drop, copied {a.edit} unchanged (pass --force to redraw)")
        print("RESULT", a.out, frame_count(a.out), "frames")
        return
    out = []
    for n, (r, (c0, c1)) in enumerate(pairs):
        shot = clip[c0:c1]
        keep = unfrozen(shot, a.freeze)
        kept = [shot[i] for i in keep]
        if r is not None:
            t = match_mapping(ref[r[0]:r[1]], kept)
        else:
            want = targets[min(n, len(targets) - 1)] if targets else len(shot)
            t = np.linspace(0, len(kept) - 1, want)
        for x in t:
            j = int(np.floor(x))
            out.append(kept[j] if j + 1 >= len(kept) else draw(kept[j], kept[j + 1], x - j))
        steps = np.diff(t)
        print(f"shot {n + 1}: clip frames {c1 - c0} (dropped {len(shot) - len(kept)} frozen) -> {len(t)} frames; "
              f"clip frames per output frame {np.median(steps):.2f} (min {steps.min():.2f}, max {steps.max():.2f})")
    h, w = out[0].shape[:2]
    source = a.audio_from or a.ref or a.edit
    sound = not a.no_audio and has_audio(source)
    target = os.path.join(work, "video.mp4") if sound else a.out
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
                          "-r", f"{fps:g}", "-i", "-", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", target],
                         stdin=subprocess.PIPE)
    for f in out:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()
    if sound:
        add_audio(target, source, a.out, len(out), fps)
    got = frame_count(a.out)
    if got != len(out):
        raise SystemExit(f"frame count mismatch: wrote {len(out)}, file has {got}")
    print("RESULT", a.out, got, "frames", f"(sound from {source})" if sound else "(no sound)")


if __name__ == "__main__":
    main()
