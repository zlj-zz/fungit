from ..style.color import Color


class Theme:
    DEFAULT = Color.fg("#ee")
    BOX_SELECTED_COLOR = Color.fg("#87CEFA")  # skyblue

    FILE_NEW = Color.fg("#4682B4")  # SteelBlue
    FILE_UNTRACK = Color.fg("#F08080")  # LightCoral

    FILE_CACHED = Color.fg("#A3BD8C")  # green
    FILE_RENAME = Color.fg("#A3BD8C")
    FILE_DELED = Color.fg("#98FB98")

    FILE_DEL = Color.fg("#F08080")
    FILE_CHANGE = Color.fg("#F08080")

    BRANCH = Color.fg("#A3BD8C")
    BRANCH_STATUS = Color.fg("#F0E68C")  # Linen

    PUSHED = Color.fg("#F0E68C")
    UNPUSHED = Color.fg("#F08080")

    ADDITION = Color.fg("#A3BD8C")
    DELETION = Color.fg("#F08080")

    ERROR = Color.fg("#F08080")  # LightCoral
