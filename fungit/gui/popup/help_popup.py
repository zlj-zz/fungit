from ..core import Win

key_map = {}
"""
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
        else:
            continue
    time.sleep(0.1)
"""


class Helper(Win):
    close: bool = False
