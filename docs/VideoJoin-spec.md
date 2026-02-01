# Design Document for `VideoJoin`

## Overview

The `VideoJoin` project is a command-line tool designed to join two video files (supporting formats like MP4, MOV, MKV, AVI, and M4V) while preserving original audio quality and synchronization, leveraging FFmpeg for efficient stream copying or fallback re-encoding. As a Cython (CyMaster type) project, it emphasizes performance optimization through compiled extensions, targeting developers and users needing quick video concatenation without quality loss. The tool scans the current directory for eligible video files, allows user selection via interactive prompts, generates a temporary file list for concatenation, and handles output naming with defaults. It includes error handling for FFmpeg availability and fallback methods for incompatible files (e.g., differing resolutions or codecs)  . The project follows modular Python structure with potential Cython compilation for speed, adhering to community standards for readability and maintainability  .

## Target Operating System

The project is designed to be cross-platform, primarily targeting Unix-like systems (Linux, macOS) due to the shebang `#!/usr/bin/env python` in `cli.py` and POSIX-compatible paths via `pathlib`. It supports Windows with minor adjustments for PATH and executable discovery, but assumes FFmpeg installation in the system PATH. For Cython builds, compatibility extends to environments with C compilers (e.g., gcc on Linux/macOS, Visual Studio on Windows). Deployment via `pyproject.toml` and `build.sh` facilitates containerization if needed, though not recommended for this simple project scale   .

## Folder Structure

The folder structure for the `VideoJoin` project is organized for modularity, documentation, and build automation, suitable for a small-to-medium Cython project with multiple contributors in mind. It separates source code, documentation, and configuration while excluding build artifacts via `.gitignore` (implied but not shown; recommend adding one for `build/`, `__pycache__/`, etc.)    .

```
VideoJoin/
├── build.sh                  # Shell script for Cython compilation and setup (POSIX-compliant for Linux/macOS)
├── docs/
│   ├── CHANGELOG.md          # High-level release notes, e.g., "v1.0.2: Initial video joiner with FFmpeg integration"
│   ├── folder-structure.md   # Detailed layout explanation, including rationale for Cython setup
│   └── VideoClip-spec.md     # Project-specific specifications, covering video formats, FFmpeg dependencies, and Cython optimization goals
├── pyproject.toml            # Configuration for build tools (e.g., setuptools, Cython), dependencies (FFmpeg via subprocess), and packaging
├── README.md                 # User guide with installation, usage, and quick start examples
└── src/
    └── VideoJoin/
        ├── cli.py            # Core command-line interface logic: file discovery, user prompts, FFmpeg execution
        ├── __init__.py       # Package initialization: exposes `ChronicleLogger` (appears mismatched; likely a placeholder or rename needed for VideoJoin context) and version
        └── __main__.py       # Entry point for direct execution: imports and runs `main()` from cli.py
```

This structure supports code modularity (src isolation), extensive documentation needs (docs/), and environment management via `pyproject.toml` for pip-installable builds. For scalability, it allows easy addition of tests/ or examples/ in future iterations without disrupting the core layout    .

### Parameters

- **Video Formats**: Accepts `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` via suffix matching in `get_mp4_files()` .
- **Output Defaults**: Suggests `{stem1} + {stem2}.mp4`; auto-appends `.mp4` if unspecified .
- **FFmpeg Modes**: 
  - Primary: Stream copy (`-c copy`) for no re-encoding (fast, lossless).
  - Fallback: Re-encode with `libx264` (CRF 18, fast preset) and AAC audio (192k bitrate) using filter_complex for concat.
- **Dependencies**: Requires FFmpeg in PATH; checked via `subprocess.run(['ffmpeg', '-version'])`. No pip packages needed beyond standard library (os, sys, pathlib, subprocess) .
- **Cython-Specific**: `build.sh` should compile `cli.py` to `.pyx` or extensions for performance (e.g., faster file iteration); `pyproject.toml` defines build backend (e.g., `cythonize` setup) .
- **User Interaction**: Numeric prompts for file selection; handles invalid inputs with loops .

## Project Name Conversion Rules

- **Package Name**: `VideoJoin` (CamelCase for directory/module, per Python PEP 8).
- **File Naming**: Snake_case for Python files (e.g., `cli.py`); descriptive and lowercase (e.g., `CHANGELOG.md`).
- **Output Files**: User-provided or default `{vid1.stem} + {vid2.stem}.mp4` (preserves original stems, adds `+` separator for clarity).
- **Temporary Files**: `filelist.txt` (fixed name, UTF-8 encoded, auto-removed post-use).
- **Versioning**: Semantic (`__version__ = "1.0.2"` in `__init__.py`); update via CHANGELOG.md for releases  .
- **Cython Builds**: Output binaries prefixed with `VideoJoin_` (e.g., `VideoJoin_cli.c`); configurable in `pyproject.toml` .

