#!/usr/bin/env python
# =============================================================================
# VideoJoin CLI — interactive two-file join via FFmpeg
# Law keys: requirement-domain-videojoin, requirement-video-ffmpeg-pipeline,
#           requirement-python-cli-interface, requirement-python-error-handling,
#           requirement-python-coding-style, requirement-runtime-prerequisites
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# =============================================================================
from __future__ import print_function, unicode_literals

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from . import __version__ as _PKG_VERSION
except Exception:
    _PKG_VERSION = "1.0.3"

APP_NAME = "VideoJoin"
CONSOLE_NAME = "video-join"

VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".m4v"}
OUTPUT_SUFFIXES = (".mp4", ".mkv", ".mov")


def out_info(msg):
    """User-facing informational line (stdout)."""
    print(msg)


def out_err(msg):
    """User-facing error line (stderr)."""
    print(msg, file=sys.stderr)


# =============================================================================
# CIAO-Lite Protection Zone — temp staging + publish (USB / multi-mount)
# System TMPDIR and removable media are often different filesystems.
# Bare os.rename / os.replace do NOT cross mounts (Linux EXDEV).
# Publish completed intermediates with shutil.move (rename same FS; copy+delete
# on EXDEV). Prefer temps next to final output when writable.
# Law: requirement-video-ffmpeg-pipeline, requirement-python-coding-style
# =============================================================================


def staging_dir_for(dest_path):
    """
    General Purpose: Choose a directory for intermediate files on the same
    filesystem as dest when possible (USB-safe). Falls back to system temp.
    """
    dest_path = Path(dest_path)
    parent = dest_path.parent
    try:
        if parent.is_dir() and os.access(str(parent), os.W_OK):
            return parent
    except OSError:
        pass
    return Path(tempfile.gettempdir())


def make_temp_path(suffix, near_path):
    """
    General Purpose: Create a unique temp file path near near_path's directory
    (same FS when writable). File is created empty and closed; caller overwrites.
    """
    d = staging_dir_for(near_path)
    fd, name = tempfile.mkstemp(suffix=suffix, prefix="videojoin_", dir=str(d))
    os.close(fd)
    return Path(name)


def promote_file(src, dest):
    """
    General Purpose: Publish src → dest using shutil.move (stdlib cross-FS safe).

    Same mount: rename. Different mount (USB, etc.): copy then remove source.
    Never use bare os.replace alone when src may live under system TMPDIR.
    """
    src = Path(src)
    dest = Path(dest)
    if not src.is_file():
        raise FileNotFoundError("promote source missing: {}".format(src))
    if dest.is_dir():
        raise IsADirectoryError("promote dest must be a file path, not a directory: {}".format(dest))
    dest.parent.mkdir(parents=True, exist_ok=True)
    # shutil.move: try rename; on EXDEV copy + unlink source
    shutil.move(str(src), str(dest))


def ensure_ffmpeg():
    """
    General Purpose: Fail closed if the system ffmpeg binary is not on PATH.
    requirement-runtime-prerequisites / requirement-video-ffmpeg-pipeline
    """
    if shutil.which("ffmpeg") is None:
        out_err("ERROR: ffmpeg not found on PATH.")
        out_err("   Install FFmpeg and ensure `ffmpeg` is available.")
        out_err("   → https://ffmpeg.org/download.html")
        return False
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        out_err("ERROR: ffmpeg found but failed to run `-version`.")
        return False
    return True


def get_video_files(directory=None):
    """
    General Purpose: List eligible video files in directory (cwd by default),
    sorted case-insensitively by name.
    """
    root = Path(directory or ".")
    return sorted(
        [
            f
            for f in root.iterdir()
            if f.is_file() and f.suffix.lower() in VIDEO_SUFFIXES
        ],
        key=lambda x: x.name.lower(),
    )


def show_list(files):
    """General Purpose: Print 1-based video list for interactive selection."""
    out_info("\nFound video files:")
    for i, f in enumerate(files, 1):
        out_info("  {:2d}. {}".format(i, f.name))
    out_info("")


def choose(files, prompt):
    """General Purpose: Prompt for 1-based index; re-prompt on invalid input."""
    while True:
        try:
            idx = int(input(prompt)) - 1
            if 0 <= idx < len(files):
                return files[idx]
            out_info("   → Enter 1–{}".format(len(files)))
        except ValueError:
            out_info("   → Please type a number")


def create_file_list(file1, file2, list_path):
    """
    General Purpose: Write FFmpeg concat demuxer list with absolute POSIX paths.
    """
    p1 = Path(file1).resolve().as_posix()
    p2 = Path(file2).resolve().as_posix()
    with open(str(list_path), "w", encoding="utf-8") as f:
        f.write("file '{}'\n".format(p1))
        f.write("file '{}'\n".format(p2))


def _file_ok(path):
    """General Purpose: True if path is a non-empty regular file."""
    try:
        p = Path(path)
        return p.is_file() and p.stat().st_size > 0
    except OSError:
        return False


