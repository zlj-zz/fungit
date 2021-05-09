import logging

from .shared import BoxType, ConfirmType
from .box_option import generate_all_box as refresh_all
from .box.navigation_box import NavBox
from .box.git_box import NAVBOXES
from .popup.wait_popup import DynamicPromptBox
from .popup.confirm_popup import ConfirmBox
from .box.content_box import ContentBox
from fungit.commands import options


LOG = logging.getLogger(__name__)


class Manager:
    # box event
    @staticmethod
    def switch_box_by_index(idx):
        NavBox.set_current(1 << (int(idx) - 1))  # Get right genre.
        refresh_all(recreate=True, update_data=False)

    @staticmethod
    def prev_box():
        _current = NavBox.current
        _index = index_of(_current, need_box=False)
        _len = len(NAVBOXES)
        new_index = _len - 1 - (_len - _index) % _len
        NavBox.set_current(1 << new_index)
        refresh_all(recreate=True, update_data=False)

    @staticmethod
    def next_box():
        _current = NavBox.current
        _index = index_of(_current, need_box=False)
        _len = len(NAVBOXES)
        new_index = (_index + 1) % _len
        NavBox.set_current(1 << new_index)
        refresh_all(recreate=True, update_data=False)

    # item event
    @staticmethod
    def prev_item():
        _current = NavBox.current
        box = NAVBOXES[_current]

        if box.selected > 0:
            box.set_selected(box.selected - 1)

    @staticmethod
    def next_item():
        _current = NavBox.current
        box = NAVBOXES[_current]

        _max_len = len(box.raw) - 1

        if box.selected < _max_len:
            box.set_selected(box.selected + 1)

    @staticmethod
    def space_event():
        _current = NavBox.current
        LOG.debug(f"space event: {_current}")
        box = NAVBOXES[_current]

        if _current & BoxType.STATUS:
            file_ = box.raw[box.selected]

            if file_.has_unstaged_change:
                options.stage(file_.name)
            else:
                options.unstage(file_.name)
            box.notify(update_data=True)
        elif _current & BoxType.BRANCH:
            branch = box.raw[box.selected]
            err, _ = options.checkout(branch.name)
            if err and "error" in err:
                ConfirmBox.main("Error", err, ConfirmType.ERROR)
            refresh_all()
        elif _current & BoxType.COMMIT:
            commit = box.raw[box.selected]
            err, resp = options.checkout(commit.sha)
            if err and "error" in err:
                ConfirmBox.main("Error", err, ConfirmType.ERROR)
            refresh_all()
            LOG.debug(f"{err} | {resp}")
        else:
            # TODO: other space event.
            pass

    @staticmethod
    def a_event():
        _current = NavBox.current
        box = NAVBOXES[_current]

        if _current & BoxType.STATUS:
            for file_ in box.raw:
                if file_.has_unstaged_change:
                    options.stage_all()
                    break
            else:
                options.unstage_all()

            box.notify(update_data=True)
        else:
            # TODO: may have other `a` event.
            pass

    @staticmethod
    def i_event():
        _current = NavBox.current
        box = NAVBOXES[_current]

        if _current == BoxType.STATUS:
            file = box.raw[box.selected]

            try:
                options.ignore(file.name)
            except Exception as e:
                ConfirmBox.main("Error", e, ConfirmType.ERROR)
            box.notify(update_data=True)
        else:
            pass

    @staticmethod
    def pull():
        DynamicPromptBox.main("Pulling... ", options.pull)
        refresh_all()

    @staticmethod
    def push():
        DynamicPromptBox.main("Pushing.. ", options.push)
        refresh_all()

    @staticmethod
    def commit():
        is_open_editor = options.commit()
        if is_open_editor:
            _current = NavBox.current
            box = NAVBOXES[_current]
            box.selected = 0
            refresh_all()

    @staticmethod
    def del_():
        _current = NavBox.current
        box = NAVBOXES[_current]

        if _current & BoxType.STATUS:
            is_confirm = ConfirmBox.main("", "Discard all changed?")
            if is_confirm:
                file = box.raw[box.selected]
                options.del_(file.name, file.tracked)
                refresh_all()
            else:
                refresh_all(update_data=False)

    @staticmethod
    def mouse_event(key, mouse_pos):
        _current = NavBox.current
        box = NAVBOXES[_current]
        sub = get_sub_content_box(box)
        mouse_x, mouse_y = mouse_pos
        LOG.debug(f"{key} {box} {sub} {sub.content_selected_line}")
        LOG.debug(f"{mouse_x} {mouse_y} {ContentBox.x} {ContentBox.y}")

        if mouse_x > ContentBox.x and mouse_y > ContentBox.y:
            LOG.debug(f"{ContentBox.h}")
            fresh = False
            if key == "mouse_scroll_down":
                if sub.content_selected_line < sub.content_len:
                    sub.content_selected_line += 1
                    fresh = True
            elif key == "mouse_scroll_up":
                if sub.content_selected_line > 0:
                    sub.content_selected_line -= 1
                    fresh = True
            if fresh:
                box.notify(update_data=False, re_profile=False)
        else:
            pass


def index_of(genre_code: int, need_box: bool = True):
    idx = list(NAVBOXES.keys()).index(genre_code)
    if need_box:
        return idx, NAVBOXES[genre_code]
    return idx


def get_sub_content_box(box):
    for sub in ContentBox.__subclasses__():
        if sub.genre & box.genre:
            return sub
