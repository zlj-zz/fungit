import time
import logging
import threading
from typing import Callable

from fungit.event.key import Key
from fungit.style import Cursor, Symbol
from fungit.event.clean_quit import quit_app
from ..renderer import Renderer
from ..core import Win


LOG = logging.getLogger(__name__)


class DynamicPromptBox(Win):

    close: bool = False
    finish: bool = False
    process_symbol = [Symbol.graph_down[key] for key in Symbol.graph_down.keys()]
    display_t: threading.Thread
    do_t: threading.Thread

    @classmethod
    def main(
        cls,
        prompt: str,
        func: Callable,
        func_args: list = list(),
        func_kwargs: dict = dict(),
        title: str = "",
    ):
        f_w, f_h = cls.t_w, cls.t_h

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

        cls.box = cls.create_profile(cls.x, cls.y, cls.w, cls.h, title=title)
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
        cls.box_content = box_content

        cls.display()
        cls.do(func, func_args, func_kwargs)
        # TODO: need improve

        Key.clear()
        while not cls.close and not cls.finish:
            # print(cls.finish)

            while Key.has_event():
                key = Key.get()

                if key == "q":
                    cls.clean()
                    quit_app()
                elif key == "escape":
                    cls.close = True
                    break
                else:
                    continue

        cls.clean()
        cls.close = False
        cls.finish = False

    @classmethod
    def display(cls):
        def _display():
            count = 0
            while not cls.close and not cls.finish:
                p_flag = cls.process_symbol[count % len(cls.process_symbol)]
                Renderer.now(cls.box_content, p_flag)
                count += 1
                time.sleep(0.1)

        cls.display_t = threading.Thread(target=_display, daemon=True)
        cls.display_t.start()

    @classmethod
    def do(cls, func: Callable, func_args: list, func_kwargs: dict):
        def _do():
            func(*func_args, **func_kwargs)
            cls.finish = True
            LOG.debug("do_ finish")

        cls.do_t = threading.Thread(target=_do, daemon=True)
        cls.do_t.start()

    @classmethod
    def clean(cls):
        if cls.do_t.is_alive():
            cls.do_t.join()
        if cls.display_t.is_alive():
            cls.display_t.join()


class InputBox:
    pass
