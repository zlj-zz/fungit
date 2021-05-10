import threading
from typing import Dict

from fungit.event.key import Key


class Renderer:
    """Holds the draw buffer and manages IO blocking queue
    * .now(*args) : Prints all arguments as a string
    * .clear(*names) : Clear named buffers, all if no argument
    """

    idle = threading.Event()
    idle.set()

    old_tree: Dict = dict()  # for diff
    _w: int = 0
    _h: int = 0
    _is_changed: bool = False

    @classmethod
    def now(cls, *args):
        """Wait for input reader and self to be idle then print to screen"""
        Key.idle.wait()
        cls.idle.wait()
        cls.idle.clear()
        try:
            print(*args, sep="", end="", flush=True)
        except BlockingIOError:
            pass
            Key.idle.wait()
            print(*args, sep="", end="", flush=True)
        cls.idle.set()
