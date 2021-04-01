from typing import Dict, List

import commands as git
from shared import GIT_TREE, GitType


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
        old_index = cls.selects.index(cls.current)
        new_index = cls.selects_len - 1 - \
            (cls.selects_len - old_index) % cls.selects_len
        cls.current = cls.selects[new_index]

    @classmethod
    def switch_to_next(cls):
        old_index = cls.selects.index(cls.current)
        new_index = (old_index + 1) % cls.selects_len
        cls.current = cls.selects[new_index]

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
        pass

    @classmethod
    def prev_item(cls):
        pass


def create_git_tree(tree: dict):
    tree[GitType.STATE] = git.state()
    tree[GitType.STATUS] = git.status()
    tree[GitType.BRANCH], tree['current_branch'] = git.branchs()
    tree[GitType.COMMIT] = git.commits()
    tree[GitType.STASH] = git.stashs()
    tree[GitType.CONTENT] = ''


def fetch_content():
    selected = Selected.current

    if selected & Selected.STATUS:
        args = GIT_TREE[GitType.STATUS]
        if not args:
            return ''
        else:
            _state, _path = args[Selected.status]

            if _state == '??':  # is mean untrack
                return git.diff(_path, tracked=False)
            elif _state.startswith('M'):
                return git.diff(_path, cached=True)
            else:
                return git.diff(_path)
    elif selected & Selected.COMMIT:
        args = GIT_TREE[GitType.COMMIT]
        if not args:
            return ''
        else:
            _commit_id = args[Selected.commit][0]
            return git.commit_info(_commit_id)
    elif selected & Selected.BRANCH:
        args = GIT_TREE[GitType.BRANCH]
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
    t = {}
    create_git_tree(t)
    pprint(t)
    pass
