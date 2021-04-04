BOXS = {}


class GitType:
    STATE = 1
    STATUS = 1 << 1
    COMMIT = 1 << 2
    BRANCH = 1 << 3
    STASH = 1 << 4
    CONTENT = 1 << 5
