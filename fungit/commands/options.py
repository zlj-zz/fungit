import logging

from .exec import run_with_git, run_cmd


LOG = logging.getLogger(__name__)

# ==========================================================
# File option.
# ==========================================================
def stage(file_path: str) -> None:
    """Stage files."""

    command = "add --"
    if "->" in file_path:
        file_path = file_path.split("->")[-1].strip()

    run_with_git(" ".join([command, file_path]))


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


def pull() -> None:
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


def commit(message: str = ""):
    if message:
        pass
        return False
    else:
        run_cmd("git commit --verbose")
        return True


# ==========================================================
# Branch option.
# ==========================================================
def checkout(path: str):
    command = f"checkout {path}"
    err, resp = run_with_git(command)
    # LOG.debug(f"{err}|{resp}")
    return err, resp
