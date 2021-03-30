import math
import enum
from typing import List, Tuple, Any

from style import Symbol, Fx, Color, Cursor, ConfigColor
from shared import GIT_TREE, BOXS, SELECTED, SelectedType
from gitree import fetch_content

BOX_SELECTED_COLOR = Color.fg('#32cd32')


class BoxMode:
    NORMAL = 1
    MINI = 1 << 2
    LINE = 1 << 3
    ERROR = 1 << 4


global BOX_MODE
BOX_MODE = BoxMode.NORMAL


class Box:
    name: str
    genre: SelectedType
    t_w: int
    t_h: int
    x: int
    y: int
    w: int
    h: int
    content: Any
    box: str

    @classmethod
    def create_profile(cls):
        _line_color = BOX_SELECTED_COLOR if cls.genre & SELECTED['selected'] else ''
        cls.box = create_profile(
            cls.x, cls.y, cls.w, cls.h, cls.name, line_color=_line_color)


class GitTypeBox(Box):
    name: str
    t_w: int
    t_h: int
    x: int
    y: int
    w: int
    h: int
    content_orignal: Any
    content: List
    box: str
    box_content: str

    @classmethod
    def create_profile(cls):
        # print(cls.genre& SELECTED['selected'])
        _line_color = BOX_SELECTED_COLOR if cls.genre & SELECTED['selected'] else ''
        cls.box = create_profile(
            cls.x, cls.y, cls.w, cls.h, cls.name, line_color=_line_color)

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line if len(line) < line_w else line[:line_w]}'
                if cls.genre & SELECTED['selected'] and idx == SELECTED[cls.name]:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class StateBox(GitTypeBox):
    name: str = 'state'
    genre = SelectedType.STATE
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
        cls.content_orignal = GIT_TREE[cls.name]
        cls.content = [cls.content_orignal]


class StatusBox(GitTypeBox):
    name: str = 'status'
    genre = SelectedType.STATUS
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
        cls.content_orignal = GIT_TREE[cls.name]  # if no data, empty list

        _content = []
        for item in cls.content_orignal:
            _content.append(' '.join(item))
        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx < cls.h - 2:
                _c = cls.line_color(line[:2])

                _line = f'{Cursor.to(start_y, start_x)}{_c}{line if len(line) < line_w else line[:line_w]}{ConfigColor.default}'
                if cls.genre & SELECTED['selected'] and idx == SELECTED[cls.name]:
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
        elif flag == 'D ':
            color = ConfigColor.status_del
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
    genre = SelectedType.BRANCH
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
        cls.content_orignal = GIT_TREE[cls.name]  # if no data, empty list
        cls.content = cls.content_orignal

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        cls.box_content = ''
        for idx, line in enumerate(cls.content):
            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line if len(line) < line_w else line[:line_w]}'
                if cls.genre & SELECTED['selected'] and idx == SELECTED[cls.name]:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class CommitBox(GitTypeBox):
    name: str = 'commit'
    genre = SelectedType.COMMIT
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
        cls.content_orignal = GIT_TREE[cls.name]  # if no data, empty list

        _content = []
        for item in cls.content_orignal:
            _content.append(' '.join(item))
        cls.content = _content

    @classmethod
    def update(cls):
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2 - 9

        cls.box_content = ''
        for idx, line in enumerate(cls.content_orignal):
            _id, _msg = line
            _id = f'{ConfigColor.commit_id}{_id}'
            _msg = f'{ConfigColor.default}{_msg if len(_msg) < line_w else _msg[:line_w]}'

            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{_id} {_msg}'
                if cls.genre & SELECTED['selected'] and idx == SELECTED[cls.name]:
                    _line = f'{Fx.b}{_line}{Fx.ub}'
                cls.box_content += _line
                start_y += 1


class StashBox(GitTypeBox):
    name: str = 'stash'
    genre = SelectedType.STASH
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
        cls.content_orignal = GIT_TREE[cls.name]

        if cls.content_orignal:
            cls.content = cls.content_orignal.split('\n')
        else:
            cls.content = []


class ContentBox(Box):
    name: str = 'content'
    genre = SelectedType.CONTENT
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


def update_box_w_h(w: int, h: int):
    # set box mode
    global BOX_MODE
    _selected_type = SELECTED['selected']
    limit_w = math.floor(w / 3)

    if w < 90 or h < 8:
        BOX_MODE = BoxMode.ERROR
    elif h <= 20:
        BOX_MODE = BoxMode.LINE
        _old = None
        for sub in GitTypeBox.__subclasses__():
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
        BOX_MODE = BoxMode.MINI
        _old = None
        for sub in GitTypeBox.__subclasses__():
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
        BOX_MODE = BoxMode.NORMAL

        StateBox.x = 1
        StateBox.y = 1
        StateBox.w = limit_w
        StateBox.h = 3

        if _selected_type & SelectedType.STASH:
            _split_h, _less = divmod(h - 4, 4)
        else:
            _split_h, _less = divmod(h - 7, 3)

        StatusBox.x = 1
        StatusBox.y = StateBox.y + StateBox.h
        StatusBox.w = limit_w
        StatusBox.h = _split_h + (1 if _less > 0 else 0)

        BranchBox.x = 1
        BranchBox.y = StatusBox.y + StatusBox.h
        BranchBox.w = limit_w
        BranchBox.h = _split_h + (1 if _less > 2 else 0)

        CommitBox.x = 1
        CommitBox.y = BranchBox.y + BranchBox.h
        CommitBox.w = limit_w
        CommitBox.h = _split_h + (1 if _less > 1 else 0)

        StashBox.x = 1
        StashBox.y = CommitBox.y + CommitBox.h
        StashBox.w = limit_w
        if _selected_type & SelectedType.STASH:
            StashBox.h = _split_h
        else:
            StashBox.h = 3


