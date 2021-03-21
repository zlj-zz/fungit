import time, math
import curses
from curses import wrapper


class GitFile():

    def __init__(self) -> None:
        self.name = ""
        self.state = ""
        self.context = ""


class GitOptions():
    pass


class Layout():
    h_line = '-'
    v_line = '|'


class Win():

    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.curs_set(0) # 设置光标不可见
        self.max_y, self.max_x = self.stdscr.getmaxyx()   # 60, 180
        self.max_y -= 1

        # 三等分大小
        self.h_split = math.floor(self.max_x / 3)
        self.v_split = math.floor(self.max_y / 3)

        # 侧边框
        self.side_start = 1
        self.side_end = self.h_split - 1   # 59
        self.side_width = self.side_end - self.side_start   # 58

        # 主框
        self.main_start = self.side_end + 2   # 61
        self.main_end = self.max_x - 1   # 179
        self.main_width = self.main_end - self.main_start   # 118

        self.init_window()

    def init_window(self):
        # 画出主框轮廓
        self.stdscr.addstr(0, self.side_start, Layout.h_line * self.side_width)
        self.stdscr.addstr(0, self.main_start, Layout.h_line * self.main_width)
        self.stdscr.addstr(self.max_y, self.side_start,
                           Layout.h_line * self.side_width)
        self.stdscr.addstr(self.max_y, self.main_start,
                           Layout.h_line * self.main_width)
        for i in range(1, self.max_y):
            self.stdscr.addstr(i, self.side_start, Layout.v_line)
            self.stdscr.addstr(i, self.side_end, Layout.v_line)
            self.stdscr.addstr(i, self.main_start, Layout.v_line)
            self.stdscr.addstr(i, self.main_end, Layout.v_line)
        self.stdscr.refresh()

    def exit(self):
        curses.endwin()


if __name__ == "__main__":
    win = Win()
    time.sleep(3)
    win.exit()
