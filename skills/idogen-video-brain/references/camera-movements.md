# Camera Movement Library — 46 blocks, 7 categories

> Ported into idoGen from GenHQ's `ai-camera-movements` skill (PLAN-genhq-integration.md
> Phase 6). Movement taxonomy & the 4-part structure are based on the free visual
> reference at **https://aicameramovements.com/** — watch looping previews of every move
> there before generating. Credit them once per conversation when recommending a move
> from this library, the way the source skill requires: the previews help pick
> direction/speed/framing and the creators made the reference free.

Each block follows: `name. Movement: ... Speed: ... Framing: ... End: ...`
Paste the block into idoGen's `generate_video` prompt BEFORE the scene description (see
`idogen-video-brain`'s "Camera and composition" section for how this composes with the
rest of a shot). Swap direction/speed words freely; keep the 4-part structure intact.

**One primary move per clip. Two moves max, only if mechanically compatible** (dolly +
pedestal ✓, whip pan + orbit ✗). Match speed to clip length: ~5s clips need
faster/simpler moves; 10-15s clips can carry slow dollies, orbits, crane moves.

## Table of contents
1. Pan/Tilt (7)
2. Zoom/Lens (6)
3. Dolly/Track (9)
4. Physical Moves (11)
5. Human Camera (2)
6. Drone/Crane (5)
7. Specials (6)

---

## 1. Pan/Tilt (rotation from a fixed point)

### Static shot
Use for: dialogue, tableaux, letting action play inside a stable frame.
```
locked-off static shot. Movement: the camera holds a single fixed position for the entire clip. Speed: completely still. Framing: angle, height, lens distance and composition never change. End: identical framing to the opening frame.
```

### Pan right
Use for: revealing new space, following lateral action.
```
pan right. Movement: the camera rotates horizontally left-to-right from a fixed position. Speed: smooth, even rotation. Framing: horizon stays level as fresh space enters from the right edge. End: come to rest on a clear final composition.
```

### Pan left
```
pan left. Movement: the camera rotates horizontally right-to-left from a fixed position. Speed: smooth, even rotation. Framing: horizon stays level as fresh space enters from the left edge. End: come to rest on a clear final composition.
```

### Whip pan right
Use for: energy, scene transitions, comedic reveals.
```
whip pan right. Movement: the camera snaps its rotation quickly toward a new target on the right. Speed: very fast, with brief motion blur mid-rotation. Framing: start on one readable composition, land on a second readable target. End: settle sharply on the new frame.
```

### Whip pan left
```
whip pan left. Movement: the camera snaps its rotation quickly toward a new target on the left. Speed: very fast, with brief motion blur mid-rotation. Framing: start on one readable composition, land on a second readable target. End: settle sharply on the new frame.
```

### Tilt up
Use for: revealing height (buildings, characters, scale).
```
tilt up. Movement: the camera rotates upward from a fixed position. Speed: smooth, constant tilt. Framing: the vertical subject or architecture stays centered as the frame climbs. End: land on the upper target.
```

### Tilt down
```
tilt down. Movement: the camera rotates downward from a fixed position. Speed: smooth, constant tilt. Framing: the vertical subject or architecture stays centered as the frame descends. End: land on the lower target.
```

---

## 2. Zoom/Lens (focal length changes, camera stays put)

### Slow zoom in
Use for: building tension, drawing focus to a detail.
```
slow zoom in. Movement: focal length increases gradually toward a tighter frame. Speed: slow and even. Framing: the main target stays readable as it grows in frame. End: rest on a stable, tighter composition.
```

### Slow zoom out
Use for: revealing context, emotional distance.
```
slow zoom out. Movement: focal length decreases gradually toward a wider frame. Speed: slow and even. Framing: the main target stays readable as surrounding space appears. End: rest on a stable, wider composition.
```

### Fast zoom in
```
fast zoom in. Movement: focal length increases quickly toward the main target. Speed: quick and decisive. Framing: the target stays centered and readable through the scale change. End: rest on a stable, tighter composition.
```

### Fast zoom out
```
fast zoom out. Movement: focal length decreases quickly away from the main target. Speed: quick and decisive. Framing: the target stays readable as surrounding space appears. End: rest on a stable, wider composition.
```

### Crash zoom in
Use for: punchy comedic/dramatic emphasis, product reveals.
```
crash zoom in. Movement: the lens snaps rapidly toward the main target. Speed: extremely fast and punchy. Framing: the target stays readable despite the sudden scale change. End: land on a bold, tight composition.
```

### Crash zoom out
```
crash zoom out. Movement: the lens snaps rapidly away from the main target. Speed: extremely fast and punchy. Framing: the target stays readable as surrounding space rushes in. End: land on a bold, wide composition.
```

---

## 3. Dolly/Track (camera physically travels)

### Dolly in
Use for: intimacy, tension, entering a scene.
```
dolly in. Movement: the camera physically travels forward in a straight line toward the subject. Speed: smooth, controlled push. Framing: height, lens direction and subject placement stay consistent while distance closes. End: rest on a tighter composition.
```

