import subprocess
import sys
import os
import re
from typing import List

from .module.file import File
from .module.branch import Branch
from .module.commit import Commit

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


def current_head():
    return _git('symbolic-ref -q --short HEAD').strip()


def state() -> list:
    '''Get current project name and head branch.'''

    path = _git('rev-parse --git-dir').strip()
    if path == '.git':
        project = os.getcwd().split('/')[-1]
    else:
        project = path.split('/')[-2]

    _head = current_head()
    return [project, _head]


def load_files(*args) -> List[List]:
    '''Get all file status.

    Args:
        args: File tuple
    '''

    command = 'status -s -u'
    resp = _git(' '.join([command, *args])).rstrip()

    files_ = []
    if resp:
        lines_ = resp.split('\n')
        for line_ in lines_:
            # _status.append((item[:2], item[3:]))
            change = line_[:2]
            staged_change = line_[:1]
            unstaged_change = line_[1:2]
            name = line_[3:]
            untracked = change in ['??', 'A ', 'AM']
            has_no_staged_change = staged_change in [' ', 'U', '?']
            has_merged_conflicts = change in [
                'DD', 'AA', 'UU', 'AU', 'UA', 'UD', 'DU']
            has_inline_merged_conflicts = change in ['UU', 'AA']

            file_ = File(name=name,
                         display_str=line_,
                         short_status=change,
                         has_staged_change=not has_no_staged_change,
                         has_unstaged_change=unstaged_change != ' ',
                         tracked=not untracked,
                         deleted=unstaged_change == 'D' or staged_change == 'D',
                         added=unstaged_change == 'A' or untracked,
                         has_merged_conflicts=has_merged_conflicts,
                         has_inline_merged_conflicts=has_inline_merged_conflicts)
            files_.append(file_)

    return files_


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


def load_branches() -> List[Branch]:
    command = 'for-each-ref --sort=-committerdate --format="%(HEAD)|%(refname:short)|%(upstream:short)|%(upstream:track)" refs/heads'
    resp = _git(command).strip()

    if not resp:
        return []

    branchs = []
    lines = resp.split('\n')

    for line in lines:
        items = line.split('|')
        branch = Branch(name=items[1],
                        pushables='?',
                        pullables='?',
                        is_head=items[0] == '*')

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


def branch_log(branch: Branch) -> str:
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


def get_first_pushed_commit(branch_name: str):
    command = 'merge-base %s %s@{u}' % (branch_name, branch_name)
    resp = _git(command).strip()
    return resp


def get_log(branch_name: str, limit: bool = False, filter_path: str = ''):
    limit_flag = '-300' if limit else ''
    filter_flag = f'--follow -- {filter_path}' if filter_path else ''
    command = f'log {branch_name} --oneline --pretty=format:"%H|%at|%aN|%d|%p|%s" {limit_flag} --abbrev=20 --date=unix {filter_flag}'
    resp = _git(command).strip()
    return resp


def load_commits(branch_name: str):
    '''Return given branch all commits.'''

    passed_first_pushed_commit = False
    first_pushed_commit = get_first_pushed_commit(branch_name)

    if not first_pushed_commit:
        passed_first_pushed_commit = True

    commits = []
    lines = get_log(branch_name).split('\n')
    for line in lines:
        split_ = line.split('|')

        sha = split_[0]
        unix_timestamp = int(split_[1])
        author = split_[2]
        extra_info = (split_[3]).strip()
        parent_hashes = split_[4]
        message = '|'.join(split_[5:])

        tag = []
        if extra_info:
            _re = re.compile(r'tag: ([^,\\]+)')
            match = _re.search(extra_info)
            if match:
                tag.append(match[1])

        if sha == first_pushed_commit:
            passed_first_pushed_commit = True
        status = {True: "unpushed", False: "pushed"}[
            not passed_first_pushed_commit]

        commit_ = Commit(sha=sha,
                         msg=message,
                         author=author,
                         unix_timestamp=unix_timestamp,
                         status=status,
                         extra_info=extra_info,
                         tag=tag)
        commits.append(commit_)

    return commits


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
