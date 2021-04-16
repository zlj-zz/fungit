import sys

sys.path.insert(0, ".")

from fungit.terminal_git.shell_complete import add_completion

if __name__ == "__main__":
    add_completion()
