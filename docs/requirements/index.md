# Requirements index

**Product:** VideoJoin (Python interactive CLI — join two local videos with FFmpeg)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type 0).  
**Product version:** **1.0.3** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)  
**Updated:** 2026-08-09

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-08-09 |
| requirement-domain-videojoin | Domain surface SSOT (four pillars: workflow, features, help, about) | domain | Active | `requirement-domain-videojoin.md` | 2026-08-09 |
| requirement-video-ffmpeg-pipeline | FFmpeg ops SSOT (stream-copy → re-encode; unique temps; shutil.move publish) | video | Active | `requirement-video-ffmpeg-pipeline.md` | 2026-08-09 |
| requirement-python-cli-interface | CLI entry points + Type N interactive session | python | Active | `requirement-python-cli-interface.md` | 2026-08-09 |
| requirement-python-coding-style | Python style; temps; **shutil.move** publish; no bare cross-mount rename | python | Active | `requirement-python-coding-style.md` | 2026-08-09 |
| requirement-python-packaging | `pyproject.toml` / version / console script packaging | python | Active | `requirement-python-packaging.md` | 2026-08-09 |
| requirement-python-project-structure | Repository and `src/VideoJoin` layout | python | Active | `requirement-python-project-structure.md` | 2026-08-09 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup | python | Active | `requirement-python-error-handling.md` | 2026-08-09 |
| requirement-runtime-prerequisites | Host FFmpeg + pip deps; no root auto-install claim | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-08-09 |

## Intentionally absent (by design)

| Surface | Status on VideoJoin |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure | **Absent** |
| Shell local `install` / `uninstall` / self-update Type 0 package | **Absent** (pip package product) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| OpenCV / duration probe dependency | **Absent** (not used by this product) |
| Second Active `requirement-domain-*` | **Forbidden** while domain-videojoin is Active |

**Install mode:** **pip / local package** (`video-join` console script). Not dual-mode shell+pip install-ensure.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for VideoJoin.  
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.  
3. Product source comments cite **only** these live requirement files — never templates/skills as behavioral authority.  
4. This versioned surface lists **requirement rows only** — do not dump templates / skills / terminologies / incidents path inventories here.  
5. Keep Status and Path in sync with each file’s header when status changes.  
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).  
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-videojoin`).  
8. **Do not introduce** online shell install or Type 1 elevation without explicit user order and registry update.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
