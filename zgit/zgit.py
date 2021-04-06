from .key import Key, Timer, process_key
from .term import Term


def main():
    Term.init()
    Key.start()

    def run():
        while not False:
            Term.refresh()
            # Timer.stamp()

            # while Timer.not_zero():
            #     if Key.input_wait(Timer.left()):
            #         process_key()
            process_key()

    run()
    # try:
    # except Exception as e:
    #     # clean_quit(1)
    #     print(e)
    #     exit(1)


if __name__ == '__main__':
    main()
