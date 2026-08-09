**file**: docs/requirements/requirement-python-coding-style.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-coding-style`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define **Python coding style and defensive file I/O conventions** for VideoJoin: how agents and maintainers write Python so path/temp/publish behavior stays multi-mount safe (including USB), without duplicating domain or FFmpeg pipeline tables.

Pipeline-specific apply of these rules is owned by **`requirement-video-ffmpeg-pipeline`**.

---

## 2. Core Rules (Mandatory)

### 2.1 General style (this product)

1. **MUST** keep the installable package under `src/VideoJoin/` with thin module entry (`__main__` / console script → `cli.main`).  
2. **MUST** cite only live `docs/requirements/requirement-*.md` keys in product-source law comments — never templates or skills as behavioral authority.  
3. **SHOULD** use clear function **General Purpose** docstrings on public helpers.  
4. **MUST** fail closed with user-visible messages on expected errors (missing FFmpeg, fewer than two videos, failed join).  
5. Optional logging deps (e.g. ChronicleLogger) **SHOULD** not break package import when unused; do not re-export names that are not defined in the package.  
6. Full StateLogic+Attr OOP shape is **aspirational** for this product’s current interactive CLI; **MUST NOT** force a whole-file rewrite solely for style while the specialized architecture remains procedural-interactive (respect working code). Future OOP migration requires explicit user order and updated REQs.

### 2.2 Temporary files

7. When the final destination path is known, **MUST** prefer creating intermediate files on the **same filesystem/mount as that destination** (writable parent of the final path).  
8. **MUST NOT** assume system `TMPDIR` / `/tmp` is the same mount as user media (USB, network, secondary disks).  
9. **MUST** clean intermediate temps on success and failure paths (best-effort).  
10. **MUST NOT** use a fixed predictable cwd name (e.g. bare `filelist.txt`) as the sole concat-list path when a unique temp can be created.

### 2.3 Publishing / moving completed files (sacred)

11. To **move or publish** a completed intermediate file from a temporary path to its final path, **MUST** use **`shutil.move`** (or a thin wrapper whose only move implementation is `shutil.move`).  
12. **MUST NOT** use bare **`os.replace`**, **`os.rename`**, **`pathlib.Path.replace`**, or **`pathlib.Path.rename`** alone as the sole publish mechanism when source and destination may be on different mounts.  
13. **MAY** still use same-FS rename semantics **inside** what `shutil.move` performs; do not reimplement fragile bare rename as product publish.  
14. **`shutil.copy2` / `copy` / `copyfile`** copy only — if used, **MUST** define whether source is kept or deleted; they are not a complete “move” by themselves.  
15. FFmpeg **MAY** write the final path directly when no intermediate publish step exists; when an intermediate is used, publish **MUST** go through `shutil.move` (or wrapper).

### 2.4 Corresponding commands / APIs (reference)

| Intent | Prefer | Avoid as sole cross-mount publish |
|--------|--------|-----------------------------------|
| Move/publish file | **`shutil.move(src, dst)`** | bare **`os.replace`**, **`os.rename`** |
| pathlib-oriented move | `Path` args + **`shutil.move`** | bare **`Path.replace`**, **`Path.rename`** across mounts |
| Copy keep source | `shutil.copy2` | treating copy as move without unlink policy |
| Same-FS atomic finish | OK via **`shutil.move`** rename path | assuming all mounts are identical |

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `VideoJoin` |
| **Primary modules** | `src/VideoJoin/cli.py`, `__main__.py`, `__init__.py` |
| **Staging helpers** | `staging_dir_for`, `make_temp_path` |
| **Publish helper** | `promote_file` → `shutil.move` |
| **Ops apply** | `requirement-video-ffmpeg-pipeline` |
| **Gate checklist (cite ID)** | **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** — run when auditing promote/staging publish paths |
| **Architecture shape today** | Interactive procedural CLI; not full StateLogic yet |
| **Version** | `1.0.3` |
| **User docs** | Root `README.md` Features must not claim Cython-required runtime or fixed `filelist.txt`-only strategy |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Multi-mount path failures are designed around.  
- **Principle 3 – Anti-fragile**: USB and system disk both work for publish.  
- **Principle 5 – SSOT**: One coding-style home for move/temp rules.  
- **Principle 11 – Temps**: Explicit staging and cleanup.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not assume one filesystem.  
- **Intentional:** `shutil.move` is the named publish API.  
- **Anti-fragile:** Same-FS temps reduce full-file copies.  
- **Over-protect:** Protection against reintroducing bare cross-device rename.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Replace `shutil.move` publish with bare `os.replace`/`os.rename` “for simplicity.”  
2. Stage all large intermediates only under system temp when final dest is known on another mount.  
3. Cite templates/skills as product-source behavioral authority.  
4. Force a full StateLogic rewrite without explicit user order while this REQ allows current interactive shape.  
5. Store secrets in style docs or code.  
6. Reintroduce fixed-name cwd `filelist.txt` as the only concat-list strategy.

**Violating this rule is a critical regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Publish of intermediates uses `shutil.move` (or thin wrapper) |
| AC-2 | Bare cross-mount rename forbidden as sole publish |
| AC-3 | Same-FS staging preferred when dest known |
| AC-4 | Pipeline REQ remains ops SSOT for encode |
| AC-5 | Registered in index |
| AC-6 | Package `__init__` does not import undefined symbols from `.cli` |
| AC-7 | Promote path audited with **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** (Pass or Revise with open residual) when ship publish code changes |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | Applies move/temp rules to encode |
| `requirement-python-project-structure` | Layout |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-python-cli-interface` | Entry |
| `requirement-python-packaging` | Export honesty |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-FS-01** | `tests/test_fs_publish.py` | todo | `shutil.move` publish helper |
| **TP-FS-02** | `tests/test_fs_publish.py` | todo | staging prefers dest parent when writable |
| **TP-PKG-01** | `tests/test_packaging.py` | todo | `import VideoJoin` succeeds |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Coding style + shutil.move / multi-mount file I/O for VideoJoin |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
