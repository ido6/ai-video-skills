---
name: "blender-blockout-pawns"
description: "Build Blender previs/blockout scenes in the pawn style (box-torso + sphere-head characters in flat-coloured primitive sets) and export them as motion/structure references for AI video (Seedance, idoGen, Kling)."
---

# Blender Blockout Pawns → AI-video previs

This skill does two things:
- It recreates Ido's reference previs look in Blender: pure **pawn** characters (a box torso and a sphere head, with no limbs, no face and no extras) inside flat-coloured primitive environments.
- It exports each scene as a **reference package for AI video**: an MP4, first and last frames, keyframe stills and the .blend file.

Rendering uses Workbench (viewport-style), so it's fast enough for animatics.

## Setup (adjust paths to your machine)

- **Blender 5.2** is at `<BLENDER_EXE>`. The user environment variable `BLENDER_PATH` points to it.
- **The kit file** is at `<BLOCKOUTS_DIR>\_kit\blockout_kit.py`. It contains the same code as the KIT section below. If it's missing or outdated, write the KIT section back to that path.
- **Output root** is `<BLOCKOUTS_DIR>\<SceneName>\`. The folder `<BLOCKOUTS_DIR>` must be connected to the session. If it isn't, ask for access with `device_request_folder_access`.
- **Scene scripts** go in `<BLOCKOUTS_DIR>\_scripts\<SceneName>.py`.

## Run modes — use A by default

**A. Background (proven to work; Blender doesn't need to be open)**
1. Write the scene script to the container. It should start with:
   ```python
   import math
   exec(open(r'<BLOCKOUTS_DIR>\_kit\blockout_kit.py', encoding='utf-8').read())
   ```
   Then add the build calls, followed by `r = export_for_ai()` or `render_still()`, and finally `print("RESULT", r)`.
2. Copy the script to `_scripts\<SceneName>.py`. Stage it under `/mnt/user-data/outputs/` and then use `device_commit_files`.
3. Run it through the Desktop Commander shell on the PC:
   `& '<BLENDER_EXE>' --background --factory-startup --python '<BLOCKOUTS_DIR>\_scripts\<SceneName>.py' 2>&1 | Select-String 'RESULT|Error|Traceback'`
   Use a timeout of about 300 s. A 5 s shot at 720p renders in well under a minute.
4. Pull back `preview.png` or `first.png`/`last.png` with `device_stage_files` and look at them with `Read`. Then iterate.

The Blender connector's `execute_blender_code_for_cli` reads `BLENDER_PATH`. It only works after the Claude desktop app has been restarted since that variable was set. If it says the executable wasn't found, use the shell route above.

**B. Live, inside the open Blender** (the connector's `execute_blender_code`, with the MCP add-on server running). Use this when Ido wants to watch or tweak in the viewport.
- In the first call, run `exec(open(r'<BLOCKOUTS_DIR>\_kit\blockout_kit.py', encoding='utf-8').read())`, then the build calls.
- `new_scene()` always creates a new scene, so Ido's own scenes are never touched.
- If a later call raises `NameError`, run the `exec` line again.

## The two looks

| | `look="previs"` (default) | `look="toy"` |
|---|---|---|
| Feel | Muted dusty pastels. Every object is a different colour | Saturated team colours, like board-game pieces |
| Head | Smooth sphere that **floats** about 6 cm above the body | Low-poly sphere (16×10) that **rests on / sinks slightly into** the body |
| Colour | Head colour differs from body colour | Head and body share one team colour (`white/black/red/blue/yellow/orange/green`) |
| Lighting | Studio light, no shadows, soft world cavity | Studio light plus soft cast shadows, no cavity (cavity draws grid lines on low-poly heads) |
| Typical set | Rooms with a dark plum ceiling, bed, desk and doors; maquettes on plinths | Halls, round felt tables, chairs, rails; crowds coloured by role |
| Exposure | +0.45 | +0.75 |

The pawn body is 0.48 w × 0.40 d m, and the standard height is 1.86 m with the head included. Kids are about 1.2 and giants about 3. `seated=True` gives a shorter torso raised to seat height, to pair with `chair()`. Ido's rule: **keep the pawn pure.** Only vary colour, `height=` and `seated=True`. Never add noses, limbs, hats or props attached to it.

When Ido doesn't say, use **previs**. Use **toy** when he mentions teams, a casino, a game, a crowd or strong colours.

## Building a shot

1. Call `new_scene(name, look, aspect="16:9")`. Aspect choices: `16:9`=1280×720, `9:16`=720×1280 (Reels/TikTok), `1:1`, `4:5`, `21:9`. Match the aspect of the AI video you're making.
2. Build the set with `room()`, then furniture with `block()`, `bed()`, `table()`, `chair()` and `cylinder()`. Use 10–40 objects; the look needs very little detail. Use `open_walls=(1,)` so the camera can sit inside the room.
3. Add pawns with `character()`. Animate them with `move()`, which glides them and turns them at corners. **Plan paths around props**, because pawns pass straight through furniture.
4. Add the camera with `camera(loc, look_at, lens=20–28)` at eye height 1.5–1.7 m, slightly off-axis, like a handheld previs camera. Two other framings: a high 3/4 view looking down at a maquette, or over-the-shoulder behind two pawns. For a camera move, keyframe `cam.location` and `cam.rotation_euler` at the start and end frames. Keep moves simple (push-in, pan, orbit), because AI models copy simple moves best.
5. Set the length. A shot is usually 5–10 s: `KIT["scene"].frame_end = 120` (5 s at 24 fps). `move()` already extends `frame_end` to cover the walk.
6. Call `render_still()` and review it. When the framing works, call `export_for_ai()`.
7. Report the scene name, the output folder and the first and last frames.

## Composition rules taken from the reference videos

- Walls, floor and ceiling are each their own colour. In previs, the ceiling is very dark plum (#3A3442), so it reads as a dark band at the top of frame.
- The camera usually sits **inside** the room. Use `open_walls` to leave out the wall behind the camera.
- Doors are thin slabs left ajar. The `door=` parameter of `room()` cuts the opening and adds the slab.
- Clutter is made of flat thin boxes, such as papers scattered on a desk or sticky notes on a wall (0.15 × 0.01 × 0.2 boxes in random pastel colours).
- Crowds: put pawns in rings around tables, lines behind counters, or pairs as guards. In the toy look, colour by role.
- Props share the pawn's scale, so a pawn's head is roughly level with a door's top third.

## AI-video handoff

`export_for_ai(every=24)` writes these files to `Videos\Blockouts\<Scene>\`:
- `<Scene>.mp4` is the motion and structure reference. It's for video-to-video, motion control, or the "reference video" input in Seedance or idoGen.
- `first.png` and `last.png` are composition inputs. For photoreal work they feed the image model that builds the real start/end frame (see overrides below); use them directly only for draft tests.
- `keys/key_####.png` is one still per second. Use these for omni-reference multishot (@Image1…) or storyboards.
- `<Scene>.blend` is the scene, kept for later edits.

