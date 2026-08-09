**file**: docs/requirements/requirement-domain-videojoin.md  
**Status**: Active (Version 1.0.0)  
**Area**: domain  
**Key**: `requirement-domain-videojoin`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for VideoJoin: which **user-facing video-join workflow steps** exist, what **features** the product claims, and how **help / about / session messaging** must describe them.

**Operational FFmpeg processing** (concat stream-copy, re-encode fallback, temp list cleanup) is **not** fully owned here — it is owned by **`requirement-video-ffmpeg-pipeline`**.  
**CLI entry and interactive session contract** are owned by **`requirement-python-cli-interface`**.

This file remains the sole Active **`requirement-domain-*`** (four pillars).

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI surface (workflow steps)

VideoJoin is an **interactive domain CLI** (not a multi-verb Type 0 shell product). Domain surface **MUST** be expressed as the following ordered session steps after entry:

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Discover videos | scan **current working directory** only | Sorted eligible video list | CLI + domain |
| D-02 | Choose first video | 1-based index into list | Chosen `Path` for first input | CLI + domain |
| D-03 | Choose second video | 1-based index into **remaining** list (first removed) | Chosen `Path` for second input; **MUST NOT** allow the same path twice | CLI + domain |
| D-04 | Choose output name | free string; empty → default pattern | Final output filename | domain + pipeline |
| D-05 | Join | two source paths + output name | Concat via FFmpeg (copy first, re-encode fallback) | `requirement-video-ffmpeg-pipeline` |
| D-06 | Report result | — | Success or failure message; temp list cleaned | CLI + error peer |

**Routing:** Entry (`video-join` / `python -m VideoJoin` / `VideoJoin.cli:main`) **MUST** reach this interactive domain session unless a future Active requirement adds non-interactive flags.

**Non-goals as domain commands (unless a future requirement adds them):** join more than two files in one session, recursive multi-folder batch queue, GUI, cloud upload, timeline multi-track editor, automatic color grade, cut/speed/boomerang editing (that is sibling product scope), root/system install ensure.

### 2.2 Pillar B — Specialized features (surface map)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Video discovery (cwd, case-insensitive suffixes) | Expose list for selection | this file + CLI |
| Two-file selection without duplicates | User picks first then second from remaining | this file + CLI |
| Output naming | Default `{stem1} + {stem2}.mp4`; append `.mp4` when extension not in allowed set | this file |
| Lossless join when possible | Prefer stream copy | `requirement-video-ffmpeg-pipeline` |
| Compatible re-encode fallback | When concat-copy fails | `requirement-video-ffmpeg-pipeline` |
| FFmpeg presence check | Fail closed before session join | `requirement-runtime-prerequisites` |

Domain **MUST NOT** restate full FFmpeg command graphs in a second competing SSOT. Pointers and feature catalog only.

### 2.3 Pillar C — Specialized project help items

Because the product is **prompt-driven**, “help” **MUST** be available as:

1. **Session banners / step labels** that name the domain capabilities: discover, pick two videos, name output, join with original audio when possible.  
2. **Product README** domain rows that match this catalog.  
3. When a future `--help` flag is implemented (CLI peer), it **MUST** list the same capabilities and non-goals.

Help / README domain rows **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Working directory | Videos must be in the current folder (not recursive today) |
| Formats | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` |
| Selection | First then second video; second list excludes first |
| Output | Default `{name1} + {name2}.mp4` |
| Quality | Stream copy first; re-encode fallback if needed |
| Prerequisite | FFmpeg on PATH |

### 2.4 Pillar D — Specialized project about items

Product identity / about **MUST** be able to report (via package metadata and/or future `about`/`--version` surface):

| Field / line | Content |
|--------------|---------|
| Product name | VideoJoin |
| Version | Package version SSOT (`__version__` / `pyproject.toml`) |
| Domain summary | Concatenate two local videos with FFmpeg (copy then fallback) |
| Runtime tools | FFmpeg (concat / encode) |
| Entry points | `video-join`, `python -m VideoJoin` |

**About is not** a remote version-check and **must not** advertise a shell `curl|sh` install channel unless a future install requirement is Active.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoJoin` |
| **Console script** | `video-join` |
| **Domain implementation module** | `src/VideoJoin/cli.py` |
| **VERSION** | `1.0.3` (align `__init__.py` and `pyproject.toml`) |
| **Input formats (current)** | `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` (suffix match, case-insensitive) |
| **Scan scope** | Current working directory only (`Path('.').iterdir()`); not recursive |
| **Output location** | Path as entered/default (typically cwd relative name) |
| **Output name default** | `{vid1.stem} + {vid2.stem}.mp4` |
| **Output extension rule** | If name does not end with `.mp4` / `.mkv` / `.mov` (case-insensitive), append `.mp4` |
| **Ops SSOT** | `requirement-video-ffmpeg-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Current interaction model** | Interactive prompts by default; no argparse surface today |
| **User docs** | Root `README.md` Features / Usage / Examples must list two-file cwd join, formats, copy-then-fallback |
| **Publish / temps** | Owned by pipeline + coding-style peers (`shutil.move` promote) |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full encode law.  
- **Principle 5 – SSOT**: One Active domain file for feature catalog.  
- **Principle 1 – Caution**: Non-goals listed so agents do not invent cloud/GUI/N-file batch scope.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second FFmpeg ops SSOT in domain.  
- **Intentional:** Pillars A–D only; encode details in pipeline requirement.  
- **Anti-fragile:** Clear ownership boundaries reduce drift between README and CLI.  
- **Over-protect:** Keep sole Active domain file; supersede before replace.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full FFmpeg filter/command law here once `requirement-video-ffmpeg-pipeline` is Active.  
2. Add online install, cloud upload, or root elevation as silent domain behavior without new requirements.  
3. Create a second Active `requirement-domain-*` without superseding this one.  
4. Drop two-file join or multi-format discovery from the claimed domain catalog while README still advertises them.  
5. Claim recursive multi-folder batch or N-file join without updating this file and peers.  
6. Silently re-scope this product into cut/speed/boomerang editing without domain rename / new REQs.

**Violating this rule is a critical domain regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present (workflow steps, feature map, help framing, about fields) |
| AC-2 | Two-video selection without duplicates documented |
| AC-3 | Output naming default and extension rule documented |
| AC-4 | Non-goals include cloud/GUI/Type 0 shell install / N-file batch unless later law says otherwise |
| AC-5 | Registered as sole Active domain SSOT |
| AC-6 | No competing full FFmpeg ops body (defers to video-ffmpeg-pipeline) |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | **Operational encode SSOT** |
| `requirement-python-cli-interface` | Entry + interactive session |
| `requirement-runtime-prerequisites` | FFmpeg presence |
| `requirement-python-error-handling` | Insufficient files / FFmpeg failures |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-VIDEOJOIN-01** | `tests/test_domain_join.py` | todo | Interactive two-file join path |
| **TP-VIDEOJOIN-02** | `tests/test_domain_join.py` | todo | Default output name |
| **TP-VIDEOJOIN-03** | `tests/test_domain_join.py` | todo | Fewer than two videos → clear exit |
| **TP-VIDEOJOIN-04** | `tests/test_domain_join.py` | todo | No same-file twice (optional) |
| **TP-CLI-03** | `tests/test_cli.py` | todo | Peer: empty/single video exit |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for VideoJoin interactive two-file join |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
