import subprocess

_GIT = "git"


def run_with_git(*args) -> str:
    """Execute a git command and return the result.

    Args:
        args: Command parameter tuple

    Returns:
        Execution result, string text
    """

    c = " ".join([_GIT, *args])
    # print(c)
    try:
        with subprocess.Popen([c], stdout=subprocess.PIPE, shell=True) as proc:
            return proc.stdout.read().decode()
    except Exception as e:
        print(e)
        return ""


def run_cmd(*args) -> str:
    try:
        with subprocess.Popen(" ".join(args), shell=True) as proc:
            proc.wait()
    except Exception as e:
        print(e)
        return ""


def run_cmd_with_resp(*args) -> str:
    try:
        with subprocess.Popen(
            " ".join(args), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
        ) as proc:
            res = proc.stdout.read().decode()
            err = proc.stderr.read().decode()
            return err, res
    except Exception as e:
        print(e)
        return e, ""
