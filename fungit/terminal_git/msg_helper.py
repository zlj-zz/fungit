import logging

from fungit.commands.exec import run_cmd_with_resp
from .gitoptions import GIT_OPTIONS, TYPES
from .shared import echo, warn, err, exit_, CommandColor, Fx


LOG = logging.getLogger()


def echo_one_help_msg(k: str):
    echo("    " + k, color=CommandColor.GREEN, nl=False)
    if GIT_OPTIONS[k]["help-msg"]:
        msg = GIT_OPTIONS[k]["help-msg"]
    else:
        msg = GIT_OPTIONS[k]["command"]
    echo((9 - len(k)) * " " + str(msg))


def echo_help_msg():
    echo("These are short commands that can replace git operations:")
    for k in GIT_OPTIONS.keys():
        echo_one_help_msg(k)


def give_tip(t: str):
    if t not in TYPES:
        err("There is no such type")
        raise SystemExit(0)

    echo(f"These are the orders of {t}")
    prefix = t[0].lower()
    for k in GIT_OPTIONS.keys():
        if k.startswith(prefix):
            echo_one_help_msg(k)


def echo_types():
    for t in TYPES:
        print(f" {t}")


def echo_description():
    from .. import __version__

    has_git = False
    try:
        err, git_version = run_cmd_with_resp("git --version")
        if git_version:
            has_git = True
        else:
            exit_(1, err)
    except Exception:
        LOG.warning("Happen error when run command with get Git version")
        git_version = ""

    echo("[fungit] version: %s" % __version__, style=Fx.b)
    echo(git_version)
    echo("Description:", style=Fx.b)
    echo(
        "Fungit terminal tool, help you use git more simple. Support Linux and MacOS.\n",
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
