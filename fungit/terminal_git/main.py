import argparse
import signal

from ..logutil import setup_logging
from . import __TERLOG__
from .gitoptions import process
from .msg_helper import echo_help_msg, echo_description, echo_types, give_tip
from .shell_complete import add_completion
from .shared import exit_


def command_g(custom_commands: list = None):
    setup_logging(debug=False, log_file=__TERLOG__)

    try:
        signal.signal(signal.SIGINT, exit_)
    except Exception:
        pass

    args = argparse.ArgumentParser()
    args.add_argument(
        "command", nargs="?", default="|", type=str, help="Short git command"
    )
    args.add_argument("args", nargs="*", type=str, help="Command parameter list")
    args.add_argument(
        "-c", "--complete", action="store_true", help="Add shell prompt script and exit"
    )
    args.add_argument(
        "-s",
        "--show-commands",
        action="store_true",
        help="List all available fame and wealth and exit",
    )
    args.add_argument(
        "-S",
        "--show-command",
        type=str,
        metavar="TYPE",
        dest="command_type",
        help="According to given type list available fame and wealth and exit",
    )
    args.add_argument(
        "-t",
        "--types",
        action="store_true",
        help="List all command type and exit",
    )
    stdargs = args.parse_args()

    if custom_commands is not None:
        stdargs = args.parse_args(custom_commands)

    if stdargs.complete:
        add_completion()
        raise SystemExit(0)

    if stdargs.show_commands:
        echo_help_msg()
        raise SystemExit(0)

    if stdargs.command_type:
        give_tip(stdargs.command_type)
        raise SystemExit(0)

    if stdargs.types:
        echo_types()
        raise SystemExit(0)

    if stdargs.command:
        if stdargs.command == "|":
            echo_description()
        else:
            command = stdargs.command
            process(command, stdargs.args)
