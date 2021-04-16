import logging

from fungit.style import Color, Fx
from . import __TERLOG__


LOG = logging.getLogger()


class CommandColor:
    RED = Color.fg("#FF6347")  # Tomato
    GREEN = Color.fg("#98FB98")  # PaleGreen
    YELLOW = Color.fg("#FFD700")  # Gold


def echo(msg: str, color="", style="", nl: bool = True):
    print(f"{style}{color}{msg}{Fx.reset}", end="\n" if nl else "")


def okay(msg: str):
    echo(f"{Fx.b}{CommandColor.GREEN}{msg}{Fx.reset}")


def warn(msg: str):
    echo(f"{Fx.b}{CommandColor.YELLOW}{msg}{Fx.reset}")


def err(msg: str):
    echo(f"{Fx.b}{CommandColor.RED}{msg}{Fx.reset}")


def exit_(*args):
    if args and args[0] == 1:
        LOG.error(args[1:])
        print(f"Please check {__TERLOG__}")

    raise SystemExit(0)
