import re

s = "[31m[4;54f───────────────────────────────────────── [11;54f───────────────────────────────────────── [5;54f│                                        │[6;54f│                                        │[7;54f│                                        │[8;54f│                                        │[9;54f│                                        │[10;54f│                                        │[4;54f┌[4;95f┐[11;54f└[11;95f┘[4;56f[[1mhelp menu[22m][11;34f[1m2 of 2[22m[0m[5;55f"


"中国"


def warp_color_str(line: str, line_width: int):
    """Warp a colored line.

    Wrap a colored string according to the width of the restriction.

    Args:
        line: A colored string.
        line_width: Limit width.
    """
    line_len = len(line)
    lines = []
    start = 0
    i = 0
    n = 0
    while i < line_len:

        if line[i] == "\x1b":
            i += 1
            while not line[i] in ["m", "f", "A", "B", "C", "D", "s", "u"]:
                i += 1
        i += 1
        n += 1
        if n == line_width - 1:
            i += 1
            lines.append(line[start:i])
            start = i
            n = 0
    if start < line_len:
        lines.append(line[start:])
    return lines


def _add111(matched):
    intStr = matched.group("number")  # 123
    print(intStr)
    intValue = int(intStr)
    addedValue = intValue + 111  # 234
    addedValueStr = str(addedValue)
    return addedValueStr


if __name__ == "__main__":
    # print(s)
    print("-" * 50)
    as_ = "aa123 aa434 aa aa483290"
    sr = re.sub(r"(?P<number>aa)\d+", "\g<number>", as_)
    print(sr)
    s = re.sub(r"\x1b(?P<need>\[[\d+;*\d*]+[ABCDf])", "\g<need>", s)

    for i in warp_color_str(s, 40):
        print(f"{len(i)}   {i}")
    ss = "────────────────────────────────────────"
    # print(len(ss))