When writing the generation prompt, tell the model to **keep the layout, blocking and camera move** from the reference. Then describe the final look: real people in place of the pawns, with materials, lighting and wardrobe. Map each pawn colour to a character, for example "the pink-bodied figure = the woman in the red dress". For multishot Seedance prompts, hand off to the `seedance-25` skill.

## Photoreal AI-video handoff: playbook overrides (2026-10-06)

The looks above are for animatics. When a clip is a **control clip for photoreal Seedance 2.5 / idoGen**, these rules from Ido's previs playbook take precedence (full detail: `idogen-video-brain` → `references/previs-to-seedance-playbook.md`; lens choice: `cinematography` → `references/camera-directing-playbook.md`):

- **Neutral grey set.** Coloured walls/ceilings bleed hue into the generation [field]. Keep flat colour only on main pawns and story props.
- **Every proxy identifiable by two cues** (colour + height/shape/position); colour-only mapping is unreliable [field]. If a pawn colour may leak into wardrobe, paint the pawn the wardrobe colour [unverified].
- **Story-critical props** (bottle, tray, glasses) get their own simple primitive.
- **Real scale**, floor present, nothing moving that shouldn't, no overlays (paths, gizmos, grid, frame counter, text) and no audio track.
- **One dominant camera move per shot, one clip per shot.** Bake only slow shoulder float; ask for fast shake in text or add in edit.
- **Lens is a cinematography decision**, not a fixed 20–28 mm default: it is baked into the clip. For 9:16 set the sensor to 36.7 mm (rotated ALEXA Mini LF gate) so Blender mm equal real mm.
- **Clip spec:** 24 fps, output aspect, whole seconds, ≥4 s (Seedance minimum), clip length = generation length, with a tail of real animation after the usable part.
- **`first.png` is not a start frame.** It is a composition input to the image model, which builds the photoreal start frame together with the sheets. Use it directly only for draft tests.
- Also export a still of the empty set per camera direction and a top view (location plan).

