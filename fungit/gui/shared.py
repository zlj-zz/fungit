class BoxType:
    STATE = 1
    STATUS = 1 << 1
    BRANCH = 1 << 2
    COMMIT = 1 << 3
    STASH = 1 << 4
    CONTENT = 1 << 5
    NO_SPACE = 1 << 6
    Tip = 1 << 7
    Input = 1 << 8


class GitActionStatus:
    NONE = 1
    PULLING = 1 << 1


class ConfirmType:
    NORMAL = 1
    ERROR = 1 << 1
