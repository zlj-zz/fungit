from typing import List, Tuple, Any

from .basic_box import Box, GitTypeBox
from zgit.style import Fx, Color, Cursor, ConfigColor
from zgit.coordinate import fetch_content, Selected, Git
from zgit.shared import TIP

BOX_SELECTED_COLOR = Color.fg('#32cd32')


class StateBox(GitTypeBox):
    name: str = 'state'
    genre = Selected.STATE
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = Git.tree[cls.genre]
        cls.content = [cls.content_orignal]


class StatusBox(GitTypeBox):
    name: str = 'status'
    genre = Selected.STATUS
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = Git.tree[cls.genre]  # if no data, empty list

        _content = []
        for item in cls.content_orignal:
            _content.append(' '.join(item))
        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        _current = Selected.selected[cls.genre]
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _c = cls.line_color(line[:2])

                _line = f'{Cursor.to(start_y, start_x)}{_c}{line if len(line) < line_w else line[:line_w]}{ConfigColor.default}'
                if cls.genre & Selected.current and idx == Selected.status:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1

    @classmethod
    def line_color(cls, flag):
        if flag == '??':
            color = ConfigColor.status_untrack
        elif flag == 'M ':
            color = ConfigColor.status_cached
        elif flag == ' M':
            color = ConfigColor.status_change
        elif flag == 'A ':
            color = ConfigColor.status_new
        elif flag == ' D':
            color = ConfigColor.status_del
        elif flag == 'D ':
            color = ConfigColor.status_deled
        elif flag == 'R ':
            color = ConfigColor.status_rename
        elif flag == '':
            pass
        elif flag == '':
            pass
        else:
            color = ConfigColor.status_del

        return color


class BranchBox(GitTypeBox):
    name: str = 'branch'
    genre = Selected.BRANCH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = Git.tree[cls.genre]  # if no data, empty list
        cls.content = cls.content_orignal

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        _current = Selected.selected[cls.genre]
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = line if len(line) < line_w else line[:line_w]
                if _line.startswith('* '):
                    _line = f'{ConfigColor.status_new}{_line}{ConfigColor.default}'
                _line = f'{Cursor.to(start_y, start_x)}{_line}'
                if cls.genre & Selected.current and idx == Selected.branch:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class CommitBox(GitTypeBox):
    name: str = 'commit'
    genre = Selected.COMMIT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = Git.tree[cls.genre]  # if no data, empty list

        _content = []
        for item in cls.content_orignal:
            _content.append(' '.join(item))
        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2 - 9

        _current = Selected.selected[cls.genre]
        _limit = 0
        if _current + 1 >= cls.h - 2:  # current selected index big than heigth
            _limit = _current + 1 - (cls.h - 2)

        cls.box_content = ''
        for idx, line in enumerate(cls.content_orignal):
            _id, _msg = line
            _id = f'{ConfigColor.commit_id}{_id}'
            _msg = f'{ConfigColor.default}{_msg if len(_msg) < line_w else _msg[:line_w]}'

            if idx >= _limit and idx - _limit < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{_id} {_msg}'
                if cls.genre & Selected.current and idx == Selected.commit:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class StashBox(GitTypeBox):
    name: str = 'stash'
    genre = Selected.STASH
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = Git.tree[cls.genre]

        if cls.content_orignal:
            cls.content = cls.content_orignal.split('\n')
        else:
            cls.content = []


class ContentBox(Box):
    name: str = 'content'
    genre = Selected.CONTENT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    @classmethod
    def generate(cls):
        cls.content_orignal = fetch_content()
        _content = []

        for line in cls.content_orignal.split('\n'):
            if len(line) < cls.w - 2:
                _content.append(line)
            else:
                _content.append(line[:cls.w - 2])
                _content.append(line[cls.w - 2:])

        cls.content = _content

    @classmethod
    def update(self):
        start_y = self.y + 1
        start_x = self.x + 1
        # print(self.x, self.y, self.w, self.h)

        self.box_content = ''
        for idx, line in enumerate(self.content):
            if idx < self.h - 2:
                self.box_content += f'{Cursor.to(start_y, start_x)}{line}'
                start_y += 1


class TipBox(Box):
    name: str = 'tip'
    genre = Selected.Tip
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    count = 0
    process_symbol = ['/', '-', '\\', '|']

    @classmethod
    def create(cls, w, h):
        cls.content_orignal = TIP
        cls.x = round(w / 4)
        cls.w = round(w / 2)
        _w = cls.w - 2
        _len = len(cls.content_orignal)
        idx = 0
        cls.content = []
        if _len > _w:
            while idx + _w < _len:
                cls.content.append(cls.content_orignal[idx:idx + _w])
                idx += _w
        cls.content.append(cls.content_orignal[idx:])
        cls.h = len(cls.content) + 2
        cls.y = round(h / 2) - round(cls.h / 2)

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        cls.box_content = ''
        for idx, line in enumerate(cls.content):

            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line}'
                cls.box_content += _line
                start_y += 1
        cls.box_content += cls.process_symbol[cls.count % 4]
        cls.count += 1

    @classmethod
    def destroy(cls):
        pass


class InputBox(Box):
    pass


class ConfirmBox(Box):
    pass


class HelpBox(Box):
    pass
