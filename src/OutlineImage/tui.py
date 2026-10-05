# =============================================================================
# Text menu session for OutlineImage.
# requirement-python-tui — menu region and the bottom input box.
# requirement-python-about — the about result page is framework_about.
# requirement-python-oop — this module defines class Tui and MenuScreenError.
# The frame is class MenuPainter. cli.py constructs Tui and calls it.
# =============================================================================
from __future__ import annotations

import curses
import threading

from .menu_painter import MenuPainter
from .menu_session import MenuSession
from .system_log import SystemLog



class MenuScreenError(Exception):
    """The terminal cannot hold the menu and the framed input box."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuScreenError")


class Tui:
    """Text menu session. The welcome page and the front board stay on this screen.

    MenuModel, MenuSession, and MenuPainter live in their own modules.
    The rows are outline, system-log, language, self-management, and Exit.
    """

    def __init__(self, app=None, app_name="OutlineImage", version=None, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Tui")
        self.app = app
        self.app_name = app_name
        if version is None:
            from . import __version__
            version = __version__
        self.version = version
        self.painter = MenuPainter(logger=logger)
        self.system_log = SystemLog(logger=logger)

    def _name(self):
        if self.app is not None:
            return self.app.app_name
        return self.app_name

    def _ver(self):
        if self.app is not None:
            return self.app.version
        return self.version

    def front_lines(self):
        """General Purpose: Path line and the front board rows."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("front")
        )

    def self_lines(self):
        """General Purpose: Path line and the self-management board under 8."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("self")
        )

    def log_lines(self):
        """General Purpose: Path line and the system-log board under 3."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("log")
        )

    def language_lines(self):
        """General Purpose: Path line and the language board under 4."""
        return [self.painter.path_line()] + self.painter.format_rows(
            self.painter.display_rows("lang")
        )

    def help_on_screen(self):
        """
        General Purpose: Help text when help is typed on the open menu.
        The typed outline-image help verb does not call this and does not draw the screen.
        """
        name = self._name()
        return (
            "help: usage for {0}.\n"
            "Verbs: help, version, about, outline, "
            "self-install, version-check, self-update, self-uninstall.\n"
            "version shows the installed version and does not call pip.\n"
            "about shows the about page.\n"
            "outline converts one folder and does not draw this menu.\n"
            "With no folder, outline uses the current directory.\n"
            "Menu row 1 outline lists 1 current folder, each subfolder, and 0 back.\n"
            "Chosen images are written as png outlines in that folder's output directory.\n"
            "version-check runs: python -m pip index versions {0}\n"
            "self-update runs: python -m pip install --upgrade {0}\n"
            "self-install runs: python -m pip install {0}\n"
            "self-uninstall runs: python -m pip uninstall -y {0}\n"
            "On the command line, self-uninstall also needs --force.\n"
            "Empty arguments on a terminal open this menu and do not run pip."
        ).format(name)

    def outline_result(self, name, screen=None, model=None):
        """General Purpose: Convert the picked folder and return the result text.

        '.' is the current folder. Any other name is one child folder.
        The default outline format is png. This does not prompt again.
        A real conversion paints the waiting sentence before the work.
        requirement-python-tui. The words are requirement-domain-outlineimage.
        """
        from .outline import convert_folder, folder_for_pick, please_wait_line

        try:
            folder = folder_for_pick(name)
        except ValueError:
            return "ERROR: {0} is not a folder on this list.".format(name)
        choice = "current" if name == "." else name
        if screen is not None and model is not None and self._screen_can_flash(screen):
            lines = self._outline_flashing(folder, choice, screen, model)
            return "\n".join(lines)

        notices = []

        def _notice(line):
            notices.append(line)
            if screen is None or model is None:
                return
            self._show_waiting(
                screen, model, list(notices) + [please_wait_line(True)]
            )

        _code, lines = convert_folder(folder, choice=choice, on_notice=_notice)
        return "\n".join(lines)

    def _screen_can_flash(self, screen):
        """A screen that can arm a short wait can flash the bullet on this thread."""
        return (
            getattr(screen, "timeout", None) is not None
            and getattr(screen, "getch", None) is not None
        )

    def _outline_flashing(self, folder, choice, screen, model):
        """Run the conversion beside a flashing please-wait bullet.

        The worker does the conversion. This thread paints. The bullet is
        not part of the returned lines. requirement-python-tui.
        """
        from .outline import convert_folder, please_wait_line

        notices = []
        lock = threading.Lock()
        done = threading.Event()
        box = {}

        def _notice(line):
            with lock:
                notices.append(line)

        def _work():
            try:
                box["out"] = convert_folder(
                    folder, choice=choice, on_notice=_notice
                )
            except Exception as exc:
                box["out"] = (1, ["ERROR: {0}".format(exc)])
            finally:
                done.set()

        if self.logger is not None:
            self.logger.log_message(
                "thread create name=outline-convert",
                component="Tui",
            )
            self.logger.log_message(
                "thread start name=outline-convert",
                component="Tui",
            )
        worker = threading.Thread(target=_work, name="outline-convert", daemon=True)
        worker.start()
        visible = True
        try:
            while not done.is_set():
                with lock:
                    body = list(notices)
                if body:
                    self._show_waiting(
                        screen, model, body + [please_wait_line(visible)]
                    )
                    visible = not visible
                try:
                    screen.timeout(400)
                    screen.getch()
                except Exception:
                    break
        finally:
            if self.logger is not None:
                self.logger.log_message(
                    "thread wait name=outline-convert on=join",
                    component="Tui",
                )
            worker.join()
            self._arm_blocking(screen)
        _code, lines = box.get("out", (1, ["ERROR: The outline did not finish."]))
        return lines

    def _show_waiting(self, screen, model, lines):
        """Paint the waiting sentence and refresh. Does not wait for a key.

        requirement-python-tui. Title is working.
        """
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        self._paint_lines(screen, model, "working", lines, pin_last=True)
        refresh = getattr(screen, "refresh", None)
        if refresh is not None:
            refresh()

    def about_text(self):
        """General Purpose: The about page body from AboutPage.framework_about."""
        if self.app is None:
            return ""
        return self.app.about.framework_about()

    def _visible_lines(self, lines, room, pin_last):
        """Lines that fit above the input box. A question pins its last line."""
        if room < 1:
            return []
        if len(lines) <= room:
            return list(lines)
        if not pin_last:
            return list(lines[-room:])
        if room == 1:
            return [lines[-1]]
        return list(lines[: room - 2]) + ["…", lines[-1]]

    def _paint_lines(self, screen, model, title, lines, pin_last):
        """Hand one question to MenuPainter. The session does not draw a second frame."""
        self.painter.paint_prompt(
            screen,
            model,
            title,
            lines,
            pin_last,
            self._name(),
            self._ver(),
            self._visible_lines,
        )

    def _arm_blocking(self, screen):
        """Clear the one-second clock wait. A no-key from that wait is not Esc."""
        arm = getattr(screen, "timeout", None)
        if arm is not None:
            arm(-1)

    def read_key(self, screen, model, lines, title="menu"):
        """
        General Purpose: Read one line from the bottom input box.

        Returns the text, or None when the person presses Esc. The board's
        one-second clock wait is cleared before each key.
        """
        model.buffer = ""
        model.cursor = 0
        model.focus = "input"
        while True:
            self._paint_lines(screen, model, title, lines, pin_last=True)
            self._arm_blocking(screen)
            key = screen.getch()
            if key in (-1, 27):
                model.error = ""
                model.buffer = ""
                model.cursor = 0
                model.focus = "list"
                return None
            if key in (10, 13, curses.KEY_ENTER):
                text = model.buffer
                model.buffer = ""
                model.cursor = 0
                model.error = ""
                return text
            if key in (curses.KEY_BACKSPACE, 127, 8):
                model._backspace()
                model.error = ""
                continue
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in model.edge_keys():
                model._slide(key)
                continue
            if key in (curses.KEY_UP, curses.KEY_DOWN):
                continue
            if 32 <= key < 127:
                model._insert(chr(key))
                model.error = ""
                continue

    def notice(self, screen, model, lines, title="result", closing=None):
        """General Purpose: Show lines until the next key. The clock wait is cleared."""
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        if closing is None:
            closing = "Press a key to return to the main menu."
        body = list(lines) + ["", closing]
        self._paint_lines(screen, model, title, body, pin_last=True)
        self._arm_blocking(screen)
        try:
            screen.getch()
        except Exception:
            return

    def _read_yes_no(self, screen, model, lines, title="system-log"):
        """y/n from the box. Esc returns None. Empty is no."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "" or raw in ("n", "no"):
                return False
            if raw in ("y", "yes"):
                return True
            model.error = "Please enter y or n"

    def _read_index(self, screen, model, lines, count, title="system-log"):
        """1-based index from the box. Ask again on a bad value. Esc returns None."""
        while True:
            raw = self.read_key(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip()
            try:
                idx = int(raw)
            except ValueError:
                model.error = "Please type a number"
                continue
            if 1 <= idx <= count:
                return idx - 1
            model.error = "Enter 1–{0}".format(count)

    def about_on_screen(self, screen=None, model=None):
        """
        General Purpose: Show the about page.
        With no screen, open the text screen when this is the direct verb.
        """
        text = self.about_text()
        if screen is not None and model is not None:
            self.notice(screen, model, text.splitlines() or [""], title="about")
            return 0
        if self.app is not None and self.app.stdout_is_tty():
            return self.open_direct("about")
        return text

    def _screen_error(self, too_small):
        if self.app is None:
            return "missing"
        if too_small:
            self.app.report_error(
                "The text screen is too small for the menu and the input box.",
                "{0} help".format(self.app.CONSOLE_NAME),
            )
        else:
            self.app.report_error(
                "The text menu could not open on this terminal.",
                "{0} help".format(self.app.CONSOLE_NAME),
            )
        return "missing"

    def _require_terminal(self):
        if self.app is None or not self.app.stdout_is_tty():
            if self.app is not None:
                self.app.report_error(
                    "No terminal for the text menu. Use a terminal.",
                    "{0} help".format(self.app.CONSOLE_NAME),
                )
            return False
        return True

    def open_text_menu(self):
        """
        General Purpose: Draw the front board. Does not convert images
        and does not run pip. Returns "missing" when the screen cannot open.
        """
        if not self._require_terminal():
            return "missing"
        try:
            import curses
        except ImportError:
            return self._screen_error(False)

        screen_box = {}

        def on_kind(kind):
            if kind == "help":
                return self.help_on_screen()
            if isinstance(kind, str) and kind.startswith("pick:"):
                return self.outline_result(
                    kind[5:],
                    screen=screen_box.get("screen"),
                    model=session.model,
                )
            if kind in ("version-check", "self-update", "self-install", "self-uninstall"):
                _code, text = self.app.self_manage.run_pip(kind)
                return text
            if kind == "view-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._view_log(screen, session.model)
            if kind == "clear-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._clear_log(screen, session.model)
            if kind == "log-folder":
                return self._log_folder()
            return None

        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=on_kind,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            screen_box["screen"] = screen
            session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            return self._screen_error(True)
        except Exception:
            return self._screen_error(False)
        return None

    def open_direct(self, kind):
        """
        General Purpose: Open the text screen on about.
        Does not start on the front board. Returns a process status.
        """
        if not self._require_terminal():
            return 1
        try:
            import curses
        except ImportError:
            self._screen_error(False)
            return 1

        code_box = {"code": 0}
        session = MenuSession(
            self._name(),
            self._ver(),
            on_version=lambda: self.app.self_manage.local_version(),
            on_about=self.about_text,
            boards=None,
            on_kind=lambda _kind: None,
            logger=self.logger,
            painter=self.painter,
        )

        def _wrapped(screen):
            try:
                if kind != "about":
                    code_box["code"] = 1
                    return
                code_box["code"] = self.about_on_screen(screen, session.model)
            except Exception as exc:
                self.notice(
                    screen, session.model, ["ERROR: {0}".format(exc)],
                    closing="Press a key to close.",
                )
                code_box["code"] = 1
            session.leave_to_front()
            # Esc and a finished page return to the front board.
            if code_box["code"] == 0:
                session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            self._screen_error(True)
            return 1
        except Exception:
            self._screen_error(False)
            return 1
        return code_box["code"]

    def _view_log(self, screen, model):
        """List log files and return the chosen file for the result page."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file:")
        picked = self._read_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        body = self.system_log.read_log(path)
        if body is None:
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        if body == "":
            body = "(empty)"
        return "{0}\n\n{1}".format(path.name, body)

    def _clear_log(self, screen, model):
        """List log files, confirm, and empty the chosen file."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file to clear:")
        picked = self._read_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        answer = self._read_yes_no(
            screen,
            model,
            ["Clear {0}? (y/n)".format(path.name)],
            title="system-log",
        )
        if answer is not True:
            return None
        if not self.system_log.clear_log(path):
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        return "Cleared {0}.".format(path.name)

    def _log_folder(self):
        """The log-folder result page. The path is logDir()."""
        return self.system_log.folder_text()
