from .key import Key
from fungit.gui.manage import Manager


def process_key():
    while Key.has_key():
        key = Key.get()

        if key == 'q':
            # from .quit import clean_quit
            # clean_quit()
            pass
        elif '1' <= key <= '5':
            Manager.switch_box_by_index(key)
        elif key == 'h' or key == 'left':
            Manager.prev_box()
        elif key == 'l' or key == 'right':
            Manager.next_box()
        elif key == 'j' or key == 'down':
            Manager.next_item()
        elif key == 'k' or key == 'up':
            Manager.prev_item()
        elif key == ' ':
            Manager.space_event()
        elif key == 'a':
            Manager.a_event()
        elif key == 'p':
            Manager.pull()
        elif key == 'P':
            Manager.push()
        else:
            continue
