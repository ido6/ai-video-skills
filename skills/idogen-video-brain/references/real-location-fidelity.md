# Real-location fidelity (real estate, venues, any place that must appear as photographed)

Source: GenHQ, 2026-09-08, "Real Estate Videos With AI" (Create Ads Path), which ships the `seedance-25-realestate` skill v3. Digest: `research/genhq/round6/realestate-and-sep-2026-digest.md`. Doc-verified, not yet output-verified on idoGen.

**Use this file when the references are photographs of a real place the client will recognise:** a listing, a hotel, a venue, the client's own shop. It overrides the location-plate habits in SKILL.md, which treat a location reference as geometry and atmosphere you may reframe and relight. Here the photo is a contract.

## 1. The reference-fidelity contract (outranks everything else)

1. **Nothing enters frame that isn't in the plate.** No set dressing, plants, people, pets or weather. A sparse room stays sparse.
2. **No geography the plate doesn't show.** Never through a doorway, round a corner or above the roofline. One plate = one shot = one field of view.
3. **The light is the photographed light.** No time-of-day change, haze, god rays, flare, halation or film-stock colour.
4. **The camera stays inside the frame.** Every move ends inside the plate's original field of view. When in doubt, hold.
5. **Optics are required, not forbidden.** Apply lens character, depth of field, grain and highlight roll-off evenly to every pixel. Otherwise anything added (a person) looks pasted on.
6. **Declare every deviation.** If the user asks for something not in the photos, name it in your message ("the teacup is the only object not in your references").

**Content layer vs capture layer.**
- *Content* (geometry, objects, finishes, colour, grade) is locked to the plate.
- *Capture* (lens, DOF, grain, roll-off) is unified across the whole frame.
- Name a camera body and lens for the optics. Never name a film stock, because stocks recolour.

## 2. Camera whitelist

**Allowed:**
- push-in (≤ about a 2× crop);
- ease-out back only as far as the plate edge;
- parallax nudge ≤ 6°;
- lateral drift of 5–15% of frame width;
- tilt or pan that ends inside the plate;
- rack focus between two in-plate targets;
- near-still hold. The default is "near-still handheld, verticals locked".

**Forbidden:**
- pull-back out of the plate;
- orbit over 6°;
- crane or drone (unless the plate itself is aerial);
- through a door or window;
- whip pan or crash zoom;
- speed ramps, slow motion or time-lapse.

This whitelist overrides `camera-movements.md` for real-location work.

## 3. Prompt shape

1. **Fixed opening paragraph:**
   - camera body + primes + aspect + T-stop, shallow DOF, highlight roll-off, even grain;
   - verticals straight;
   - colour true to the plates: no grade, stock, HDR or sharpening;
   - nothing that is not in the plate.
2. **Plate-matched paragraph,** filled only from what the photos show: light direction, time of day, the real materials, "clear air, nothing added". Exclude watermarks and agency logos on the plates by name.
3. **Timestamped shots,** each opening with an anchor clause: `Anchored to @ImageN — stays entirely within that frame's field of view.` One bracket = one continuous take; beats inside it are plain time markers.
4. **Audio:** diegetic only, no music.

**Budget and wording:**
- about 5,000 characters per field;
- speech runs at about 2.6 words per second; spell numbers out;
- never write "4K/8K/ultra-detailed";
- never write "fast" (use "decisive" or "controlled quick");
- the last shot opens with `Final beat:` and has motion alive on the closing frame.

**Workflow:**
- Match the generation's aspect ratio to the reference photo.
- **Never use storyboards or location sheets as references for a real space.** Only the real photos.
- Two passes: a ~30s base generation, then ~10s detail shots per room ("direct the shot, don't just ask for close-ups").
- A 360° room orbit needs separate front and back photos.
- Aerials and walkthroughs only where they are honest to the client.

## 4. Detail shots need an event

A close-up with nothing changing renders as a photo. Every detail shot carries an event, and ends on a focus move.

- **Plate-justified events:** a fire, a fan's moving shadow, a curtain in an open door, a sun patch creeping, a foliage reflection.
- **Optical events:** a travelling specular, raking light over a texture, focus that travels, objects passing through the focus plane.

Other rules:
- A switched-off TV is a mirror. Write it OFF: "no picture, no menu, no logo, no glow".
- Empty furniture never moves by itself.
- One physical cause (a fan, sun through louvres) seen across several shots makes the cuts read as one moment.

## 5. Placing a person into a real plate (the integration checklist)

Write all of these into every person shot:
1. One depth of field for person and room.
2. A **real contact shadow** matching the plate's light direction and length. Its absence is the biggest tell.
3. Light wrap and colour bounce from real nearby surfaces.
4. Shared grain.
5. Correct parallax.
6. Occlusion by a real foreground element.
7. The plate's own camera height and eyeline.
8. Micro-motion: weight shifts, blinks, breath.

- Choose a plate with depth, a readable floor, and something to stand behind.
- A moving shadow (fan, branch) crossing the face is the best single integration tool.

**Performance.**
- A posture is a photograph. Write about three named movements at named moments.
- Start the person mid-action and keep them moving while speaking.
- For a match on action across a cut: the movement starts in shot A, and shot B opens "MID-MOVEMENT … no reset, no pause, no repeat".

## 6. Two photos of the same room (the mirrored-room failure)

- Never label the views "front/back".
- State in capitals that the images are **THE SAME ROOM FROM OPPOSITE ENDS**, one wall seen from two sides.
- Give a room map by what is on each wall, and count everything: "ONE fireplace … NOTHING IS DUPLICATED".
- Order the rotation with exit directions. For a shot of one end, say the other end is directly behind camera.
- Separate plates beat a labelled contact sheet.
- Pans never turn a corner. If a 360° pass merges the ends, cut it to 180°.

## 7. Time of day is a subtraction

- **Night:**
  - every light already on stays exactly as it is, with no new sources; only the daylight is removed;
  - the exterior gets only spill from the room's own lamps;
  - whatever light survives becomes the dominant source;
  - it is still darkening on the last frame.
- State each shot's light state as a progression. Never average warm practicals with cool daylight.
- Close a light mechanism that exists in the plate (louvres) rather than inventing blinds.

## 8. Transformation shots (staging, build, renovation)

- **Frame:** a locked tripod, the only exception to "never locked" here. First frame = the before plate; final frame = the after plate (use `end_image_id`, or `@ImageN is the last frame.`).
- **Objects built in place:**
  - each rises from the floor behind a leading edge (flat for rugs), and that edge carries NO glow, line or shimmer;
  - stagger the builds;
  - contact shadows grow with the object;
  - a small settle at the end.
- **A house rising:** one whole object pushed up. Kill the word "build": no bricks, scaffolding or builders.
- **Falling mass:** a shadow racing ahead, a shockwave, one camera shake, motion blur on the fast part.
- **Renovation** is decay run backwards: stains shrink, cracks zip closed, paint lies back down, dust lifts, weathering drains out. End with the power coming back: lights ignite, the fan catches.
- **Close with the forbidden list:** no glowing edge, scan line, particles, sweep of light, sliding in, popping in, builders or people.
- A macro shot on a built object is fine; the plate behind it goes out of focus.

## 9. Claims and copy

- Use only the facts the user supplied, unrounded.
- No invented superlatives, agents, phone numbers or URLs.
- Bedroom and lifestyle lines point outward, at the room, the morning or the view, not at the buyer.

**Transitions:** hard cut by default; match cut; push-in to push-in; directional drift match. A 1s dissolve is for chapter breaks only.
