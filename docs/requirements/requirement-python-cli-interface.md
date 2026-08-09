**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official **command-line entry points**, **empty-argv behavior**, and **interactive session contract** for the VideoJoin Python package.

Domain step catalog is owned by **`requirement-domain-videojoin`**. Encode ops are owned by **`requirement-video-ffmpeg-pipeline`**.

---

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named **`video-join`** pointing at `VideoJoin.cli:main` (declared in packaging SSOT).  
2. **MUST** support module execution: **`python -m VideoJoin`**.  
3. **MUST** keep `main()` as the single runtime entry for the interactive join session (thin package surface).  
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv / default mode (Type N)

5. **MUST** treat bare invocation (`video-join` with no args) as **Type N**: start the **interactive domain session**, not Type O online install-ensure.  
6. **MUST NOT** default empty argv to shell channel install or self-update.  
7. Future non-interactive flags **MAY** be added only with Active updates to this file and domain peers.

### 2.3 Interactive session contract

8. **MUST** scan the **current working directory** for eligible video files (domain format set).  
9. **MUST** list discoverable videos with 1-based indices, sorted case-insensitively by name.  
10. **MUST** exit cleanly with a clear message when fewer than **two** eligible videos are found.  
11. **MUST** prompt for first video index, then second index from the **remaining** set (first choice excluded).  
12. **MUST** re-prompt on non-numeric or out-of-range selection rather than proceeding with invalid indices.  
13. **MUST** prompt for output filename with a documented default when empty.  
14. **MUST** print the chosen pair and output path before running FFmpeg.  
15. **MUST** print a clear success or failure outcome after the join attempt.

### 2.4 Flags (current vs future)

16. **Current product law:** interactive prompts only — no required argparse surface.  
17. When flags are introduced, **MUST** document them in this file’s Implementation Notes and keep domain catalog honest.  
18. Recommended future flags (not required until implemented): `--help`, `--version`, optional non-interactive operands for file1/file2/output.

### 2.5 Output behavior

19. **MUST** print human-readable progress for discovery, selection, and FFmpeg stages.  
20. **SHOULD** route durable diagnostics through ChronicleLogger when logging is wired; **MUST** still emit user-visible errors on failure paths.  
21. **MUST NOT** mix machine-only JSON mode into normal interactive sessions unless a `--json` mode is explicitly implemented and documented.

### 2.6 Non-interactive environments

22. When stdin is not a TTY, interactive prompts **SHOULD** fail closed with a clear message **or** require non-interactive flags once those exist.  
23. Agents **MUST NOT** assume CI can drive the current prompt-only UI without a test harness that feeds stdin.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `video-join = VideoJoin.cli:main` |
| **Module entry** | `src/VideoJoin/__main__.py` → `main()` |
| **CLI module** | `src/VideoJoin/cli.py` |
| **Empty argv** | Banner + cwd scan + prompts (`ensure_ffmpeg` first) |
| **Argparse** | not implemented today |
| **Quiet/JSON flags** | not implemented today |
| **Privilege** | user-level only |
| **Ship CLI SSOT** | `src/VideoJoin/cli.py` |
| **Startup gate** | `ensure_ffmpeg()` (`shutil.which` + `ffmpeg -version`) inside `main()` |
| **Selection helpers** | `get_video_files`, `show_list`, `choose`, `resolve_output_name` |
| **Join helper** | `join_videos` (pipeline peer) |
| **User docs** | Root `README.md` Usage / Examples must match this contract |
| **Product version** | `1.0.3` |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry and Type N empty-argv are explicit.  
- **Principle 16 – Interactive awareness**: Prompt UI is declared; CI limits honest.  
- **Principle 5 – SSOT**: One CLI surface for entry contract.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fewer than two videos → exit; invalid index → re-prompt.  
- **Intentional:** Interactive default matches product design.  
- **Anti-fragile:** Module + console script dual entry.  
- **Over-protect:** No install-ensure on empty argv.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv to Type O online install without explicit user order and new install requirements.  
2. Remove console script or module entry without packaging + docs update.  
3. Bypass domain/pipeline peers by reimplementing join only in a second ad-hoc script as the “real” product.  
4. Require root to run normal joining.  
5. Allow selecting the same file twice as first and second without domain law change.

**Violating this rule is a critical CLI regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `video-join` entry declared in packaging |
| AC-2 | `python -m VideoJoin` works |
| AC-3 | Empty argv starts interactive session |
| AC-4 | Fewer than two videos → clear exit |
| AC-5 | Invalid index re-prompts |
| AC-6 | Success or failure is user-visible after FFmpeg |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-videojoin` | Domain steps |
| `requirement-video-ffmpeg-pipeline` | Encode ops |
| `requirement-python-packaging` | Console script name |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-runtime-prerequisites` | FFmpeg check |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-01** | `tests/test_cli.py` | todo | Module entry starts session |
| **TP-CLI-02** | `tests/test_cli.py` | todo | Invalid index re-prompt |
| **TP-CLI-03** | `tests/test_cli.py` | todo | Empty cwd / single video exit |
| **TP-CLI-04** | `tests/test_cli.py` | optional | Non-TTY fail-closed |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law for VideoJoin |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
