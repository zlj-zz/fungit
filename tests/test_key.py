import sys

sys.path.insert(0, ".")

from fungit.event.key import Key

if __name__ == "__main__":

    Key.start()
    while True:
        while Key.has_event():
            print(Key.get())
