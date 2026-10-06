# GenHQ Seedance / Kling / Omni dialects

Ported into idoGen from the GenHQ classroom corpus (PLAN-genhq-integration.md Phase 6,
`research/genhq/digest/CLAUDE_SKILLS.md` §4.1, `VIDEO_TOOLS.md` §2.1-2.7, §2.17). Doc-verified
against the GenHQ source skills, not output-verified against idoGen's own generations —
treat every rule below as a documented convention to try, not a proven fact about how
idoGen's Seedance/Kling/Omni providers actually behave.

idoGen already ships its own Seedance dialect (`buildVideoPrompt({ dialect: 'seedance' })`
in `app/lib/videoPresets.ts`, plus `SEEDANCE_REALISM_CONSTRAINT` — see CLAUDE.md "Video
realism is a SEPARATE layer from image realism"). The material below is a second,
independent layer of technique on top of that: when to use it, and where it disagrees
with idoGen's own already-shipped code.

## 1. Seedance 2.0 vs 2.5 — they give OPPOSITE instructions, on purpose

This is the sharpest documented contradiction in the whole corpus (CLAUDE_SKILLS.md
§4.1), and it is about **model behaviour**, not house style:

| | Seedance 2.0 (2026-04 guide, `seedance-genhq`) | Seedance 2.5 (`seedance-25`, 2026-08) |
|---|---|---|
| Camera bodies / film stock | **Banned** — "the model has no concept of camera brands... meaningless to the model" | **Mandatory, verbatim, every prompt** — fixed opening line names an exact body, lens set, and film stock |
| Locked-off / static camera | A normal, recommended camera term | **Banned in shot text** — the mandatory opening block commits every shot to handheld micro-drift; write "handheld micro-drift, frame effectively still" instead. (2026-09: this ban comes with GenHQ's opening block, not from the model; Sep 2026 Seedance 2.5 prompts without that block use locked-off shots deliberately — interview, CCTV, end holds, transformation shots.) |
| Duration | Hard-capped 4-15s | ~~No hard cap, up to ~40 shots at 60s~~ (2026-08 claim, **superseded 2026-09**: the Seedance 2.5 optimizer and all Sep lessons cap one generation at **30s** — plan longer pieces as linked ≤30s segments; see `seedance-25-sep2026-lessons.md` §0) |
| Per-shot lens numbers (`85mm`, `f/2.8`) | 2.0 guide says use them; both Seedance skills say the model ignores per-shot mm specs and treats lenses as buckets | Same bucket rule, but the mandatory OPENING block itself does carry hard specs as a whole-sequence look signature |

**Read this as a version boundary, not a bug in either source**: the 2.0-era guidance and
the 2.5-era `seedance-25` skill are each internally consistent, they just disagree with
each other because the underlying model changed. **Pick by which Seedance model idoGen is
actually calling** (2.0 via WaveSpeed/fal/Poyo vs 2.5 via BytePlus/`seedance-25`-style
providers), never mix the two rule sets in one prompt, and don't silently prefer the
newer one just because it's newer — CLAUDE.md already records that idoGen's own Seedance
dialect work is doc-verified only, so treat any of this as an A/B candidate, not a default.

**The Seedance 2.5 mandatory opening block** (verbatim from `seedance-25`, for reference —
this is GenHQ's own house style, not something idoGen's code emits automatically):
```
Arricam LT, Cooke S4/i primes, 35mm Kodak Vision3 500T, 1.85:1 spherical, T2.8, shallow depth of field, halation on highlights, fine organic grain, lifted milky blacks, low contrast, no sharpening, no HDR.

[GRADE NAME] grade: [hero tone] as the hero tone, [dominant field colour] field, [ground/base tone], [shadow character], [atmospheric quality]. Handheld with micro-drift, never locked off. Naturalistic performance, real dialogue sync, no music.
```
If a user explicitly wants this exact "GenHQ look," it composes as an opt-in preset
layered on top of idoGen's existing Seedance dialect — never swap it in as the silent
default, and never mix `ARRI ALEXA` / `65mm IMAX` language into the same shot as this
block (they conflict — see the "Named Camera Bodies" note below).

**Avoid the word "fast" in Seedance prompts (both 2.0 and 2.5).** It is the single most
reliable trigger for jitter/motion-artifact in both versions. Use "decisive," "snap,"
"controlled quick," "kinetic," "rapid" instead — the same rule idoGen's own CLAUDE.md
notes elsewhere for a different reason (jitter, not just style).

**Direction vocabulary (both 2.0 and 2.5).** Seedance reads rotation more reliably as a
clock direction or a degree count than as screen-relative "left"/"right", which is
ambiguous between camera-relative and subject-relative. Rewrite: `pans left`/`turns
left` → `rotates anti-clockwise`; `pans right`/`turns right` → `rotates clockwise`; a
bare "turns" with no direction → `turns roughly N degrees` (pick a concrete number —
45/90/180 — rather than leaving the amount vague). This is a phrasing convention to
apply by hand when writing a Seedance shot, not something idoGen's `buildVideoPrompt`
rewrites automatically today.

## 2. Bracket-timestamp beats (multishot / omni-reference mode)

When a generation is genuinely multi-shot (several reference images each pinned to a
different beat, not just one continuous take), GenHQ's convention is to open each beat
with a bracketed timestamp — this is read as a hard editorial-cut instruction, distinct
from a continuous take:

```
[00:00-00:03] Shot 1: <subject + action first, camera and style modify it, not define it>
[00:03-00:06] Shot 2: ...
```

Rules that make this reliable:
- **One clear action per shot.** Multiple competing actions and the model butchers at least one.
- **Front-load the subject** — the first 20-30 words of each shot get the most weight.
- ~~**Fractional seconds are fine** (`[00:00-00:03.5]`)~~ — superseded 2026-09: the Seedance
  2.5 optimizer treats ranges as event budgets and never claims 0.5s precision, and the Sep
  lessons use **whole seconds only**. Timestamps must still tile the runtime contiguously —
  no gaps, no overlaps.
- **Word count scales with shot length** — roughly 10-15 words per second of shot.
- **Mark the final beat**: the last shot opens with `Final beat:` and keeps motion alive
  through the closing frame (drifting steam, a settling breath, decelerating push) —
  never freeze-frame language ("hold on the hero frame," "frozen mid-air"). (2026-09 carve-out:
  a *designed* brand end card or game title card may hold static — name it as a card, strip
  the live-action treatment from it; the rule above still governs live-action closers.)
- **@Image references are named inline** in whichever shot uses them ("Open on @Image1
  as the first frame...", "The product from @Image2 sits on..."). Filler shots that
  don't tie to a reference use no @mention.

This is the same shape as idoGen's own `SEEDANCE_REALISM_CONSTRAINT`/`SEEDANCE_SUBTITLE_GUARD`
approach — a small, precisely-worded addition near the end of the compiled prompt — so it
composes naturally with idoGen's existing subject-first Seedance reordering.

## 3. Storyboard mode (a Director feature idoGen doesn't have yet)

When a user supplies a **storyboard image** (a single frame holding multiple numbered
panels) alongside separate character/asset references, the storyboard is a **blocking
guide that never appears on screen** — it only steers framing and composition; the other
references supply the actual on-screen subjects.

Invoke it inline, per panel:
```
Match the framing and composition of Panel N in @Image1 (storyboard reference).
```
then describe the real subjects using their own references in the same shot (`@Image2`,
`@Image3`, ...). Give every distinct entity its own `@mention` — never reuse one label
for two different characters. Shot order is then fixed by panel order (skip any
shot-ordering question you'd otherwise ask).

This is a real gap in idoGen's Director planner today (no storyboard-image input exists),
so treat this section as technique to reach for manually when a user hands you a
storyboard image and asks for a matching video sequence — not as something idoGen's UI
currently automates.

## 4. Transition families + editing-style map

Every shot in a multishot sequence should specify BOTH its exit and the next shot's
entry — never a bare "cut to Shot N." Four families, pick from the one that matches the
locked editing style; don't mix energies within one sequence:

1. **Cuts** — hard cut (default), match cut (shared compositional/movement element
   bridges the two shots), smash cut (jarring, deliberate energy shift).
2. **Camera-driven** — push-in to push-in, pull-out to pull-out, match-on-motion with
   direction, whip pan with direction, through-the-object, crash zoom. The camera's own
   motion IS the bridge; **speed-ramp across the cut** (outgoing shot accelerates into
   it, incoming shot decelerates out of it) is what sells continuity.
3. **In-frame element** — an object/hand/shadow/light wipes across frame and reveals the
   next shot, motivated by something visible (never a generic "flash to white").
4. **Optical** (use sparingly) — cross dissolve, fade to black, unmotivated flash to
   white. Easy to overuse; reads as beginner editing when leaned on too hard.

Editing-style → family fit: calm/sensorial leans hard cut + slow push-in-to-push-in +
light wipe (avoid whip pan/crash zoom/smash cut); high-energy/kinetic leans smash cut +
whip pan + crash zoom + speed-ramp transitions (avoid cross dissolve/fade to black).

## 5. Kling 3.0 — the burger formula + @tag character/costume binding

Kling 3.0 has its own "burger" prompt formula, distinct from Seedance's subject-first
reordering. Two shapes, pick by mode:

**Text-to-video:**
```
[Medium] + [Shot] + [Angle] + [Movement] + [Focus] + [Subject] + [Lighting] + [Color]
```

**Multi-shot / image-to-video:**
```
[camera angle + shot-type], [camera movement], [action/sequence], [subject/enviro shifts], [dialogue], [SFX/music]
```

**`@tag` binding for cross-shot consistency inside one multi-shot generation**: Kling
lets you bind a character or costume to a tag (`@Josi`, `@Ugg`) and combine them
(`@JOSI + @UGG`) so the same face/outfit holds across every shot in that one generation —
GenHQ's own material calls this "Hot Tip: Bind characters when using multi-shot for
consistency." Kling also supports dialogue delivery direction written inline before the
quote (`he says: (gravelly cockney london gangster voice) "he's a liability that bloke."`)
and inline SFX cues (`SFX: Two distinct 'spritz' sounds followed by a satisfied "Mmm."`).

**Motion Control**: up to 30s of driving footage can be uploaded to transfer body
language + lip sync onto a generation — useful for expressive acting or branded-avatar
content. Strip the driving footage's audio and replace with a clean voice (e.g.
ElevenLabs) if the original audio isn't usable.

## 6. Omni-family video editing — lock clause + preserve-list (opposite of Seedance)

Google Omni Flash / Omni edits an EXISTING clip rather than generating from scratch — "the
Nano Banana of video." **Unlike Seedance, negative phrasing works reliably here and is
used constantly.** The reusable pattern, present in every real GenHQ Omni example:

1. **An opening lock clause** — `Modify the reference video.` / `Lock the original video
   completely.` / `keep this video the same but...` / `CRITICAL: Maintain the EXACT same
   camera angle and framing.`
2. **An explicit preserve-list** naming every element that must not move (people, camera,
   background objects, weather, wardrobe not being changed).
3. **The single change**, with its trigger and second-by-second timing (e.g. "at the exact
   moment he snaps his fingers, a wave rises...").
4. **A closing exclusion line** — `No cuts, no zoom, no camera change. Only add ...`

10-second maximum duration per Omni Flash generation — trim and process longer footage in
10s chunks.

## 7. Hybrid real-footage workflow: driving video + texture reference

For blending real (phone/camera) footage with an AI cinematic look, the GenHQ "magic
prompt" pattern is:

```
Use @video as the driving video for this generation and @image as the texture reference.
```

Workflow: film the real footage first (the "driving video" — it supplies motion/timing/
performance) → grade a still frame of it into the target cinematic look with an image
model → feed BOTH back into the video generator, the graded still as the "texture
reference," the raw footage as the "driving video." The generator preserves the real
footage's motion while re-texturing it to match the graded still. This is the technique
behind idoGen's own `openRemoteMediaStream`-adjacent video-to-video paths conceptually,
though idoGen has no dedicated UI for it yet — reach for it manually when a user wants to
stylize real footage rather than generate from nothing.

## 8. UGC / organic mode — when the request wants it to look phone-shot, not filmed

Everything under `idogen-video-brain`'s main SKILL.md targets a CINEMATIC register. When
a request is explicitly for UGC / social / "looks like a real person shot this on their
phone," switch registers instead of softening the cinematic vocabulary — a half-cinematic
UGC piece reads worse than either pure version.

**Never appears in genuine UGC/organic output, in any field:**
- Named cinema bodies or formats (ARRI ALEXA, RED, 65mm, IMAX, anamorphic, Super 8)
- Film-stock/grade language ("film grain," "teal and orange," "cinematic grade")
- Crew-implied camera work (dolly, crane, jib, Steadicam, orbit, arc, drone, or
  "locked-off on a tripod" AS A STYLE CHOICE)
- Designed lighting (softbox, key/fill/rim, volumetric shafts, "motivated" lighting)
- Optical polish (anamorphic flares, oval bokeh, chromatic aberration as a look, speed ramps)
- Directorial name-drops (a director's name, "A24," "shot like a music video")

**Replace it with**: handheld phone / propped phone / front-facing selfie, organic
micro-shake, wide phone lens with barrel distortion, available light only (name the real
source in the room — ceiling light, window daylight, appliance light), "ungraded
phone-camera look, mild sensor noise, no color treatment," a lived-in cluttered setting,
small performance imperfections (a blink, a stumble, a laugh that jolts the camera). The
one permitted exception is a studio-lit macro product/food insert between handheld shots
— a real UGC-ad convention — described as "bright, even, clean digital," never a graded
image.

**Re-declare the character's full physical description verbatim in every shot** that uses
them, not "the same person as before" — this is the single biggest lever against a
character drifting across a multi-shot UGC sequence, and it mirrors idoGen's own
untucked-lock finding ("restate the rule, don't rely on references alone" — see CLAUDE.md).

**Diegetic sound only, always.** No music, no score, no soundtrack in a UGC/organic
prompt's audio description — name the specific sounds the visual actually implies
(fabric rustle, a spoon scraping a pack, distant traffic), never a generic "ambient sound."

## 9. Frozen-subject / freeze-frame as a deliberate effect

When a beat calls for a held instant rather than continuous motion, name it explicitly
rather than leaving it to a generic "pause": **freeze frame** (a single frame held static
for a beat) or **bullet time** (frozen action while the camera continues moving through
the still moment — "bullet time freeze" / "frozen moment, camera orbits"). Distinct from
the final-beat rule above (§2) — that rule is about NEVER freezing the closing frame of a
sequence; this is about using a freeze deliberately mid-sequence as a punctuation effect.
