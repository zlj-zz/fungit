
from typing import Dict


GIT_TREE = dict()

SELECTED = dict()

BOXS = {}


class Selected():
    STATE = 1
    STATUS = 1 << 1
    COMMIT = 1 << 2
    BRANCH = 1 << 3
    STASH = 1 << 4
    CONTENT = 1 << 5

    selects = []
    selects_len = 0

    selected: Dict = {}

    @classmethod
    def initial(cls):
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
