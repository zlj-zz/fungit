import subprocess
import re
from typing import List

_GIT = 'git'


def __git(*args) -> str:
    '''Execute a git command and return the result.

    Args:
        args: Command parameter tuple

    Returns:
        Execution result, string text
    '''

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
    '''Get current status.'''

    res = __git('symbolic-ref', '-q', '--short', 'HEAD').strip()
    return res


def status(*args) -> List[List]:
    '''Get all file status.

    Args:
        args: File tuple
    '''

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


def stage(*args) -> None:
    '''Stage files.'''

    command = 'add --'
    s = __git(' '.join([command, *args])).rstrip()


def stage_all() -> None:
    '''Stage all files.'''

    __git('add -A')


def unstage(*args, tracked: bool = True) -> None:
    '''Unstage files.'''

    if tracked:
        command = 'reset HEAD --'
    else:
        command = 'rm --cached --force --'

    __git(' '.join([command, *args]))


def unstage_all() -> None:
    '''Unstage all files.'''

    __git('reset')


def branchs() -> List:
    '''Get all branchs and current branch, return a list.

    Returns:
        branch list
        example:
            [ ['* main', 'dev', 'test'], 'main']
    '''

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
    '''Gets all logs of a given branch.

    Args:
        branch: branch name
    '''

    if branch.startswith('* '):
        branch = branch[2:]

    arg = 'log %s --graph --all --decorate' % branch
    resp = __git(arg).rstrip()
    return resp


def commits() -> List[List]:
    '''Return current branch all commits.'''

    res = __git('log', '--oneline').strip()
    return [[line[:7], line[8:]]for line in res.split('\n')]


def commit_info(commit: str) -> str:
    '''Gets the information for a given submission.

    Args:
        commit: commit id
    '''

    return commit_file_info(commit)


def commit_file_info(commit: str, file_name: str = '') -> str:
    '''Gets the change of a file in a given commit.

    Args:
        commit: commit id
        file_name: file name(include full path)
    '''

    arg = 'show %s %s' % (commit, file_name)
    resp = __git(arg).rstrip()
    return resp


def stashs() -> str:
    '''Get stash list.'''

    arg = 'stash list'
    resp = __git(arg)
    return resp


def diff(file: str, tracked: bool = True, cached: bool = False) -> str:
    '''Get the diff of given file.

    Args:
        file: file path
        tracked: Is the file tracked
        cached: Is the file staged
    '''

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
    '''Determine whether a branch is the current branch.'''

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
