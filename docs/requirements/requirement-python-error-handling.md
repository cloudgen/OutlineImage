**file**: docs/requirements/requirement-python-error-handling.md  
**Status**: Active (Version 1.1.0)  
**Area**: python  
**Key**: `requirement-python-error-handling`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how VideoJoin **detects, reports, and recovers from errors** during interactive sessions and FFmpeg processing without destroying the user’s source media.

---

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore a failed join when the product claims success.  
2. **MUST NOT** treat invalid user input as success.  
3. **MUST** prefer clear human-readable messages over stack traces for expected user mistakes.  
4. **MUST** leave both source videos intact on all failure paths.

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| Fewer than two eligible videos | Discovery returns &lt; 2 | Message + non-zero exit |
| Invalid selection index | Out of range / non-numeric | Re-prompt (do not proceed) |
| FFmpeg missing | subprocess cannot find binary / version check fails | Actionable message: install FFmpeg; exit non-zero |
| Stream-copy failure | primary FFmpeg non-zero | Attempt fallback re-encode (pipeline peer); do not claim lossless success |
| Fallback failure | re-encode FFmpeg non-zero / exception | Report failure; do not claim success |
| Temp list cleanup failure | unlink errors | Best-effort; do not mask original error |

### 2.3 Cleanup on failure

5. **MUST** attempt to remove the concat list temp file after failed or successful demuxer-path jobs.  
6. **MUST NOT** delete the final user output path solely because a later optional step failed, unless the partial final is known corrupt — then document and remove only that corrupt final.  
7. **MUST NOT** delete either source media as cleanup.

### 2.4 Logging

8. **SHOULD** use ChronicleLogger for durable diagnostics when configured.  
9. **MUST** still print user-visible failure reason on the console for interactive sessions.  
10. **MUST NOT** log secrets (none expected in this product).

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Primary FFmpeg check** | `subprocess.run` on stream-copy path; success only if returncode 0 and intermediate file present |
| **Fallback FFmpeg** | second `subprocess.run`; success only if returncode 0 and intermediate present; else message + `sys.exit(1)` |
| **Fewer than two videos** | print + `sys.exit(1)` |
| **Invalid index** | re-prompt loop in `choose` |
| **Temp cleanup** | unique list + media temps unlinked in `finally` (best-effort) |
| **FFmpeg missing** | `ensure_ffmpeg` via `shutil.which` + version probe; exit non-zero before join |
| **ChronicleLogger** | optional; not required for console error paths |
| **Non-interactive** | not fully specified; prompt-only UI may hang if stdin closed — future improvement |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on encode errors and missing tools.  
- **Principle 11 – Temps**: Cleanup without destroying sources.  
- **Principle 12 – Traceability**: User-visible failure reasons.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Invalid selection never reaches FFmpeg.  
- **Intentional:** Category table is product law.  
- **Anti-fragile:** Cleanup best-effort.  
- **Over-protect:** Source media is sacred.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Swallow FFmpeg errors without user-visible failure.  
2. Delete source media on error.  
3. Claim success after a failed join.  
4. Replace clear messages with silent `pass`.  
5. Log credentials or API tokens (none should exist).

**Violating this rule is a critical safety regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Invalid selection does not encode |
| AC-2 | FFmpeg missing surfaces actionable error |
| AC-3 | Source files remain after failure |
| AC-4 | Temp list cleaned best-effort |
| AC-5 | Fewer than two videos exits with message |
| AC-6 | Failed join does not print pure success |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | Ops that can fail |
| `requirement-python-cli-interface` | Prompts / exits |
| `requirement-runtime-prerequisites` | Missing FFmpeg |
| `requirement-domain-videojoin` | Session outcomes |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ERR-01** | `tests/test_errors.py` | todo | No FFmpeg → message |
| **TP-ERR-02** | `tests/test_errors.py` | todo | One video only → exit |
| **TP-ERR-03** | `tests/test_errors.py` | todo | Sources intact after failed encode |
| **TP-FFMPEG-05** | `tests/test_ffmpeg_pipeline.py` | todo | Fallback fail-closed |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial error-handling law for VideoJoin |
| 2026-08-09 | Active 1.1.0 | Fail-closed fallback + unique temp cleanup notes |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
