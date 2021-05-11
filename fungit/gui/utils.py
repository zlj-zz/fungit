import re
import logging


LOG = logging.getLogger(__name__)

# yapf: disable
widths = [
    (126, 1), (159, 0), (687, 1), (710, 0), (711, 1), (727, 0),
    (733, 1), (879, 0), (1154, 1), (1161, 0), (4347, 1), (4447, 2),
    (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1), (9002, 2),
    (11021, 1), (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2),
    (19967, 1), (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2), (120831, 1),
    (262141, 2), (1114109, 1),
]
# yapf: enable


def get_width(r):
    global widths
    if r == 0xE or r == 0xF:
        return 0
    for num, wid in widths:
        if r <= num:
            return wid
    return 1


def wrap_color_str(line: str, columns: int):
    """Warp a colored line.

    Wrap a colored string according to the width of the restriction.

    Args:
        line: A colored string.
        line_width: Limit width.
    """
    line = re.sub(r"\x1b(?P<need>\[\d+;*\d*[suABCDf])", "\g<need>", line)
    # line = line.replace("\\", "\\\\")
    line_len = len(line)
    lines = []
    start = 0
    i = 0
    count = 0
    while i < line_len:
        if line[i] == "\x1b":
            i += 1
            while not line[i] in ["m"]:
                i += 1
        i += 1
        if i < line_len:
            count += get_width(ord(line[i]))
        else:
            count += 0
        if count + 1 >= columns - 1:
            i += 1
            lines.append(line[start:i])
            start = i
            count = 0
    if start < line_len:
        lines.append(line[start:])
    # LOG.debug(f"{lines}")
    return lines
