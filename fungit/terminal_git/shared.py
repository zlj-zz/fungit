import enum
import subprocess

from fungit.style import Color, Fx


class CommandColor:
    RED = Color.fg("#FF6347")  # Tomato
    GREEN = Color.fg("#98FB98")  # PaleGreen
    YELLOW = Color.fg("#FFD700")  # Gold


def echo(msg: str, color="", style="", nl: bool = True):
    print(f"{style}{color}{msg}{Fx.reset}", end="\n" if nl else "")


def okay(msg: str):
    echo(f"{Fx.b}{CommandColor.GREEN}{msg}{Fx.reset}")


def warn(msg: str):
    echo(f"{Fx.b}{CommandColor.YELLOW}{msg}{Fx.reset}")


def err(msg: str):
    echo(f"{Fx.b}{CommandColor.RED}{msg}{Fx.reset}")


def run_shell(c: str):
    try:
        with subprocess.Popen(c, shell=True) as proc:
            proc.wait()
    except Exception as e:
        err("An error occurred in the trigger operation(run_shell).")
        exit(1)


def run_shell_with_resp(c: str):
    try:
        response = subprocess.check_output([c], shell=True).decode()
        return response
    except Exception as e:
        err("An error occurred in the trigger operation(run_shell_with_resp).")
        exit(1)
