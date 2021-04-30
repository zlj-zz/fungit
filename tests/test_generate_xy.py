import sys


sys.path.insert(0, ".")

from fungit.gui.box.git_box import GIT_BOXES
from fungit.gui.box_option import generate_git_box_w_h, generate_all_box


def test_generate_xywh():

    generate_git_box_w_h()
    for sub in GIT_BOXES:
        print(sub.x, sub.y, sub.w, sub.h)
    print(GIT_BOXES)


def test_first_render():

    generate_all_box()


if __name__ == "__main__":
    test_first_render()
    pass
