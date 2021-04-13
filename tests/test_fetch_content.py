import sys

sys.path.insert(0, ".")

from fungit.gui.box.content_box import fetch_content
from fungit.gui.box.navigation_box import NavBox
from fungit.gui.box.git_box import StatusBox, BranchBox
from fungit.shared import GitType

if __name__ == "__main__":

    NavBox.current = GitType.BRANCH
    BranchBox.fetch_data()
    BranchBox.selected = 1

    print(fetch_content(BranchBox))