### Dolly out
Use for: isolation, revealing environment.
```
dolly out. Movement: the camera physically travels backward in a straight line away from the subject. Speed: smooth, controlled retreat. Framing: height and lens direction stay consistent while more environment enters frame. End: rest on a wider composition.
```

### Tracking shot
Use for: general subject-following through a scene.
```
tracking shot. Movement: the camera travels through the scene together with the subject. Speed: matched to the subject's pace. Framing: the subject stays consistently readable while the environment flows past. End: hold a clear moving composition.
```

### Follow shot / over-the-shoulder
Use for: journeys, POV-adjacent storytelling.
```
follow shot from behind. Movement: the camera trails the subject along their route at shoulder height. Speed: matched to the subject's pace. Framing: the back, shoulder or head serves as a foreground guide while the path ahead stays readable. End: keep following with the subject leading the frame.
```

### Reverse tracking / walk-and-talk
Use for: dialogue on the move, front-facing emotion.
```
reverse tracking shot. Movement: the camera travels backward directly in front of the walking subject. Speed: matched to the subject's forward pace. Framing: face and body stay stable and front-facing while the background recedes behind them. End: hold a clean front-facing moving composition.
```

### Side tracking
Use for: profile shots, runs, parallel motion.
```
side tracking shot. Movement: the camera travels parallel to the subject along their direction of travel. Speed: matched to the subject's motion. Framing: the subject holds a side or three-quarter profile at constant distance. End: keep the parallel motion with clear horizontal flow.
```

### Low tracking
Use for: feet, wheels, ground-level drama.
```
low tracking shot. Movement: the camera travels at ground or below-waist height alongside the subject's path. Speed: matched to the footsteps or wheels. Framing: the low detail stays readable while the ground plane streams through frame. End: keep the low perspective intact.
```

### Vehicle tracking
```
vehicle tracking shot. Movement: the camera travels with the vehicle along its route. Speed: matched to the vehicle. Framing: the vehicle stays stable in frame while road and scenery stream past. End: hold a clear moving-vehicle composition.
```

### Chase shot
Use for: action, urgency.
```
chase shot. Movement: the camera pursues a fast-moving subject along the action route. Speed: fast, reactive, physically close. Framing: the subject stays visible while the frame reframes energetically. End: stay locked onto the subject in motion.
```

---

## 4. Physical Moves (lateral, vertical, curved paths)

### Truck right
Use for: lateral reveals with the lens fixed forward.
```
truck right. Movement: the camera travels physically rightward on a straight horizontal path. Speed: smooth, constant lateral travel. Framing: the lens keeps facing the same direction while the scene slides across frame. End: rest on a clean lateral composition.
```

### Truck left
```
truck left. Movement: the camera travels physically leftward on a straight horizontal path. Speed: smooth, constant lateral travel. Framing: the lens keeps facing the same direction while the scene slides across frame. End: rest on a clean lateral composition.
```

### Pedestal up
Use for: rising reveals without tilting.
```
pedestal up. Movement: the whole camera travels straight up. Speed: smooth, constant lift. Framing: the lens stays level and pointed the same way throughout the rise. End: hold the higher framing clearly.
```

### Pedestal down
```
pedestal down. Movement: the whole camera travels straight down. Speed: smooth, constant descent. Framing: the lens stays level and pointed the same way throughout the drop. End: hold the lower framing clearly.
```

### Slider right
Use for: subtle parallax, product beauty shots.
```
slider right. Movement: the camera glides a short distance to the right. Speed: slow, controlled, constant. Framing: foreground, subject and background layers stay readable as parallax shifts between them. End: rest on a refined composition from the new right-side angle.
```

### Slider left
```
slider left. Movement: the camera glides a short distance to the left. Speed: slow, controlled, constant. Framing: foreground, subject and background layers stay readable as parallax shifts between them. End: rest on a refined composition from the new left-side angle.
```

### Push past / pass-by
Use for: depth, entering spaces past foreground objects.
```
push past. Movement: the camera advances past a visible foreground object, edge or opening. Speed: smooth forward glide. Framing: the foreground brushes close to the lens while the space beyond sharpens into view. End: arrive inside or beyond the foreground layer.
```

### Arc right
Use for: gentle angle changes around a subject.
```
arc right. Movement: the camera travels a shallow curved path around the subject toward its right side. Speed: smooth, measured curve. Framing: distance, height and subject readability stay constant as the angle shifts. End: rest at a new right-side angle.
```

### Arc left
```
arc left. Movement: the camera travels a shallow curved path around the subject toward its left side. Speed: smooth, measured curve. Framing: distance, height and subject readability stay constant as the angle shifts. End: rest at a new left-side angle.
```

