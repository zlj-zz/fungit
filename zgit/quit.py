from .renderer import Renderer
from .key import Key
from .term import Term


def clean_quit(errcode: int = 0, errmsg: str = "", thread: bool = False):
    """Stop background input read, save current config and reset terminal settings before quitting"""
    Key.stop()
    Renderer.now(Term.clear, Term.normal_screen, Term.show_cursor,
                 Term.mouse_off, Term.mouse_direct_off, Term.title())
    Term.echo(True)

    raise SystemExit(errcode)
