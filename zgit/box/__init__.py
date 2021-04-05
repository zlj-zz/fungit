from zgit.shared import BOXS
from .box import *


def update_git_box_w_h(w: int, h: int):
    # set box mode
    global BOX_MODE
    _selected_type = Selected.current
    limit_w = math.floor(w / 3)

    if w < 90 or h < 8:
        pass
    elif h <= 20:
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
        StateBox.x = 1
        StateBox.y = 1
        StateBox.w = limit_w
        StateBox.h = 3

        if _selected_type & Selected.STASH:
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
        if _selected_type & Selected.STASH:
            StashBox.h = _split_h
        else:
            StashBox.h = 3


def create_content_box(w, h):
    limit_w = math.floor(w / 3)

    ContentBox.x = limit_w + 1
    ContentBox.y = 1
    ContentBox.w = w - limit_w
    ContentBox.h = h - 1

    ContentBox.create_profile()
    ContentBox.generate()
    ContentBox.update()

    BOXS[ContentBox.name] = ContentBox


def create_boxs(w: int, h: int):
    update_git_box_w_h(w, h)  # generate profile w, h
    for sub in GitTypeBox.__subclasses__():
        sub.create_profile()  # generate profile
        sub.generate()  # process data
        sub.update()  # generate box content
        BOXS[sub.name] = sub
        # print(sub)
    create_content_box(w, h)
