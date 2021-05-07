import os
import math

from .core import Win
from .shared import BoxType, ConfirmType
from .box.navigation_box import NavBox
from .box.git_box import GIT_BOXES
from .box.content_box import ContentBox
from .popup.confirm_popup import ConfirmBox
from fungit.event.clean_quit import quit_app


def generate_all_box(
    recreate: bool = False, update_data: bool = True, lazy_render: bool = False
):
    if recreate:
        w, h = os.get_terminal_size()
        Win.t_w, Win.t_h = w, h
        generate_git_box_w_h()  # update all nav box (w)idth and (h)eigth.
        create_content_box()

    for sub in GIT_BOXES:
        if update_data:  # Update raw data.
            sub.fetch_data()
            sub.generate()
        sub.create_profile()
        sub.update()
        if not lazy_render:
            sub.render()


def generate_git_box_w_h():
    w, h = Win.t_w, Win.t_h

    _selected_type = NavBox.current
    limit_w = math.floor(w / 3)

    if w < 90 or h < 8:
        tip = "Not enough space!\nTerminal must be higher than 8 and wider than 90.\nPlease press `q` to exit."
        ConfirmBox.main("Error", tip, ConfirmType.ERROR, full=True)
        quit_app()

    elif h <= 20:
        _old = None
        for sub in GIT_BOXES:
            sub.x = 1
            sub.w = limit_w

            if not _old:
                sub.y = 1
            else:
                sub.y = _old.y + _old.h
            _old = sub

            if sub.genre & _selected_type:
                sub.h = h - (1 * 4) - 1
            else:
                sub.h = 1

    elif h <= 25:
        _old = None
        for sub in GIT_BOXES:
            sub.x = 1
            sub.w = limit_w

            if not _old:
                sub.y = 1
            else:
                sub.y = _old.y + _old.h
            _old = sub

            if sub.genre & _selected_type:
                sub.h = h - (3 * 4) - 1
            else:
                sub.h = 3

    else:
        temp_x = GIT_BOXES[0].x = 1
        temp_y = GIT_BOXES[0].y = 1
        temp_w = GIT_BOXES[0].w = limit_w
        temp_h = GIT_BOXES[0].h = 3

        if _selected_type & BoxType.STASH:
            _split_h, _less = divmod(h - 4, 4)
        else:
            _split_h, _less = divmod(h - 7, 3)

        for idx, sub in enumerate(GIT_BOXES[1:-1]):
            sub.x = 1
            sub.y = temp_y + temp_h
            sub.w = limit_w
            sub.h = _split_h + (1 if _less > idx else 0)

            temp_x, temp_y, temp_w, temp_h = sub.x, sub.y, sub.w, sub.h

        GIT_BOXES[-1].x = 1
        GIT_BOXES[-1].y = temp_y + temp_h
        GIT_BOXES[-1].w = limit_w
        if _selected_type & BoxType.STASH:
            GIT_BOXES[-1].h = _split_h
        else:
            GIT_BOXES[-1].h = 3


def create_content_box():
    w, h = Win.t_w, Win.t_h
    limit_w = math.floor(w / 3)

    ContentBox.x = limit_w + 1
    ContentBox.y = 1
    ContentBox.w = w - limit_w
    ContentBox.h = h - 1

    for sub_con in ContentBox.__subclasses__():
        sub_con.create_profile()
