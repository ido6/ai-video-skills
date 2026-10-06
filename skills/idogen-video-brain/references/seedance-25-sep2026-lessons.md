# Seedance 2.5: September 2026 lessons (official optimizer, NextGen AI, GenHQ)

Sources, read 2026-09-30:
- **sd25-pe v0.3.4**: the Seedance 2.5 prompt-optimizer skill file (`owner: seedance`, shipped with Dan Kieft's iPhone lesson). This is the closest thing to an official syntax doc. Where it and a classroom skill disagree about **syntax**, it wins.
- **Dan Kieft / NextGen AI**, five lessons from Aug–Sep 2026: cinematic ads, 14 prompt ideas, iPhone footage to cinema, ultra-realistic video, and the Pixar-style animation workflow with its prompter skill file.
- **GenHQ**, 2026-09-05, "Cinematic Sequences in Seedance 2.5".

Raw packs: `research/nextgen/2026-09/`. Real-property and real-location rules live in `real-location-fidelity.md`.

All of this is doc-verified, not output-verified on idoGen's own generations. Treat it as the current best convention and A/B it the first time it is load-bearing.

## 0. What this updates (newest dated lesson wins; older claim kept with its date)

| Topic | Older rule (where) | Sep 2026 rule | Resolution |
|---|---|---|---|
| Max length | "No hard cap, up to ~40 shots at 60s" (dialects §1, GenHQ `seedance-25`, 2026-08) | 30s maximum per generation (sd25-pe; Pixar prompter; engine-ranking's 4–30s); GenHQ 09-05 says to split a story into ~30s generations | **30s is the ceiling.** Plan longer pieces as linked ≤30s segments. The 60s claim is superseded. |
| Locked-off on 2.5 | "Banned in shot text" (dialects §1, from GenHQ's opening block) | Dan's 2.5 prompts use locked-off shots on purpose: interview tripod, knight, CCTV, the end hold of the ad. GenHQ real-estate transformations use a locked tripod. | The ban belongs to **GenHQ's opt-in opening block**, not to the model. With that block, keep the ban. Without it, locked-off is fine when the shot calls for it. People shots still default to near-static handheld (C3). |
| Timestamp precision | Fractional seconds are fine (dialects §2) | sd25-pe treats ranges as event budgets and never claims 0.5s precision. The Pixar prompter uses whole seconds only. | **Whole seconds**, consecutive, no overlaps. |
| Never freeze the last frame | `Final beat:` rule (dialects §2, R48) | Designed end cards (brand card, game title card) hold static or freeze on purpose | Keep `Final beat:` for live-action closers. A designed brand or title card may hold still, but it must be named as a card. |
| Negatives on Seedance | No negative block; at most one short closer (SKILL.md, C6) | sd25-pe bans *automatic* boilerplate: no unrequested watermark, subtitle, duplicate or quality lines. Dan and the Pixar prompter use a scoped `[EXCLUSIONS]` block sized to real risk. | On 2.5, a short `[EXCLUSIONS]` block is fine **if you can name the shot each line protects**. Generic lists stay banned. The no-subtitles closer is added only when dialogue or narration makes burned-in text a real risk. |
| Reference labels | `@Image1..N` by attachment order (R17) | sd25-pe writes compact `@Image1` with no space. The Pixar prompter prefers named elements (`@Mia`) because numbered slots get reassigned. | Use **named elements on Higgsfield** (the element name is stable). On idoGen, number by attachment order and check with `preview_references`. |
| Duration, fps, aspect ratio in prose | Never (SKILL.md) | Dan's packs sometimes write "Duration: 30 seconds" and "24 fps" | Unchanged: never write them. sd25-pe agrees; parameters stay parameters. |

## 1. Official mechanics (sd25-pe)

**Separate parameters from content.** Aspect ratio, total duration, resolution, fps and the audio toggle are parameters and never go in the prose. Time ranges the *user* wrote are content: keep them. Never invent numeric ranges just to fill a target duration. Stretch existing beats with natural business instead (a gaze shift, a breath, a pickup).

**Some tasks lock parameters automatically:**
- Editing locks the source video's aspect ratio and approximate duration (±0.3s).
- First-frame and first/last-frame generation lock the aspect ratio to the first image. Both images must share one ratio, or the last frame stretches.
- Extension locks the source's aspect ratio.

**Hard input limits:**
- up to 30 images, each ≤4K;
- up to 10 videos, ≤30s combined;
- up to 10 audio clips, ≤30s combined;
- up to 50 references in total.

Recommended, not hard: 1–8 distinct subjects across images; 5–10s per audio or video reference; for editing, a source under 20s plus 1–5 images.

**Build a story contract first,** from the user's words, not from the references:
- subjects and their count;
- causal order of events;
- prop ownership and handoffs;
- spatial relations;
- the ending state.

References may supply only what is visibly or audibly *there*: face, hair, clothing, material, layout, motion, voice. Never let a reference promote a guess (age, relationship, profession, brand) into a story fact. If the user says "person", keep "person".

**One explicit role per activated material, one line per entity.** Never write a range sentence like "A and B reference @Image1 and @Image2". Each line says what to take and what to leave:

```
<Character A> corresponds to @Image1. Use only the face, hairstyle and clothing. Do not use the image background.
<Prop A> corresponds to @Image3 and belongs only to <Character A>.
<Scene A> references @Image4. Use only the layout, architecture and light. Do not use the people in it.

[Unused Materials]
@Image5 and @Audio2 are not used and must not define people, scenes, props, actions, camera or audio.
```

- Any attached material you don't use goes under `[Unused Materials]` by number. Otherwise the model reactivates it.
- Mapping priority: the user's explicit assignment, then the prompt text, then what the material shows, then filename, then upload order. Upload order is a last tie-breaker, not evidence.
- A single-person sheet never defines two characters who appear together.
- A reference video with no stated role passes on only the dimensions you name (motion, camera, pacing). It never passes on identity, wardrobe or the whole scene. If it already defines the action exactly, say which dimensions to inherit; don't re-describe the action, because the two will conflict.

**Dialogue ledger.** Per stage, record who speaks, the exact words, the language, and on-screen or off-screen.
- Never invent a sentence around a quoted fragment.
- If only an intention is given ("asserts authority"), play it through mouth, pauses and posture, not new lines.
- The written line beats the words in a reference audio clip. The audio supplies voice, accent, pace and emotion only, unless the user asks to reuse its words.

**Show the trigger before the reaction.** If a character reacts to something, the cause must be visible first: in the same frame, or linked by one explicit gaze or camera move. Never push to a face-only close-up before the audience has seen the cause. Dan's T-rex prompt does exactly this: the medium shot keeps the rider sharp and the dinosaur readable in the background.

**Staged events.** Each stage carries one primary state change and an observable end state:

```
[Stage N]
Opening state: <...>.  Primary event: <one change>.  End state: <visible state>.
```

For a handoff, state the ownership change explicitly ("after the handoff it is only in B's hands").

**Keyframes: exact sentences, never softened.** Write the standalone sentence `@ImageN is the first frame.` or `@ImageN is the last frame.` Then describe that frame's composition in a new sentence. Other references follow, each saying it does *not* change the first-frame or last-frame composition.

Several keyframes:
1. Open with "Use @Image1 through @ImageN in order as keyframes."
2. Define each state in turn.
3. The keyframes are semantic anchors, not static holds.

(This is the official wording and is sharper than the softer "Open on @ImageN as the first frame" in the producer's REF mode. It is **untested** on idoGen's `*-seedance-25-ref` engines. Until a pilot shows otherwise, P3's approval rule stands: in REF mode the still is a close guide and frame 1 is not guaranteed. Use the sentence, but don't promise an exact match.)

**Storyboard grid:**
- ≤15 panels, minimal labels;
- state the reading order;
- say not to use its line art, labels or placeholder characters;
- write one line per shot.

**Blockout video** (Blender, previs or a phone rehearsal):
- **Coarse**: grey geometry. It supplies only path, blocking, camera, cuts and rhythm. Map each blockout shape to its final subject.
- **Fine**: structure is already final. Re-render its materials, look and scene, and keep its structure, action and camera.
- Either way, exclude production markers: path lines, axes, frustums, text.
- A blockout is a **generation** reference, never an editing master.

Dan's Blender example uses the camera-only form: "@Video1 as a camera movement reference only; match its movement, speed and framing". He then pins story beats to the reference's own timing ("exactly as @Video1 zooms in, the camera pushes into his face").

**Camera terms need a target:** `technique + subject + start + direction + end`. For niche or ambiguous terms, add the observable result: which subject stays sharp, which way the background blurs, what loses focus and what gains it. Focal length and aperture may supplement, never replace, the visible outcome.

**Audio markup (official):**

| Content | Syntax |
|---|---|
| Music / score | `(...)` |
| Sound effect | `<...>` |
| Dialogue | `{...}` |
| On-screen subtitle | `【...】` |

- Once `<>` means sound effects, never put character names in angle brackets.
- Language per speaker: `language + optional accent + delivery + speaker + {line}`. Don't invent an accent the user didn't ask for. With English lines, say "in English" at minimum.
- For a silent piece, constrain everything together: mouths naturally closed, no narration, only the named ambience, no subtitles or signs.

**Product and process demos.** Replace every abstract claim ("efficient", "premium") with `initial state → one concrete operation → observable result`, one operation per stage.

## 2. Editing, extension and audio-only edits (sd25-pe)

Every edit names **one source video as the sole editing master**. A prompt that only describes the target look silently turns into regeneration.

Edit skeleton:
1. `[Edit Goal] Edit @Video1. Change only <object/region> to <target>.`
2. `[Source Video Role]`: what the master defines (scene, camera, motion paths, occlusion, event order).
3. `[Target Material Role]`: what each reference supplies.
4. `[Edit Objects and Scope]`: target count and what to preserve.
5. `[Timeline Inheritance]`.

Close every edit with one of these two scope sentences, verbatim:
- local edit: `Except for the objects explicitly modified above, all other visible people, props, and background elements in @Video1 remain unchanged and must not be replaced or removed.`
- keep-only edit: `Except for the objects explicitly retained above, remove all other visible subjects from @Video1. Do not add unspecified objects.`

**Motion-slot replacement** (swap a moving thing for a different kind of thing):
1. Remove the original subject.
2. The new subject inherits exactly the original's appearance timing, path, speed and occlusion.
3. State that the original no longer appears.

Keep the preserve-list to the neighbours that genuinely must not change. A long list dilutes the edit.

**Audio-only edit** (change voice, language, music or ambience): the master still owns picture, lip-sync timing, camera and rhythm. By default keep the words and speaking times. To remove music, just say so; don't invent a target audio.

**Extension:**
- **Forward**: the new first frame continues the source's last frame. List pose, props, camera, light, audio state and motion direction.
- **Backward**: describe what happens before, then name the source's first frame as the explicit end state. Things that belong only to later events must not appear early.
- Both directions: every subject stays one continuous instance, never duplicated or split, and keeps the same anatomy and part count.
- Edit plus extend in one request: edit first to make a new master, then extend that master. That is two prompts in order.

This complements Omni/O1 editing (dialects §6, `edit_video_o1`). That family uses the lock clause and preserve-list; Seedance 2.5 uses the closed-scope sentence above.

## 3. Your own footage as the performance (Dan, "iPhone footage → cinematic")

Shoot a rough take with friends on a phone (any room, any clothes, chairs for car seats), then re-cast and re-set it. Decide which of three contracts the source video carries and **name what it must not pass on**:

1. **Motion only.** "@Video1 defines ONLY the body movement, timing and physical performance." List the source faces, wardrobe, props, walls and studio framing as NOT used, then write the new scene, characters and camera. A timestamped action line per second works well for dialogue beats in a short clip.
2. **Motion + cutting master.** "@Video1 is the motion, timing and cutting reference; @Image1 is the character and location." Mirror the source's cut count and cut proportions, for example "exactly two HARD CUTS mirroring the cut timing proportions of @Video1". If the source voice must not carry over, say so and describe a new voice.
3. **Full performance master, voice swapped.** The source keeps staging, pauses, gestures, jump cuts and *its exact dialogue and practical sounds*; only the voice identity changes. Say "identical words, timing, pauses; no summarising or rewriting any line". Give every extra image exactly one job (hat only, shirt text only, poster only), and say that no reference may replace the room, camera or staging. Preserve prop state sequences literally, e.g. lamp off → on → off.

For any of the three:
- Keep the source camera when it is part of the performance (a locked-off rehearsal stays locked-off).
- When a character must be in frame from frame 1, say so. Rehearsal clips often start empty.
- Write weight into costume: "armour reads heavy, each swing has inertia".

**Adding VFX to real footage** (Dan's "Pandora doorway" edit):
- Declare the source (length, resolution, fps) as the base layer: preserved exactly, not restyled, relit, re-timed, stabilised or reframed.
- Key every stage to the **source's own seconds**. The first stage is "untouched, pixel-identical".
- The effect reacts to the performer, never the reverse: "do not add movement he does not perform". An existing recoil gets *re-motivated* by the effect.
- Give the effect's direction and physics explicitly: an outward blast throws hair *toward* camera, slime drips and does not crawl.
- Name an inventory cap for anything that must stay unseen ("one claw, one pressed mass behind glass, one tail-tip; that is the whole inventory").
- Additions must match the source's **capture layer**: same phone grain, softness, highlight roll-off, motion blur, contact shadows and occlusion.
- Light from the new element lands on the performer as highlights, not as a grade.
- Mark the sound section "only if the model generates audio".

## 4. Realism packs: structure, performance, sound (Dan, "Ultra Realistic")

**One continuous take can still be staged.** Dan's long one-takes use:

```
[GOAL] [CONTINUITY]
[STAGE n | a-bs | title]   Initial state / Primary event / End state / Cut type: NO CUT — continuous take.
[VISUAL STYLE] [CAMERA AND PERFORMANCE] [AUDIO] [EXCLUSIONS] [MAINTAIN CONSISTENCY]
```

This conflicts with the Pixar prompter's rule that a new block is read as a cut (§7). Both are Dan's and both are dated Sep 2026, so there is no single winner. When you stage a one-take, write `Cut type: NO CUT` on every stage, and say "one continuous take, no cuts" in both the camera block and the exclusions. If the take still comes back chopped, collapse it into one block with plain time markers inside (the GenHQ real-estate form).

**Handheld as a present third person.** The operator breathes, drifts, is late on a reframe and flinches on an impact. Describe that operator per stage instead of naming a rig. OTS weaving between two people reads as "wedged into the argument"; a fixed-radius orbit reads as observation.

**Performance as a ladder of verbs.** Write the arc first as 6–8 plain actions: ride happily → hear footsteps, lose the smile → look back reluctantly → freeze and scream → pedal frantically → hide → cover the mouth → one shaky breath. Then expand each into gaze, mouth, breath, hands and shoulders inside its stage. A body turn is ordered: eyes first, then chin, then torso.

**First-frame still for a realistic character.** Build the start image from an identity sheet with a "Directed" still prompt. It takes the look of the character and the action of the shot; the sheet recipe is in idogen-image-brain `references/character-and-product-sheets-sep2026.md`. Generate it with `generate_image` `look: "soul"`. The still gives:
- the identity bind;
- a locked camera and one situation;
- where the eyes go (not into the lens);
- mouth closed;
- a lens / aperture / grain / grade line.

**Sound design with positions.** Each effect gets its own `<...>` with source, character, distance and screen position, and it changes as the camera passes it: a fan grows louder, passes camera-right, then falls behind.
- Three depth layers: close sounds dry and detailed, mid sounds with room reflections, far sounds filtered by distance.
- A sound starts only when its visible source moves or is acted on.
- Never more than **two prominent effects at the same instant**. Leave clean gaps around the key hits and the spoken line.
- Keep each sound source visible when its sound first enters.
- Never let the model swap named effects for generic "cinematic booms/whooshes".

**Non-diegetic score, when wanted.** This is an explicit opt-in over the default "No music" (R50). Put score cues in `(...)` at the beat they belong to.
- If the score should be present from frame 1, say so; otherwise the model eases in from silence.
- Sync hits to on-screen events ("sub-bass hit on the exact frame each streetlight dies").
- Design the curve: thicken, thin out just before the peak, stinger, hard cut to silence.

## 5. Capture-look recipes (Dan, "14 prompts")

Each is a register, not a cinematic shot with a filter. Most need the UGC barred list (dialects §8).

- **Self-filmed UGC ad.**
  1. Open extremely close and out of focus, mid-sentence, phone at arm's length with visible grip shake.
  2. She props the phone against the counter; the focus resolves into a steady head-and-shoulders frame.
  3. The audio goes from close phone-mic to a roomier sound the moment the phone is set down.
  4. Only then does the product come up to the lens.
  An invented presenter is described in full text with no person reference; the product still gets its reference.
- **Paparazzi.** Start already inside the crowd, with no establishing shot. Heads, phones and lenses pass through the foreground. The operator is jostled. Autofocus breathes and auto-exposure reacts to the flashes. The whole thing is one take.
- **CCTV.** Fixed high corner mount, wide lens with edge curvature, flat fluorescent light, a green-grey tint, sensor noise, compression. A burned-in timestamp and camera ID is the one place on-screen text belongs. Ambient audio only.
- **Camcorder vlog.** Name the device era (an early-2000s consumer camcorder). Hand-held selfie for the first 20–30s before any resting position. Cap dialogue at a fixed number of short lines spread across the piece; most of the runtime is silent observation.
- **First-person POV.** Only hands and forearms, never the body, including in reflections. Write the action as one object chain (raw pasta → pot → pan → plate → garnish → served), with "nothing teleports, duplicates or changes into another object". Use one purposeful hard cut to show elapsed time rather than a magic state change.
- **Time freeze.** Everything stops at a named instant: people mid-step, hair suspended, objects where they were at impact. The camera keeps moving through the frozen world. A position rule fixes where the key subject waits (e.g. at the interception point). Time resumes "instantly with no visual effect", and objects then land in a stated order.
- **Room from a photo, staged with action.** Lock the layout, list the objects, and "do not add furniture or people". Also say "do not use @Image1's empty mood": a plate's stillness bleeds into the shot otherwise. Phone realism: auto-exposure hunts when bright screens die, one late reframe, rolling-shutter wobble on a jerk.
- **Travel montage from stills.** List the references in playback order, one timeline line per reference with its dialogue, and add one voice reference for the whole piece.

## 6. Ads (Dan, "Cinematic AI Ads", Aug–Sep 2026)

**Concept first.** The first second must stop the scroll: an absurd, physical interruption of an ordinary moment (a horse's head through a bathroom door takes the crisps).
- Comedy is **played completely straight**. Nobody in frame knows it is funny.
- The product is the **only strongly saturated colour** in the frame.

**Block order for ad prompts:**
1. `[REFERENCE MATERIALS]`: one line per reference with "use only … / do not use the grey studio background", ending with "Each reference is one person or one object and appears once."
2. `[VOICES]`: a voice card per speaker, plus a narrator "arriving from outside the story".
3. `[GOAL]`: one or two lines, with "played completely straight".
4. `[CAMERA GEOMETRY]`, **read before anything else**, whenever an entrance direction matters: camera axis, which wall the door is on, the direction of travel across frame, and "this geometry never changes".
5. `[CONTINUITY]`, then `[SHOT]` or `[SHOTS]` with timings and cut type.
6. `[VISUAL STYLE] [CAMERA AND PERFORMANCE] [AUDIO] [EXCLUSIONS] [MAINTAIN CONSISTENCY]`.

**The product-scale stress test** (UGC product videos):
- The **product sheet** carries the real dimensions ("infer real-world scale from the sheet; do not guess, do not default to a generic size").
- A second reference, a **close-up of the front label**, is the text authority: exact wording, typeface and layout.
- A plain comparison object (an unlabelled wine bottle) and the hand both stay in frame.
- A hard cut to a clearly different angle and height tests whether the size survives.
- Numbers are never spoken or shown on screen.
- The presentation beat is held square to camera long enough to read every line, then tilted only a few degrees each way. It never turns far enough to show the reverse panel: the back of a pack is where text garbles.
- Reflections never cross the print.
- State the liquid level, cap and seal state as fixed facts.

**End card as its own shot:**
- a flat full-bleed background in the brand colour;
- the pack from its reference, straight-on;
- one line of type;
- static for its whole duration;
- none of the live-action treatment (no grain, flare or vignette);
- the ship or room sound cuts to silence on the card, then one product sound and the narrator line.

Exact text is still not guaranteed (R32, R44). Composite the card in post if the type garbles.

**Consistent look across a campaign.** Give Claude the moodboard and ask for a reusable **style block**: lighting, palette, composition, grain, lens, ambience and location. Paste that block verbatim into every image and video prompt of the campaign.

**Multiplying one ad:**
- **Flavours / SKUs**: keep the whole prompt and swap only the product sheet and the label close-up. One generation per variant.
- **Presenter or market**: a video edit that replaces the person with a new reference and re-voices in another language with a named accent, keeping the timing. This is the audio-edit rule in §2 plus a subject replacement.

## 7. Animation (Dan, Pixar-style prompter, Sep 2026)

For feature-style 3D animation, **invert the live-action look layer**. Keep the structure (blocking, spatial locks, eye life); drop the realism vocabulary.

**Look block.**
- Never write: film stocks, grain, pores, "documentary", "naturalistic", FOV degrees, or distance-based camera feels (e.g. "paparazzi 20m").
- Write instead: production CG from a feature-quality 3D animated film, stylised proportions, matte skin with warm subsurface through ears and fingertips, and cloth with weight and few large folds.
- Depth of field and bokeh are allowed as *rendered in-camera artefacts*.
- Light is designed, not exposed: key direction and colour, rim, bounce, practicals. State the palette with its single saturated accent.

**Motion is designed.** Write these as observable results, since average AI motion is linear:
- anticipation (winds the other way first);
- snap between poses with a small overshoot that settles;
- moving holds (breath, drift, blink);
- follow-through (hair and cloth arrive late and keep going);
- movement in arcs;
- weight read from timing.

Ban "even, sliding, game-engine motion".

**Acting:** the body plays broad and the face stays honest. Mugging is the top tell.

**Identity has no real-world fallback.** Bind the reference hard and restate only one or two design-critical anchors. Re-describing the whole design overwrites the reference.

**When a referenced character appears as a drawing or photo inside the scene,** bind its tag inline at that point. Otherwise the model draws a stranger.

**Shot format** (Pixar prompter; in this lesson's workflow it wins over stages for dialogue-driven segments):

```
SHOT n | a–bs
<Shot size and angle. What happens. Camera move.>
@Name: {exact line}          (mark only "off camera" / "voiceover"; on-camera is the default)
Hard cut.
```

- **One block = one shot.** A continuous move split across blocks comes back chopped; two cuts inside one block won't both survive.
- State "exactly N shots and N−1 transitions" in the camera block and repeat "no extra cuts anywhere" in the exclusions. Models invent cuts.
- Timecodes are whole seconds, add up to ≤30, and are budgeted shot by shot. A single short line needs about 2s; two lines in one shot need about 4s.
- Every line appears once, verbatim, in braces. Never describe a line ("she says a name"), and never repeat it in `[AUDIO]`.
- `[EXCLUSIONS]` is normally three lines: *the only spoken words are the lines in braces*; *no extra cuts*; plus the one thing this segment could really get wrong.
- Hard cut is the default. Name any other transition (a diegetic wipe, a move through darkness, a match to an established framing) and ban the rest. A framing that must repeat is defined once and referenced twice.
- Every revision outputs the **full prompt**, opening with two lines on what changed. Never ship fragments.

**Extending a finished segment** (Higgsfield "Sequel"): re-attach every reference, add a *geometry reference* (a still that fixes who sits where and the camera side, "do not use the faces in it"), and state in `[GOAL]` that this is one of several linked segments and exactly where it ends, "do not resolve anything".

**Script before prompts:**
- Lock every line of dialogue, verbatim, before the shot list exists.
- Test the story: is the ordinary world ordinary enough, is there a rule-of-three with a break, and does a running gag escalate visibly?
- Plant the payoff early, cut to the reaction face, and prefer business over dialogue.

**Storyboards** (GPT Image 2):
- painted colour boards, 8 panels per sheet (2×4), which double as the film's colour script;
- two sentences per panel: what is in frame, then light and palette;
- **name skin tone in every panel**, because boards carry no references and default everyone to white.

## 8. Workflow points (GenHQ 2026-09-05, Short Film Path)

- Continuity comes from one camera, one lens and one stock across every generation. Lock the global look block at the top of every prompt. This applies only when using GenHQ's cinematic block.
- Write the script like directing on set: camera position, seconds per beat, acting nuance, voice delivery, and what each sound lands on. Acting nuance was the module's biggest tip.
- The Seedance 2.5 prompt field holds about 10,000 characters. A ~30s generation holds continuity better than many short ones.
- **If dialogue comes out sped up, the prompt has too many words for the runtime.** Cut lines or add seconds.
- Mine the best seconds of each take, give timestamped feedback, and stitch the best parts of different takes. Cut into the action early and remove dead space.
- Voice lock via a recorded reference: see idogen-acting, "Voice references and dialogue language".
