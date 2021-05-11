import re
import logging


LOG = logging.getLogger(__name__)


def wrap_color_str(line: str, columns: int):
    """Warp a colored line.

    Wrap a colored string according to the width of the restriction.

    Args:
        line: A colored string.
        line_width: Limit width.
    """
    line = re.sub(r"\x1b(?P<need>\[[\d+;*\d*]+[suABCDf])", "\g<need>", line)
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
        count += 1
        if count >= columns - 1:
            i += 1
            lines.append(line[start:i])
            start = i
            count = 0
    if start < line_len:
        lines.append(line[start:])
    # LOG.debug(f"{lines}")
    return lines
