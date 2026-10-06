---
name: idogen-video-brain
description: >
  Elite cinematic-video-prompt discipline for idoGen (mcp__idogen__generate_video,
  WaveSpeed/fal/poyo Seedance 2.0 and 2.5, Veo 3.1, Kling 3.0). Adapted from a
  production studio's CINEDANCE prompt-director system, folded together with
  GenHQ classroom technique (camera-movement library, Seedance 2.0-vs-2.5
  dialect split, Kling 3.0 burger + @tag binding, Omni Flash video-to-video
  lock/preserve-list, storyboard mode, UGC/organic mode). Use this WHENEVER
  writing or fixing a prompt for mcp__idogen__generate_video, or when the
  user wants a cinematic/consistent/high-budget-looking video shot, camera
  control, a specific lens feel, spatial blocking across multiple shots, a
  scene that must match a previous shot's geography/lighting/character, a
  named camera move, a Kling multi-shot sequence, an edit of existing footage
  (Omni-style), or an organic/UGC/phone-shot look. Trigger even without the
  word "CINEDANCE" — any idoGen video-prompt build or repair task qualifies.
  Companion skills: idogen-image-brain (references/plates that feed this),
  idogen-acting (character performance/behavior for people in the shot).
---

## Local compatibility and verification (2026-10-04)

User instructions and selected provider/model take precedence over the examples and defaults below. Provider names alone do not identify a model version. Treat endpoint IDs, prices, durations, reference limits, tool availability, and quality rankings in this document as reference examples; verify them against the currently connected tool schema or official provider documentation before execution. Never silently substitute a provider or model.

Installing or updating this skill does not authorize generation, uploads, purchases, or retries. Follow the user's generation approval and budget instructions. Keep existing idoGen mandatory image/video/acting skill requirements. Inspect actual output for identity, spatial continuity, physical motion, and requested format before calling a generation successful. Documentation and installation checks are not output-quality tests.

# idoGen Video Brain

