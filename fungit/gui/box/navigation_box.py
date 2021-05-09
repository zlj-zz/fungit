from typing import List, Any

from fungit.style import Fx, Cursor
from ..shared import BoxType
from ..renderer import Renderer
from ..theme import Theme
from ..core import Win
from .content_box import ContentBox


class NavBox(Win):
    # only change in father class, sub class only read
    current: int = BoxType.STATUS

    name: str
    genre: int
    x: int
    y: int
    w: int
    h: int
    raw: Any
    content: List
    start_idx: int  # display start item index
    selected: int  # selected item
    box: str  # box profile string
    box_content: str

    @classmethod
    def set_current(cls, t: int):
        cls.current = t

    @classmethod
    def set_selected(cls, v):
        cls.selected = v
        cls.notify()

    @classmethod
    def create_profile(cls):
        _line_color = Theme.BOX_SELECTED_COLOR if cls.genre & cls.current else ""
        _item_msg = (
            f"{cls.selected + 1} of {len(cls.content)}" if len(cls.content) > 1 else ""
        )
        cls.box = super().create_profile(
            cls.x, cls.y, cls.w, cls.h, cls.name, _item_msg, line_color=_line_color
        )

    @classmethod
    def fetch_data(cls):
        """Get raw data.

        Get the list of original data and cache it in `cls.raw`, each of which
        is an independent data object instance(Override by subclass).
        """
        pass

    @classmethod
    def generate(cls):
        """Content of production display.

        All the acquired data is produced as the class content that can be
        displayed, colored and cached in `cls.content`(Override by subclass).
        """
        pass

    @classmethod
    def update(cls):
        """Update display content.

        According to the currently selected item to update the displayed
        content block (current item BOLD), generate a content string, and
        assign it to `cls.box_content`.
        """
        start_x = cls.x + 1
        start_y = cls.y + 1
        height_ = cls.h - 2

        _current = cls.selected

        if _current - cls.start_idx + 1 > height_:
            cls.start_idx += 1
        elif _current < cls.start_idx:
            cls.start_idx -= 1
        else:
            # If range size > height, start index ++.
            # If select index < first start index, start index --.
            # Else do nothing.
            pass

        start_idx = cls.start_idx
        cls.box_content = ""
        for idx, line in enumerate(cls.content[cls.start_idx :]):
            if idx < height_:
                _line = f"{Cursor.to(start_y, start_x)}{line}"
                if cls.genre & cls.current and idx + start_idx == _current:
                    _line = f"{Fx.b}{_line}{Fx.ub}"
                cls.box_content += _line
                start_y += 1

    @classmethod
    def render(cls):
        Renderer.now(cls.box, cls.box_content)

        if cls.current & cls.genre:
            ContentBox.notify(cls)

    @classmethod
    def notify(
        cls,
        update_data: bool = False,
        re_profile: bool = True,
        lazy_render: bool = False,
    ):
        if update_data or not cls.raw:
            cls.fetch_data()
            cls.generate()
        if re_profile or not cls.box:
            cls.create_profile()
        # every notify must update display string and render all.
        cls.update()
        if not lazy_render:
            cls.render()
