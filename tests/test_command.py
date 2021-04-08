import sys
import os

sys.path.append('.')


def test_load_branches():
    from fungit.commands.commands import _git, load_branches
    resp = load_branches()
    print(len(resp))
    for branch in resp:
        print(branch.name, branch.pushables,
              branch.pullables, branch.upstream_name, branch.is_head)


def test_load_commits():
    from fungit.commands.commands import current_head, load_commits
    head = current_head()
    resp = load_commits(head)
    print(len(resp))
    for commit in resp:
        print(commit.sha, commit.msg, commit.author,
              commit.unix_timestamp, commit.status, commit.extra_info, commit.tag, commit.action)


if __name__ == '__main__':
    test_load_branches()
    pass
