from typing import List, Any

from fungit.commands import info
from fungit.gui.theme import Theme
from fungit.style import Cursor, Fx
from ..shared import BoxType
from . import Box

ADDITION_FLAG = "+"
DELETION_FLAG = "-"


class ContentBox(Box):
    name: str = ""
    genre = BoxType.CONTENT
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    raw: Any = None
    content: List = []
    box: str = ""
    box_content: str = ""

    box_selected_idx: int = -1
    last_notifier: Box = None

    @classmethod
    def fetch_data(cls, c):
        cls.raw = fetch_content(c)

    @classmethod
    def generate(cls):

        _content = []
        for line in cls.raw.split("\n"):
            if len(line) < cls.w - 2:
                _content.append(line)
            else:
                _content.append(line[: cls.w - 2])
                _content.append(line[cls.w - 2 :])

        cls.content = _content

    @classmethod
    def update(self):
        start_y = self.y + 1
        start_x = self.x + 1

        self.box_content = ""
        count_ = 0
        for line in self.content:
            if isinstance(line, list):
                for sub_line in line:
                    if count_ < self.h - 2:
                        self.box_content += f"{Cursor.to(start_y, start_x)}{sub_line}"
                        start_y += 1
                        count_ += 1
                    else:
                        break
            else:
                if count_ < self.h - 2:
                    self.box_content += f"{Cursor.to(start_y, start_x)}{line}"
                    start_y += 1
                    count_ += 1

    @classmethod
    def notify(cls, notifier: Box):
        for sub in cls.__subclasses__():
            if notifier.genre & sub.genre:
                if not sub.box:
                    sub.create_profile()
                if sub.box_selected_idx or sub.box_selected_idx != notifier.selected:
                    sub.box_selected_idx = notifier.selected
                    sub.fetch_data(notifier)
                    sub.generate()
                sub.update()
                sub.render()
                break  # Finish the remaining cycle after the operation.

    @staticmethod
    def split_out_of_str(s: str, limit: int) -> list:
        idx = 0
        s_len = len(s)
        sub_lines = []
        while idx + limit < s_len:
            sub_lines.append(s[idx : idx + limit])
            idx += limit
        sub_lines.append(s[idx:])
        return sub_lines


# These subclasses will be called by the notify() method of the parent class
# to achieve the same type of content data for one layer cache. Subclasses
# override the generate() method of the parent class to color different types
# of content.
class StateContentBox(ContentBox):
    name: str = "Information"
    genre = BoxType.CONTENT | BoxType.STATE


class StatusContentBox(ContentBox):
    name: str = "File"
    genre = BoxType.CONTENT | BoxType.STATUS

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        _content = []
        lines_ = cls.raw.split("\n")

        if len(lines_) < 4:
            super().generate()
            return

        # First four line be bolded.
        for i in range(4):
            _content.append(f"{Fx.b}{lines_[i]}{Fx.ub}")

        if lines_[4].endswith("@@"):
            _content.append(f"{Theme.BOX_SELECTED_COLOR}{lines_[4]}{Theme.DEFAULT}")
        else:
            _content.append(lines_[4])

        for line in lines_[5:]:
            line_len = len(line)
            if line_len <= line_w:
                if line.startswith(ADDITION_FLAG):
                    line = f"{Theme.ADDITION}{line}{Theme.DEFAULT}"
                elif line.startswith(DELETION_FLAG):
                    line = f"{Theme.DELETION}{line}{Theme.DEFAULT}"
                _content.append(line)
            else:
                sub_lines = cls.split_out_of_str(line, line_w)
                if line.startswith(ADDITION_FLAG):
                    sub_lines[0] = Theme.ADDITION + sub_lines[0]
                    sub_lines[-1] = sub_lines[-1] + Theme.DEFAULT
                elif line.startswith(DELETION_FLAG):
                    sub_lines[0] = Theme.DELETION + sub_lines[0]
                    sub_lines[-1] = sub_lines[-1] + Theme.DEFAULT
                _content.append(sub_lines)

        cls.content = _content


class BranchContentBox(ContentBox):
    name: str = "Log"
    genre = BoxType.CONTENT | BoxType.BRANCH


class CommitContentBox(ContentBox):
    name: str = "Patch"
    genre = BoxType.CONTENT | BoxType.COMMIT

    @classmethod
    def generate(cls):
        line_w = cls.w - 2
        _content = []
        lines_ = cls.raw.split("\n")
        lines_len = len(lines_)

        _content.append(f"{Theme.PUSHED}{Fx.b}{lines_[0]}{Fx.ub}{Theme.DEFAULT}")

        if lines_len >= 3:
            for i in range(1, 3):
                _content.append(f"{Fx.b}{lines_[i]}{Fx.ub}")

        if lines_len > 3:
            for line in lines_[3:]:
                line_len = len(line)
                if line_len <= line_w:
                    if line.startswith(ADDITION_FLAG):
                        line = f"{Theme.ADDITION}{line}{Theme.DEFAULT}"
                    elif line.startswith(DELETION_FLAG):
                        line = f"{Theme.DELETION}{line}{Theme.DEFAULT}"
                    _content.append(line)
                else:
                    sub_lines = cls.split_out_of_str(line, line_w)
                    if line.startswith(ADDITION_FLAG):
                        sub_lines[0] = Theme.ADDITION + sub_lines[0]
                        sub_lines[-1] = sub_lines[-1] + Theme.DEFAULT
                    elif line.startswith(DELETION_FLAG):
                        sub_lines[0] = Theme.DELETION + sub_lines[0]
                        sub_lines[-1] = sub_lines[-1] + Theme.DEFAULT
                    _content.append(sub_lines)

        cls.content = _content


class StashContentBox(ContentBox):
    name: str = "Stash"
    genre = BoxType.CONTENT | BoxType.STASH


def fetch_content(c):
    selected = c.current

    if selected & BoxType.STATUS:
        _status_list = c.raw
        if not _status_list:
            return "No changed file."
        else:
            file_ = _status_list[c.selected]

            if not file_.tracked:  # is mean untrack
                return info.diff(file_.name, tracked=False)
            elif file_.has_staged_change:
                return info.diff(file_.name, cached=True)
            else:
                return info.diff(file_.name)
    elif selected & BoxType.COMMIT:
        args = c.raw
        if not args:
            return "No commits."
        else:
            _commit_id = args[c.selected].sha
            return info.commit_info(_commit_id)
    elif selected & BoxType.BRANCH:
        args = c.raw
        if not args:
            return "No local branches."
        else:
            _branch = args[c.selected]
            return info.branch_log(_branch)
    elif selected & BoxType.STASH:
        # TODO:
        return "Don't support display."
    elif selected & BoxType.STATE:
        return info.INTRODUCE


# _CACHED = re.compile(r'^[A-Z]\s$')
