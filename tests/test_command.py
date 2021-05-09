import sys
import re

sys.path.insert(0, ".")

from fungit.commands.loading import (
    load_branches,
    current_head,
    load_commits,
    load_files,
    load_stashes,
)
from fungit.commands import run_with_git, run_cmd_with_resp


def test_load_branches():

    resp = load_branches()
    print(len(resp))
    for branch in resp:
        print(
            branch.name,
            branch.pushables,
            branch.pullables,
            branch.upstream_name,
            branch.is_head,
        )


def test_load_commits():

    head = current_head()
    resp = load_commits(head)
    print(len(resp))
    for commit in resp:
        print(
            commit.sha,
            commit.msg,
            # commit.author,
            # commit.unix_timestamp,
            # commit.status,
            # commit.extra_info,
            # commit.tag,
            # commit.action,
        )


def test_load_files():

    resp = load_files()
    for file in resp:
        # print(file.name, file.display_str, file.short_status, file.has_staged_change,
        #       file.has_unstaged_change, file.tracked, file.deleted, file.added,
        #       file.has_merged_conflicts, file.has_inline_merged_conflicts)
        print(
            file.name,
            file.tracked,
            file.has_staged_change,
            file.has_unstaged_change,
            file.added,
        )


def test_diff():
    from fungit.commands import diff

    re_1 = re.compile(r"(@@).*?(@@)")
    resp = diff("fungit/gui/box/navigation_box.py")
    rrr = re_1.sub(">>>>", resp)
    # print(resp)
    print(rrr)


def test_commit_info():
    from fungit.commands import commit_info

    resp = commit_info("HEAD")
    print(resp)


if __name__ == "__main__":
    # print(checkout("dev"))
    load_stashes()
    pass
