import time

from fungit.gui.core import Win
from fungit.gui.manage import Manager
from .key import Key
from .clean_quit import quit_app


def process_key():
    while Key.has_event():
        key = Key.get()

        if Win.no_space and key != "q":
            return

        if key in ["mouse_scroll_up", "mouse_scroll_down", "mouse_click"]:
            mouse_pos = Key.get_mouse()
            Manager.mouse_event(key, mouse_pos)

        elif key == "q":
            quit_app()
        elif "1" <= key <= "5":
            Manager.switch_box_by_index(key)
        elif key == "h" or key == "left":
            Manager.prev_box()
        elif key == "l" or key == "right":
            Manager.next_box()
        elif key == "j" or key == "down":
            Manager.next_item()
        elif key == "k" or key == "up":
            Manager.prev_item()
        elif key == " ":
            Manager.space_event()
        elif key == "a":
            Manager.a_event()
        elif key == "p":
            Manager.pull()
        elif key == "P":
            Manager.push()
        elif key == "C":
            Manager.commit()
        elif key == "d":
            Manager.del_()
        elif key == "i":
            Manager.i_event()
        elif key == "?":
            Manager.open_help_menu()
        else:
            continue
    time.sleep(0.1)
