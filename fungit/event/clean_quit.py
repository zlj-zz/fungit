import logging

from ..term import Term
from .key import Key


LOG = logging.getLogger(__name__)


def quit_app(code: int = 0, message: str = ""):
    Term.clear()
    Key.stop()
    if message:
        LOG.warning(message)
        print(message)
    raise SystemExit(code)
