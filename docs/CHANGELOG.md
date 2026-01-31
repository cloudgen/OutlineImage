# CHANGELOG

## [Unreleased]
### Added
- Placeholder for upcoming features, such as batch video joining or GUI integration  .

### Changed
- No changes yet.

### Deprecated
- No deprecations.

### Removed
- No removals.

### Fixed
- No fixes.

### Security
- No security updates   .

---

## [1.0.1] - 2023-10-01
### Added
- Core video joining functionality using FFmpeg for stream copy (lossless) or fallback re-encoding, supporting MP4, MOV, MKV, AVI, M4V formats .
- Interactive CLI for file selection, output naming, and error handling (e.g., FFmpeg availability check) .
- Modular structure with `cli.py` for logic, `__init__.py` for package init and version exposure, and `__main__.py` for entry point .
- Temporary file list generation (`filelist.txt`) for concat, with automatic cleanup .
- Cython build support via `build.sh` and `pyproject.toml` for performance optimization in file scanning and subprocess calls .

### Changed
- Initial implementation focuses on procedural functions; future refactors may introduce classes like `VideoJoiner` without altering existing code .

### Deprecated
- None in initial release.

### Removed
- None.

### Fixed
- Handles invalid user inputs in file selection loops; prevents duplicate selections by filtering remaining files .
- Fallback re-encode addresses common FFmpeg concat failures (e.g., resolution mismatches) with high-quality presets (libx264 CRF 18, AAC 192k) .

### Security
- Subprocess calls to FFmpeg use safe parameters (`-safe 0` for file paths); no user input directly injected into commands  .

---

This CHANGELOG follows semantic versioning and reverse chronological order for clear project evolution tracking, suitable as an extension to any README.md overview    . Update sections as changes occur, keeping descriptions concise and categorized for quick reference  .