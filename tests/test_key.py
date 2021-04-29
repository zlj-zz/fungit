import sys

sys.path.insert(0, ".")

from fungit.event.key import Key
from fungit.term import Term

if __name__ == "__main__":

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
                Term.clear()
                exit(0)
