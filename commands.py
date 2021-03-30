import subprocess
import re
from typing import List

_GIT = 'git'


def __git(*args) -> str:
    c = ' '.join([_GIT, *args])
    # print(c)
    try:
        with subprocess.Popen(
                [c], stdout=subprocess.PIPE, shell=True) as proc:
            return(proc.stdout.read().decode())
    except Exception as e:
        print(e)
        return ''


def state() -> str:
    res = __git('symbolic-ref', '-q', '--short', 'HEAD').strip()
    return res


def status(*args) -> List[List]:
    command = 'status -s'
    s = __git(' '.join([command, *args])).rstrip()

    _status = []
    if s:
        files = s.split('\n')
        for item in files:
            if item.endswith('/'):  # It's a directory
                _dir = item.split(' ')[1]
                fs = status(_dir)
                _status.extend(fs)
            else:
                _status.append((item[:2], item[3:]))

    return _status


def branchs() -> List[str]:
    command = 'branch'
    b = __git(command).rstrip()

    brs = b.split('\n')

    res = []
    curr = ''
    for br in brs:
        res.append(br)
        if is_selected_branch(br):
            curr = br[2:]
    return [res, curr]


def branch_log(branch: str) -> str:
    # 'command': 'git log --graph --all --decorate ',
    arg = 'log %s --graph --all --decorate' % branch
    resp = __git(arg).rstrip()
    return resp


def commits() -> List[List]:  # return current branch all commits.
    res = __git('log', '--oneline').strip()
    return [[line[:7], line[8:]]for line in res.split('\n')]


def commit_info(commit: str):
    return commit_file_info(commit)


def commit_file_info(commit: str, file_name: str = ''):
    arg = 'show %s %s' % (commit, file_name)
    resp = __git(arg).rstrip()
    return resp


def stashs() -> str:
    arg = 'stash list'
    resp = __git(arg)
    return resp


def diff(file: str, tracked: bool = True, cached: bool = False) -> str:
    args = ['diff', '--submodule', '--no-ext-diff']
    if cached:
        args.append('--cached')

    if not tracked:
        args.append('--no-index -- /dev/null')
    else:
        args.append('--')

    args.append(file)

    res = __git(*args).rstrip()
    return res


def is_selected_branch(branch: str) -> bool:
    return branch.startswith('* ')


# TODO: just temp introduce
INTRODUCE = '''\
A terminal tool, help you use git more simple. Support Linux and MacOS.
   
Usage: g <option> [<args>]

You can use `-h` and `--help` to get how to use pyzgit.
'''


if __name__ == '__main__':
    from pprint import pprint
    # pprint(status())
    # print(branchs())
    # print(state())
    # print(commits())
    # print(diff('style.py', tracked=False))
    pprint(diff('git/shared.py'))
    # print(diff('git/shared.py', cached=True))
    # print(branch_log('main'))
    # print(commit_file_info('1210f62', 'git/main.py'))
    # print(commit_info('1210f62'))
    pass
