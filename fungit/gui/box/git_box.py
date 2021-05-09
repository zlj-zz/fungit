import logging
from typing import List, Any

from fungit.commands import loading
from fungit.style import Symbol
from ..shared import BoxType
from ..theme import Theme
from .navigation_box import NavBox


LOG = logging.getLogger(__name__)


class StateBox(NavBox):
    name: str = "state"
    genre = BoxType.STATE
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
        cls.raw = loading.load_state()

    @classmethod
    def generate(cls):
        cls.content.clear()
        line_w = cls.w - 2
        _project, _head = cls.raw
        item = f"{_project} {Symbol.right} {_head}"
        cls.content.append(item if len(item) <= line_w else item[:line_w])


class StatusBox(NavBox):
    name: str = "status"
    genre = BoxType.STATUS
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
        cls.raw = loading.load_files()
        while True:
            try:
                cls.raw[cls.selected]
                break
            except IndexError:  # out of range (rename, ignore, commit)
                if cls.selected == 0:  # It means no data.
                    break
                cls.selected -= 1
                continue

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        _content = []

        for file_ in cls.raw:
            str_len = len(file_.display_str)
            display_str = (
                file_.display_str if str_len >= line_w else file_.display_str[:line_w]
            )
            color_ = cls.line_color(file_)
            line_ = f"{color_}{display_str}{Theme.DEFAULT}"
            _content.append(line_)

        cls.content = _content

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
            if f.has_unstaged_change:
                color = Theme.FILE_UNTRACK
            else:
                color = Theme.FILE_NEW

        return color


class BranchBox(NavBox):
    name: str = "branch"
    genre = BoxType.BRANCH
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


class CommitBox(NavBox):
    name: str = "commit"
    genre = BoxType.COMMIT
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


class StashBox(NavBox):
    name: str = "stash"
    genre = BoxType.STASH
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
        cls.raw = loading.load_stashes()

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        content_ = []

        for stash in cls.raw:
            name = stash.name
            content_.append(name[:line_w] if len(name) > line_w else name)

        cls.content = content_


# GIT_BOXES = [StateBox, StatusBox, BranchBox, CommitBox, StashBox]

NAVBOXES = {
    StateBox.genre: StateBox,
    StatusBox.genre: StatusBox,
    BranchBox.genre: BranchBox,
    CommitBox.genre: CommitBox,
    StashBox.genre: StashBox,
}
