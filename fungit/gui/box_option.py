import os
import math

from .core import Win
from .shared import BoxType
from .box.navigation_box import NavBox
from .box.git_box import NAVBOXES
from .box.content_box import ContentBox
from fungit.gui.box.error_box import NoSpaceBox


def generate_all_box(
    recreate: bool = False, update_data: bool = True, lazy_render: bool = False
):
    if recreate:
        w, h = os.get_terminal_size()
        Win.t_w, Win.t_h = w, h

        generate_git_box_w_h()  # update all sub nav box (w)idth and (h)eight.
        create_content_box()

    # Render all boxes.
    if not Win.no_space:
        for sub in boxes_cache():
            sub.notify(update_data=update_data, lazy_render=lazy_render)
    else:
        NoSpaceBox.notify()


def generate_git_box_w_h():
    w, h = Win.t_w, Win.t_h

    _selected_type = NavBox.current
    limit_w = math.floor(w / 3)

    if Win.no_space:
        Win.no_space = False

    if w < 90 or h < 8:
        Win.no_space = True
        NoSpaceBox.x = NoSpaceBox.y = 1
        NoSpaceBox.w, NoSpaceBox.h = w, h

    elif h <= 20:
        _old = None
        for sub in boxes_cache():
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
        for sub in boxes_cache():
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
        boxes_ = boxes_cache()
        temp_x = boxes_[0].x = 1
        temp_y = boxes_[0].y = 1
        temp_w = boxes_[0].w = limit_w
        temp_h = boxes_[0].h = 3

        if _selected_type & BoxType.STASH:
            _split_h, _less = divmod(h - 4, 4)
        else:
            _split_h, _less = divmod(h - 7, 3)

        for idx, sub in enumerate(boxes_[1:-1]):
            sub.x = temp_x
            sub.y = temp_y + temp_h
            sub.w = limit_w
            sub.h = _split_h + (1 if _less > idx else 0)

            temp_x, temp_y, temp_w, temp_h = sub.x, sub.y, sub.w, sub.h

        boxes_[-1].x = 1
        boxes_[-1].y = temp_y + temp_h
        boxes_[-1].w = limit_w
        if _selected_type & BoxType.STASH:
            boxes_[-1].h = _split_h
        else:
            boxes_[-1].h = 3


def create_content_box():
    w, h = Win.t_w, Win.t_h
    limit_w = math.floor(w / 3)

    ContentBox.x = limit_w + 1
    ContentBox.y = 1
    ContentBox.w = w - limit_w
    ContentBox.h = h - 1

    for sub_con in ContentBox.__subclasses__():
        sub_con.create_profile()


def _boxes_cache():
    cache = None

    def close_():
        nonlocal cache
        if cache:
            return cache
        else:
            cache = list(NAVBOXES.values())
            return cache

    return close_


# Closure function, cache `boxes.values()`
boxes_cache = _boxes_cache()
