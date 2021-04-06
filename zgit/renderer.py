import threading
import copy
from typing import Dict

from .shared import BOXS, GitActionStatus
from .box import create_boxs, TipBox


class Renderer:
    '''Holds the draw buffer and manages IO blocking queue
    * .buffer([+]name[!], *args, append=False, now=False, z=100) : Add *args to buffer
    * - Adding "+" prefix to name sets append to True and appends to name's current string
    * - Adding "!" suffix to name sets now to True and print name's current string
    * .out(clear=False) : Print all strings in buffer, clear=True clear all buffers after
    * .now(*args) : Prints all arguments as a string
    * .clear(*names) : Clear named buffers, all if no argument
    * .last_screen() : Prints all saved buffers
    '''
    idle = threading.Event()
    idle.set()

    old_tree: Dict = dict()  # for diff
    _w: int = 0
    _h: int = 0
    _is_changed: bool = False

    @classmethod
    def render(cls, *args):
        tree, Selected, w, h = args

        if w != cls._w or h != cls._h:
            cls._w, cls._h = w, h

        if not cls.old_tree or Selected.full or Selected.old != Selected.current:
            # ... create box
            create_boxs(cls._w, cls._h)

            for key in BOXS.keys():
                box = BOXS[key]
                cls.now(box.box)
                cls.now(box.box_content)

            Selected.full = False
            if Selected.old != Selected.current:
                Selected.old = Selected.current
        else:
            # if Selected.old != Selected.current:
            #     cls._is_changed = True

            #     for key in BOXS.keys():
            #         box = BOXS[key]
            #         if box.genre & Selected.old or box.genre & Selected.current:
            #             box.create_profile()
            #             box.update()
            #             cls.now(box.box, box.box_content)
            #     Selected.old = Selected.current

            for key in BOXS.keys():
                box = BOXS[key]
                if Selected.change[box.genre]:
                    cls._is_changed = True

                    box.create_profile()
                    box.generate()
                    box.update()
                    cls.now(box.box, box.box_content)
                    Selected.change[box.genre] = False

            if cls._is_changed:
                _c = BOXS['content']
                _c.generate()
                _c.update()
                cls.now(_c.box, _c.box_content)

                cls._is_changed = False

            # do diff
            pass

        # check state
        if Selected.action != GitActionStatus.NONE:
            if Selected.action == GitActionStatus.PULLING:
                TipBox.update()
                cls.now(TipBox.box, TipBox.box_content)
            pass

        cls.old_tree = copy.deepcopy(tree)  # cache tree

    @classmethod
    def now(cls, *args):
        '''Wait for input reader and self to be idle then print to screen'''
        cls.idle.wait()
        cls.idle.clear()
        try:
            print(*args, sep="", end="", flush=True)
        except BlockingIOError:
            pass
            print(*args, sep="", end="", flush=True)
        cls.idle.set()
