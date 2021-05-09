import time
import logging

from fungit.event.key import Key
from fungit.style import Cursor
from fungit.event.clean_quit import quit_app
from ..core import Win
from ..renderer import Renderer
from ..shared import ConfirmType
from ..theme import Theme


class ConfirmBox(Win):
    """Pop up class for confirmation.

    `enter`, `space`, `y`, `Y` is confirm.
    `escape` is cancel.
    """

    close: bool = False

    @classmethod
    def main(
        cls, title: str, prompt: str, status=ConfirmType.NORMAL, full: bool = False
    ):
        f_w, f_h = cls.t_w, cls.t_h

        # get box `x` and `(w)idth`
        if full:
            cls.x = 1
            cls.w = f_w
        else:
            cls.x = round(f_w / 4)
            cls.w = round(f_w / 2)

        line_len = cls.w - 2
        prompt = prompt.replace("\t", "")
        prompts = prompt.split("\n")

        # process prompt string.
        cls.content = []
        for line in prompts:
            prompt_len = len(line)
            idx: int = 0
            if prompt_len > line_len:
                while idx + line_len < prompt_len:
                    cls.content.append(line[idx : idx + line_len])
                    idx += line_len
            cls.content.append(line[idx:])

        # get box `y` and `(h)eigth`.
        if full:
            cls.h = f_h
            cls.y = 1
        else:
            cls.h = len(cls.content) + 2
            cls.y = round(f_h / 2) - round(cls.h / 2)

        # get color
        color = cls.status_color(status)

        # create box profile
        cls.box = cls.create_profile(
            cls.x, cls.y, cls.w, cls.h, title=title, line_color=color
        )

        # create the content in box.
        start_x = cls.x + 1
        start_y = cls.y + 1

        cls.box_content = ""
        for idx, line in enumerate(cls.content):

            if idx < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{color}{line}{Theme.DEFAULT}"
                cls.box_content += _line
                start_y += 1

        # render
        Renderer.now(cls.box, cls.box_content)

        # listen key
        is_confirm: bool = False
        Key.clear()
        while not cls.close:
            while Key.has_event():
                key = Key.get()

                if key == "q":
                    cls.close = True
                    quit_app()
                elif key in ["enter", "y", "Y", " "]:
                    cls.close = True
                    is_confirm = True
                    break
                elif key == "escape":  # escape
                    cls.close = True
                    break
                else:
                    continue
            time.sleep(0.1)

        Key.clear()
        cls.close = False
        return is_confirm

    @classmethod
    def status_color(cls, status):
        if status & ConfirmType.ERROR:
            return Theme.ERROR
        else:
            return ""