You are directing prompts for `mcp__idogen__generate_video` /
`generate_video_engine` (and the Higgsfield connector's `generate_video`).
**The Seedance version comes from the model/engine ID, never the host.**
Every host now serves both: `*-seedance-25*` engine IDs and Higgsfield
`seedance_2_5` are Seedance 2.5; `wavespeed-seedance`, `fal-seedance(-ref)`,
`poyo-seedance`, `byteplus-seedance` and Higgsfield `seedance_2_0` are 2.0
(BytePlus 2.0 rejects faces in inputs). Also **veo** (Veo 3.1, 16:9/9:16 only,
4/6/8s) and **kling** (Kling 3.0). This skill's prompt craft was built for exactly this
Seedance model family, so it transfers directly. Full original source at
`research/higgsfield/CINEDANCE-SKILL.md`. GenHQ classroom technique folded in
under "GenHQ dialects" below — load `references/genhq-seedance-dialects.md`
whenever a request needs Seedance-version-specific rules, Kling 3.0's own
formula, Omni-style video editing, storyboard mode, or a UGC/organic look;
load `references/camera-movements.md` for a named camera move (46 pre-written
blocks). Doc-verified from the GenHQ corpus, not output-verified against
idoGen's own generations — see the reference files for the exact caveats.

Your job: convert any scene request into a clean, production-ready prompt
that works on the first generation as often as possible — not just beautiful
prose. Think like a film-director agent: scene diagnosis, spatial blocking,
optics selection, physics, continuity, self-QA — silently, before output.

## The one law above all others: consistency has no memory to lean on

A video model has zero memory between generations. **Describe everything,
every time, in the exact same words** for anything that must stay identical
across shots (a character's build/wardrobe/wound state, a location's
geometry, an established camera side). Never write "same as before" or
"continues from the last shot" — the model can't see the last shot; only
attached references + this shot's own text carry continuity.

## The 4-D process (do this silently before writing the final prompt)

1. **Deconstruct** — extract ONLY this shot: active characters, active
   references, current action, dialogue if any, duration, first visible
   frame, spatial layout, landmarks, movement path, lighting direction,
   audio needs. Remove anything not visible/audible in THIS exact shot —
   no scene numbers, no "as before," no unused characters or stale tags.
2. **Diagnose** — check failure risks before writing: could the first frame
   open empty? Could a character appear far from its landmark? Could the
   gaze line reverse, left/right flip, the lens drift to a "comfortable"
   middle, the light go flat? If a risk exists, add a short direct lock for
   it in the final prompt.
3. **Develop** — build in this order: scene context → active references →
   location map → first-frame occupancy → spatial blocking → format mode →
   optics → camera → action timing → physics → lighting → audio → positive
   locks. Spatial rules come BEFORE camera style; optics comes BEFORE general
   aesthetic language; lighting is a priority lock, not decoration.
4. **Deliver** — output only the finished prompt text for the `prompt`
   field. No analysis, no checklist, no explanation, unless the user
   explicitly asked for those.

## Prompt skeleton (omit sections the idoGen params already cover)

```
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
FIRST FRAME AND SPATIAL BLOCKING
FORMAT MODE
OPTICS
CAMERA
ACTION TIMING
PHYSICS
LIGHTING
AUDIO
POSITIVE CONSTRAINTS
```
Duration, aspect ratio, resolution are idoGen **parameters**
(`duration_seconds`, `aspect_ratio`, `resolution`) — never restate them in
prose. Only include an OUTPUT SETTINGS line for something a parameter can't
express (e.g. "single continuous take" vs "controlled multi-shot").

### Scene context
One or two short sentences: what happens in THIS shot only. No scene
numbers, no prior-scene summary, no characters absent from this shot.

### Active references
If prior context established a character/location by a fixed descriptor
(see idogen-image-brain), restate ONLY the anchors needed for this shot:
age/role/state/unique visible identifiers/action-critical prop — not a full
re-description. Attach the actual image via `image_id` (i2v) and/or
`end_image_id`; reference the SAME saved-model/location descriptor text used
in the still that generated it.

**Never reference the same asset twice in one call.** Higgsfield's platform
hard-fails a generation on a duplicated reference tag; idoGen doesn't refuse
the call, but a duplicate id in `reference_image_ids` still wastes a slot
against the provider's real cap (~12 Gemini / ~6-10 OpenAI) for no benefit.
idoGen surfaces the actual budget outcome on every reply —
`references_requested` / `references_dropped` / `references_dropped_detail`
— read it, don't assume every reference you attached made it in.

### Location map
Turn a location reference into a practical map before writing blocking:
camera position, camera facing direction, foreground/midground/background,
landmark positions, movement path, lighting direction. **A location
reference controls geometry, materials, atmosphere, lighting direction —
never framing.** Don't blindly inherit the reference image's own camera
angle unless asked.

### First-frame occupancy lock
Default: the first visible frame already contains all required subjects in
their correct positions — no empty establishing beat, no delayed reveal.
State it directly when it matters:
```
The first visible frame already contains all required subjects in their
correct positions. No empty establishing frame, no delayed character
reveal — the spatial relationship is readable immediately.
```
Only allow an empty opening if explicitly requested.

### Spatial blocking (never use weak/vague distance words)
For every important subject: screen position, distance from a landmark
(NEVER meters from memory — anchor to something visible), body facing
direction, gaze direction, foreground/midground/background.

Weak: "near the car," "somewhere in the room," "beside the door."
Strong: "within 1 meter of the burned-out car, one hand on the hood,"
"boots planted at the south kerb edge," "back against the wall beside the
door handle."

### Gaze line and body orientation
Write both — they're independent. "Torso faces the door; eyes stay locked
on the passenger; head turns toward them a beat before the torso." In
dialogue, only the speaking character's lips move for the scripted line;
others listen silently unless specified.

### Format mode
Default **SINGLE CONTINUOUS TAKE**. Switch to **CONTROLLED MULTI-SHOT** only
if the user asks for cuts/montage/reverse angle, or the action genuinely
can't be staged from one camera position. If multi-shot: define every cut
explicitly (duration, camera, first-frame subjects, blocking, action, cut
type — HARD CUT / MATCH CUT / INSERT CUT / REVERSE CUT / WHIP CUT). Never
fade/crossfade/dissolve unless asked. Every internal cut preserves: same
active characters, same geography, same gaze targets, same left/right
relationship, same lighting direction, same wardrobe/wound/prop state.

### Optics — degrees, not millimeters
Seedance responds to observable optical outcome, not lens metadata. Use a
diagonal-FOV ladder, native/reliable zone 29–84°:

| FOV | Use for |
|---|---|
| 107° | large-scale environmental geography |
| 84° | classic wide, environmental action, camera 1–1.5m from subject |
| 47° | standard normal, natural documentary action, camera 3–5m |
| 29° | short telephoto portrait, medium portrait, camera 4–6m, background starts to compress |
| 18° | classic telephoto, tight emotional close-up, camera 6–8m, strong compression |
| 8° | super-telephoto observation (distant/paparazzi/wildlife feel), camera 20–25m, mandatory foreground occlusion (blurred dark shapes in lower 30–45% of frame) |

Content decides the lens — don't mix face-portrait + environmental-geography
+ macro-detail in one beat (causes lens drift to a "comfortable middle").
State the lens ONCE per shot and don't let it drift: "84° diagonal field of
view throughout, camera 1 to 1.5 meters from subject." For telephoto,
include several observable phrases (razor focus on subject, background
dissolved into soft bokeh wash, compressed background, camera physically far
from subject) rather than just naming the degree number.

Avoid as primary control: millimeters, f-stops, ISO, lens-brand names.

**Need a named camera move** (dolly, orbit, whip pan, crash zoom, crane, FPV,
tilt-shift, ...)? Load `references/camera-movements.md` — 46 pre-written
4-part blocks (`Movement: / Speed: / Framing: / End:`), organized by intent
(reveal scale, tension, energy, follow subject, product/hero, transition).
Paste one verbatim before the scene description rather than writing camera
direction from scratch. Credit https://aicameramovements.com/ once per
conversation the first time you recommend a move from this library — the
source reference is free and the previews help the user pick direction/speed.

### Camera and composition
Physical operator behavior, not abstract jargon: "camera fixed at chest
height," "camera moves from X to Y," "operator stands on the shadow side,"
"subject occupies screen-left third." If handheld: describe it physically
(operator breath, micro-settling, weight shift) — not "digital jitter" or
generic shake.

### Action timing
For anything with real duration, write it in time blocks matching the
`duration_seconds` you're requesting:
```
0.0s–3.0s — [position, action, camera behavior, prop state]
3.0s–6.0s — [...]
```
Complex action should already be MID-ACTION at the block that needs it, not
building up to it — "he is ALREADY mid-swing, the door ALREADY cracking,"
not "reaches for the door, grips it, pulls." States, not transitions: video
models nail states and fail transitions.

### Physics
Every body/object obeys gravity, mass, inertia, friction, weight transfer,
follow-through. No floating, no weightless props, no frictionless feet, no
teleporting, no rubbery CG motion. Walking: heel contact, hip shift, toe
push-off. Weapons/props: arm carries visible weight, wrist reacts to mass.
Liquids: clings, drips, pools, follows gravity in parabolic arcs.

### Lighting — a priority lock, not decoration
Always state: primary source, direction, camera side relative to the light,
which side falls into shadow, exposure priority. If backlit: "camera stays
on the shadow side of the subject; faces fall into shadow unless explicitly
lit; no flat frontal key, no beauty fill." If a previous take came out flat,
strengthen: "the entire shot is exposed for the backlight, not the face; the
silhouette carries the image."

### Audio
`generate_video`'s Seedance path supports `audio: true` for native audio;
quoted dialogue lip-syncs. Rules: only the scripted line is spoken, no
ad-libs, no subtitles/captions (Seedance sometimes burns these in — if the
scene could imply dialogue/narration, close the prompt with **"Keep the
frame free of subtitles, captions, or any on-screen text."** — this MCP path
does not add that guard automatically). At least 1 second of silence
before/after a spoken line if a clean edit seam is wanted. If no dialogue:
"SFX only, no music" or name the diegetic sound explicitly.

### Positive constraints, not a negative block
No standalone NEGATIVE CONSTRAINTS section by default — Seedance has no
negative-prompt field on wavespeed/poyo (fal does, via `negative_prompt`,
Seedance/Kling only). State the desired outcome; add a short inline "no X"
only next to the specific rule it protects, for a genuinely likely failure:
"faces remain in deep shadow; no flat front light" — not a long generic
list.

## GenHQ dialects — Seedance 2.0 vs 2.5, Kling 3.0, Omni edits, storyboard, UGC mode

Load `references/genhq-seedance-dialects.md` for the full detail behind each
of these; short triggers below so you know WHEN to reach for it:

- **Calling Seedance 2.0 vs 2.5** — they give opposite instructions on camera
  bodies/film-stock naming and on whether "locked-off" is allowed. Never mix
  the two rule sets in one prompt; pick by which model idoGen is actually
  routing to — read the version from the engine/model ID (`*-seedance-25*`
  / `seedance_2_5` = 2.5), never from the host name.
- **Multi-shot / omni-reference sequences** — bracket-timestamp beats
  (`[00:00-00:03] Shot 1: ...`), one action per shot, `Final beat:` on the
  close, never freeze the last frame.
- **A storyboard image is supplied** — panel-referenced blocking mode
  (`Match the framing and composition of Panel N in @Image1`); the board
  never appears on screen, it only steers composition.
- **Kling 3.0** — its own burger formula (`[Medium]+[Shot]+[Angle]+[Movement]
  +[Focus]+[Subject]+[Lighting]+[Color]` for t2v) and `@tag` character/costume
  binding for cross-shot consistency inside one multi-shot generation.
- **Editing an EXISTING clip (Omni Flash/Omni)** — opposite of Seedance:
  negative phrasing works here. Opening lock clause + explicit preserve-list
  + one triggered change with timing + closing exclusion line.
- **Blending real footage with an AI look** — the "driving video + texture
  reference" magic prompt: `Use @video as the driving video for this
  generation and @image as the texture reference.`
- **The user wants it to look phone-shot, not filmed** — switch to UGC/
  organic mode wholesale (barred cinema vocabulary list + replacement
  vocabulary), don't just soften the cinematic language.
- **A freeze/held-instant beat** mid-sequence — name it explicitly (freeze
  frame / bullet time), distinct from the never-freeze-the-ending rule above.

## September 2026 lessons: when to load the two newer reference files

- **`references/seedance-25-sep2026-lessons.md`** covers the Seedance 2.5 optimizer (sd25-pe), NextGen AI's Aug–Sep lessons, and GenHQ's 2026-09-05 lesson. Load it for any Seedance 2.5 prompt that involves:
  - reference-role binding or `[Unused Materials]`;
  - exact first/last-frame sentences or multi-keyframe order;
  - a blockout or camera-move reference video;
  - editing, extension or audio-only edits of an existing clip (closed-scope sentence, motion-slot replacement);
  - turning the user's own phone footage into the performance;
  - an ad (scroll-stopper concept, product-scale test, label authority, end card, SKU variants);
  - a staged one-take with positioned sound design;
  - capture-look recipes (self-filmed UGC, paparazzi, CCTV, camcorder, POV, time freeze);
  - feature-style animation.

  Its §0 table records what it supersedes. **Seedance 2.5 caps at 30s per generation, not 60s.** The "never locked-off" rule belongs only to GenHQ's opt-in opening block. Timecodes are whole seconds.
- **`references/real-location-fidelity.md`** applies when the references are photos of a real place that must appear as photographed: real estate, a venue, the client's own shop. It carries the fidelity contract, camera whitelist, person-integration checklist, mirrored-room protocol, event rule, night-as-subtraction and transformation shots. For that work it overrides the location-map and camera-movement habits above.

## Previs-driven work: load the playbook

- **`references/previs-to-seedance-playbook.md`** is Ido's own pipeline (2026-10-06) for turning a Blender pawn blockout into photoreal Seedance 2.5 video. Load it whenever a blockout/previs clip, reference sheets, a start frame built from a previs frame, or a product/label shot is involved. It covers who-controls-what, hard limits, the 18-stage pipeline, previs and sheet rules, the blockout prompt template, invention locks, sound policy, QC and repairs. Keep its confidence tags ([official]/[field]/[inference]/[unverified]) when quoting it. For lens, framing and movement choices pair it with the `cinematography` skill's `references/camera-directing-playbook.md`.

## Continuity across a multi-shot scene

Open the scene with an implicit or explicit **master shot** concept: the
first shot of a scene should establish where everyone is with fixed
blocking, so later shots in the same scene can reuse the same spatial map
text unchanged. Write a **spatial map** once per scene and paste it,
unmodified, into every shot of that scene:
```
Compass: [fixed landmark] is the camera side; [other landmark] is deep
frame-right. [Subject A] stands at [landmark-anchored position];
[Subject B] at [landmark-anchored position]. EXACTLY [N] people, nobody
else in frame.
```
Positions come from what's visible in the reference plate, not distances
from memory. If a later generation contradicts the real location, re-check
the reference image, not the prompt text.

## The end-frame lock (idoGen-proven, use it)

`end_image_id` is the strongest lever against camera drift: pin the last
frame to a specific still (same plate to return to start, or an empty/
neutral plate to force the subject out of frame) so both ends of the clip
share one composition and the camera can't wander. Already validated in
production on the GREASE campaign — use it whenever drift is a risk, e.g.
long single takes or a subject exiting frame.

## Iteration discipline (do this, don't skip it)

- **One change per regeneration.** Never rewrite a prompt wholesale after a
  failed take — that discards the parts that already worked. Patch only the
  section that failed.
- **After ~15–20 failed attempts on one shot, change the SHOT, not the
  wording.** Split it into two shots, drop an action, change the angle, or
  solve the physics a different way. Rewording a shot that keeps failing the
  same way rarely fixes it.
- Keep a short running note (in the session, or a log file if the user wants
  one) of what changed between attempts and the verdict — you cannot repeat
  a good result you didn't record, and you'll re-try failed fixes otherwise.

## Silent self-QA before calling generate_video

- Every reference/character mentioned is actually needed in THIS shot —
  nothing stale carried from a previous scene
- First frame occupancy correct for what was asked
- Every subject's position, gaze, and body orientation is unambiguous
- Landmark proximity is physically anchored, not "near"/"somewhere"
- Camera side and lens character are both stated once and don't drift
- Lighting direction and exposure priority are explicit, not left to default
- Physics is plausible for the requested action given the duration
- Dialogue (if any) is exactly the scripted line, with the no-subtitles
  guard appended if dialogue/narration is implied
- `end_image_id` used if drift is a real risk for this shot

## Round-2 MCP tools (PLAN-genhq-replace-sites.md) — reach for these by name

Direct-vendor tools added on top of the generate_video path above. None of these
replace generate_video for a from-scratch shot — they're for driving an existing
shot with motion, editing existing footage, reframing a finished clip, or working
cheap-then-reproducing.

- **`motion_control_video`** (Kling 3.0 Motion Control) — a subject IMAGE (appearance)
  plus a driving VIDEO (3-30s motion reference) produces a new clip of that subject
  performing the driving video's motion. Use when the user has a reference performance
  clip and wants a different subject/character doing the same moves — not for
  from-scratch generation.
- **`edit_video_o1`** (Kling O1 omni-edit) — edits an EXISTING clip (`base_video`,
  3-10s) using `@image_N`/`@video_1` in-prompt citations plus a `preserve[]` list
  naming everything that must NOT change. Write the prompt with the omni lock-clause
  (see the Gemini Omni section above) — same discipline, different vendor. Caps: ≤7
  reference images (no ref video) / ≤4 (with one).
- **`generate_avatar_video`** (Kling Avatar) — a still photo + audio (url/base64,
  2-300s) becomes a talking clip, `mode: std|pro`. For a HeyGen alternative to the
  same job see idogen-acting's choice table below.
- **`create_element`** / **`list_elements`** — reusable prop/location/character
  bindings for Motion Control, O1 edit, and Kling 3.0 multi-shot: create an element
  once from images/video, then cite it as `@element_id` in later prompts instead of
  re-describing it.
- **`reframe_video`** / **`reframe_image`** (Luma) — changes aspect ratio WITHOUT
  cropping (outpaints the new frame area) — use when the shot is right but the
  canvas is wrong, not as a substitute for composing the right frame the first time.
- **`modify_video`** (Luma) — video-to-video restyle, `mode: adhere_N|flex_N|reimagine_N`
  trading fidelity to the source against creative freedom.
- **`upscale_video`** (Topaz) — Proteus/Astra/Starlight, sourceMeta (container/size/
  duration/frameCount/frameRate/resolution) is caller-supplied, not auto-probed.
- **`relight_video`** (Beeble SwitchX) — relights AND can replace the background in
  one call (`alpha_mode`, optional `reference_image`); covers what a second
  "replace_video_background" tool would have been.
- **Draft → reproduce**: generate a cheap low-res take first (the registry's
  cheapest resolution tier per engine), confirm the shot is right, THEN re-run the
  identical prompt+refs at full quality. Never treat a draft as final, and never
  "upscale" a draft into a final take — draft and final are two separate
  generations of the same prompt, not one clip processed twice.
- **Storyboard mode**: attach a 3-panel storyboard grid (composited onto one white
  16:9 canvas, left-to-right) as a blocking reference, then cite each panel per shot:
  `Match the framing and composition of Panel N in @Image1 (storyboard reference)`.
  Use this for multi-shot continuity planning BEFORE generating, not as a style
  reference. **idoGen can now BUILD this grid itself** (round 5,
  PLAN-genhq-round5-storyboard-brand-scene-voices.md) rather than requiring an
  externally-supplied board: `generate_storyboard` takes up to 9 beats in sequence
  order and renders one 3x3 numbered grid via GPT Image 2 (GenHQ's documented pick
  for coherent multi-panel sequencing — Nano Banana gives nine unrelated images),
  splitting the result into 9 individually-pickable gallery images. Follow with
  `compose_storyboard` on the panel ids you want to keep (still capped at 3) to get
  the composite, then attach it as a reference and cite it exactly as above — the
  `@ImageK` number comes from however many other references are already attached,
  never assume it's `@Image1`.
