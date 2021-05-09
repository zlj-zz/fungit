from typing import Any, List

from ..shared import BoxType
from ..theme import Theme
from .navigation_box import NavBox


class NoSpaceBox(NavBox):
    name: str = "no_space"
    genre = BoxType.NO_SPACE
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    start_idx: int = 0
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        cls.raw = "Not enough space!\nTerminal must be 8x90 or above.\nPlease press `q` to exit."

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        _content = []

        for file_ in cls.raw.split("\n"):
            str_len = len(file_)
            display_str = file_ if str_len >= line_w else file_[:line_w]
            line_ = f"{Theme.ERROR}{display_str}{Theme.DEFAULT}"
            _content.append(line_)

        cls.content = _content
