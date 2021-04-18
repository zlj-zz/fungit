import logging

from .exec import run_with_git


LOG = logging.getLogger(__name__)

# ==========================================================
# File option.
# ==========================================================
def stage(*args) -> None:
    """Stage files."""

    command = "add --"
    run_with_git(" ".join([command, *args]))


def stage_all() -> None:
    """Stage all files."""

    run_with_git("add -A")


def unstage(*args, tracked: bool = True) -> None:
    """Unstage files."""

    if tracked:
        command = "reset HEAD --"
    else:
        command = "rm --cached --force --"

    run_with_git(" ".join([command, *args]))


def unstage_all() -> None:
    """Unstage all files."""

    run_with_git("reset")


def pull():
    run_with_git("pull")


def push(force: bool = False, safe: bool = True):
    command_force = ""
    if force:
        if safe:
            command_force = "--force-with-lease"
        else:
            command_force = "--force"

    command = " ".join(["push", command_force])
    run_with_git(command)


# ==========================================================
# Branch option.
# ==========================================================
def checkout(path: str):
    command = f"checkout {path}"
    err, resp = run_with_git(command)
    return err, resp
