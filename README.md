# VideoJoin - Join two local videos with FFmpeg (stream-copy first)

![Version](https://img.shields.io/badge/Version-1.0.3-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/Wilgat/VideoJoin?style=flat-square)](https://github.com/Wilgat/VideoJoin)
[![Python](https://img.shields.io/badge/Python-2.7%2B%20(3.x%20recommended)-blue?style=flat-square)]()

VideoJoin is a lightweight **interactive** command-line tool that concatenates **two** video files from the current directory using **FFmpeg**. It prefers **stream copy** (no re-encode when possible) and **fail-closed re-encode fallback** when copy fails. Intermediate files are staged next to the output path when possible and published with **`shutil.move`** for multi-mount safety (for example USB).

## Features

- Interactive pick of first and second video (same file cannot be chosen twice)
- Discovers `.mp4`, `.mov`, `.mkv`, `.avi`, `.m4v` in the **current working directory** (sorted case-insensitively)
- Stream-copy join first (`ffmpeg` concat demuxer); re-encode fallback (`libx264` CRF 18, AAC 192k)
- Fail-closed: no success message if both paths fail
- Unique temp list + media intermediates; cleanup on success and failure
- Publish intermediates with `shutil.move` (same FS rename; cross-mount copy+delete)
- FFmpeg on `PATH` checked before joining
- Console script `video-join` and module entry `python -m VideoJoin`

## Quick Installation

**System requirement:** [FFmpeg](https://ffmpeg.org/download.html) must be installed and available as `ffmpeg` on your `PATH`. The package does **not** install FFmpeg via pip.

### Local install (primary)

From a checkout:

```bash
git clone https://github.com/Wilgat/VideoJoin.git
cd VideoJoin
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
```

This installs the console entry **`video-join`** and the package **`VideoJoin`**.

Optional dependency declared in packaging: `ChronicleLogger` (not required for the current interactive console paths).

### PyPI

A future `pip install VideoJoin` channel may appear when the project is published to PyPI. **Today, install from source** as above. Do not assume a live PyPI release without checking [the project page](https://github.com/Wilgat/VideoJoin).

## Usage

After install:

```bash
# ensure videos are in the current directory
cd /path/to/folder/with/clips
video-join
```

Or:

```bash
python -m VideoJoin
```

Session steps:

1. Lists eligible videos in the current directory  
2. Choose first video (number)  
3. Choose second video from the remaining list  
4. Confirm or edit output name (default: `{stem1} + {stem2}.mp4`)  
5. FFmpeg stream-copy → on failure, re-encode → publish result  

Exit codes: non-zero if fewer than two videos, FFmpeg missing, or join fails.

## Examples

```text
$ video-join
Video Joiner – WITH ORIGINAL AUDIO (using ffmpeg)

VideoJoin 1.0.3

Found video files:
   1. clip1.mp4
   2. clip2.mkv

Choose FIRST video → 1

Found video files:
   1. clip2.mkv

Choose SECOND video → 1

Output filename [clip1 + clip2.mp4]: joined.mp4

Joining with perfect audio sync:
   clip1.mp4
 + clip2.mkv
 → joined.mp4
   Staging dir → .

Running ffmpeg (stream copy – no quality loss)…
SUCCESS! Perfectly joined with original sound → joined.mp4
```

Import for scripts (thin entry):

```python
from VideoJoin import main
# interactive session; expects cwd videos + TTY stdin
```

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Linux | Primary; tested development path |
| macOS | Supported when Python + FFmpeg on PATH |
| Windows | Supported when Python + FFmpeg on PATH (venv activate differs) |
| Architectures | Any with CPython + FFmpeg binary |

Interactive prompts need a terminal (or fed stdin). Non-interactive automation flags are not implemented yet.

## Related Projects

- [VideoJoin on GitHub](https://github.com/Wilgat/VideoJoin) — this repository  
- Sibling media tooling (same author ecosystem) may include other FFmpeg CLIs; this product is **two-file join only**, not cut/speed/boomerang editing  

## Contributing

1. Keep product law under `docs/requirements/` in sync when behavior changes.  
2. Prefer small, CIAO-safe changes; do not remove Protection Zones in `cli.py` (staging / `shutil.move` publish) without explicit design.  
3. Version dual SSOT: bump **`pyproject.toml`** and **`src/VideoJoin/__init__.__version__`** together.  
4. Open issues and pull requests on GitHub.

## License

MIT — see [`LICENSE.md`](./LICENSE.md). Also declared in `pyproject.toml`.

## Last Update

2026-08-09 — README aligned with **1.0.3** (fail-closed join, unique temps, `shutil.move` promote, honest install/runtime docs).
