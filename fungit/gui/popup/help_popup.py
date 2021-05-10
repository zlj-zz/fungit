import logging
from typing import Dict
import math

from ..core import Win
from fungit.style import Cursor, Symbol
from fungit.event.key import Key
from fungit.event.clean_quit import quit_app


LOG = logging.getLogger(__name__)


class HelperBox(Win):
    close: bool = False

    @classmethod
    def help(cls):
        help_dict: Dict[str, str] = {
            "(space)": "toggle file",
            "(p)": "pull",
            "(P)": "push",
            "(C)": "open editor for commit",
            "(d)": "delete",
            "(i)": "ignore current file",
        }
        help_len = len(help_dict)
        w = 40
        y = (cls.t_h) // 4
        x = (cls.t_w - w - 2) // 2
        h = (cls.t_h - y) // 2

        if help_len > h:
            pages = math.ceil(help_len / h)
        else:
            h = help_len
            pages = 0
        page = 1

        # print(x, y, w, h)
        cls.box = cls.create_profile(x, y, w + 2, h + 2, "help menu")
        cls.box_content: str = ""

        def update():
            out = ""
            cy = 0
            if pages:
                page_end = f"{page} of {pages}"
                cls.box = cls.create_profile(
                    x, y, w + 2, h + 2, "help menu", page_end=page_end
                )
                LOG.debug(cls.box)
            for n, (key, desc) in enumerate(help_dict.items()):
                if pages and n < (page - 1) * h:
                    continue
                out += f'{Cursor.to(y+1+cy, x+1)}{("" if key.startswith("_") else key):^10.10}{desc:30.30}'
                cy += 1
                if cy == h:
                    break
            if cy < h:
                for i in range(h - cy):
                    out += f'{Cursor.to(y+1+cy+i, x+1)}{" " * (w-2)}'

            cls.box_content = out
            cls.render()

        update()

        Key.clear()
        while not cls.close:
            while Key.has_event():
                key = Key.get()

                if key == "q":
                    quit_app()
                elif key in ["escape", " ", "enter"]:
                    cls.close = True
                    break
                elif key in ["j", "down"]:
                    if page < pages:
                        page += 1
                        update()
                elif key in ["k", "up"]:
                    if page > 1:
                        page -= 1
                        update()
                else:
                    try:
                        idx = int(key)
                        if 1 <= idx <= pages:
                            page = idx
                            update()
                    except Exception:
                        continue

        cls.close = False
