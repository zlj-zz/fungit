import sys
import os

sys.path.append('.')

if __name__ == '__main__':

    from fungit.event.key import Key
    # from old_zgit.key import Key
    Key.start()
    while True:
        while Key.has_key():
            print(Key.get())
