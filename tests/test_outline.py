# outline — folder conversion and menu row 1.
# The typed verb converts a folder and does not draw the menu.
# Menu row 1 lists the current folder, each subfolder, and Back.
import io
import os
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from OutlineImage.cli import Cli
from OutlineImage.menu_model import MenuModel
from OutlineImage.menu_painter import MenuPainter
from OutlineImage.outline import (
    convert_folder,
    list_images,
    main as convert_main,
    model_weights_path,
    please_wait_line,
    selected_choice_line,
)
from OutlineImage.tui import Tui


class TestOutline(unittest.TestCase):
    """Typed outline converts a folder. Menu row 1 picks that folder."""

    def test_cli_outline_converts_the_current_folder_and_skips_the_menu(self):
        app = Cli()
        self.assertIn("outline", Cli.PRODUCT_VERBS)
        self.assertNotIn("hello", Cli.PRODUCT_VERBS)
        self.assertNotIn("join", Cli.PRODUCT_VERBS)
        self.assertNotIn("list-videos", Cli.PRODUCT_VERBS)
        self.assertFalse(Cli.opens_text_screen(["outline"]))
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertTrue(Cli.opens_text_screen([]))
            self.assertFalse(Cli.opens_text_screen(["outline"]))
            self.assertFalse(Cli.opens_text_screen(["outline", "photos"]))
            self.assertTrue(Cli.opens_text_screen(["about"]))
            self.assertFalse(Cli.opens_text_screen(["join"]))
            self.assertFalse(Cli.opens_text_screen(["list-videos"]))
        finally:
            Cli.stdout_is_tty = previous
        folder = tempfile.mkdtemp(prefix="ojempty_", dir="/tmp")
        previous_dir = os.getcwd()
        os.chdir(folder)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["outline"])
        finally:
            os.chdir(previous_dir)
        self.assertEqual(code, 0)
        self.assertIn("No supported images found in", buf.getvalue())
        self.assertIn(os.path.realpath(folder), buf.getvalue())
        self.assertNotIn("has been selected", buf.getvalue())

    def test_outline_rejects_a_missing_folder_and_a_foreign_format(self):
        app = Cli()
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = app.run(["outline", "/tmp/outline-image-missing-folder"])
        self.assertEqual(code, 1)
        self.assertIn("is not a folder", out.getvalue())
        self.assertNotIn("has been selected", out.getvalue())
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = app.run(["version", "photos"])
        self.assertEqual(code, 1)
        self.assertIn("A folder is only for outline", err.getvalue())

    def test_removed_video_verbs_are_unknown(self):
        app = Cli()
        for verb in ("join", "list-videos", "hello"):
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run([verb])
            self.assertEqual(code, 1, verb)
            self.assertIn("Unknown verb '{0}'".format(verb), err.getvalue())
        help_buf = io.StringIO()
        with redirect_stdout(help_buf):
            self.assertEqual(app.run(["help"]), 0)
        text = help_buf.getvalue()
        self.assertIn("outline", text)
        self.assertNotIn("list-videos", text)
        self.assertNotIn("FFmpeg", text)
        self.assertNotIn("ffmpeg", text)
        self.assertNotIn("concatenate", text)

    def test_menu_row_1_lists_the_current_folder_and_subfolders(self):
        home = tempfile.mkdtemp(prefix="ojhome_", dir="/tmp")
        folder = tempfile.mkdtemp(prefix="ojclips_", dir="/tmp")
        os.mkdir(os.path.join(folder, "beta"))
        os.mkdir(os.path.join(folder, "alpha"))
        os.mkdir(os.path.join(folder, ".hidden"))
        saved = os.environ.get("OUTLINEIMAGE_LANG")
        os.environ.pop("OUTLINEIMAGE_LANG", None)
        previous = os.getcwd()
        os.chdir(folder)
        painter = MenuPainter(home=home)
        try:
            self.assertEqual(painter.language.code(), "en")
            rows = painter.display_rows("front")
            self.assertEqual(
                rows[0],
                (1, "outline", "convert images in a chosen folder to outlines", "outline"),
            )
            model = MenuModel(painter=painter)
            self.assertIsNone(model._activate(1, "outline"))
            self.assertEqual(model.layer, "folders")
            picked = painter.display_rows("folders")
            self.assertEqual(picked[0][0], 1)
            self.assertEqual(picked[0][1], "current")
            self.assertEqual(picked[0][3], "pick:.")
            self.assertEqual(picked[1][1], "alpha")
            self.assertEqual(picked[1][3], "pick:alpha")
            self.assertEqual(picked[2][1], "beta")
            self.assertEqual(picked[2][3], "pick:beta")
            self.assertEqual(picked[-1][0], 0)
            self.assertEqual(picked[-1][3], "back")
            shorts = [row[1] for row in picked]
            self.assertNotIn(".hidden", shorts)
            self.assertIsNone(model._activate(0, "back"))
            self.assertEqual(model.layer, "front")
        finally:
            os.chdir(previous)
            if saved is None:
                os.environ.pop("OUTLINEIMAGE_LANG", None)
            else:
                os.environ["OUTLINEIMAGE_LANG"] = saved

    def test_empty_folder_does_not_import_the_image_stack(self):
        folder = tempfile.mkdtemp(prefix="ojnone_", dir="/tmp")
        code, lines = convert_folder(folder)
        self.assertEqual(code, 0)
        self.assertEqual(list_images(folder), ())
        self.assertIn("No supported images", lines[0])
        self.assertNotIn("has been selected", "\n".join(lines))

    def _image(self, folder, name="photo.png"):
        path = os.path.join(folder, name)
        with open(path, "wb") as handle:
            handle.write(b"png")
        return path

    def _run_convert(self, folder, choice="outline", weights_present=False):
        order = []
        notices = []

        def new_session(name):
            order.append("session")
            return object()

        def extract(image_path, output_dir, session, output_format, stack):
            order.append("extract")
            return Path(output_dir) / "{0}_detailed_outline.png".format(Path(image_path).stem)

        class _Weights(object):
            def is_file(self):
                return weights_present

        stack = (object(), object(), object(), new_session, object())
        with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
            "OutlineImage.outline.model_weights_path", return_value=_Weights()
        ), patch("OutlineImage.outline.extract_detailed_outline", side_effect=extract):
            code, lines = convert_folder(
                folder,
                choice=choice,
                on_notice=lambda line: notices.append(line) or order.append(line),
            )
        return code, lines, notices, order

    def test_sentence_names_the_choice_and_the_process(self):
        self.assertEqual(
            selected_choice_line("outline", "Converting images"),
            "outline has been selected. Converting images takes time to finish.",
        )
        self.assertEqual(
            selected_choice_line("current", "Downloading the AI model"),
            "current has been selected. Downloading the AI model takes time to finish.",
        )

    def test_weights_path_uses_u2net_home_when_it_is_set(self):
        folder = tempfile.mkdtemp(prefix="oju2_", dir="/tmp")
        saved = os.environ.get("U2NET_HOME")
        try:
            os.environ["U2NET_HOME"] = folder
            self.assertEqual(
                model_weights_path(),
                Path(folder) / "isnet-general-use.onnx",
            )
            os.environ["U2NET_HOME"] = "   "
            self.assertEqual(
                model_weights_path("isnet-general-use"),
                Path.home() / ".u2net" / "isnet-general-use.onnx",
            )
        finally:
            if saved is None:
                os.environ.pop("U2NET_HOME", None)
            else:
                os.environ["U2NET_HOME"] = saved

    def test_converting_then_download_before_the_model_session(self):
        folder = tempfile.mkdtemp(prefix="ojslow_", dir="/tmp")
        self._image(folder)
        code, lines, notices, order = self._run_convert(folder, weights_present=False)
        converting = "outline has been selected. Converting images takes time to finish."
        downloading = "outline has been selected. Downloading the AI model takes time to finish."
        self.assertEqual(code, 0)
        self.assertEqual(notices, [converting, downloading])
        self.assertEqual(lines[0], converting)
        self.assertEqual(lines[1], downloading)
        self.assertLess(order.index(converting), order.index(downloading))
        self.assertLess(order.index(downloading), order.index("session"))
        self.assertIn("Saved outline -> photo_detailed_outline.png", lines)

    def test_cached_weights_do_not_say_the_model_is_downloading(self):
        folder = tempfile.mkdtemp(prefix="ojcache_", dir="/tmp")
        self._image(folder)
        _code, lines, notices, order = self._run_convert(folder, weights_present=True)
        self.assertEqual(
            notices,
            ["outline has been selected. Converting images takes time to finish."],
        )
        self.assertNotIn("Downloading the AI model", "\n".join(lines))
        self.assertLess(order.index(notices[0]), order.index("session"))

    def test_bad_format_missing_output_and_import_stay_honest(self):
        folder = tempfile.mkdtemp(prefix="ojhonest_", dir="/tmp")
        code, lines = convert_folder(folder, output_format="gif")
        self.assertEqual(code, 1)
        self.assertNotIn("has been selected", "\n".join(lines))
        self._image(folder)
        blocker = os.path.join(folder, "output")
        with open(blocker, "w") as handle:
            handle.write("x")
        code, lines = convert_folder(folder, on_notice=lambda line: None)
        self.assertEqual(code, 1)
        self.assertNotIn("has been selected", "\n".join(lines))
        os.remove(blocker)
        with patch("OutlineImage.outline._image_stack", side_effect=ImportError("no")):
            code, lines = convert_folder(folder, on_notice=lambda line: None)
        self.assertEqual(code, 1)
        self.assertEqual(
            lines[0],
            "outline has been selected. Converting images takes time to finish.",
        )
        self.assertIn("Pillow, opencv-python-headless, numpy, and rembg", lines[1])
        self.assertNotIn("Downloading the AI model", "\n".join(lines))

    def test_cli_outline_flushes_the_sentence_once_before_the_session(self):
        folder = tempfile.mkdtemp(prefix="ojcli_", dir="/tmp")
        self._image(folder)
        seen = []
        buf = io.StringIO()

        def new_session(name):
            seen.append(buf.getvalue())
            return object()

        stack = (object(), object(), object(), new_session, object())

        class _Missing(object):
            def is_file(self):
                return False

        previous = os.getcwd()
        os.chdir(folder)
        try:
            with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
                "OutlineImage.outline.model_weights_path", return_value=_Missing()
            ), patch(
                "OutlineImage.outline.extract_detailed_outline",
                return_value=Path(folder) / "output" / "photo_detailed_outline.png",
            ), redirect_stdout(buf):
                code = Cli().run(["outline"])
        finally:
            os.chdir(previous)
        text = buf.getvalue()
        converting = "outline has been selected. Converting images takes time to finish."
        downloading = "outline has been selected. Downloading the AI model takes time to finish."
        self.assertEqual(code, 0)
        self.assertEqual(seen[0].splitlines()[:2], [converting, downloading])
        self.assertEqual(text.count(converting), 1)
        self.assertEqual(text.count(downloading), 1)
        self.assertIn("Output format: .png", text)

    def test_convert_py_uses_its_own_choice_and_prints_once(self):
        folder = tempfile.mkdtemp(prefix="ojconv_", dir="/tmp")
        self._image(folder)
        buf = io.StringIO()

        def new_session(name):
            return object()

        stack = (object(), object(), object(), new_session, object())

        class _Present(object):
            def is_file(self):
                return True

        with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
            "OutlineImage.outline.model_weights_path", return_value=_Present()
        ), patch(
            "OutlineImage.outline.extract_detailed_outline",
            return_value=Path(folder) / "output" / "photo_detailed_outline.png",
        ), redirect_stdout(buf):
            code = convert_main(["--input-dir", folder])
        text = buf.getvalue()
        sentence = "convert.py has been selected. Converting images takes time to finish."
        self.assertEqual(code, 0)
        self.assertEqual(text.count(sentence), 1)
        self.assertNotIn("Downloading the AI model", text)

    def test_version_does_not_announce_a_slow_process(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = Cli().run(["version"])
        self.assertEqual(code, 0)
        self.assertNotIn("has been selected", buf.getvalue())

    def test_folder_pick_paints_before_the_session_and_front_row_does_not(self):
        home = tempfile.mkdtemp(prefix="ojthome_", dir="/tmp")
        folder = tempfile.mkdtemp(prefix="ojtpick_", dir="/tmp")
        os.mkdir(os.path.join(folder, "alpha"))
        self._image(folder)
        self._image(os.path.join(folder, "alpha"), "shot.jpg")
        order = []

        def new_session(name):
            order.append("session")
            return object()

        def extract(image_path, output_dir, session, output_format, stack):
            return Path(output_dir) / "out.png"

        stack = (object(), object(), object(), new_session, object())

        class _Missing(object):
            def is_file(self):
                return False

        class _Screen(object):
            def __init__(self):
                self.refreshes = 0

            def refresh(self):
                self.refreshes += 1
                order.append("refresh")

        tui = Tui(app_name="OutlineImage", version="1.0.0")
        tui.painter = MenuPainter(home=home)

        def paint_prompt(screen, model, title, lines, pin_last, name, ver, visible):
            order.append(("paint", title, list(lines)))

        tui.painter.paint_prompt = paint_prompt
        screen = _Screen()
        model = MenuModel(painter=tui.painter)
        previous = os.getcwd()
        os.chdir(folder)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertIsNone(model._activate(1, "outline"))
            self.assertEqual(model.layer, "folders")
            self.assertNotIn("has been selected", buf.getvalue())
            with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
                "OutlineImage.outline.model_weights_path", return_value=_Missing()
            ), patch(
                "OutlineImage.outline.extract_detailed_outline", side_effect=extract
            ):
                text = tui.outline_result(".", screen=screen, model=model)
                alpha = tui.outline_result("alpha", screen=screen, model=model)
                quiet = tui.outline_result(".", screen=None, model=None)
        finally:
            os.chdir(previous)
        converting = "current has been selected. Converting images takes time to finish."
        downloading = "current has been selected. Downloading the AI model takes time to finish."
        bullet = please_wait_line(True)
        self.assertTrue(text.startswith(converting + "\n" + downloading))
        self.assertNotIn("please wait", text)
        self.assertEqual(order[0], ("paint", "working", [converting, bullet]))
        self.assertEqual(order[1], "refresh")
        self.assertEqual(
            order[2], ("paint", "working", [converting, downloading, bullet])
        )
        self.assertEqual(order[3], "refresh")
        self.assertEqual(order[4], "session")
        self.assertTrue(alpha.startswith("alpha has been selected. Converting images takes time to finish."))
        self.assertNotIn("please wait", alpha)
        self.assertTrue(quiet.startswith(converting))
        self.assertNotIn("please wait", quiet)
        self.assertGreaterEqual(screen.refreshes, 2)

    def test_please_wait_bullet_flashes_and_is_removed(self):
        self.assertEqual(please_wait_line(True), "• please wait")
        self.assertEqual(please_wait_line(False), "  please wait")
        self.assertEqual(len(please_wait_line(True)), len(please_wait_line(False)))
        folder = tempfile.mkdtemp(prefix="ojwait_", dir="/tmp")
        self._image(folder)
        hold = threading.Event()

        def new_session(name):
            hold.wait(2)
            return object()

        stack = (object(), object(), object(), new_session, object())

        class _Missing(object):
            def is_file(self):
                return False

        class _Screen(object):
            def timeout(self, _ms):
                return None

            def getch(self):
                return -1

            def refresh(self):
                return None

        paints = []

        def paint_prompt(screen, model, title, lines, pin_last, name, ver, visible):
            paints.append(list(lines))
            marks = [line for line in paints if line and line[-1].endswith("please wait")]
            if len(marks) >= 2 and marks[0][-1] != marks[-1][-1]:
                hold.set()

        tui = Tui(app_name="OutlineImage", version="1.0.0")
        tui.painter = MenuPainter(home=tempfile.mkdtemp(prefix="ojwh_", dir="/tmp"))
        tui.painter.paint_prompt = paint_prompt
        screen = _Screen()
        model = MenuModel(painter=tui.painter)
        previous = os.getcwd()
        os.chdir(folder)
        try:
            with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
                "OutlineImage.outline.model_weights_path", return_value=_Missing()
            ), patch(
                "OutlineImage.outline.extract_detailed_outline",
                return_value=Path(folder) / "output" / "photo_detailed_outline.png",
            ):
                text = tui.outline_result(".", screen=screen, model=model)
        finally:
            os.chdir(previous)
        self.assertTrue(hold.is_set())
        self.assertNotIn("please wait", text)
        self.assertTrue(text.startswith(
            "current has been selected. Converting images takes time to finish."
        ))
        self.assertEqual(paints[0][-1], please_wait_line(True))
        self.assertIn(please_wait_line(False), [line[-1] for line in paints])

    def test_terminal_bullet_is_erased_when_the_work_finishes(self):
        folder = tempfile.mkdtemp(prefix="ojtty_", dir="/tmp")
        self._image(folder)

        class _Tty(io.StringIO):
            def isatty(self):
                return True

        buf = _Tty()
        seen = []

        def new_session(name):
            seen.append(_visible(buf.getvalue()))
            return object()

        stack = (object(), object(), object(), new_session, object())

        class _Missing(object):
            def is_file(self):
                return False

        previous = os.getcwd()
        os.chdir(folder)
        try:
            with patch("OutlineImage.outline._image_stack", return_value=stack), patch(
                "OutlineImage.outline.model_weights_path", return_value=_Missing()
            ), patch(
                "OutlineImage.outline.extract_detailed_outline",
                return_value=Path(folder) / "output" / "photo_detailed_outline.png",
            ), redirect_stdout(buf):
                code = Cli().run(["outline"])
        finally:
            os.chdir(previous)
        self.assertEqual(code, 0)
        self.assertEqual(seen[0][-1], "• please wait")
        finished = _visible(buf.getvalue())
        self.assertNotIn("please wait", "\n".join(finished))
        self.assertIn("Output format: .png", finished)


def _visible(text):
    """Apply carriage returns so a test can read the line the operator sees."""
    rows = [""]
    for char in text:
        if char == "\n":
            rows.append("")
        elif char == "\r":
            rows[-1] = ""
        else:
            rows[-1] += char
    return [row for row in rows if row.strip()]


if __name__ == "__main__":
    unittest.main()
