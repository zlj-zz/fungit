
GIT_TREE = dict()

SELECTED = dict()

BOXS = {}


class SelectedType:
    STATE = 1
    STATUS = 1 << 1
    COMMIT = 1 << 2
    BRANCH = 1 << 3
    STASH = 1 << 4
    CONTENT = 1 << 5


def initial_selection():
    SELECTED['old_selected'] = 0
    SELECTED['selected'] = SelectedType.STATUS
    SELECTED['state'] = 0
    SELECTED['status'] = 0
    SELECTED['commit'] = 0
    SELECTED['branch'] = 0
    SELECTED['stash'] = 0
