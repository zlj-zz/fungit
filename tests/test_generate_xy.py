import sys


sys.path.insert(0, ".")

from fungit.gui.box.git_box import GIT_BOXS
from fungit.gui.box_option import update_git_box_w_h, initial_git_box


def test_generate_xywh():

    update_git_box_w_h()
    for sub in GIT_BOXS:
        print(sub.x, sub.y, sub.w, sub.h)
    print(GIT_BOXS)


def test_frist_render():

    initial_git_box()


if __name__ == "__main__":
    test_frist_render()
    pass
