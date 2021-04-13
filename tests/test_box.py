import sys

sys.path.insert(0, ".")

from fungit.gui.box.func_box import ConfirmBox
from fungit.event.key import Key


def test_confirm_box():

    Key.start()
    # ConfirmBox.main('', 'are you sure?')
    is_confirm = ConfirmBox.main(
        "confirm",
        "All the acquired data is produced as the class content that can be displayed, colored and cached in `cls.content`(Override by subclass).",
    )
    print(is_confirm)
    Key.stop()
    print(">>>>>>>>>")


if __name__ == "__main__":
    test_confirm_box()
    pass
