class Cursor:
    """Class with collection of cursor movement functions: .t[o](line, column) | .r[ight](columns) | .l[eft](columns) | .u[p](lines) | .d[own](lines) | .save() | .restore()"""

    @staticmethod
    def to(line: int, col: int) -> str:
        # * Move cursor to line, column
        return "\033[{};{}f".format(line, col)

    @staticmethod
    def right(dx: int) -> str:
        return "\033[{}C".format(dx)

    @staticmethod
    def left(dx: int) -> str:
        return "\033[{}D".format(dx)

    @staticmethod
    def up(dy: int) -> str:
        return "\033[{}A".format(dy)

    @staticmethod
    def down(dy: int) -> str:
        return "\033[{}B".format(dy)

    save: str = "\033[s"  # * Save cursor position
    restore: str = "\033[u"  # * Restore saved cursor postion
    t = to
    r = right
    l = left
    u = up
    d = down
