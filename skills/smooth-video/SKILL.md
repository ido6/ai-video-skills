---
name: smooth-video
description: "Make joined AI video play smoothly by pace-matching: every frame is a real frame or an optical-flow in-between, never a skipped or repeated one. Use when an AI edit (Seedance video edit, Kling, Luma, any v2v) comes back longer or shorter than the part it replaces and must go back into a film; when several AI clips are joined into one video; or when a finished AI video stutters, has stuck/frozen frames or jitter ('גיטרים', 'תקוע', 'קופץ')."
---

# Smooth video (pace-match)

AI video tools rarely return the length they were given, and they add **freezes** (a frame that barely differs from the one before) of their own. Fitting a clip to a slot by picking the nearest frame then skips some frames and repeats others: that is the stutter. **Pace-match** instead: every output frame is either a source frame or an optical-flow in-between drawn at the exact moment it needs, and, when the clip replaces a part of a film, timed to move exactly like the part it replaces.

Tools: `scripts/` beside this file. They need Python with `opencv-python` + `numpy`, and `ffmpeg` on PATH. Every script writes a **new** file; the source video stays as it is.

## Steps

1. **Measure.** Run `python scripts/check_smooth.py <clip>` on every clip involved, and on the film (`--ref` the original when there is one). Done when you know, for each part: its frame count vs the span it must fill, where its cuts are, and its frozen frames.
2. **Pace-match each part.** Pick the branch:
   - **Replaces a part of a film** (the original part exists): cut that exact span out of the film (`ffmpeg -ss <start> -t <len>`, re-encoded so frames are exact), then `python scripts/pace_match.py --edit <ai_part> --ref <original_span> --out <part_paced>`. Shots and cuts are paired automatically; when cut counts differ, pass `--shots ref_from-ref_to:clip_from-clip_to,...`.
   - **A clip with no reference** (joining raw AI clips, or a stuttering clip): `python scripts/pace_match.py --edit <clip> --out <clip_paced>` drops the freezes and respaces it evenly to its own length, or to `--frames N`.
   Done when every paced part prints exactly the frame count of its span, shot by shot, with each cut on the same frame as the original.
3. **Put it together.**
   - **Parts into a film:** `python scripts/splice_parts.py --film <film> --out <film_v2> --part <start_s>:<end_s>:<part_paced> ...`. It colour-matches each shot to the one it replaces, keeps the film's audio and every frame, and refuses a part whose frame count does not match.
   - **Clips into one video:** first make every clip the same size and fps, then join them with `ffmpeg -f concat` or the concat filter, re-encoding.
   Done when the new file has the expected total frame count (`ffprobe -count_frames`).
4. **Verify against the reference.** Run `python scripts/check_smooth.py <new> --ref <original> --ranges <each edited span>`, and the same on the original (without `--ref`) for its own counts. Done when, in every edited span that has movement:
   - frozen frames are at or below the reference's count (a held pose is frozen in the reference too);
   - jumps are no more than the reference's;
   - "follows ref" is 0.85 or higher where the subject moves.
   A span where only the camera drifts (an empty shot, a slow creep zoom), or with motion under about 2, scores lower on "follows" because the AI redraws the handheld drift; judge it by eye, frozen frames and jumps still at or below the reference's. Then show the user a side-by-side, and a half-speed version of the edited spans (`setpts=2*PTS`), before calling it finished.

## Gotchas (seen on real runs)

- **Seedance video edit changes the length.** A 3 s input came back 4.04 s (slowed down 1.35×); a 6 s input came back 5.7 s. Its outputs also had 1–3 freezes of their own. Send inputs of 4 s or more that start and end on cuts. Never trust the returned length: pace-match every time.
- **Replace whole shots.** Swapping edited frames in mid-shot shows a jump where the original and the edit meet. Cut each part from cut to cut.
- **An audio track shorter than the video** makes `ffmpeg -shortest` drop the last frames. `splice_parts.py` keeps every frame.
- **Colour:** match per shot and start fresh at each cut, so one shot's grade never bleeds into the next.

## Engines

- **OpenCV DIS optical flow** (default, `--engine opencv`): chosen as the default after a side-by-side test. It's as smooth as RIFE, needs only `opencv-python`, no GPU needed.
- **RIFE** (`--engine rife --rife <rife-ncnn-vulkan.exe> --gpu 1`): about 10% sharper during fast motion such as crash zooms, but about 2.5 s per frame. It needs `rife-ncnn-vulkan` (github.com/nihui/rife-ncnn-vulkan, about 430 MB): ask the user before downloading it. `rife-ncnn-vulkan -v` lists the GPU ids; on a laptop with Intel + NVIDIA graphics the NVIDIA card is usually 1.
- **Still not smooth enough:** Topaz Video AI (Apollo or Chronos) run on the raw AI clips. The user runs it; prepare the clips and the exact frame counts for them.