## KIT — the contents of blockout_kit.py

```python
# ---- BLOCKOUT KIT (paste once per session, then call the helpers) ----
import bpy, math, random, os, glob
from mathutils import Vector

OUT_ROOT = os.path.join(os.path.expanduser("~"), "Videos", "Blockouts")
ASPECTS = {"16:9": (1280, 720), "9:16": (720, 1280), "1:1": (1080, 1080), "4:5": (1080, 1350), "21:9": (1680, 720)}

PREVIS = ["#9C7393", "#8DB59A", "#88BDB0", "#C48DAA", "#ADB277", "#88A2B5",
          "#8E78AA", "#BFAE94", "#7FA393", "#B28AA1", "#A2C0AA", "#D6A9B8",
          "#B3A28A", "#7E5A70", "#9FA6C2"]
TOY = {"white": "#E8E8E2", "black": "#0B0C0E", "blue": "#1667A8", "yellow": "#C9A20E",
       "red": "#B0122E", "orange": "#C27A12", "green": "#2E6B4A", "felt": "#2A6A48",
       "cream": "#E6DDC4", "wood": "#5A3218", "brass": "#9C8240", "floor": "#E3D2B0",
       "wall_teal": "#4E7468", "wall_wine": "#5C3740", "wall_taupe": "#6B5E4C"}
KIT = {"look": "previs", "rng": random.Random(7), "col": None}

def _rgba(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, 1.0)

def _mat(hexcol, rough=0.85):
    name = "BK_" + hexcol.lstrip("#")
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.diffuse_color = _rgba(hexcol); m.roughness = rough
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b: b.inputs["Base Color"].default_value = _rgba(hexcol); b.inputs["Roughness"].default_value = rough
    return m

def _pick(color):
    if color is None:
        return KIT["rng"].choice(PREVIS) if KIT["look"] == "previs" else TOY["cream"]
    return TOY.get(color, color)

def _link(ob):
    for c in ob.users_collection: c.objects.unlink(ob)
    KIT["col"].objects.link(ob); return ob

def new_scene(name="Blockout", look="previs", seed=7, fps=24, aspect="16:9", res=None):
    """look: 'previs' (videos 1-2: Workbench, muted random pastels, no cast shadows)
             'toy'    (video 3: saturated team colours, soft shadows, low-poly heads)"""
    KIT["look"] = look; KIT["rng"] = random.Random(seed)
    sc = bpy.data.scenes.new(name); KIT["scene"] = sc
    if bpy.context.window: bpy.context.window.scene = sc
    col = bpy.data.collections.new(name + "_SET"); sc.collection.children.link(col); KIT["col"] = col
    sc.render.fps = fps; sc.render.resolution_x, sc.render.resolution_y = res or ASPECTS[aspect]
    sc.render.resolution_percentage = 100; sc.frame_start = 1; sc.frame_end = 1
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.show_specular_highlight = False
    if look == "previs":
        sh.color_type = "MATERIAL"          # palette is baked into materials (stable across renders)
        sh.show_shadows = False; sh.show_cavity = True
        sh.cavity_type = "WORLD"; sh.cavity_ridge_factor = 0.3; sh.cavity_valley_factor = 0.6
        sh.show_object_outline = False
    else:
        sh.color_type = "MATERIAL"; sh.show_shadows = True; sh.shadow_intensity = 0.35
        sc.display.shadow_focus = 0.6; sc.display.light_direction = (0.35, -0.45, 0.82)
        sh.show_cavity = False             # cavity draws grid lines on the faceted heads
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = 0.45 if look == "previs" else 0.75   # matched to reference frame brightness
    return sc

def block(name, size, loc, color=None, rot_z=0.0, bevel=0.0):
    """Axis-aligned box. size=(x,y,z) in metres, loc = centre of the BOTTOM face."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] + size[2] / 2))
    ob = bpy.context.active_object; ob.name = name; ob.scale = size; ob.rotation_euler.z = rot_z
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        m = ob.modifiers.new("Bevel", "BEVEL"); m.width = bevel; m.segments = 3
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    ob.data.materials.append(_mat(_pick(color))); return _link(ob)

def cylinder(name, r, h, loc, color=None, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=(loc[0], loc[1], loc[2] + h / 2))
    ob = bpy.context.active_object; ob.name = name; ob.data.materials.append(_mat(_pick(color))); return _link(ob)

def room(name="Room", w=6, d=5, h=2.8, t=0.1, ceiling=True, door=None, floor_color=None, wall_colors=None, open_walls=()):
    """Each wall is its own object so every wall gets its own colour.
    door=(wall_index 0..3, offset_along_wall, width, height) cuts an opening by splitting that wall."""
    fc = floor_color or ("#8EBFAE" if KIT["look"] == "previs" else TOY["floor"])
    block(name + "_floor", (w, d, t), (0, 0, -t), fc)
    if ceiling: block(name + "_ceiling", (w, d, t), (0, 0, h), "#3A3442" if KIT["look"] == "previs" else "#5A5650")
    specs = [((w, t), (0, d / 2)), ((w, t), (0, -d / 2)), ((t, d), (w / 2, 0)), ((t, d), (-w / 2, 0))]
    for i, ((sx, sy), (x, y)) in enumerate(specs):
        if i in open_walls: continue   # 0=+Y back, 1=-Y front, 2=+X right, 3=-X left
        c = (wall_colors[i] if wall_colors else None)
        if door and door[0] == i:
            _, off, dw, dh = door; L = sx if sx > sy else sy; horiz = sx > sy
            a, b = -L / 2, off - dw / 2; c2, d2 = off + dw / 2, L / 2
            for k, (s, e) in enumerate(((a, b), (c2, d2))):
                ln, mid = e - s, (s + e) / 2
                size = (ln, t, h) if horiz else (t, ln, h)
                pos = (x + mid, y, 0) if horiz else (x, y + mid, 0)
                block(f"{name}_wall{i}_{k}", size, pos, c)
            size = (dw, t, h - dh) if horiz else (t, dw, h - dh)
            pos = (x + off, y, dh) if horiz else (x, y + off, dh)
            block(f"{name}_wall{i}_lintel", size, pos, c)
            block(f"{name}_door{i}", (dw * 0.95, 0.04, dh * 0.98) if horiz else (0.04, dw * 0.95, dh * 0.98),
                  (x + off + (dw * 0.45 if horiz else 0), y + (0 if horiz else dw * 0.45), 0), None,
                  rot_z=math.radians(70))
        else:
            block(f"{name}_wall{i}", (sx, sy, h), (x, y, 0), c)

def character(name, loc=(0, 0, 0), color=None, height=1.86, rot_z=0.0, seated=False):
    """THE pawn: rectangular box torso + sphere head, no limbs, no face.
    previs: head floats with a small gap, smooth sphere, body ~0.48w x 0.40d.
    toy:    head rests on / slightly sinks into the body, low-poly sphere (polygonal silhouette)."""
    look = KIT["look"]; s = height / 1.86
    bw, bd = 0.48 * s, 0.40 * s
    head_r = (0.25 if look == "previs" else 0.23) * s
    gap = 0.06 * s if look == "previs" else -0.03 * s
    body_h = (height - 2 * head_r - gap) * (0.55 if seated else 1.0)
    z0 = loc[2] + (0.45 * s if seated else 0)
    root = bpy.data.objects.new("CHAR_" + name, None); root.empty_display_size = 0.3
    root.location = (loc[0], loc[1], z0); root.rotation_euler.z = rot_z; _link(root)
    c = _pick(color) if color else (KIT["rng"].choice(PREVIS) if look == "previs" else TOY["white"])
    body = block(name + "_body", (bw, bd, body_h), (0, 0, 0), c); body.parent = root
    if look == "previs":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=head_r, segments=48, ring_count=24,
                                             location=(0, 0, body_h + gap + head_r))
        head = bpy.context.active_object; bpy.ops.object.shade_smooth()
        hc = KIT["rng"].choice(PREVIS)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=head_r, segments=16, ring_count=10,
                                             location=(0, 0, body_h + gap + head_r))
        head = bpy.context.active_object; bpy.ops.object.shade_smooth()   # polygonal silhouette, smooth shading
        hc = c
    head.name = name + "_head"; head.data.materials.append(_mat(hc)); _link(head); head.parent = root
    return root

def table(name, size=(1.2, 0.7), h=0.75, loc=(0, 0, 0), top=None, legs=None, round_r=None):
    if round_r:
        cylinder(name + "_top", round_r, 0.06, (loc[0], loc[1], loc[2] + h - 0.06), top)
        cylinder(name + "_base", round_r * 0.85, h - 0.06, loc, legs or "wood")
        return
    block(name + "_top", (size[0], size[1], 0.05), (loc[0], loc[1], loc[2] + h - 0.05), top)
    lc = legs or _pick(None)
    for sx in (-1, 1):
        for sy in (-1, 1):
            block(f"{name}_leg{sx}{sy}", (0.05, 0.05, h - 0.05),
                  (loc[0] + sx * (size[0] / 2 - 0.05), loc[1] + sy * (size[1] / 2 - 0.05), loc[2]), lc)

def chair(name, loc=(0, 0, 0), rot_z=0.0, color=None, legs=None):
    root = bpy.data.objects.new(name, None); root.location = loc; root.rotation_euler.z = rot_z; _link(root)
    c = color or _pick(None)
    parts = [block(name + "_seat", (0.48, 0.46, 0.06), (0, 0, 0.42), c),
             block(name + "_back", (0.48, 0.06, 0.55), (0, 0.2, 0.48), c)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(block(f"{name}_leg{sx}{sy}", (0.04, 0.04, 0.42), (sx * 0.2, sy * 0.19, 0), legs or c))
    for p in parts: p.parent = root
    return root

def bed(name, loc=(0, 0, 0), rot_z=0.0):
    root = bpy.data.objects.new(name, None); root.location = loc; root.rotation_euler.z = rot_z; _link(root)
    ps = [block(name + "_frame", (1.7, 2.1, 0.32), (0, 0, 0), None, bevel=0.03),
          block(name + "_mattress", (1.6, 2.0, 0.2), (0, 0, 0.32), None, bevel=0.05),
          block(name + "_duvet", (1.62, 1.4, 0.06), (0, -0.3, 0.5), None, bevel=0.03),
          block(name + "_headboard", (1.8, 0.1, 1.05), (0, 1.07, 0), None, bevel=0.02)]
    for x in (-0.4, 0.4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.6, vertices=24, location=(x, 0.85, 0.63),
                                            rotation=(0, math.radians(90), 0))
        p = bpy.context.active_object; p.name = name + "_pillow"; bpy.ops.object.shade_smooth()
        p.data.materials.append(_mat(_pick(None))); _link(p); ps.append(p)
    for p in ps: p.parent = root
    return root

def camera(loc=(0, -4, 1.6), look_at=(0, 0, 1.2), lens=24, name="CAM"):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_start = 0.05
    cam = bpy.data.objects.new(name, cd); cam.location = loc; _link(cam)
    d = Vector(look_at) - Vector(loc); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    KIT["scene"].camera = cam; return cam

def move(obj, path, start=1, frames_per_m=24, turn_frames=6, bob=0.0):
    """Glide a character (no walk cycle) through (x,y) points. Turns to face each leg over
    turn_frames at the corner, then slides. Optional bob (metres) for a hint of steps.
    Returns the last frame."""
    sc = KIT["scene"]; z = obj.location.z; f = start
    pts = [Vector((p[0], p[1], z)) for p in path]
    obj.location = pts[0]; obj.keyframe_insert("location", frame=f)
    for a, b in zip(pts, pts[1:]):
        d = b - a; yaw = math.atan2(d.y, d.x) + math.pi / 2   # pawn faces local -Y
        prev = obj.rotation_euler.z; yaw = prev + ((yaw - prev + math.pi) % (2 * math.pi) - math.pi)  # shortest turn
        obj.keyframe_insert("rotation_euler", index=2, frame=f)
        f += turn_frames; obj.rotation_euler.z = yaw
        obj.keyframe_insert("rotation_euler", index=2, frame=f); obj.keyframe_insert("location", frame=f)
        f += max(1, int(d.length * frames_per_m)); obj.location = b
        obj.keyframe_insert("location", frame=f); obj.keyframe_insert("rotation_euler", index=2, frame=f)
    if bob:
        for k in range(start, f + 1, 6):
            obj.location.z = z + (bob if (k // 6) % 2 else 0); obj.keyframe_insert("location", index=2, frame=k)
    sc.frame_end = max(sc.frame_end, f); return f

def render_still(path=None):
    """Quick preview. Default: <OUT_ROOT>/<scene>/preview.png"""
    sc = KIT["scene"]; _set_png(sc); path = path or os.path.join(_out_dir(), "preview.png"); sc.render.filepath = path
    bpy.ops.render.render(write_still=True, scene=sc.name); return path

def _out_dir(sub=""):
    d = os.path.join(OUT_ROOT, KIT["scene"].name, sub); os.makedirs(d, exist_ok=True); return d

def _set_png(sc):
    ims = sc.render.image_settings
    if hasattr(ims, "media_type"): ims.media_type = "IMAGE"
    ims.file_format = "PNG"; ims.color_mode = "RGB"

def export_for_ai(every=24, mp4=True, save_blend=True):
    """Previs package for AI video (Seedance / idoGen / Kling):
    <OUT_ROOT>/<scene>/
      <scene>.mp4            full motion reference (H.264)
      first.png / last.png   first & last frame (first+last-frame modes)
      keys/key_####.png      a still every `every` frames (omni-reference / storyboard)
      <scene>.blend          the scene, to tweak later
    Returns a dict of paths."""
    sc = KIT["scene"]; out = _out_dir(); res = {"dir": out}
    _set_png(sc); f0, f1 = sc.frame_start, sc.frame_end
    for tag, fr in (("first", f0), ("last", f1)):
        sc.frame_set(fr); sc.render.filepath = os.path.join(out, tag + ".png")
        bpy.ops.render.render(write_still=True, scene=sc.name); res[tag] = sc.render.filepath
    if f1 > f0:
        kd = _out_dir("keys")
        for fr in range(f0, f1 + 1, every):
            sc.frame_set(fr); sc.render.filepath = os.path.join(kd, f"key_{fr:04d}.png")
            bpy.ops.render.render(write_still=True, scene=sc.name)
        res["keys"] = sorted(glob.glob(os.path.join(kd, "*.png")))
    if mp4 and f1 > f0:
        ims = sc.render.image_settings
        if hasattr(ims, "media_type"): ims.media_type = "VIDEO"
        ims.file_format = "FFMPEG"; ff = sc.render.ffmpeg
        ff.format = "MPEG4"; ff.codec = "H264"; ff.constant_rate_factor = "HIGH"; ff.audio_codec = "NONE"
        sc.render.filepath = os.path.join(out, sc.name + "_")
        bpy.ops.render.render(animation=True, scene=sc.name)
        vids = sorted(glob.glob(os.path.join(out, sc.name + "_*.mp4")), key=os.path.getmtime)
        if vids:
            final = os.path.join(out, sc.name + ".mp4")
            if os.path.exists(final): os.remove(final)
            os.replace(vids[-1], final); res["mp4"] = final
        _set_png(sc)
    if save_blend:
        res["blend"] = os.path.join(out, sc.name + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath=res["blend"], copy=True)
    sc.frame_set(f0); return res
# ---- END BLOCKOUT KIT ----
```

