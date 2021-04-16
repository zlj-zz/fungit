import sys
import signal

from ..logutil import setup_logging
from . import __TERLOG__
from .gitoptions import GIT_OPTIONS, process
from .msg_helper import give_tip, echo_help_msg, echo_description
from .shell_complete import add_completion
from .shared import exit_


def g(custom_commands: list = None):
    setup_logging(debug=False, log_file=__TERLOG__)

    if custom_commands is not None:
        return

    try:
        signal.signal(signal.SIGINT, exit_)
    except Exception:
        pass

    commands = sys.argv
    if len(commands) == 1:
        echo_description()
    elif commands[1] == "-h" or commands[1] == "--help":
        echo_help_msg(commands[2:])
    elif commands[1] == "--complete":
        add_completion()
    elif commands[1] not in GIT_OPTIONS.keys():
        give_tip(commands[1])
        exit(0)
    else:
        process(commands[1], commands[2:])
