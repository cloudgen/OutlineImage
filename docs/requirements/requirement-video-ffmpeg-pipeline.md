**file**: docs/requirements/requirement-video-ffmpeg-pipeline.md  
**Status**: Active (Version 1.1.0)  
**Area**: video  
**Key**: `requirement-video-ffmpeg-pipeline`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **operational Single Source of Truth** for VideoJoin media processing: two-file concat via FFmpeg, preferred stream-copy path, re-encode fallback, concat list lifecycle, intermediate staging, publish via **`shutil.move`**, and invocation rules.

Domain feature catalog and user workflow labels live in **`requirement-domain-videojoin`**. Interactive prompts live in **`requirement-python-cli-interface`**. File move/temp style lives in **`requirement-python-coding-style`**.

---

## 2. Core Rules (Mandatory)

### 2.1 Pipeline order

1. **MUST** process a join job in this order: **validate inputs → prepare unique concat list (demuxer path) → stream-copy to intermediate → on success publish intermediate to final → else re-encode to intermediate → on success publish → cleanup temps**.  
2. **MUST** write the final successful output to the user-chosen output path (or default name).  
3. **MUST NOT** overwrite or delete the user’s two **source** files as the “output” path.  
4. **MUST NOT** use either source path as the final output path.

### 2.2 Primary path — stream copy (concat demuxer)

5. **MUST** attempt a **stream-copy** join first when implementing the default product path (no re-encode when codecs/container allow).  
6. **MUST** use FFmpeg concat demuxer with a **unique temporary** file list listing both inputs in order (absolute paths preferred in the list).  
7. **MUST** map video and optional audio (`-map 0:v` and audio if present) so audio is not dropped when present on the concat stream.  
8. **MUST** use non-interactive overwrite flags on FFmpeg stages that intentionally replace intermediates (`-y`).  
9. **MUST** treat stream-copy success as: FFmpeg exit code **0** **and** intermediate output file present and non-empty.  
10. On stream-copy success, **MUST** publish the intermediate to the final path via **`promote_file` / `shutil.move`** (see coding-style peer).

### 2.3 Fallback path — re-encode concat

11. When stream-copy fails (non-zero exit or missing intermediate), **MUST** attempt a **re-encode** concat of the same two sources into a temporary intermediate (not claimed as success yet).  
12. **MUST** keep video and audio streams joined into one continuous output for both inputs (product uses `filter_complex` concat of `v` and `a`).  
13. **MUST** treat fallback success only as: FFmpeg exit code **0** **and** intermediate present and non-empty.  
14. On fallback success, **MUST** publish via **`shutil.move`** (or thin wrapper).  
15. On fallback failure, **MUST NOT** print a success message; **MUST** fail closed (non-zero process exit from the join session).  
16. **MUST** document encode defaults in Implementation Notes.  
17. Changing codec/CRF/preset/bitrate **MUST** update Implementation Notes in the same change as code.  
18. **MUST NOT** claim a lossless pipeline when the fallback re-encode path ran.

### 2.4 FFmpeg invocation

19. **MUST** invoke the system **`ffmpeg`** binary (PATH-resolved) via subprocess — not a reimplemented codec stack.  
20. **MUST** use argument lists (not shell string interpolation of free-form user filter graphs).  
21. **MUST** treat missing `ffmpeg` as a **runtime prerequisite failure** (pointer to `requirement-runtime-prerequisites`) before join work proceeds.  
22. **MUST NOT** require root/sudo for FFmpeg.

### 2.5 Temporary files, staging, publish, cleanup

23. **MUST** create the concat list with a **unique** temp path (prefer same filesystem as final output when writable).  
24. **MUST** stage large media intermediates with unique temps near the final output when possible (`requirement-python-coding-style`).  
25. **MUST** publish completed intermediates with **`shutil.move`** (or `promote_file` wrapper) — **not** bare `os.replace`/`os.rename` alone.  
26. **MUST** attempt cleanup of concat list and leftover intermediates after success or failure (best-effort; do not mask the primary error).  
27. **MUST NOT** leave success dependent on deleting the user’s source media.  
28. **MUST NOT** use a fixed cwd-only name such as bare `filelist.txt` as the only concat-list strategy.

### 2.6 Source safety