## API cheat-sheet

- `new_scene(name, look="previs"|"toy", seed=7, fps=24, aspect="16:9", res=None)` creates a fresh scene and switches to it. `seed` controls which pastel colours are picked.
- `block(name, (sx,sy,sz), (x,y,z_bottom), color=None, rot_z=0, bevel=0)`. `color` can be None (a palette colour), a TOY key, or a hex value.
- `cylinder(name, r, h, (x,y,z_bottom), color, verts=32)`
- `room(name, w, d, h, ceiling=True, door=(wall_idx, offset, width, height), wall_colors=[4], open_walls=(idx,))`. Walls are 0 = +Y back, 1 = −Y front, 2 = +X, 3 = −X.
- `character(name, (x,y,z), color=None, height=1.86, rot_z=0, seated=False)` returns the `CHAR_<name>` empty. The pawn faces local −Y.
- `table(name, (w,d), h, (x,y,z), top, legs, round_r=None)`, `chair(name, (x,y,z), rot_z, color, legs)`, `bed(name, (x,y,z), rot_z)`
- `camera(loc, look_at, lens=24)`
- `move(char_root, [(x,y),...], start=1, frames_per_m=24, turn_frames=6, bob=0.0)` returns the last frame.
- `render_still(path=None)` returns the PNG path (default `<scene>\preview.png`).
- `export_for_ai(every=24, mp4=True, save_blend=True)` returns a dict of paths.

