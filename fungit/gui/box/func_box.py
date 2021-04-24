import os
import time
import logging

from fungit.event.key import Key
from fungit.style import Cursor, Symbol
from fungit.event.clean_quit import quit_app
from ..utils import create_profile
from ..renderer import Renderer
from ..shared import ConfirmType
from ..theme import Theme
from . import Box


LOG = logging.getLogger(__name__)


class DynamicPromptBox(Box):

    close: bool = False
    count = 0
    process_symbol = [Symbol.graph_down[key] for key in Symbol.graph_down.keys()]

    @classmethod
    def main(cls, title, prompt):
        f_w, f_h = os.get_terminal_size()

        cls.x = round(f_w / 4)
        cls.w = round(f_w / 2)
        _w = cls.w - 2
        _len = len(prompt)
        idx = 0
        cls.content = []
        if _len > _w:
            while idx + _w < _len:
                cls.content.append(prompt[idx : idx + _w])
                idx += _w
        cls.content.append(prompt[idx:])
        cls.h = len(cls.content) + 2
        cls.y = round(f_h / 2) - round(cls.h / 2)

        cls.box = create_profile(cls.x, cls.y, cls.w, cls.h, title=title)
        Renderer.now(cls.box)

        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        box_content = ""
        for idx, line in enumerate(cls.content):

            if idx < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{line}"
                box_content += _line
                start_y += 1

        # cls.box_content += cls.process_symbol[cls.count % 4]
        # cls.count += 1
        cls.box_content = (
            box_content + cls.process_symbol[cls.count % len(cls.process_symbol)]
        )
        start_time = time.time()
        while not cls.close:
            if time.time() - start_time > 0.2:
                cls.count += 1
                cls.box_content = (
                    box_content
                    + cls.process_symbol[cls.count % len(cls.process_symbol)]
                )
                start_time = time.time()
            # cls.render()
            Renderer.now(cls.box_content)

            while Key.has_event():
                key = Key.get()

                if key == "q":
                    pass
                elif key == "scape":
                    cls.close = True
                    break
                else:
                    continue

        cls.close = False
        cls.count = 0


class ConfirmBox:
    close: bool = False

    @classmethod
    def main(
        cls, title: str, prompt: str, status=ConfirmType.NORMAL, full: bool = False
    ):
        f_w, f_h = os.get_terminal_size()

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

        LOG.debug(prompts)

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
        cls.box = create_profile(
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
                LOG.debug(key)

                if key == "q":
                    cls.close = True
                    quit_app()
                elif key in ["enter", "y", "Y", " "]:
                    cls.close = True
                    is_confirm = True
                    break
                elif key == "scape":  # escape
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


class InputBox:
    pass
