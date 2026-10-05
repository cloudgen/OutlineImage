# Requirements index

**Product:** VideoJoin (Python CLI — text menu on a terminal; join two local videos with FFmpeg)
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type O).
**Product version:** **1.0.5** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)
**Updated:** 2026-10-04

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-04 |
| requirement-domain-videojoin | Domain surface SSOT (four pillars: join verb, list-videos, help, about) | domain | Active | `requirement-domain-videojoin.md` | 2026-10-04 |
| requirement-python-about | About page: identity, host check, star box. No `--json` | python | Active | `requirement-python-about.md` | 2026-10-04 |
| requirement-video-ffmpeg-pipeline | FFmpeg ops SSOT (stream-copy → re-encode; unique temps; shutil.move publish) | video | Active | `requirement-video-ffmpeg-pipeline.md` | 2026-10-04 |
| requirement-python-cli-interface | CLI entry, typed verbs, empty-argv menu on a terminal and help off a terminal | python | Active | `requirement-python-cli-interface.md` | 2026-10-04 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`; required floor points at packaging | python | Active | `requirement-python-cli-logging.md` | 2026-10-04 |
| requirement-python-tui | Text menu: join, system-log, language, self-management, Exit. Path word is selected by the language requirement. Default is `Path`. Menu columns are display columns | python | Active | `requirement-python-tui.md` | 2026-10-04 |
| requirement-python-cli-language | Menu language: front row 4, codes 41–53, leaf `~/.local/VideoJoin/language`. `language` is not an argv verb | python | Active | `requirement-python-cli-language.md` | 2026-10-04 |
| requirement-python-oop | L2 class map. Running tree stays three modules until an implement order | python | Active | `requirement-python-oop.md` | 2026-10-04 |
| requirement-python-coding-style | Python style; temps; **shutil.move** publish; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-04 |
| requirement-python-packaging | `pyproject.toml` / version / console script; ChronicleLogger floor | python | Active | `requirement-python-packaging.md` | 2026-10-04 |
| requirement-python-project-structure | Repository and `src/VideoJoin` layout (running tree vs target map) | python | Active | `requirement-python-project-structure.md` | 2026-10-04 |
| requirement-python-readme | Root user document: sections, badges, picture catalog, related projects | python | Active | `requirement-python-readme.md` | 2026-10-04 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-04 |
| requirement-runtime-prerequisites | Host FFmpeg + required ChronicleLogger; no root auto-install | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-04 |

## Intentionally absent (by design)

| Surface | Status on VideoJoin |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure / `curl\|sh` | **Absent** |
| Shell local `install` / `uninstall` / shell self-update | **Absent** (pip package) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| OpenCV / duration probe dependency | **Absent** |
| Second Active `requirement-domain-*` | **Forbidden** while domain-videojoin is Active |
| Front row 2, cut / speed / boomerang, `list-mp4` | **Absent**. Front row 1 is `join`. Typed list is `list-videos` |
| `requirement-python-dependency-management` | **Absent**. ChronicleLogger floor is packaging + runtime. Law and the live manifest are `ChronicleLogger>=1.3.1` |
| `requirement-python-version` | **Absent**. Version SSOT is the `__version__` string |
| `requirement-python-json-output` | **Absent**. This product does not claim `--json`. The about page does not grow a JSON stream |
| `requirement-python-graceful-exit` | **Absent**. Control-C is not confirmed law. Row 9 Exit returns 0 with no confirm |
| `requirement-python-interactive-vs-noninteractive` | **Absent**. Empty argv on a terminal versus help off a terminal is the CLI interface |
| `requirement-python-pyenv`, `requirement-python-conda`, build-script, `requirement-python-oop-architecture` | **Absent**. Host-check path reads for pyenv and conda stay on `requirement-python-about`. Class homes are `requirement-python-oop` |
| Actor-role requirement file | **Absent**. Class residual is no dest approver |

**Install mode:** **pip / local package** (`video-join` console script). Not a shell installer.

**Pip lifecycle:** claimed. Rows 84–87 and the typed verbs `version-check`, `self-update`, `self-install`, and `self-uninstall` are `requirement-python-cli-interface` and `requirement-python-tui`. They use `python -m pip`. They are not a shell channel. Empty argv does not run them.

**Logger:** required (`ChronicleLogger>=1.3.1` in law and in `pyproject.toml`). `def main` in `src/VideoJoin/cli.py` writes `ChronicleLogger(...)`.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for VideoJoin.
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.
3. Product source comments cite **only** these live requirement files.
4. This versioned surface lists **requirement rows only**.
5. Keep Status and Path in sync with each file’s header when status changes.
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-videojoin`).
8. **Do not introduce** a shell installer or Type 1 elevation without an explicit user order and a registry update.
9. **Do not** treat pip rows 84–87 as a reason to add a shell installer. **Do not** mark those pip rows absent.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