## Recipes

**Bedroom walk (previs).** Tested: the pawn walks from the foreground out through the door.
```python
new_scene("Bedroom_Walk", "previs", aspect="16:9")
room("Bedroom", w=6, d=5, h=2.8, door=(0, 1.5, 0.9, 2.1), open_walls=(1,))
bed("Bed", (-1.6, 1.0, 0)); table("Desk", (1.1, 0.6), 0.75, (-2.3, -1.4, 0))
hero = character("Hero", (0.6, -1.8, 0))
move(hero, [(0.6, -1.8), (0.6, 0.4), (1.5, 2.1)], frames_per_m=20)   # door at x=1.5 on the back wall
camera((2.4, -2.2, 1.6), (-0.2, 0.6, 1.1), lens=22)
r = export_for_ai()
```

**Bedroom still (previs).**
```python
new_scene("Bedroom", "previs")
room("Bedroom", w=5, d=4.5, h=2.7, door=(3, 0.8, 0.9, 2.1), open_walls=(1,))
bed("Bed", (-1.2, 1.0, 0)); table("Desk", (1.1, 0.6), 0.75, (1.6, 1.4, 0))
block("Dresser", (0.9, 0.45, 0.85), (-2.0, -1.2, 0)); cylinder("Rug", 1.0, 0.01, (0, -0.3, 0), "#7FA393", verts=48)
character("Hero", (-0.3, -0.2, 0), rot_z=math.radians(15))
camera((1.4, -1.9, 1.6), (-0.3, 0.6, 1.1), lens=22)
render_still()
```

