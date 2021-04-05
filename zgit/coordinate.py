import re
from typing import Dict, List

import zgit.commands as git
from .shared import GitType


class Git():
    tree: dict = {}

    @classmethod
    def initial(cls):
        cls.update_state()
        cls.update_status()
        cls.update_branch()
        cls.update_commit()
        cls.update_stash()
        cls.tree[GitType.CONTENT] = ''

    @classmethod
    def update_state(cls):
        cls.tree[GitType.STATE] = git.state()

    @classmethod
    def update_status(cls):
        cls.tree[GitType.STATUS] = git.status()

    @classmethod
    def update_branch(cls):
        cls.tree[GitType.BRANCH], cls.tree['current_branch'] = git.branchs()

    @classmethod
    def update_commit(cls):
        cls.tree[GitType.COMMIT] = git.commits()

    @classmethod
    def update_stash(cls):
        cls.tree[GitType.STASH] = git.stashs()


class Selected(GitType):
    selects: List = []
    selects_len: int = 0

    selected: Dict = {}

    @classmethod
    def initial(cls) -> None:
        cls.selected['old_selected'] = 0
        cls.selected['selected'] = cls.STATUS
        cls.selected[cls.STATE] = 0
        cls.selected[cls.STATUS] = 0
        cls.selected[cls.BRANCH] = 0
        cls.selected[cls.COMMIT] = 0
        cls.selected[cls.CONTENT] = 0

        cls.selects = [cls.STATE, cls.STATUS,
                       cls.BRANCH, cls.COMMIT, cls.STASH]

        cls.selects_len = 5

        cls.change = {}
        for i in cls.selects:  # Mark whether a category has changed
            cls.change[i] = False

        cls.change[cls.CONTENT] = False

    @classmethod
    @property
    def old(cls):
        return cls.selected['old_selected']

    @classmethod
    @property
    def current(cls):
        return cls.selected['selected']

    @classmethod
    def switch_to_prev(cls):
        cls.old = cls.current

        old_index = cls.selects.index(cls.current)
        new_index = cls.selects_len - 1 - \
            (cls.selects_len - old_index) % cls.selects_len
        cls.current = cls.selects[new_index]

    @classmethod
    def switch_to_next(cls):
        cls.old = cls.current

        old_index = cls.selects.index(cls.current)
        new_index = (old_index + 1) % cls.selects_len
        cls.current = cls.selects[new_index]

    @classmethod
    def switch_by_index(cls, index):
        cls.old = cls.current

        _index = int(index) - 1
        cls.current = cls.selects[_index]

    @classmethod
    @property
    def state(cls):
        return 0

    @classmethod
    @property
    def status(cls):
        return cls.selected[cls.STATUS]

    @classmethod
    @property
    def branch(cls):
        return cls.selected[cls.BRANCH]

    @classmethod
    @property
    def commit(cls):
        return cls.selected[cls.COMMIT]

    @classmethod
    @property
    def content(cls):
        return cls.selected[cls.CONTENT]

    @classmethod
    def next_item(cls):
        _max_idx = len(Git.tree[cls.current]) - 1
        if cls.selected[cls.current] < _max_idx:
            cls.selected[cls.current] += 1

        cls.change[cls.current] = True

    @classmethod
    def prev_item(cls):
        if cls.selected[cls.current] > 0:
            cls.selected[cls.current] -= 1

        cls.change[cls.current] = True

    @classmethod
    def switch_status(cls):
        _status, _file = Git.tree[cls.STATUS][cls.selected[cls.STATUS]]
        if _CACHED.match(_status):
            git.unstage(_file)
        else:
            git.stage(_file)
        Git.update_status()

        cls.change[cls.current] = True

    @classmethod
    def switch_all(cls):
        for _status, _ in Git.tree[cls.STATUS]:
            if not _CACHED.match(_status):
                git.stage_all()
                break
        else:
            git.unstage_all()
        Git.update_status()

        cls.change[cls.current] = True


_CACHED = re.compile(r'^[A-Z]\s$')


def fetch_content():
    selected = Selected.current

    if selected & Selected.STATUS:
        args = Git.tree[GitType.STATUS]
        if not args:
            return ''
        else:
            _state, _path = args[Selected.status]

            if _state == '??':  # is mean untrack
                return git.diff(_path, tracked=False)
            elif _CACHED.match(_state):
                return git.diff(_path, cached=True)
            else:
                return git.diff(_path)
    elif selected & Selected.COMMIT:
        args = Git.tree[GitType.COMMIT]
        if not args:
            return ''
        else:
            _commit_id = args[Selected.commit][0]
            return git.commit_info(_commit_id)
    elif selected & Selected.BRANCH:
        args = Git.tree[GitType.BRANCH]
        if not args:
            return ''
        else:
            _branch = args[Selected.branch]
            return git.branch_log(_branch)
    elif selected & Selected.STASH:
        # TODO:
        return 'Dont support display.'
    elif selected & Selected.STATE:
        return git.INTRODUCE


if __name__ == '__main__':
    from pprint import pprint
    Git.initial()
    pprint(Git.tree)
    pass
