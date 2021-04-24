import logging
from typing import List, Any

from fungit.commands import loading
from fungit.style import Fx, Cursor, Symbol
from ..shared import BoxType
from ..theme import Theme
from .navigation_box import NavBox


class StateBox(NavBox):
    name: str = "state"
    genre = BoxType.STATE
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        cls.raw = loading.load_state()

    @classmethod
    def generate(cls):
        _project, _head = cls.raw
        cls.content = [f"{_project} {Symbol.right} {_head}"]


class StatusBox(NavBox):
    name: str = "status"
    genre = BoxType.STATUS
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        cls.raw = loading.load_files()

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        _content = []

        for file_ in cls.raw:
            str_len = len(file_.display_str)
            display_str = (
                file_.display_str if str_len > line_w else file_.display_str[:line_w]
            )
            color_ = cls.line_color(file_)
            line_ = f"{color_}{display_str}{Theme.DEFAULT}"
            _content.append(line_)

        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1

        _current = cls.selected
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than height
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ""
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{line}"
                if cls.genre & cls.current and idx == _current:
                    _line = f"{Fx.b}{_line}{Fx.ub}"
                cls.box_content += _line
                start_y += 1

    @classmethod
    def line_color(cls, f):
        color = Theme.DEFAULT
        if f.tracked:
            if f.has_unstaged_change:
                color = Theme.FILE_CHANGE
            elif f.has_staged_change:
                color = Theme.FILE_CACHED
            elif f.deleted:
                color = Theme.FILE_DEL
        else:  # untracked
            if f.added:
                color = Theme.FILE_NEW
            else:
                color = Theme.FILE_UNTRACK

        return color

    @classmethod
    def notify(cls, update_data: bool = False, re_profile: bool = True):
        if update_data:
            cls.fetch_data()
            cls.generate()
            try:
                cls.raw[cls.selected]
            except ValueError:
                cls.selected -= 1
        if re_profile:
            cls.create_profile()
        # every notify must update display string and render all.
        cls.update()
        cls.render()


class BranchBox(NavBox):
    name: str = "branch"
    genre = BoxType.BRANCH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        cls.raw = loading.load_branches()

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        content_ = []

        for branch in cls.raw:
            prefix_ = "* " if branch.is_head else "  "
            prefix_len = len(prefix_)

            status_, status_len = "", 0
            if branch.upstream_name:
                status_ = (
                    f" {Symbol.up}{branch.pushables}{Symbol.down}{branch.pullables}"
                )
                status_len = len(branch.pushables) + len(branch.pullables) + 3

            less_len = line_w - prefix_len - status_len
            name_ = branch.name
            name_len = len(branch.name)
            if name_len > less_len:
                name_ = f"{name_[:less_len - 3]}..."

            line_ = f"{Theme.BRANCH}{prefix_}{Theme.DEFAULT}{name_}{Theme.BRANCH_STATUS}{status_}{Theme.DEFAULT}"
            content_.append(line_)

        cls.content = content_

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1

        _current = cls.selected
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ""
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{line}"
                if cls.genre & cls.current and idx == _current:
                    _line = f"{Fx.b}{_line}{Fx.ub}"
                cls.box_content += _line
                start_y += 1


class CommitBox(NavBox):
    name: str = "commit"
    genre = BoxType.COMMIT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        # get current head commit list
        cls.raw = loading.load_commits(loading.current_head())

    @classmethod
    def generate(cls):
        line_w = cls.w - 2 - 9
        content_ = []

        for commit in cls.raw:
            color_ = Theme.PUSHED if commit.is_pushed() else Theme.UNPUSHED
            id_ = commit.sha[:7]
            msg_ = commit.msg
            msg_ = msg_ if len(msg_) <= line_w else msg_[:line_w]
            content_.append(f"{color_}{id_} {Theme.DEFAULT}{msg_}")

        cls.content = content_

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1

        _current = cls.selected
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than height
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ""
        for idx, line in enumerate(cls.content):

            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{line}"
                if cls.genre & cls.current and idx == _current:
                    _line = f"{Fx.b}{_line}{Fx.ub}"
                cls.box_content += _line
                start_y += 1


class StashBox(NavBox):
    name: str = "stash"
    genre = BoxType.STASH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    selected: int = 0
    box: str = ""
    box_content: str = ""

    @classmethod
    def fetch_data(cls):
        cls.raw = loading.load_stashes()

    @classmethod
    def generate(cls):

        if cls.raw:
            cls.content = cls.raw.split("\n")
        else:
            cls.content = []


GIT_BOXES = [StateBox, StatusBox, BranchBox, CommitBox, StashBox]
