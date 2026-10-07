# =============================================================================
# Detailed outline images.
# requirement-domain-outlineimage — one folder in, outline files in output/.
# ./convert.py calls convert_folder. The text menu and the outline verb do too.
# The model loads only when this folder has a supported image.
# A slow start shows its sentence before the work.
# requirement-domain-outlineimage — converting images, and a missing model.
# =============================================================================
from __future__ import annotations

import argparse
import os
import sys
import threading
from pathlib import Path


SUPPORTED_INPUT_EXTENSIONS = (".webp", ".png", ".jpg", ".jpeg")
OUTPUT_FORMATS = ("png", "webp", "jpg", "jpeg", "bmp", "tiff")
OUTPUT_DIR_NAME = "output"
DEFAULT_FORMAT = "png"
MODEL_NAME = "isnet-general-use"
MAX_EDGE = 1600
# A soft alpha fringe is not part of the object.
ALPHA_THRESHOLD = 24
MIN_OUTLINE_AREA = 50
# Each photo picks its own edge cut inside this band.
# Flat plastic stays near the low end, so a seam still draws.
# A scuffed or contrasty photo stays near the high end, so the scuffs stay out.
# Color stays lower than brightness: a hole can match the object in
# brightness and still differ in color. requirement-domain-outlineimage.
BRIGHT_LOW_FLOOR = 14
BRIGHT_LOW_CAP = 32
BRIGHT_HIGH_FLOOR = 40
BRIGHT_HIGH_CAP = 80
COLOR_LOW_FLOOR = 6
COLOR_LOW_CAP = 14
COLOR_HIGH_FLOOR = 16
COLOR_HIGH_CAP = 40
BRIGHT_EDGE_SIGMA = 36
COLOR_EDGE_SIGMA = 22
BRIGHT_SPECK = 22
COLOR_SPECK = 10
EDGE_SPECK = 12


def list_subfolders(folder):
    """General Purpose: Immediate child folders, hidden names omitted, sorted.

    Names are the directory entries. A missing folder yields an empty tuple.
    """
    place = Path(folder)
    try:
        names = [
            entry.name
            for entry in place.iterdir()
            if entry.is_dir() and entry.name and not entry.name.startswith(".")
        ]
    except OSError:
        return ()
    names.sort(key=str.lower)
    return tuple(names)


def list_images(folder):
    """General Purpose: Supported images in this folder. Subfolders are not scanned."""
    place = Path(folder)
    try:
        files = [
            entry
            for entry in place.iterdir()
            if entry.is_file() and entry.suffix.lower() in SUPPORTED_INPUT_EXTENSIONS
        ]
    except OSError:
        return ()
    files.sort(key=lambda item: item.name.lower())
    return tuple(files)


def folder_for_pick(name, place=None):
    """General Purpose: '.' is this folder. Any other token is one child name.

    A name with a separator, or '.' / '..', is refused.
    """
    root = Path(place if place is not None else os.getcwd()).expanduser().resolve()
    if name == ".":
        return root
    if (
        not name
        or name in (".", "..")
        or name != Path(name).name
        or "/" in name
        or "\\" in name
    ):
        raise ValueError(name)
    return root / name


def output_dir_for(folder):
    """General Purpose: The output folder next to the images being converted."""
    return Path(folder) / OUTPUT_DIR_NAME


def selected_choice_line(choice, process):
    """General Purpose: The one sentence shown before a slow process starts.

    requirement-domain-outlineimage owns the words. A function that returns
    the sentence is enough. This is not a module-level message constant.
    """
    return "{0} has been selected. {1} takes time to finish.".format(choice, process)


def please_wait_line(visible):
    """General Purpose: The flashing please-wait bullet for a slow process.

    Visible shows the bullet. Hidden keeps the words and the same width so
    only the bullet flashes. requirement-domain-outlineimage owns the words.
    A function that returns the line is enough.
    """
    mark = "•" if visible else " "
    return "{0} please wait".format(mark)


