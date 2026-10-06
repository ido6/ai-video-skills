# ai-video-skills

Claude Code / Claude.ai skills for planning and prompting AI video (Seedance 2.5, idoGen, Higgsfield), built around a Blender previs → photoreal video pipeline.

| Skill | What it does |
|---|---|
| `skills/idogen-video-brain` | Cinematic video-prompt discipline for idoGen / Seedance / Kling / Veo. `references/previs-to-seedance-playbook.md` is the full blockout → photoreal pipeline (limits, sheets, prompt template, QC). |
| `skills/cinematography` | Shot language, lighting, lenses. `references/camera-directing-playbook.md` covers 9:16 composition, handheld with tension, lens/FOV tables, camera packages, packshots. Based on [fal-ai-community/skills](https://github.com/fal-ai-community/skills) (see `INSTALL-SOURCE.md`). |
| `skills/blender-blockout-pawns` | Builds pawn-style Blender blockouts and exports them as motion/structure references for AI video. Replace `<BLENDER_EXE>` and `<BLOCKOUTS_DIR>` with your paths. |
| `skills/seedance-25` | Seedance 2.5 multishot omni-reference prompts. |

## Install

Claude Code: copy a skill folder into `~/.claude/skills/`.
Claude.ai: zip a skill folder and upload it under Settings → Skills.

Rules carry confidence tags ([official], [field], [inference], [unverified]). Treat [unverified] items as hypotheses to test.
