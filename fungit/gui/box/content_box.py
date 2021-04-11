import re
from typing import List, Any

from . import Box
from ..style import Cursor
from fungit.shared import GitType
import fungit.commands as git


class ContentBox(Box):
    name: str = 'content'
    genre = GitType.CONTENT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    content_orignal: Any = None
    content: List = []
    box: str = ''
    box_content: str = ''

    last_notifier: Box = None

    @classmethod
    def fetch_data(cls, c):
        cls.content_orignal = fetch_content(c)

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

    @classmethod
    def notify(cls, notifier: Box):
        if notifier is not cls.last_notifier:
            cls.create_profile()
            cls.last_notifier = notifier
        cls.fetch_data(notifier)
        cls.generate()
        cls.update()
        cls.render()
        pass


# _CACHED = re.compile(r'^[A-Z]\s$')


def fetch_content(c):
    selected = c.current

    if selected & GitType.STATUS:
        _status_list = c.raw
        if not _status_list:
            return ''
        else:
            file_ = _status_list[c.selected]

            if not file_.tracked:  # is mean untrack
                return git.diff(file_.name, tracked=False)
            elif file_.has_staged_change:
                return git.diff(file_.name, cached=True)
            else:
                return git.diff(file_.name)
    elif selected & GitType.COMMIT:
        args = c.raw
        if not args:
            return ''
        else:
            _commit_id = args[c.selected].sha
            return git.commit_info(_commit_id)
    elif selected & GitType.BRANCH:
        args = c.raw
        if not args:
            return ''
        else:
            _branch = args[c.selected]
            return git.branch_log(_branch)
    elif selected & GitType.STASH:
        # TODO:
        return 'Dont support display.'
    elif selected & GitType.STATE:
        return git.INTRODUCE
