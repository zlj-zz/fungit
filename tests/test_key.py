from re import S
import sys
import signal

sys.path.insert(0, ".")

from fungit.event.key import Key
from fungit.term import Term


def signal_test(signum, frame):
    print(signum)
    print(frame)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_test)

    Term.init()
    Key.start()
    while True:
        while Key.has_event():
            key = Key.get()
            print(key)
            if key in ["mouse_scroll_up", "mouse_scroll_down", "mouse_click"]:
                mouse_pos = Key.get_mouse()
                print(mouse_pos)
            if key == "q":
                Key.stop()
                Term.clear()
                exit(0)
