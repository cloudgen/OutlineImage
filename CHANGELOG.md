# CHANGELOG

All notable changes to **OutlineImage** are documented here.  
Version SSOT: `pyproject.toml` + `src/OutlineImage/__init__.__version__`.

## [1.0.0] - 2026-10-05

### Added

- Package name is **OutlineImage**. Console script is `outline-image`. Version is **1.0.0**.
- `outline` converts images in one folder to detailed outline images. The default file is PNG in that folder's `output` directory.
- Menu row **1 outline** lists **1** current folder, each subfolder, and **0** back, then runs that conversion.
- `./convert.py` calls the same conversion.
- Pip dependencies are `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `Pillow>=12.1.0`, `opencv-python-headless>=5.0.0.93`, and `rembg>=2.0.85`.
- Public source is `https://github.com/cloudgen/OutlineImage`. The README Screenshots section shows captures of this program.

### Changed

- Specialized from the HelloTui bootstrap. The welcome verb is gone.
- Language leaf is `~/.local/OutlineImage/language`. `OUTLINEIMAGE_LANG` overrides that file for one process and does not write it.

## [Unreleased] — HelloTui bootstrap history

The notes below, through the 1.0.5 section, are the HelloTui bootstrap this tree was copied from. They are not a second OutlineImage release.

### Removed

- Join, file listing, and FFmpeg. `join` and `list-videos` are not verbs. The program does not scan the folder for media and does not call an encoder.

### Changed

- Package name is **HelloTui**. Console script is `hello-tui`. Version is reset to **1.0.0**.
- Typed `hello` prints `Welcome to HelloTui 1.0.0.` in the terminal and does not draw the menu.
- Front row **1** is **hello**. Choosing it shows that same welcome line on the menu.
- The about page domain line is `Show a welcome message`. Self-management row 83 reads "version and this computer."

## [1.0.5] - 2026-10-04

### Changed

- `about` shows one page: product identity, a host check of this computer, and a star box. The page stays English. It does not probe `ffmpeg` and it does not print a pip install line.
- Self-management row 83 reads "version, FFmpeg, and this computer."
- Version is **1.0.5**. `ChronicleLogger>=1.3.1` is unchanged.
- Product README Screenshots links every picture in `screenshots/` with an absolute `https` URL. Menu pictures captured before the about page still show **1.0.4**.

## [1.0.4] - 2026-10-04

### Added

- Text menu on a terminal when `video-join` is started with no arguments. Front rows are join (1), system-log (3), language (4), self-management (8), and Exit (9). system-log lists view-log (31), clear-log (32), log-folder (33), and Back (0). language lists English through Ελληνικά (41–53) and Back (0). self-management lists version (82), about (83), version-check (84), self-update (85), self-uninstall (86), self-install (87), and Back (0).
- Menu language file `~/.local/VideoJoin/language`. `VIDEOJOIN_LANG` overrides that file for one process and does not write it. `language` is not a command-line verb.
- Typed verbs `help`, `version`, `about`, `hello`, `join`, `list-videos`, `self-install`, `version-check`, `self-update`, and `self-uninstall`.
- `ChronicleLogger` is constructed in `main` and required at `ChronicleLogger>=1.3.1`.
- Product README shows the main menu, the system-log board, the language board, and the self-management board.
- Product README PyPI version badge (`pypi.org/project/VideoJoin`).

### Changed

- Empty argv on a terminal opens that menu and does not start the join questions. With no terminal, empty argv prints help and returns 0.
- Quick Installation documents **`pip install VideoJoin`**. This tree is **1.0.4**. A registry probe on 2026-08-19 reported **1.0.3**. Checkout `pip install -e .` stays the local path.
- Join still prefers stream copy, then re-encode, and still publishes with `shutil.move`.

---

## [1.0.3] - 2026-08-09

### Added

- Same-FS staging helpers (`staging_dir_for`, `make_temp_path`) and **`promote_file` → `shutil.move`** for publishing intermediates.
- Unique temp concat list and media intermediates (no fixed cwd-only `filelist.txt` strategy).
- Product requirements set (class, domain, pipeline, CLI, coding-style, packaging, structure, errors, runtime).
- Promote gate checklist **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** (blank + filled run).

### Changed

- Join pipeline: stream-copy to temp → promote; on failure re-encode to temp → promote.
- Package public surface: `__version__` and `main` only (no phantom `ChronicleLogger` re-export from `.cli`).
- Product README rewritten for install/usage honesty (local package primary; FFmpeg system dep).

### Fixed

- Fail-closed re-encode path: non-zero FFmpeg or missing intermediate no longer prints success.
- Reject final output path equal to either source path.

### Security

- Still user-level only; no Type 1 elevation. FFmpeg invoked with argument lists (no shell string interpolation of free-form filters).

---

## [1.0.2] - prior

### Added

- Interactive two-file join with FFmpeg stream-copy and re-encode fallback.
- Package layout under `src/VideoJoin/` with console script `video-join`.

### Notes

- Earlier packaging claims may have listed broad Python support and optional Cython tooling; runtime join does not require Cython.

---

Update this file when shipping version bumps; keep body complete (no hollow TBD sections for claimed releases).
