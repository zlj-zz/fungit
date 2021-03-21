# import click
from .gitoptions import GIT_OPTIONS, process
from .helper import give_tip, echo_help_msg, echo_discription
import sys
sys.path.append('.')


def g(coustom_commands: list = None):
    if coustom_commands is not None:
        return

    commands = sys.argv
    if len(commands) == 1:
        echo_discription()
    elif commands[1] == '-h' or commands[1] == '--help':
        echo_help_msg(commands[2:])
    elif commands[1] not in GIT_OPTIONS.keys():
        give_tip(commands[1])
        exit(0)
    else:
        process(commands[1], commands[2:])


if __name__ == "__main__":
    g()
