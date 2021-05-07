import re
import logging


LOG = logging.getLogger(__name__)


def warp_color_str(line: str, line_width: int):
    """Warp a colored line.

    Wrap a colored string according to the width of the restriction.

    Args:
        line: A colored string.
        line_width: Limit width.
    """
    clear_ = re.sub(r"\x1b\[.*?m", "", line)  # ^[[...m
    clear_len = len(clear_)
    if clear_len <= line_width:
        return line
    flag_ = clear_[line_width - 1]
    # flag_ is a special char.
    if flag_ in ["(", ")", "[", "]", "{", "}", "*", "."]:
        flag_ = f"\{flag_}"
    for idx, sub in enumerate(re.finditer(flag_, clear_), start=1):
        if line_width - 1 == sub.start():
            break
    index_ = line.find(flag_, idx) + 1
    return [line[:index_], line[index_:]]
