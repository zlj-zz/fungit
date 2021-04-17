import logging

from fungit.style import Color, Fx
from . import __TERLOG__


LOG = logging.getLogger(__name__)


class CommandColor:
    """Terminal print color class."""

    RED = Color.fg("#FF6347")  # Tomato
    GREEN = Color.fg("#98FB98")  # PaleGreen
    YELLOW = Color.fg("#FFD700")  # Gold


def echo(msg: str, color="", style="", nl: bool = True):
    """Print to terminal.

    Print special information with color and style according to the
    incoming parameters.

    Args:
        msg: A special message.
        color: Message color.
        style: Message style, like: [bold, underline].
        nl: Is there a line feed.
    """
    print(f"{style}{color}{msg}{Fx.reset}", end="\n" if nl else "")


def okay(msg: str):
    """Print green information."""
    echo(f"{Fx.b}{CommandColor.GREEN}{msg}{Fx.reset}")


def warn(msg: str):
    """Print yellow information."""
    echo(f"{Fx.b}{CommandColor.YELLOW}{msg}{Fx.reset}")


def err(msg: str):
    """Print red information."""
    echo(f"{Fx.b}{CommandColor.RED}{msg}{Fx.reset}")


def exit_(*args):
    """Exit program.

    Receive error code, error message. If the error code matches, print the
    error information to the log. Then the command line output prompt, and
    finally exit.

    Args:
        *args:
            code: Exit code.
            msg: Error message.
    """
    if args and args[0] == 1:
        LOG.error(args[1:])
        print(f"Please check {__TERLOG__}")

    raise SystemExit(0)