def _run_ffmpeg(cmd, label):
    """
    General Purpose: Run one FFmpeg command; return True on exit 0.
    Does not modify the user's source media paths.
    """
    out_info(label)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        if err:
            # Keep message short for users; full stderr not always needed.
            tail = err[-500:] if len(err) > 500 else err
            out_err("   ffmpeg: {}".format(tail.splitlines()[-1] if tail else "failed"))
        return False
    return True


def join_videos(vid1, vid2, out_path):
    """
    General Purpose: Concatenate two videos to out_path (copy then re-encode).
    Stages unique temps near out_path; publishes with shutil.move.
    Returns True on success. Leaves sources intact.
    Law: requirement-video-ffmpeg-pipeline, requirement-python-coding-style
    """
    vid1 = Path(vid1)
    vid2 = Path(vid2)
    out_path = Path(out_path)

    if not vid1.is_file() or not vid2.is_file():
        out_err("ERROR: one or both input videos are missing.")
        return False

    try:
        if out_path.resolve() in (vid1.resolve(), vid2.resolve()):
            out_err("ERROR: output path must not be one of the source files.")
            return False
    except OSError:
        pass

    list_path = None
    copy_temp = None
    reenc_temp = None
    try:
        list_path = make_temp_path(".txt", out_path)
        copy_temp = make_temp_path(".mp4", out_path)
        create_file_list(vid1, vid2, list_path)

        cmd_copy = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c",
            "copy",
            "-map",
            "0:v",
            "-map",
            "0:a?",
            str(copy_temp),
        ]
        if _run_ffmpeg(cmd_copy, "Running ffmpeg (stream copy – no quality loss)…") and _file_ok(
            copy_temp
        ):
            promote_file(copy_temp, out_path)
            copy_temp = None  # moved away
            out_info(
                "\nSUCCESS! Perfectly joined with original sound → {}".format(out_path)
            )
            return True

        out_info(
            "Fast method failed (different resolutions/codec?). Trying safe re-encode..."
        )
        reenc_temp = make_temp_path(".mp4", out_path)
        cmd_reenc = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(vid1),
            "-i",
            str(vid2),
            "-filter_complex",
            "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-map",
            "[v]",
            "-map",
            "[a]",
            str(reenc_temp),
        ]
        if _run_ffmpeg(cmd_reenc, "Running ffmpeg (re-encode fallback)…") and _file_ok(
            reenc_temp
        ):
            promote_file(reenc_temp, out_path)
            reenc_temp = None
            out_info("\nDone (with re-encode) → {}".format(out_path))
            return True

        out_err("ERROR: join failed on both stream-copy and re-encode paths.")
        return False
    except (OSError, FileNotFoundError, IsADirectoryError) as exc:
        out_err("Job failed: {}".format(exc))
        err = getattr(exc, "errno", None)
        if err in (getattr(os, "EXDEV", 18), 18):
            out_err(
                "   Hint: cross-filesystem publish failed. "
                "Temps stage next to the output; publish uses shutil.move."
            )
        return False
    finally:
        for p in (list_path, copy_temp, reenc_temp):
            if p is not None and Path(p).exists():
                try:
                    os.unlink(str(p))
                except OSError:
                    pass


def resolve_output_name(vid1, vid2, raw_name):
    """
    General Purpose: Build output filename from user input or default pattern.
    """
    default_name = "{} + {}.mp4".format(vid1.stem, vid2.stem)
    out_name = (raw_name or "").strip() or default_name
    lower = out_name.lower()
    if not lower.endswith(OUTPUT_SUFFIXES):
        out_name += ".mp4"
    return Path(out_name)


def main():
    """
    General Purpose: Interactive two-video join session (Type N empty argv).
    Law: requirement-python-cli-interface, requirement-domain-videojoin
    """
    if not ensure_ffmpeg():
        sys.exit(1)

    out_info("Video Joiner – WITH ORIGINAL AUDIO (using ffmpeg)\n")
    out_info("{} {}".format(APP_NAME, _PKG_VERSION))

    files = get_video_files()
    if len(files) < 2:
        out_err("Need at least 2 video files in this folder!")
        sys.exit(1)

    show_list(files)
    vid1 = choose(files, "Choose FIRST video → ")

    remaining = [f for f in files if f != vid1]
    show_list(remaining)
    vid2 = choose(remaining, "Choose SECOND video → ")

    default_name = "{} + {}.mp4".format(vid1.stem, vid2.stem)
    raw = input("\nOutput filename [{}]: ".format(default_name)).strip()
    out_path = resolve_output_name(vid1, vid2, raw)

    out_info("\nJoining with perfect audio sync:")
    out_info("   {}".format(vid1.name))
    out_info(" + {}".format(vid2.name))
    out_info(" → {}\n".format(out_path))
    out_info("   Staging dir → {}".format(staging_dir_for(out_path)))

    ok = join_videos(vid1, vid2, out_path)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
