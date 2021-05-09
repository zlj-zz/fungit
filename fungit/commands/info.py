import logging

from . import run_with_git


LOG = logging.getLogger(__name__)


def branch_log_graph(branch, plain: bool = False) -> str:
    """Gets all logs of a given branch.

    Args:
        branch: branch name
        plain: wether has color.
    """
    branch_name = branch.name
    color_str = "never" if plain else "always"

    arg = "log %s --graph --abbrev-commit --decorate --date=relative --pretty=medium --color=%s" % (
        branch_name,
        color_str,
    )
    _, resp = run_with_git(arg)
    return resp.rstrip()


def commit_info(commit: str, plain: bool = False) -> str:
    """Gets the information for a given submission.

    Args:
        commit: commit id.
        plain: wether has color.
    """
    return commit_file_info(commit, plain=plain)


def commit_file_info(commit: str, file_name: str = "", plain: bool = False) -> str:
    """Gets the change of a file in a given commit.

    Args:
        commit: commit id.
        file_name: file name(include full path).
        color: If with color.
        plain: wether has color.
    """
    color_str = "never" if plain else "always"

    arg = "show --color=%s %s %s" % (color_str, commit, file_name)
    _, resp = run_with_git(arg)
    return resp.rstrip()


def diff(
    file: str, tracked: bool = True, cached: bool = False, plain: bool = False
) -> str:
    """Get the diff of given file.

    Args:
        file: file path
        tracked: Is the file tracked
        cached: Is the file staged
        plain: wether has color.
    """
    args = ["diff", "--submodule", "--no-ext-diff"]

    if plain:
        args.append("--color=never")
    else:
        args.append("--color=always")

    if cached:
        args.append("--cached")

    if not tracked:
        args.append("--no-index -- /dev/null")
    else:
        args.append("--")

    if "->" in file:  # rename
        file = file.split("->")[-1].strip()

    args.append(file)

    _, res = run_with_git(*args)
    return res.rstrip()


def stash_info(index: int, plain: bool = False):
    """Show stash content.

    Args:
        index: stash index.
        plain: wether has color.
    """
    color = "never" if plain else "always"
    command_str = "stash show -p --stat --color=%s stash@\{%d\}" % (color, index)

    _, res = run_with_git(command_str)
    return res.rstrip()


def is_selected_branch(branch: str) -> bool:
    """Determine whether a branch is the current branch."""
    return branch.startswith("* ")


# TODO: just temp introduce
INTRODUCE = """\
  __                   _ _
 / _|_   _ _ __   __ _(_) |_
| |_| | | | '_ \ / _` | | __|
|  _| |_| | | | | (_| | | |_
|_|  \__,_|_| |_|\__, |_|\__|
                 |___/

A terminal tool, help you use git more simple. Support Linux and MacOS.
https://github.com/zlj-zz/fungit/

"""
