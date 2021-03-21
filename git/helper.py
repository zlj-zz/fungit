from .gitoptions import GIT_OPTIONS
from .shared import echo, Color, Style


def echo_one_help_msg(k):
    echo('    ' + k, color=Color.GREEN, nl=False)
    if GIT_OPTIONS[k]['help-msg']:
        msg = GIT_OPTIONS[k]['help-msg']
    else:
        msg = GIT_OPTIONS[k]['command']
    echo((8 - len(k)) * ' ' + str(msg))


def echo_help_msg():
    echo("usage: g <command> [<args>]", style=Style.BOLD)
    echo('')
    echo("These are short commands that can replace git operations:")
    for k in GIT_OPTIONS.keys():
        echo_one_help_msg(k)


def give_tip(c: str):
    echo('\nMaybe what you want is:')
    c = c[0]
    for k in GIT_OPTIONS.keys():
        if k.startswith(c):
            echo_one_help_msg(k)