def open_terminal_wait(stream, interval=0.45):
    """General Purpose: Flash a please-wait bullet on one terminal line.

    Returns (show, erase). show paints the bullet and keeps it flashing.
    erase stops the flash and clears that line. A stream that is not a
    terminal gets two no-ops. This is not a status log.
    requirement-domain-outlineimage.
    """
    isatty = getattr(stream, "isatty", None)
    if isatty is None or not isatty():
        return (lambda: None, lambda: None)

    state = {"on": True, "shown": False, "stop": threading.Event(), "thread": None}
    lock = threading.Lock()

    def _write(text):
        stream.write(text)
        stream.flush()

    def _paint():
        with lock:
            _write("\r" + please_wait_line(state["on"]))

    def _loop():
        while not state["stop"].wait(interval):
            state["on"] = not state["on"]
            _paint()

    def show():
        if state["thread"] is not None and state["thread"].is_alive():
            return
        state["stop"].clear()
        state["on"] = True
        state["shown"] = True
        _paint()
        state["thread"] = threading.Thread(
            target=_loop, name="please-wait", daemon=True
        )
        state["thread"].start()

    def erase():
        if not state["shown"]:
            return
        state["stop"].set()
        thread = state["thread"]
        if thread is not None:
            thread.join(timeout=1.0)
            state["thread"] = None
        state["shown"] = False
        blank = " " * len(please_wait_line(True))
        with lock:
            _write("\r" + blank + "\r")

    return show, erase


def run_terminal_conversion(stream, **kwargs):
    """General Purpose: Print each waiting sentence, flash please wait, then the rest.

    The bullet is erased before the next sentence and before the result lines.
    Returned lines still lead with the sentences. This prints only the remainder.
    requirement-python-cli-interface.
    """
    spoken = []
    show, erase = open_terminal_wait(stream)

    def _notice(line):
        erase()
        stream.write(line + "\n")
        stream.flush()
        spoken.append(line)
        show()

    code, lines = convert_folder(on_notice=_notice, **kwargs)
    erase()
    rest = lines[len(spoken):]
    if rest:
        stream.write("\n".join(rest) + "\n")
        stream.flush()
    return code


def model_weights_path(model_name=MODEL_NAME):
    """General Purpose: The weights file for this model name.

    U2NET_HOME, when set and not blank, is the directory. Otherwise the
    file lives in the home directory's .u2net folder. The name is the
    model plus .onnx. requirement-domain-outlineimage owns this path.
    """
    home = os.environ.get("U2NET_HOME", "")
    if home.strip():
        root = Path(home)
    else:
        root = Path.home() / ".u2net"
    return root / "{0}.onnx".format(model_name)


def _image_stack():
    """Import the image stack once. The menu can list folders without it."""
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import new_session, remove

    return cv2, np, Image, new_session, remove


def _drop_short_edges(cv2, np, edges, min_area):
    """Drop edge specks shorter than min_area. Real seams are longer."""
    count, labels, stats, _centers = cv2.connectedComponentsWithStats(edges, 8)
    kept = np.zeros_like(edges)
    for index in range(1, count):
        if stats[index, cv2.CC_STAT_AREA] >= min_area:
            kept[labels == index] = 255
    return kept


