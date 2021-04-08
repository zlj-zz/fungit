from .style import Color


class Theme:
    DEFAULT = Color.fg('#ee')
    BOX_SELECTED_COLOR = Color.fg('#FFB6C1')

    FILE_NEW = Color.fg('#87CEFA')
    FILE_UNTRACK = Color.fg('#F08080')

    FILE_CACHED = Color.fg('#98FB98')
    FILE_RENAME = Color.fg('#98FB98')
    FILE_DELED = Color.fg('#98FB98')

    FILE_DEL = Color.fg('#9370DB')
    FILE_CHANGE = Color.fg('#9370DB')

    BRANCH = Color.fg('#87CEFA')
    BRANCH_STATUS = Color.fg('#F0E68C')

    PUSHED = Color.fg('#F0E68C')
    UNPUSHED = Color.fg('#F08080')