29. **MUST** treat both input paths as read-only inputs for the join job.  
30. **MUST** fail closed if either input cannot be used by FFmpeg (surface error via error-handling peer).

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Ops module** | `src/VideoJoin/cli.py` |
| **Helpers** | `staging_dir_for`, `make_temp_path`, `promote_file`, `create_file_list`, `join_videos`, `ensure_ffmpeg` |
| **Primary command shape** | `ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i <list> -c copy -map 0:v -map 0:a? <temp_out>` |
| **Concat list** | unique temp via `make_temp_path(".txt", final_out)`; lines `file '<abs-posix>'\n` |
| **Fallback command shape** | `ffmpeg -y … -i vid1 -i vid2 -filter_complex '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]' -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k -map '[v]' -map '[a]' <temp_out>` |
| **Fallback encode** | video libx264 CRF 18 preset `fast`; audio AAC 192k |
| **Publish** | `promote_file` → `shutil.move` temp → final |
| **Promote gate checklist** | **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** (fill when auditing promote) |
| **User docs** | Root `README.md` must describe copy-first, re-encode fallback, fail-closed, temps + `shutil.move` publish honestly |
| **Overwrite policy** | Final path may replace prior same-named output; sources never targeted as output |
| **Cleanup** | Unlink list + unused temps in `finally` |
| **Elevation** | None — all work as invoking user |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Prefer non-destructive source handling; external FFmpeg may fail.  
- **Principle 2 – Intentional**: Copy-first then fallback order is product law.  
- **Principle 11 – Temps**: Unique list + intermediate lifecycle is explicit.  
- **Principle 5 – SSOT**: One ops home for join/encode behavior.  
- **Principle 3 – Anti-fragile**: Multi-mount publish via `shutil.move`.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fail closed on missing FFmpeg and failed fallback; do not silently claim success.  
- **Intentional:** Stream-copy first, re-encode second, then publish.  
- **Anti-fragile:** Unique temps + `shutil.move` cover USB/cross-mount.  
- **Over-protect:** Source paths are read-only inputs.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Overwrite or delete the user’s source media as the “output” path.  
2. Drop audio mapping while claiming “original audio preserved.”  
3. Remove concat-list / intermediate cleanup without an explicit alternative safety design.  
4. Shell-out to FFmpeg with unsanitized free-form user filter graphs.  
5. Move full encode law only into domain without keeping this ops SSOT.  
6. Add root/sudo FFmpeg elevation without elev allowlist law and user order.  
7. Remove the stream-copy-first policy without updating domain/README claims about lossless join.  
8. Print success after a non-zero FFmpeg fallback.  
9. Reintroduce fixed-name cwd `filelist.txt` as the only list strategy.  
10. Replace `shutil.move` publish with bare cross-mount rename alone.

**Violating this rule is a critical media-safety regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Stream-copy concat attempted before re-encode fallback |
| AC-2 | Two sources joined in selection order |
| AC-3 | Source files not modified in place as outputs |
| AC-4 | Unique concat list cleaned best-effort |
| AC-5 | Fallback encode defaults documented |
| AC-6 | FFmpeg missing handled as prerequisite failure before join |
| AC-7 | Fallback non-zero exits fail closed (no false success) |
| AC-8 | Intermediate publish uses `shutil.move` / `promote_file` |
| AC-9 | Temps staged near final output when parent is writable |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-videojoin` | Domain surface |
| `requirement-python-cli-interface` | User inputs |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-python-coding-style` | Temps + `shutil.move` |
| `requirement-runtime-prerequisites` | `ffmpeg` present |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-FFMPEG-01** | `tests/test_ffmpeg_pipeline.py` | todo | Stream-copy join two compatible MP4 |
| **TP-FFMPEG-02** | `tests/test_ffmpeg_pipeline.py` | todo | Fallback when copy fails |
| **TP-FFMPEG-03** | `tests/test_ffmpeg_pipeline.py` | todo | Unique list cleanup after run |
| **TP-FFMPEG-04** | `tests/test_ffmpeg_pipeline.py` | todo | Source files unchanged after join |
| **TP-FFMPEG-05** | `tests/test_ffmpeg_pipeline.py` | todo | Fallback fail-closed |
| **TP-FS-01** | `tests/test_fs_publish.py` | todo | promote uses shutil.move |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial FFmpeg join pipeline law for VideoJoin |
| 2026-08-09 | Active 1.1.0 | Unique temps, shutil.move publish, fail-closed fallback |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
