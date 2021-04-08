import sys
import os

sys.path.append('.')

if __name__ == '__main__':
    from fungit.commands.commands import _git, load_branch
    resp = load_branch()
    print(len(resp))
    for branch in resp:
        print(branch.name, branch.pushables,
              branch.pullables, branch.upstream_name, branch.is_head)
