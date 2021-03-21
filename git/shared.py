import enum
import subprocess

SET_SEQ = '\033[{}m'
REST_SEQ = '\033[0m'


class Color(enum.Enum):
    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    PURPEL = '35'
    SKYFBLUE = '36'
    WHITE = '37'


class Style(enum.Enum):
    BOLD = '1'
    UNDERLINE = '4'
    FLASH = '5'


def echo(msg: str, color: Color = None, style: Style = None, nl: bool = True):
    c = []
    if color:
        c.append(color.value)
    if style:
        c.append(style.value)

    SEQ = SET_SEQ.format(';'.join(c))

    print('{}{}{}'.format(SEQ, str(msg), REST_SEQ), end='\n' if nl else '')


def warn(msg: str):
    echo(msg, Color.YELLOW, Style.BOLD)


def run_shell(c: str):
    subprocess.Popen(c, shell=True)


def run_shell_with_resp(c: str):
    response = subprocess.check_output([c], shell=True).decode()
    return response
