from ..style.color import Color


class Theme:
    _skyblue = Color.fg("#87CEFA")  # skyblue
    _steel_blue = Color.fg("#4682B4")  # SteelBlue
    _light_coral = Color.fg("#F08080")  # LightCoral
    _green = Color.fg("#A3BD8C")  # green
    _linen = Color.fg("#F0E68C")  # Linen
    _gold = Color.fg("#FFD700")

    DEFAULT = Color.fg("#ff")
    BOX_SELECTED_COLOR = _skyblue

    FILE_NEW = _steel_blue
    FILE_UNTRACK = _light_coral

    FILE_CACHED = _green
    FILE_RENAME = _green
    FILE_DELED = _green

    FILE_DEL = _light_coral
    FILE_CHANGE = _light_coral

    BRANCH = _green
    BRANCH_STATUS = _linen

    PUSHED = _linen
    UNPUSHED = _light_coral

    ADDITION = _green
    DELETION = _light_coral

    ERROR = _light_coral
