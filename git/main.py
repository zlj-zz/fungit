# import click
import sys
sys.path.append('.')

from .helper import give_tip, echo_help_msg
from .gitoptions import GIT_OPTIONS, process
from .shared import echo, Color


def g(coustom_commands: list = None):
    if coustom_commands is not None:
        return

    commands = sys.argv
    if len(commands) == 1 or commands[1] == '-h' or commands[1] == '--help':
        echo_help_msg()
    elif commands[1] not in GIT_OPTIONS.keys():
        echo("Dont support this option.", color=Color.RED)
        give_tip(commands[1])
        exit(0)
    else:
        process(commands[1], commands[2:])


if __name__ == "__main__":
    g()