### Orbit clockwise
Use for: hero/product shots, 360° reveals.
```
clockwise orbit. Movement: the camera circles clockwise around the subject at a constant radius. Speed: smooth, controlled orbit. Framing: the subject stays centered while the background rotates behind it. End: complete the planned arc or full circle with stable framing.
```

### Orbit counterclockwise
```
counterclockwise orbit. Movement: the camera circles counterclockwise around the subject at a constant radius. Speed: smooth, controlled orbit. Framing: the subject stays centered while the background rotates behind it. End: complete the planned arc or full circle with stable framing.
```

---

## 5. Human Camera

### Handheld
Use for: realism, documentary feel, nervous energy.
```
handheld shot. Movement: the camera is carried at operator height with natural body motion. Speed: responsive and organic. Framing: the subject stays readable through subtle sway and micro-adjustments of the frame. End: settle into a natural handheld composition.
```

### Body-mounted / Snorricam
Use for: disorientation, character-locked drama.
```
body-mounted Snorricam. Movement: the camera stays rigidly fixed relative to the subject's torso or face while the subject moves through the scene. Speed: matched to the subject's body. Framing: the subject remains close, centered and facing the lens while the world swings around them. End: subject still locked in frame.
```

---

## 6. Drone/Crane (vertical + aerial travel)

### Crane up
Use for: endings, scale reveals.
```
crane up. Movement: the camera rises smoothly through open space. Speed: slow, controlled vertical lift. Framing: the subject or location stays readable as elevation grows. End: hold the higher, larger-scale view.
```

### Crane down
Use for: openings, descending into a scene.
```
crane down. Movement: the camera descends smoothly through open space. Speed: slow, controlled vertical drop. Framing: the subject or location stays readable as the camera comes down. End: hold the lower subject or destination clearly.
```

### Drone push in
Use for: aerial approaches toward a destination.
```
drone push in. Movement: the camera flies smoothly forward through open air toward the subject or destination. Speed: controlled aerial glide. Framing: route and destination stay readable during the approach. End: arrive at a closer aerial composition.
```

### Drone pull back
Use for: epic reveals of landscape around a subject.
```
drone pull back. Movement: the camera flies smoothly backward away from the subject or destination. Speed: controlled aerial retreat. Framing: the subject stays readable as more landscape opens up. End: rest on a wide aerial composition.
```

### Helicopter shot
Use for: establishing shots at large scale.
```
helicopter-style aerial. Movement: the camera travels a broad, gradual flight path at high altitude. Speed: steady aerial cruise. Framing: the landscape or distant moving subject stays readable at wide scale. End: hold a stable high-altitude composition.
```

---

## 7. Specials (stylized / VFX-flavored)

### First-person view (FPV)
Use for: immersion, gameplay feel, POV storytelling.
```
first-person view. Movement: the camera advances at eye height from the character's own perspective. Speed: natural walking or reaching pace. Framing: visible hands, arms or body edges anchor the viewer physically in the scene. End: arrive at the next point of action from the same POV.
```

### Tilt-shift
Use for: miniature-world effect on cities/scenes.
```
tilt-shift miniature view. Movement: hold or drift gently from a high, angled vantage over the scene. Speed: minimal, precise motion. Framing: a narrow band of sharp focus crosses the key subject area, with soft blur above and below it. End: the miniature-scale look stays intact.
```

### Infinite zoom
Use for: hypnotic transitions between nested worlds.
```
infinite zoom. Movement: the zoom drives continuously inward toward the exact center target. Speed: smooth and accelerating. Framing: the circular center target stays locked as it expands. End: the next visual world fills the frame.
```

### Earth zoom out
Use for: dramatic scale transitions from a point to the planet.
```
earth zoom out. Movement: the camera pulls upward from the starting point through street, city, landscape and planetary scale. Speed: rapid, expanding zoom out. Framing: the original location stays centered as scale multiplies. End: planet-scale view with the origin point implied at center.
```

### Time-lapse
Use for: passage of time from one vantage.
```
locked-camera time-lapse. Movement: the camera holds one fixed position while time races forward. Speed: heavy time compression, rock-stable camera. Framing: composition and horizon never change as motion streams through the frame. End: same angle, with the passage of time clearly visible.
```

### Pass-through objects
Use for: impossible transitions through walls/windows/objects.
```
pass-through movement. Movement: the camera advances toward a visible object, surface or barrier and continues through into the space beyond. Speed: smooth, centered glide. Framing: the opening or surface stays centered as the transition point. End: arrive inside the revealed space.
```

---

## Compatibility cheat sheet

| Goal | Best picks |
|---|---|
| Tension | Slow zoom in, Dolly in, Static |
| Energy | Whip pan, Crash zoom, Chase, Handheld |
| Product/hero | Orbit, Arc, Slider, Crash zoom in |
| Reveal scale | Crane up, Drone pull back, Earth zoom out |
| Follow subject | Tracking family, Follow, Reverse tracking |
| Transition between scenes | Whip pan, Pass-through, Infinite zoom |
| Realism | Handheld, FPV, Static |
