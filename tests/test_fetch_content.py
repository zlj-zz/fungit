import sys

sys.path.insert(0, ".")

from fungit.gui.box.content_box import fetch_content
from fungit.gui.box.navigation_box import NavBox
from fungit.gui.box.git_box import StatusBox, BranchBox
from fungit.gui.shared import BoxType

if __name__ == "__main__":

    NavBox.current = BoxType.BRANCH
    BranchBox.fetch_data()
    BranchBox.selected = 1

    print(fetch_content(BranchBox))
