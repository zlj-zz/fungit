import subprocess
import logging

LOG = logging.getLogger(__name__)

_GIT = "git"


def run_with_git(*args) -> tuple:
    """Execute a git command and return the result.

    Args:
        args: Command parameter tuple

    Returns:
        Execution result, string text
    """

    command = " ".join([_GIT, *args])
    LOG.debug(f"<run_with_git> {command}")
    try:
        with subprocess.Popen(
            [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        ) as proc:
            res = proc.stdout.read().decode()
            err = proc.stdout.read().decode()
            return err, res
    except Exception as e:
        LOG.warning(e)
        return e, ""


def run_cmd(*args):
    try:
        with subprocess.Popen(" ".join(args), shell=True) as proc:
            proc.wait()
    except Exception as e:
        LOG.warning(e)


def run_cmd_with_resp(*args) -> tuple:
    try:
        with subprocess.Popen(
            " ".join(args), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
        ) as proc:
            res = proc.stdout.read().decode()
            err = proc.stderr.read().decode()
            return err, res
    except Exception as e:
        LOG.warning(e)
        print(e)
        return e, ""
