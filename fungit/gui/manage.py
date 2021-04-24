import logging
import threading

from .shared import BoxType, ConfirmType
from .box_option import initial_git_box as refresh_all
from .box.navigation_box import NavBox
from .box.git_box import GIT_BOXES
from .box.func_box import DynamicPromptBox, ConfirmBox
from fungit.commands import options


LOG = logging.getLogger(__name__)


class Manager:
    # box event
    @staticmethod
    def switch_box_by_index(idx):
        NavBox.set_current(GIT_BOXES[int(idx) - 1].genre)
        refresh_all(update_data=False)

    @staticmethod
    def prev_box():
        _current = NavBox.current
        _index = index_of(_current, need_box=False)
        _len = len(GIT_BOXES)
        new_index = _len - 1 - (_len - _index) % _len
        NavBox.set_current(GIT_BOXES[new_index].genre)
        refresh_all(update_data=False)

    @staticmethod
    def next_box():
        _current = NavBox.current
        _index = index_of(_current, need_box=False)
        _len = len(GIT_BOXES)
        new_index = (_index + 1) % _len
        NavBox.set_current(GIT_BOXES[new_index].genre)
        refresh_all(update_data=False)

    # item event
    @staticmethod
    def prev_item():
        _current = NavBox.current
        _, box = index_of(_current)

        if box.selected > 0:
            box.set_selected(box.selected - 1)

    @staticmethod
    def next_item():
        _current = NavBox.current
        _, box = index_of(_current)

        _max_len = len(box.raw) - 1

        if box.selected < _max_len:
            box.set_selected(box.selected + 1)

    @staticmethod
    def space_event():
        _current = NavBox.current
        LOG.debug(f"space event: {_current}")
        _, box = index_of(_current)

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
            # TODO: checkout commit has bug and error
        else:
            # TODO:
            pass

    @staticmethod
    def a_event():
        _current = NavBox.current
        _, box = index_of(_current)

        if _current & BoxType.STATUS:
            for file_ in box.raw:
                if file_.has_unstaged_change:
                    options.stage_all()
                    break
            else:
                options.unstage_all()

            box.notify(update_data=True)
        else:
            # TODO:
            pass

    @staticmethod
    def i_event():
        _current = NavBox.current
        _, box = index_of(_current)

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
        def _pull_option():
            options.pull()
            DynamicPromptBox.close = True

        t = threading.Thread(target=_pull_option)
        t.setDaemon(True)
        t.start()

        DynamicPromptBox.main("", "Pulling... ")
        refresh_all()

    @staticmethod
    def push():
        def _push_option():
            options.push()
            DynamicPromptBox.close = True

        t = threading.Thread(target=_push_option)
        t.setDaemon(True)
        t.start()

        DynamicPromptBox.main("", "Pushing.. ")
        refresh_all()

    @staticmethod
    def commit():
        is_open_editor = options.commit()
        if is_open_editor:
            _current = NavBox.current
            _, box = index_of(_current)
            box.selected = 0
            refresh_all()

    @staticmethod
    def del_():
        _current = NavBox.current
        _, box = index_of(_current)

        if _current & BoxType.STATUS:
            is_confirm = ConfirmBox.main("", "Discard all changed?")
            if is_confirm:
                file = box.raw[box.selected]
                options.del_(file.name, file.tracked)
                refresh_all()
            else:
                refresh_all(update_data=False)


def index_of(t, need_box: bool = True):
    for idx, sub in enumerate(GIT_BOXES):
        if sub.genre & t:
            if need_box:
                return idx, sub
            return idx