def _foreground_mask(cv2, alpha):
    """Binary object mask. A one-pixel close and open removes alpha pinholes."""
    _level, mask = cv2.threshold(alpha, ALPHA_THRESHOLD, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask


def _edge_limits(cv2, np, blurred, inner, low_floor, high_floor, low_cap, high_cap):
    """Cut for this photo, kept inside the band.

    OpenCV Canny compares its cuts to a Sobel gradient, so the same Sobel
    on the foreground picks the cut. A quiet surface gets the low end.
    A busy surface gets the high end.
    """
    gradient_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = np.abs(gradient_x) + np.abs(gradient_y)
    values = magnitude[inner > 0]
    if values.size == 0:
        return float(low_floor), float(high_floor)
    high = float(np.percentile(values, 90))
    low = high * 0.40
    low = float(np.clip(low, low_floor, low_cap))
    high = float(np.clip(max(high, low + 8.0), high_floor, high_cap))
    return low, high


def _channel_edges(cv2, np, plane, mask, inner, band, sigma, min_area):
    """Canny on one channel. Outside the object is filled so the rim is not an edge."""
    foreground = plane[mask > 0]
    if foreground.size == 0:
        return np.zeros(mask.shape, np.uint8)
    filled = plane.copy()
    filled[mask == 0] = int(np.median(foreground))
    blurred = cv2.bilateralFilter(filled, d=5, sigmaColor=sigma, sigmaSpace=sigma)
    low, high = _edge_limits(cv2, np, blurred, inner, *band)
    found = cv2.Canny(blurred, low, high)
    found = cv2.bitwise_and(found, inner)
    return _drop_short_edges(cv2, np, found, min_area)


def _detail_edges(cv2, np, bgr, mask):
    """Inner lines from brightness and from color.

    The cut follows this photo. A gray hole in a bright object can share a
    brightness and still differ in color, so the color band stays lower.
    """
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    inner = cv2.erode(mask, kernel)
    bright_band = (
        BRIGHT_LOW_FLOOR, BRIGHT_HIGH_FLOOR, BRIGHT_LOW_CAP, BRIGHT_HIGH_CAP,
    )
    color_band = (
        COLOR_LOW_FLOOR, COLOR_HIGH_FLOOR, COLOR_LOW_CAP, COLOR_HIGH_CAP,
    )
    edges = _channel_edges(
        cv2, np, lab[:, :, 0], mask, inner,
        bright_band, BRIGHT_EDGE_SIGMA, BRIGHT_SPECK,
    )
    for channel in (1, 2):
        edges = cv2.bitwise_or(
            edges,
            _channel_edges(
                cv2, np, lab[:, :, channel], mask, inner,
                color_band, COLOR_EDGE_SIGMA, COLOR_SPECK,
            ),
        )
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    edges = cv2.bitwise_and(edges, inner)
    return _drop_short_edges(cv2, np, edges, EDGE_SPECK)


def extract_detailed_outline(image_path, output_dir, session, output_format, stack):
    """
    General Purpose: Outer and inner outlines on a black canvas.

    output_format is an extension without a dot. The file name is
    <stem>_detailed_outline.<ext> inside output_dir. Brightness edges and
    color edges are both drawn. The cut follows the photo, so a part that
    matches the object in brightness still appears.
    """
    cv2, np, Image, _new_session, remove = stack
    ext = output_format.lstrip(".").lower()
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        if max(img_rgb.size) > MAX_EDGE:
            img_rgb.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        cutout = remove(img_rgb, session=session)

    img_rgba = np.array(cutout)
    img_bgra = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGRA)
    height, width = img_bgra.shape[:2]
    fg_mask = _foreground_mask(cv2, img_bgra[:, :, 3])
    silhouette_contours, _hierarchy = cv2.findContours(
        fg_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    silhouette_contours = [
        contour
        for contour in silhouette_contours
        if cv2.contourArea(contour) > MIN_OUTLINE_AREA
    ]
    edges = _detail_edges(cv2, np, img_bgra[:, :, :3], fg_mask)
    canvas = np.zeros((height, width), dtype=np.uint8)
    canvas = cv2.bitwise_or(canvas, edges)
    cv2.drawContours(
        canvas,
        silhouette_contours,
        -1,
        255,
        thickness=1,
        lineType=cv2.LINE_AA,
    )
    out_file = Path(output_dir) / "{0}_detailed_outline.{1}".format(image_path.stem, ext)
    if not cv2.imwrite(str(out_file), canvas):
        raise OSError("could not write {0}".format(out_file))
    return out_file


def convert_folder(
    folder,
    output_format=DEFAULT_FORMAT,
    output_dir=None,
    choice="outline",
    on_notice=None,
):
    """
    General Purpose: Write one outline image for each supported image in folder.

    Returns (exit code, lines). Does not prompt and does not draw the menu.
    An empty folder does not load the model. The default format is png.
    Outlines go in <folder>/output unless output_dir is set.
    When images exist, the converting sentence is shown before the import.
    The download sentence is shown only when the weights file is absent,
    immediately before the model session. on_notice receives each sentence
    as it is shown. None prints and flushes. Those sentences also lead lines.
    A caller that prints lines must skip the sentences it already showed.
    requirement-domain-outlineimage.
    """
    place = Path(folder).expanduser()
    if not place.is_dir():
        return 1, [
            "ERROR: {0} is not a folder.".format(place),
            "   Next: outline-image outline",
        ]
    ext = (output_format or DEFAULT_FORMAT).lstrip(".").lower()
    if ext not in OUTPUT_FORMATS:
        return 1, [
            "ERROR: Unsupported format '{0}'.".format(output_format),
            "   Next: outline-image outline --format png",
        ]
    images = list_images(place)
    dest = Path(output_dir) if output_dir is not None else output_dir_for(place)
    if not images:
        return 0, [
            "No supported images found in {0}.".format(place.resolve()),
        ]
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return 1, [
            "ERROR: Cannot create {0}: {1}".format(dest, exc),
            "   Next: choose a folder you can write",
        ]
    notices = []

    def _say(process):
        line = selected_choice_line(choice, process)
        notices.append(line)
        if on_notice is None:
            print(line, flush=True)
        else:
            on_notice(line)

    def _done(code, body):
        return code, list(notices) + list(body)

    _say("Converting images")
    try:
        cv2, np, Image, new_session, remove = _image_stack()
    except ImportError:
        return _done(
            1,
            [
                "ERROR: Pillow, opencv-python-headless, numpy, and rembg are required.",
                '   Next: python -m pip install "OutlineImage"',
            ],
        )
    stack = (cv2, np, Image, new_session, remove)
    if not model_weights_path().is_file():
        _say("Downloading the AI model")
    try:
        session = new_session(MODEL_NAME)
    except Exception as exc:
        return _done(
            1,
            [
                "ERROR: Could not load the outline model: {0}".format(exc),
                "   Next: outline-image outline",
            ],
        )
    lines = [
        "Output format: .{0}".format(ext),
        "Images: {0}".format(len(images)),
    ]
    failed = False
    for index, image_path in enumerate(images, start=1):
        lines.append(
            "[{0}/{1}] Processing: {2}".format(index, len(images), image_path.name)
        )
        try:
            out_file = extract_detailed_outline(
                image_path, dest, session, ext, stack
            )
        except Exception as exc:
            failed = True
            lines.append("ERROR: Failed on {0}: {1}".format(image_path.name, exc))
            continue
        lines.append("Saved outline -> {0}".format(out_file.name))
    lines.append("Outlines saved in: {0}".format(dest.resolve()))
    return _done(1 if failed else 0, lines)


def main(argv=None):
    """General Purpose: ./convert.py entry. Same conversion as the outline verb."""
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Extract detailed black and white outlines from images.",
    )
    parser.add_argument(
        "--format",
        "-f",
        default=DEFAULT_FORMAT,
        choices=list(OUTPUT_FORMATS),
        help="Output image format (default: png)",
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        default=".",
        help="Input folder to scan (default: current directory)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Output folder (default: <input>/output)",
    )
    args = parser.parse_args(argv)
    return run_terminal_conversion(
        sys.stdout,
        folder=args.input_dir,
        output_format=args.format,
        output_dir=args.output_dir,
        choice="convert.py",
    )


if __name__ == "__main__":
    sys.exit(main())
