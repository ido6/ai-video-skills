"""Find the frame where something happens in one area of a clip (an object appears, starts to move, jumps),
so a clip can be cut just before it.

  python find_moment.py clip.mp4 --roi 0,0.5,1,0.5 --from 3 --to 4.5 --out sheet.jpg

--roi is x,y,w,h as fractions of the frame (0,0.5,1,0.5 = the bottom half). The script prints, for every frame in the
range, how much that area changed compared with the whole frame (light evened out, camera drift subtracted), ranks the
biggest local changes, and writes a contact sheet of the area with each frame's time and number drawn on it (no font
files needed). Look at the sheet around the top-ranked frames; the cut goes on the frame before the event starts.
"""
import argparse
import numpy as np
import cv2


def level(g):
    return (g - g.mean()) / (g.std() + 1e-3) * 40.0 + 128.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--roi", default="0,0,1,1", help="x,y,w,h as fractions of the frame")
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=1e9)
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--width", type=int, default=220, help="width of each tile in the sheet")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--out", default="moment_sheet.jpg")
    a = ap.parse_args()
    x, y, w, h = (float(v) for v in a.roi.split(","))
    cap = cv2.VideoCapture(a.clip)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    tiles, rows, prev_r, prev_f, n = [], [], None, None, 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        t = n / fps
        if t > a.t1:
            break
        H, W = f.shape[:2]
        crop = f[int(y * H):int((y + h) * H), int(x * W):int((x + w) * W)]
        g_full = level(cv2.cvtColor(cv2.resize(f, (135, 240)), cv2.COLOR_BGR2GRAY).astype(np.float32))
        g_roi = level(cv2.cvtColor(cv2.resize(crop, (160, max(1, int(160 * crop.shape[0] / crop.shape[1])))),
                                   cv2.COLOR_BGR2GRAY).astype(np.float32))
        if t >= a.t0:
            if prev_r is not None:
                local, whole = float(np.mean(np.abs(g_roi - prev_r))), float(np.mean(np.abs(g_full - prev_f)))
                rows.append((n, t, local, local - whole))
            tile = cv2.resize(crop, (a.width, int(a.width * crop.shape[0] / crop.shape[1])))
            label = f"{t:.3f}s f{n}"
            cv2.putText(tile, label, (5, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(tile, label, (5, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            tiles.append(tile)
        prev_r, prev_f, n = g_roi, g_full, n + 1
    if not tiles:
        raise SystemExit("no frames in that range")
    while len(tiles) % a.cols:
        tiles.append(np.zeros_like(tiles[0]))
    sheet = np.vstack([np.hstack(tiles[i:i + a.cols]) for i in range(0, len(tiles), a.cols)])
    cv2.imwrite(a.out, sheet)
    print(f"{a.clip}: {fps:g} fps, frames in range {len(rows) + 1}, sheet {a.out}")
    for n, t, local, excess in rows:
        print(f"  f{n:4d} {t:6.3f}s area change {local:5.2f} beyond whole frame {excess:+5.2f}")
    print("biggest local changes (likely events):")
    for n, t, local, excess in sorted(rows, key=lambda r: -r[3])[:a.top]:
        print(f"  f{n} at {t:.3f}s ({excess:+.2f}); cut before it: --frames {n} / -t {n / fps:.3f}")


if __name__ == "__main__":
    main()