Adhere to lowercase for paths and filenames to ensure cross-platform compatibility, avoiding spaces or special characters  .

## Class Structure

The project uses procedural functions in `cli.py` rather than heavy OOP, but `__init__.py` hints at potential class exposure (e.g., `ChronicleLogger`—recommend renaming to `VideoJoiner` for alignment). No explicit classes in provided code; future Cython extensions could wrap FFmpeg calls in a class for modularity .

### Attributes

- None explicitly defined (functional style). Potential additions:
  - `__version__`: String "1.0.2" (package-level).
  - `__all__`: List `["ChronicleLogger"]` (exports; update to `["VideoJoiner", "main"]` if class added) .

### Methods

#### Instance Methods

- No instance methods currently (all standalone functions). Proposed structure for a `VideoJoiner` class in Cython-optimized refactor:
  - `__init__(self, directory: Path = Path('.'))`: Initializes with working directory for file scanning.
  - `scan_videos(self) -> List[Path]`: Returns sorted video files (calls `get_mp4_files()` logic) .
  - `select_videos(self) -> Tuple[Path, Path]`: Handles interactive prompts for first/second video.
  - `join(self, vid1: Path, vid2: Path, output: str) -> bool`: Executes FFmpeg concat (primary/fallback), returns success flag.
  - `cleanup(self)`: Removes temporary `filelist.txt`  .

These would be appended as `# NEW:` in code if implemented, preserving existing functions [[Professional Rules]].

## Functionality Supported

- **File Discovery**: Scans current directory for video files, sorts case-insensitively, lists with indices .
- **Interactive Selection**: Prompts for first/second video, prevents duplicates, validates input .
- **Output Handling**: Customizable filename with defaults; ensures valid extension.
- **FFmpeg Integration**: 
  - Concat via filelist (stream copy for speed/lossless audio/video).
  - Fallback re-encode for mismatches (concat filter_complex, high-quality presets).
- **Error Handling**: Checks FFmpeg presence; exits on insufficient files; captures subprocess output for diagnostics.
- **Cleanup**: Auto-removes temp files; prints success/failure messages.
- **Cython Potential**: Compile for faster I/O (e.g., `pathlib` iterations); `build.sh` automates `cythonize` and install  .
- **Extensibility**: Modular for adding formats, batch joining, or GUI (future tests/ folder)  .

Supports simple projects without heavy deployment (no Docker recommended) but scalable for collaboration via Git  .

## Usage Example

1. **Setup**: Place video files in the project root or run directory. Ensure FFmpeg is installed and in PATH.

2. **Run Directly**:
   ```
   python -m src.VideoJoin
   ```
   Or make executable: `chmod +x src/VideoJoin/__main__.py` and run `./src/VideoJoin/__main__.py`.

3. **Interactive Session Example**:
   ```
   $ python -m src.VideoJoin
   Video Joiner – WITH ORIGINAL AUDIO (using ffmpeg)

   Found video files:
     1. video1.mp4
     2. video2.mkv

   Choose FIRST video → 1
   Found video files:
     1. video2.mkv

   Choose SECOND video → 1

   Output filename [video1 + video2.mp4]: my_joined_video.mp4

   Joining with perfect audio sync:
      video1.mp4
    + video2.mkv
    → my_joined_video.mp4

   Running ffmpeg (stream copy – no quality loss)…
   SUCCESS! Perfectly joined with original sound → my_joined_video.mp4
      Play it with any player – audio is there.
   ```

4. **Build for Cython** (via `build.sh`):
   ```
   # Example build.sh content (POSIX-compliant):
   # ===== BEGIN NEW CODE =====
   # NEW: cythonize -i src/VideoJoin/cli.pyx  # Assuming .pyx conversion
   # NEW: python -m build
   # ===== END NEW CODE =====
   chmod +x build.sh
   ./build.sh
   pip install -e .
   ```

5. **Package Install**: `pip install -e .` (uses `pyproject.toml` for editable install)   .

For maintenance, update CHANGELOG.md per release and use `.gitignore` for build artifacts  . If adding tests, place in `tests/` with `pytest` integration .