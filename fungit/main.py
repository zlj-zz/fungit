#!/usr/bin/python3
import argparse

from .logutil import setup_logging
from .term import Term
from .gui.box_option import initial_git_box
from .event.key import Key
from .event.process import process_key


def main(costom_commands: list = []):
    args = argparse.ArgumentParser()
    args.add_argument(
        "-v", "--version", action="store_true", help="show version info and exit"
    )
    # TODO:finish show version
    args.add_argument(
        "--debug",
        action="store_true",
        help="start with loglevel set to DEBUG overriding value set in config",
    )
    stdargs = args.parse_args()
    if costom_commands:
        stdargs = args.parse_args(costom_commands)

    DEBUG: bool = stdargs.debug

    Term.init()
    setup_logging(DEBUG)

    initial_git_box()
    Key.start()

    def run():
        while not False:
            # Term.refresh()
            # Timer.stamp()

            # while Timer.not_zero():
            #     if Key.input_wait(Timer.left()):
            #         process_key()
            process_key()

    run()
    # try:
    # except Exception as e:
    #     # clean_quit(1)
    #     print(e)
    #     exit(1)
