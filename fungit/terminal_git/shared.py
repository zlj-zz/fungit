import subprocess

from fungit.style import Color, Fx


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