**Maquette on a plinth (previs).** Build a room, then a plinth `block` about 0.7 m high. On it, lay out a mini floor plan from 0.25 m-tall thin wall blocks and add tiny pawns with `height=0.12`. Put a full-size pawn beside the plinth, looking down. Use a high 3/4 camera at about 2.6 m with `lens=24`.

**Casino table (toy).** Use `room(..., ceiling=False, wall_colors=["wall_taupe"]*4, open_walls=(1,))`. Add a dais `cylinder`, then `table(round_r=1.6, top="felt", legs="wood")`. Place 8 chairs at angle `a` with `rot_z=a - pi/2`, and 8 red `seated=True` pawns at `0.97×` the chair radius. Add blue dealers behind a counter, orange guards at the sides, and a white and a black hero pawn in the foreground.

## Gotchas

- The render is one flat colour: the camera is inside or behind a wall. Fix it with `open_walls` or move the camera.
- Pawns pass through furniture, so route `move()` paths around props.
- Workbench colour comes from `material.diffuse_color`. Don't switch `color_type` to `RANDOM`, because those colours change whenever objects are renamed.
- In background mode `bpy.context.window` is None. The kit handles this by always targeting `KIT["scene"]`.
- Brightness is matched to the reference videos through `view_settings.exposure` (previs 0.45, toy 0.75). Tune it there.
- Blender 5.x uses `image_settings.media_type` ("IMAGE"/"VIDEO"), and the kit handles it. The kit needs Blender 4.1 or later.
- In background mode, write output under `Videos\Blockouts`. That's the folder the session can read back.