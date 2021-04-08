from os import name
import re
from typing import List, Any

from .navigation_box import NavBox
from ..style import Fx, Cursor, Symbol
from ..theme import Theme
from fungit.shared import GitType
import fungit.commands as git


class StateBox(NavBox):
    name: str = 'state'
    genre = GitType.STATE
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    selected: int = 0
    box: str = ''
    box_content: str = ''

    @classmethod
    def fetch_data(cls):
        cls.content_orignal = git.state()

    @classmethod
    def generate(cls):
        _project, _head = cls.content_orignal
        cls.content = [f'{_project} {Symbol.right} {_head}']


class StatusBox(NavBox):
    name: str = 'status'
    genre = GitType.STATUS
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    selected: int = 0
    box: str = ''
    box_content: str = ''

    @classmethod
    def fetch_data(cls):
        cls.content_orignal = git.status()

    @classmethod
    def generate(cls):

        _content = []
        for item in cls.content_orignal:
            _content.append(' '.join(item))
        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        _current = cls.selected
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _c = cls.line_color(line[:2])

                _line = f'{Cursor.to(start_y, start_x)}{_c}{line if len(line) < line_w else line[:line_w]}{Theme.DEFAULT}'
                if cls.genre & cls.current and idx == _current:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1

    @classmethod
    def line_color(cls, flag):
        if flag == '??':
            color = Theme.FILE_UNTRACK
        elif flag == 'M ':
            color = Theme.FILE_CACHED
        elif flag == ' M':
            color = Theme.FILE_CHANGE
        elif flag == 'A ':
            color = Theme.FILE_NEW
        elif flag == ' D':
            color = Theme.FILE_DEL
        elif flag == 'D ':
            color = Theme.FILE_DELED
        elif flag == 'R ':
            color = Theme.FILE_RENAME
        else:
            color = Theme.DEFAULT

        return color

    @classmethod
    def switch_status(cls):
        _status, _path = cls.content_orignal[cls.selected]
        if _CACHED.match(_status):
            git.unstage(_path)
        else:
            git.stage(_path)

        cls.notify(update_data=True)

    @classmethod
    def switch_all(cls):
        for _status, _ in cls.content_orignal:
            if not _CACHED.match(_status):
                git.stage_all()
                break
        else:
            git.unstage_all()

        cls.notify(update_data=True)


class BranchBox(NavBox):
    name: str = 'branch'
    genre = GitType.BRANCH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    selected: int = 0
    box: str = ''
    box_content: str = ''

    @classmethod
    def fetch_data(cls):
        cls.content_orignal = git.load_branches()

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        content_ = []

        for branch in cls.content_orignal:
            prefix_ = '* ' if branch.is_head else '  '
            prefix_len = len(prefix_)

            status_, status_len = '', 0
            if branch.upstream_name:
                status_ = f' {Symbol.up}{branch.pushables}{Symbol.down}{branch.pullables}'
                status_len = len(branch.pushables) + len(branch.pullables) + 3

            less_len = line_w - prefix_len - status_len
            name_ = branch.name
            name_len = len(branch.name)
            if name_len > less_len:
                name_ = f'{name_[:less_len - 3]}...'

            line_ = f'{Theme.BRANCH}{prefix_}{Theme.DEFAULT}{name_}{Theme.BRANCH_STATUS}{status_}{Theme.DEFAULT}'
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

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line}'
                if cls.genre & cls.current and idx == _current:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class CommitBox(NavBox):
    name: str = 'commit'
    genre = GitType.COMMIT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    selected: int = 0
    box: str = ''
    box_content: str = ''

    @classmethod
    def fetch_data(cls):
        # get current head commit list
        cls.content_orignal = git.load_commits(git.current_head())

    @classmethod
    def generate(cls):
        line_w = cls.w - 2 - 9
        content_ = []

        for commit in cls.content_orignal:
            color_ = Theme.PUSHED if commit.is_pushed() else Theme.UNPUSHED
            id_ = commit.sha[:7]
            msg_ = commit.msg
            msg_ = msg_ if len(msg_) <= line_w else msg_[line_w]
            content_.append(f'{color_}{id_} {Theme.DEFAULT}{msg_}')

        cls.content = content_

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1

        _current = cls.selected
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ''
        for idx, line in enumerate(cls.content):

            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line}'
                if cls.genre & cls.current and idx == _current:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class StashBox(NavBox):
    name: str = 'stash'
    genre = GitType.STASH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def fetch_data(cls):
        cls.content_orignal = git.stashs()

    @classmethod
    def generate(cls):

        if cls.content_orignal:
            cls.content = cls.content_orignal.split('\n')
        else:
            cls.content = []


GIT_BOXS = [StateBox, StatusBox, BranchBox, CommitBox, StashBox]

_CACHED = re.compile(r'^[A-Z]\s$')
