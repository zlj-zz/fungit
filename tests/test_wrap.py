from cgi import test
import sys
import re

sys.path.insert(0, ".")
from fungit.gui.utils import wrap_color_str


s = "[31m[4;54f───────────────────────────────────────── [11;54f───────────────────────────────────────── [5;54f│                                        │[6;54f│                                        │[7;54f│                                        │[8;54f│                                        │[9;54f│                                        │[10;54f│                                        │[4;54f┌[4;95f┐[11;54f└[11;95f┘[4;56f[[1mhelp menu[22m][11;34f[1m2 of 2[22m[0m[5;55f"


"中国"


def test_wrap():
    resp = wrap_color_str(s, 40)
    print(resp)


if __name__ == "__main__":
    # print(s)
    test_wrap()

    ss = "────────────────────────────────────────"
    # print(len(ss))
