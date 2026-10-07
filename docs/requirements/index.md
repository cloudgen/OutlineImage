# Requirements index

**Product:** OutlineImage (Python CLI — text menu on a terminal; `outline` writes a detailed outline image for each picture in a chosen folder, default PNG in that folder's `output` directory; menu row 1 picks the current folder or a subfolder)
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type O).
**Product version:** **1.0.1** (align `pyproject.toml`, `__init__.__version__`, root `README.md` Version badge)
**Updated:** 2026-10-07

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-07 |
| requirement-domain-outlineimage | Domain surface SSOT (typed `outline`, folder board on menu row 1, help, about, waiting sentence and a flashing please-wait bullet before converting images and before a model download; lines from brightness and color, sensitivity per photo, no guessed shape) | domain | Active | `requirement-domain-outlineimage.md` | 2026-10-07 |
| requirement-python-about | About page: identity, host check, star box. No `--json` | python | Active | `requirement-python-about.md` | 2026-10-07 |
| requirement-video-ffmpeg-pipeline | Retired. No encoder, no concat, no media publish | video | Retired | `requirement-video-ffmpeg-pipeline.md` | 2026-10-05 |
| requirement-python-cli-interface | CLI entry, typed verbs, empty-argv menu on a terminal and help off a terminal. `outline` and `./convert.py` print the waiting sentence, flash please wait on a terminal, and erase that bullet when the work finishes | python | Active | `requirement-python-cli-interface.md` | 2026-10-07 |
| requirement-python-cli-logging | ChronicleLogger construct in `def main`; required floor points at packaging | python | Active | `requirement-python-cli-logging.md` | 2026-10-07 |
| requirement-python-tui | Text menu: outline, system-log, language, self-management, Exit. Row 1 lists the current folder, each subfolder, and back. A folder pick paints a working page with the waiting sentence and a flashing please-wait bullet. The bullet is gone on the result page. Path word is selected by the language requirement. Default is `Path`. Menu columns are display columns | python | Active | `requirement-python-tui.md` | 2026-10-07 |
| requirement-python-cli-language | Menu language: front row 4, codes 41–53, leaf `~/.local/OutlineImage/language`. `language` is not an argv verb | python | Active | `requirement-python-cli-language.md` | 2026-10-04 |
| requirement-python-oop | L2 class map. Running tree stays three modules until an implement order | python | Active | `requirement-python-oop.md` | 2026-10-04 |
| requirement-python-coding-style | Python style; temps; **shutil.move** publish; end state is the class map | python | Active | `requirement-python-coding-style.md` | 2026-10-04 |
| requirement-python-packaging | `pyproject.toml` / version / console script. Pip strings point at the dependency file | python | Active | `requirement-python-packaging.md` | 2026-10-07 |
| requirement-python-dependency-management | Pip strings: `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `Pillow>=12.1.0`, `opencv-python-headless>=5.0.0.93`, `rembg>=2.0.85`. No GUI `opencv-python`. No menu wheel | python | Active | `requirement-python-dependency-management.md` | 2026-10-05 |
| requirement-python-project-structure | Repository and `src/OutlineImage` layout (running tree vs target map) | python | Active | `requirement-python-project-structure.md` | 2026-10-04 |
| requirement-python-readme | Root user document: sections, badges, picture catalog, related projects, plain-language outline method | python | Active | `requirement-python-readme.md` | 2026-10-07 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup; console sentences stay | python | Active | `requirement-python-error-handling.md` | 2026-10-04 |
| requirement-runtime-prerequisites | Pip image stack + required ChronicleLogger; no host FFmpeg; no root auto-install | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-07 |

## Intentionally absent (by design)

| Surface | Status on OutlineImage |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure / `curl\|sh` | **Absent** |
| Shell local `install` / `uninstall` / shell self-update | **Absent** (pip package) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| OpenCV as a host duration probe | **Absent**. `opencv-python-headless>=5.0.0.93` is a pip dependency for outlines (`requirement-python-dependency-management`) |
| Second Active `requirement-domain-*` | **Forbidden**. The sole Active domain file is `requirement-domain-outlineimage.md` |
| Front row 2, cut / speed / boomerang, `list-mp4`, `hello`, `join`, `list-videos`, FFmpeg | **Absent**. Front row 1 is `outline` |
| `requirement-python-version` | **Absent**. Version SSOT is the `__version__` string |
| `requirement-python-json-output` | **Absent**. This product does not claim `--json`. The about page does not grow a JSON stream |
| `requirement-python-graceful-exit` | **Absent**. Control-C is not confirmed law. Row 9 Exit returns 0 with no confirm |
| `requirement-python-interactive-vs-noninteractive` | **Absent**. Empty argv on a terminal versus help off a terminal is the CLI interface |
| `requirement-python-pyenv`, `requirement-python-conda`, build-script, `requirement-python-oop-architecture` | **Absent**. Host-check path reads for pyenv and conda stay on `requirement-python-about`. Class homes are `requirement-python-oop` |
| Actor-role requirement file | **Absent**. Class residual is no dest approver |

**Install mode:** **pip / local package** (`outline-image` console script). Not a shell installer.

**Pip lifecycle:** claimed. Rows 84–87 and the typed verbs `version-check`, `self-update`, `self-install`, and `self-uninstall` are `requirement-python-cli-interface` and `requirement-python-tui`. They use `python -m pip`. They are not a shell channel. Empty argv does not run them.

**Logger:** required (`ChronicleLogger>=1.3.1` in law and in `pyproject.toml`). `def main` in `src/OutlineImage/cli.py` writes `ChronicleLogger(...)`.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for OutlineImage.
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.
3. Product source comments cite **only** these live requirement files.
4. This versioned surface lists **requirement rows only**.
5. Keep Status and Path in sync with each file’s header when status changes.
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-outlineimage`).
8. **Do not introduce** a shell installer or Type 1 elevation without an explicit user order and a registry update.
9. **Do not** treat pip rows 84–87 as a reason to add a shell installer. **Do not** mark those pip rows absent.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
