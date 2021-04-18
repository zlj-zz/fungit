import logging
import threading

from .box_option import initial_git_box as refresh_all
from .box.navigation_box import NavBox
from .box.git_box import GIT_BOXES
from .box.func_box import DynamicPromptBox, ConfirmBox
from fungit.shared import GitType
import fungit.commands as git


LOG = logging.getLogger(__name__)


class Manager:
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

        if _current & GitType.STATUS:
            box.switch_status()
        if _current & GitType.BRANCH:
            branch = box.raw[box.selected]
            err, _ = git.checkout(branch.name)
            if err:
                ConfirmBox.main("Error", err)
                return
            refresh_all()
        else:
            # TODO:
            pass

    @staticmethod
    def a_event():
        _current = NavBox.current
        _, box = index_of(_current)

        if _current & GitType.STATUS:
            box.switch_all()
        else:
            # TODO:
            pass

    @staticmethod
    def pull():
        def _pull_option():
            git.pull()
            DynamicPromptBox.close = True

        t = threading.Thread(target=_pull_option)
        t.setDaemon(True)
        t.start()

        DynamicPromptBox.main("", "Pulling... ")
        refresh_all()

    @staticmethod
    def push():
        def _push_option():
            git.push()
            DynamicPromptBox.close = True

        t = threading.Thread(target=_push_option)
        t.setDaemon(True)
        t.start()

        DynamicPromptBox.main("", "Pushing.. ")
        refresh_all()


def index_of(t, need_box: bool = True):
    for idx, sub in enumerate(GIT_BOXES):
        if sub.genre & t:
            if need_box:
                return idx, sub
            return idx
