import logging

from fungit.commands import run_cmd_with_resp
from .gitoptions import GIT_OPTIONS, TYPES
from .shared import echo, warn, err, exit_, CommandColor, Fx


LOG = logging.getLogger(__name__)


def echo_one_help_msg(k: str):
    """Print a tip.

    Find the corresponding help information according to the `k` value and
    print it. If the help information does not exist, print the executed
    full command.

    Args:
        k: Short command.
    """
    echo("    " + k, color=CommandColor.GREEN, nl=False)
    if GIT_OPTIONS[k]["help-msg"]:
        msg = GIT_OPTIONS[k]["help-msg"]
    else:
        msg = GIT_OPTIONS[k]["command"]
    echo((9 - len(k)) * " " + str(msg))


def echo_help_msg():
    """Print help message."""
    echo("These are short commands that can replace git operations:")
    for k in GIT_OPTIONS.keys():
        echo_one_help_msg(k)


def give_tip(t: str):
    """Print a part of help message.

    Print the help information of the corresponding part according to the
    incoming command type string. If there is no print error prompt for the
    type.

    Args:
        t: A command type.
    """
    if t not in TYPES:
        err("There is no such type")
        raise SystemExit(0)

    echo(f"These are the orders of {t}")
    prefix = t[0].lower()
    for k in GIT_OPTIONS.keys():
        if k.startswith(prefix):
            echo_one_help_msg(k)


def echo_types():
    """Print all command types."""
    for t in TYPES:
        print(f" {t}")


def echo_description():
    """Print the description information"""
    from .. import __version__

    has_git = False
    try:
        _, git_version = run_cmd_with_resp("git --version")
        if git_version:
            has_git = True
    except Exception:
        LOG.warning("Happen error when run command with get Git version")
        git_version = ""

    echo("[fungit] version: %s" % __version__, style=Fx.b)
    echo(git_version)
    echo("Description:", style=Fx.b)
    echo(
        (
            "Fungit terminal tool, help you use git more simple."
            " Support Linux and MacOS.\n"
        ),
        style=Fx.underline,
    )

    echo("Usage: g <option> [<args>]", style=Fx.b)
    echo("You can use ", nl=False)
    echo("-h", color=CommandColor.GREEN, nl=False)
    echo(" and ", nl=False)
    echo("--help", color=CommandColor.GREEN, nl=False)
    echo(" to get how to use command fungit.\n")

    if not has_git:
        warn("Don't found Git, maybe need install.")
