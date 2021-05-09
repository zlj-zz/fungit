#!/usr/bin/python3
import argparse
import platform
import signal
import logging

from . import __version__, __license__, __author__, __git_url__
from .logutil import setup_logging
from .term import Term
from .gui.box_option import generate_all_box
from .event.key import Key
from .event.process import process_key
from .event.clean_quit import quit_app


LOG = logging.getLogger(__name__)


def main(costom_commands: list = []):
    args = argparse.ArgumentParser()
    args.add_argument(
        "-v", "--version", action="store_true", help="show version info and exit"
    )
    args.add_argument(
        "--debug",
        action="store_true",
        help="start with loglevel set to DEBUG overriding value set in config",
    )
    stdargs = args.parse_args()
    if costom_commands:
        stdargs = args.parse_args(costom_commands)

    if stdargs.version:
        print(
            f"[fungit]: {__version__}, license={__license__}, os={platform.system()}, arch={platform.machine()}"
        )
        print(f"author={__author__}, url={__git_url__}")
        raise SystemExit(0)

    DEBUG: bool = stdargs.debug

    # Mark signal
    try:
        signal.signal(signal.SIGINT, signal_quit)  # Ctrl + c
        signal.signal(signal.SIGWINCH, signal_resize)  # Terminal resized
    except Exception as e:
        print("Error: initialize single failed! -> %s" % e)
        quit_app()

    setup_logging(DEBUG)
    Term.init()
    Key.start()
    generate_all_box(recreate=True)

    def run():
        while not False:
            # while Timer.not_zero():
            #     if Key.input_wait(Timer.left()):
            #         process_key()
            process_key()

    try:
        run()
    except Exception as e:
        if DEBUG:
            raise e
        LOG.error(e)
        quit_app()


def signal_resize(signum, frame):
    generate_all_box(recreate=True, update_data=False)


def signal_quit(signum, frame):
    quit_app()
