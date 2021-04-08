import subprocess
import sys
import os
import re
from typing import List

from .module.branch import Branch

_GIT = 'git'


def _git(*args) -> str:
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


def state() -> list:
    '''Get current project name and head branch.'''

    path = _git('rev-parse --git-dir').strip()
    if path == '.git':
        project = os.getcwd().split('/')[-1]
    else:
        project = path.split('/')[-2]

    _head = _git('symbolic-ref', '-q', '--short', 'HEAD').strip()
    return [project, _head]


def status(*args) -> List[List]:
    '''Get all file status.

    Args:
        args: File tuple
    '''

    command = 'status -s -u'
    s = _git(' '.join([command, *args])).rstrip()

    _status = []
    if s:
        files = s.split('\n')
        for item in files:
            _status.append((item[:2], item[3:]))

    return _status


def stage(*args) -> None:
    '''Stage files.'''

    command = 'add --'
    s = _git(' '.join([command, *args])).rstrip()


def stage_all() -> None:
    '''Stage all files.'''

    _git('add -A')


def unstage(*args, tracked: bool = True) -> None:
    '''Unstage files.'''

    if tracked:
        command = 'reset HEAD --'
    else:
        command = 'rm --cached --force --'

    _git(' '.join([command, *args]))


def unstage_all() -> None:
    '''Unstage all files.'''

    _git('reset')


def branchs() -> List:
    '''Get all branchs and current branch, return a list.

    Returns:
        branch list
        example:
            [ ['* main', 'dev', 'test'], 'main']
    '''

    command = 'branch'
    b = _git(command).rstrip()

    brs = b.split('\n')

    res = []
    curr = ''
    for br in brs:
        res.append(br)
        if is_selected_branch(br):
            curr = br[2:]
    return [res, curr]


def load_branch() -> List[Branch]:
    command = 'for-each-ref --sort=-committerdate --format="%(HEAD)|%(refname:short)|%(upstream:short)|%(upstream:track)" refs/heads'
    resp = _git(command).strip()

    if not resp:
        return []

    branchs = []
    lines = resp.split('\n')

    for line in lines:
        items = line.split('|')
        branch = Branch(items[1], '?', '?', items[0] == '*')

        upstream_name = items[2]

        if not upstream_name:
            branchs.append(branch)
            continue

        branch.upstream_name = upstream_name

        track = items[3]
        _re = re.compile(r'ahead (\d+)')
        match = _re.search(track)
        if match:
            branch.pushables = str(match[1])
        else:
            branch.pushables = '0'

        _re = re.compile(r'behind (\d+)')
        match = _re.search(track)
        if match:
            branch.pullables = str(match[1])
        else:
            branch.pullables = '0'

        branchs.append(branch)

    return branchs


def branch_log(branch: str) -> str:
    '''Gets all logs of a given branch.

    Args:
        branch: branch name
    '''

    # if branch.startswith('* '):
    #     branch = branch[2:]
    branch_name = branch.name

    arg = 'log %s --graph --decorate' % branch_name
    resp = _git(arg).rstrip()
    return resp


def commits() -> List[List]:
    '''Return current branch all commits.'''

    res = _git('log', '--oneline').strip()
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
    resp = _git(arg).rstrip()
    return resp


def stashs() -> str:
    '''Get stash list.'''

    arg = 'stash list'
    resp = _git(arg)
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

    res = _git(*args).rstrip()
    return res


def is_selected_branch(branch: str) -> bool:
    '''Determine whether a branch is the current branch.'''

    return branch.startswith('* ')


def pull():

    _git('pull')


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
