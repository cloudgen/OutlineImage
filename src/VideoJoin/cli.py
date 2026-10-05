#!/usr/bin/env python
# =============================================================================
# VideoJoin CLI — text menu and typed verbs.
# Law keys: requirement-python-cli-interface, requirement-python-cli-logging,
#           requirement-python-tui, requirement-python-oop,
#           requirement-python-about, requirement-domain-videojoin,
#           requirement-python-error-handling, requirement-python-coding-style,
#           requirement-runtime-prerequisites
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# def main writes ChronicleLogger(...). This module does not construct it
# at import time and does not re-export it.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import sys

from .about_page import AboutPage
from .check_system import CheckSystem
from .join import Join
from .self_management import SelfManage
from .tui import Tui


class Cli:
    """Parser, dispatch, verbs, and the tty gate. One class in this file.

    Identity, verb lists, and suffix sets are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    """

    from . import __version__ as VERSION

    APP_NAME = "VideoJoin"
    CONSOLE_NAME = "video-join"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "hello",
        "join",
        "list-videos",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".m4v"}
    OUTPUT_SUFFIXES = (".mp4", ".mkv", ".mov")
    AUTHOR_NAME = "Wilgat Wong"
    AUTHOR_EMAIL = "wilgat.wong@gmail.com"
    HOMEPAGE = "https://github.com/Wilgat/VideoJoin"
    LAST_UPDATE = "2026-10-04"
    DOWNLOAD_URL = ""
    BASIC_USAGE = "video-join join"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli.VERSION
        self.join = Join(
            logger=logger,
            video_suffixes=Cli.VIDEO_SUFFIXES,
            output_suffixes=Cli.OUTPUT_SUFFIXES,
        )
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli.VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli.VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.tui = Tui(self, logger=logger)

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, hello, and the pip verbs do not draw the screen.
        Empty argv, join, list-videos, and about do, when stdout is a terminal.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdout_is_tty():
            return False
        verb = None
        saw_force = False
        for token in argv:
            if token == "--force":
                saw_force = True
                continue
            if token.startswith("-"):
                return False
            if verb is None:
                verb = token
                continue
            return False
        if saw_force and verb != "self-uninstall":
            return False
        if verb in ("join", "list-videos", "about"):
            return True
        return verb is None

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def build_parser(self):
        """
        General Purpose: One optional product verb. No file-operand flags.
        help is also --help. --force belongs only to self-uninstall.
        """
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=(
                "{0} — concatenate two videos in this folder.\n"
                "With no arguments on a terminal, opens the text menu.\n"
                "With no arguments and no terminal, prints this help and stops.\n"
                "Product verbs: help, version, about, hello, join, list-videos,\n"
                "self-install, version-check, self-update, self-uninstall.\n"
                "help prints this usage. version prints the installed version.\n"
                "about and hello print a page. hello does not draw the menu.\n"
                "join asks for two videos in this folder and an output name.\n"
                "list-videos lists eligible videos and does not join.\n"
                "version-check runs: python -m pip index versions VideoJoin\n"
                "self-update runs: python -m pip install --upgrade VideoJoin\n"
                "self-install runs: python -m pip install VideoJoin\n"
                "self-uninstall runs: python -m pip uninstall -y VideoJoin\n"
                "and needs --force. Empty arguments do not install or update.\n"
                "Formats: .mp4 .mov .mkv .avi .m4v."
                .format(Cli.APP_NAME)
            ),
        )
        parser.add_argument(
            "verb",
            nargs="?",
            default=None,
            metavar="verb",
            help=(
                "Product verb: help, version, about, hello, join, list-videos, "
                "self-install, version-check, self-update, or self-uninstall"
            ),
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(Cli.APP_NAME, Cli.VERSION),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line.",
        )
        return parser

    def _page(self, text):
        print(text)
        return 0

    def _verb_hello(self):
        """Hello from this package, then the help next step. Does not draw the menu."""
        print(self.tui.hello_text())
        print("Next: {0} help".format(Cli.CONSOLE_NAME))
        return 0

    def _unknown_verb(self, token):
        names = ", ".join(Cli.PRODUCT_VERBS)
        return self.report_error(
            "Unknown verb '{0}'.".format(token),
            "{0} help — verbs: {1}".format(Cli.CONSOLE_NAME, names),
        )

    def _print_video_list(self):
        """Eligible names on the console. Does not join and does not draw the screen."""
        print(self.tui._video_listing())
        return 0

    def _dispatch(self, args):
        """One product verb, the front board, or a fail-closed stop."""
        verb = args.verb
        if args.force and verb != "self-uninstall":
            return self.report_error(
                "--force is only for self-uninstall.",
                "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
            )
        if verb == "about":
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "hello":
            return self._verb_hello()
        if verb == "version":
            return self._page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not args.force:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
                )
            return self.self_manage.emit(verb)
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb)
        if verb == "join":
            if not self.stdout_is_tty():
                return self.report_error(
                    "No terminal for join. Use a terminal.",
                    "{0} join".format(Cli.CONSOLE_NAME),
                )
            return self.tui.open_direct("join")
        if verb == "list-videos":
            result = self.tui.list_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb is not None:
            return self._unknown_verb(verb)
        if not self.stdout_is_tty():
            self.build_parser().print_help()
            return 0
        action = self.tui.open_text_menu()
        if action == "missing":
            return 1
        return 0

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        parser = self.build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            code = exc.code
            if code is None or code == 0:
                return 0
            return int(code)
        if args.verb == "help":
            parser.print_help()
            return 0
        return self._dispatch(args)


def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    from VideoJoin import __version__

    screen = Cli.opens_text_screen(argv)
    logger = ChronicleLogger(
        logname="VideoJoin",
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())
