import logging
from typing import Any, List

from fungit import __version__
from fungit.style import Fx, Cursor
from ..shared import BoxType
from ..theme import Theme
from .navigation_box import NavBox


LOG = logging.getLogger(__name__)


class BottomLine(NavBox):
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
    def create_profile(cls):
        pass

    @classmethod
    def fetch_data(cls):
        left_ = "1-5: jump to panel, q: quit, esc: cancel, ← → ↑ ↓: navigate"
        right_ = "Zachary"
        cls.raw = "\n".join([left_, right_, __version__])

    @classmethod
    def generate(cls):
        line_w = cls.t_w
        y_ = cls.t_h
        # LOG.debug(f"{line_w} {y_}")
        _content = []

        lines = cls.raw.split("\n")
        len_ = len(lines[1]) + len(lines[2]) + 1
        if len(lines[0]) > line_w - len_ - 1:
            lines[0] = lines[0][: line_w - len_ - 1]

        _content.append(f'{Cursor.to(y_, 1)}{" "*line_w}')
        _content.append(f"{Cursor.to(y_, 1)}{Theme._steel_blue}{lines[0]}")
        x_ = line_w - len_
        _content.append(
            f"{Cursor.to(y_, x_)}{Theme._gold}{lines[1]} {Theme._green}{lines[2]}{Theme.DEFAULT}"
        )

        cls.content = _content

    @classmethod
    def update(cls):
        cls.box_content = ""
        for line in cls.content:
            cls.box_content += line