def create_content_box(w, h):
    limit_w = math.floor(w / 3)

    ContentBox.x = limit_w + 1
    ContentBox.y = 1
    ContentBox.w = w - limit_w
    ContentBox.h = h - 1

    ContentBox.content_orignal = fetch_content()

    ContentBox.create_profile()
    ContentBox.generate()
    ContentBox.update()

    BOXS[ContentBox.name] = ContentBox


def create_boxs(w: int, h: int):
    update_box_w_h(w, h)  # generate profile w, h
    for sub in GitTypeBox.__subclasses__():
        sub.create_profile()  # generate profile
        sub.generate()  # process data
        sub.update()  # generate box content
        BOXS[sub.name] = sub
        # print(sub)
    create_content_box(w, h)


def create_profile(x: int = 0, y: int = 0, width: int = 0, height: int = 0, title: str = "", title2: str = "", line_color: Color = None, title_color: Color = None, fill: bool = True, box=None) -> str:
    '''Create a box from a box object or by given arguments'''
    # out: str = f'{Term.fg}{Term.bg}'
    out: str = f''
    num: int = 0
    if not line_color:
        line_color = ''
    if not title_color:
        title_color = ''

    # * Get values from box class if given
    if box:
        x = box.x
        y = box.y
        width = box.width
        height = box.height
        title = box.name
        num = box.num
    hlines: Tuple[int, int] = (y, y + height - 1)

    out += f'{line_color}'

    # * Renderer all horizontal lines
    for hpos in hlines:
        out += f'{Cursor.to(hpos, x)}{Symbol.h_line * (width - 1)}'

    # * Renderer all vertical lines and fill if enabled
    for hpos in range(hlines[0]+1, hlines[1]):
        out += f'{Cursor.to(hpos, x)}{Symbol.v_line}{Cursor.r(width-2)}{Symbol.v_line}'

    # * Renderer corners
    out += f'{Cursor.to(y, x)}{Symbol.left_up}\
	{Cursor.to(y, x + width - 1)}{Symbol.right_up}\
	{Cursor.to(y + height - 1, x)}{Symbol.left_down}\
	{Cursor.to(y + height - 1, x + width - 1)}{Symbol.right_down}'

    # * Renderer titles if enabled
    if title:
        numbered: str = ""
        out += f'{Cursor.to(y, x + 2)}{Symbol.title_left}{Fx.b}{numbered}{title_color}{title}{Fx.ub}{line_color}{Symbol.title_right}'
    if title2:
        out += f'{Cursor.to(hlines[1], x + 2)}{Symbol.title_left}{title_color}{Fx.b}{title2}{Fx.ub}{line_color}{Symbol.title_right}'

    # return f'{out}{Term.fg}{Cursor.to(y + 1, x + 1)}'
    return f'{out}{Fx.reset}'


if __name__ == '__main__':
    import os
    import time
    from pprint import pprint
    from gitree import create_git_tree

    t = {}
    create_git_tree(t)
    w = os.get_terminal_size().columns
    h = os.get_terminal_size().lines

    from term import Term
    from renderer import Renderer
    Term.width = os.get_terminal_size().columns
    Term.height = os.get_terminal_size().lines

    Renderer.now(Term.alt_screen, Term.clear, Term.hide_cursor,
                 Term.mouse_on, Term.title("ZGit"))

    create_boxs(t, w, h)
    # print(sub.x, sub.y, sub.w, sub.h)
    from key import Key
    Key.start()

    while True:
        for sub in GitTypeBox.__subclasses__():
            print(sub.box)
        while Key.has_key():
            print(Key.get())

        time.sleep(.2)


'''
{'branch': ['* main', 'test'],
 'commit': [['7a26c2a', 'fix: zsh complete template'],
             ['14cb2e5', 'init']],
 'content': 'diff --git a/git/shared.py b/git/shared.py\n'
            'index 541c111..82ebe09 100644\n'
            '--- a/git/shared.py\n'
            '+++ b/git/shared.py\n'
            '@@ -60,5 +60,5 @@ def run_shell_with_resp(c: str):\n'
            '         response = subprocess.check_output([c], '
            'shell=True).decode()\n'
            '         return response\n'
            '     except Exception as e:\n'
            "-        err('An error occurred in the trigger "
            "operation(run_shell_with_resp).')\n"
            '-        exit(1)\n'
            "+        err('An error occurred in the trigger "
            "operation(run_shell).')\n"
            "+        return ''",
 'current_branch': 'main',
 'stash': '',
 'state': 'main',
 'status': [['M', 'git/shared.py'],
            ['D', 'urwid_test.py'],
            ['??', 'zgit.py']]}
'''
