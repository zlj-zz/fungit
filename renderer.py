import threading
import copy
from typing import Dict

from coordinate import create_git_tree, Selected
from shared import BOXS
from box import create_boxs


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
    strings: Dict[str, str] = {}
    z_order: Dict[str, int] = {}
    saved: Dict[str, str] = {}
    save: Dict[str, bool] = {}
    once: Dict[str, bool] = {}
    idle = threading.Event()
    idle.set()

    old_tree: Dict = dict()  # for diff
    _w: int = 0
    _h: int = 0

    @classmethod
    def render(cls, tree: dict, *args):
        w, h = args
        if w != cls._w or h != cls._h:
            cls._w, cls._h = w, h

        if not tree:
            Selected.initial()
            create_git_tree(tree)  # create tree

        if not cls.old_tree:
            # ... create box
            boxs = create_boxs(cls._w, cls._h)

            for key in BOXS.keys():
                box = BOXS[key]
                cls.now(box.box)
                cls.now(box.box_content)
        else:
            if Selected.old != Selected.current:
                for key in BOXS.keys():
                    box = BOXS[key]
                    if box.genre & Selected.old or box.genre & Selected.current:
                        box.create_profile()
                        box.update()
                    cls.now(box.box)
                Selected.old = Selected.current

            for key in BOXS.keys():
                box = BOXS[key]
                if Selected.change[box.genre]:
                    print(Selected.selected[box.genre])
                    box.update()
                    cls.now(box.box_content)
                    Selected.change[box.genre] = False

            _c = BOXS['content']
            _c.generate()
            _c.update()
            cls.now(_c.box_content)

            # do diff
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

    @classmethod
    def buffer(cls, name: str, *args: str, append: bool = False, now: bool = False, z: int = 100, only_save: bool = False, no_save: bool = False, once: bool = False):
        string: str = ""
        if name.startswith("+"):
            name = name.lstrip("+")
            append = True
        if name.endswith("!"):
            name = name.rstrip("!")
            now = True
        cls.save[name] = not no_save
        cls.once[name] = once
        if not name in cls.z_order or z != 100:
            cls.z_order[name] = z
        if args:
            string = "".join(args)
        if only_save:
            if name not in cls.saved or not append:
                cls.saved[name] = ""
            cls.saved[name] += string
        else:
            if name not in cls.strings or not append:
                cls.strings[name] = ""
            cls.strings[name] += string
            if now:
                cls.out(name)

    @classmethod
    def out(cls, *names: str, clear=False):
        out: str = ""
        if not cls.strings:
            return
        if names:
            for name in sorted(cls.z_order, key=cls.z_order.get, reverse=True):  # type: ignore
                if name in names and name in cls.strings:
                    out += cls.strings[name]
                    if cls.save[name]:
                        cls.saved[name] = cls.strings[name]
                    if clear or cls.once[name]:
                        cls.clear(name)
            cls.now(out)
        else:
            for name in sorted(cls.z_order, key=cls.z_order.get, reverse=True):  # type: ignore
                if name in cls.strings:
                    out += cls.strings[name]
                    if cls.save[name]:
                        cls.saved[name] = cls.strings[name]
                    if cls.once[name] and not clear:
                        cls.clear(name)
            if clear:
                cls.clear()
            cls.now(out)

    @classmethod
    def saved_buffer(cls) -> str:
        out: str = ""
        for name in sorted(cls.z_order, key=cls.z_order.get, reverse=True):  # type: ignore
            if name in cls.saved:
                out += cls.saved[name]
        return out

    @classmethod
    def clear(cls, *names, saved: bool = False):
        if names:
            for name in names:
                if name in cls.strings:
                    del cls.strings[name]
                if name in cls.save:
                    del cls.save[name]
                if name in cls.once:
                    del cls.once[name]
                if saved:
                    if name in cls.saved:
                        del cls.saved[name]
                    if name in cls.z_order:
                        del cls.z_order[name]
        else:
            cls.strings = {}
            cls.save = {}
            cls.once = {}
            if saved:
                cls.saved = {}
                cls.z_order = {}


if __name__ == '__main__':
    pass
