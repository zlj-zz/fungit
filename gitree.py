import commands as git
from shared import SelectedType


def create_git_tree(tree: dict):
    tree['state'] = git.state()
    tree['status'] = git.status()
    tree['branchs'], tree['current_branch'] = git.branchs()
    tree['commits'] = git.commits()
    tree['stashs'] = git.stashs()
    tree['content'] = ''


def fetch_content(selected: SelectedType, *args):
    print(args)
    if selected & SelectedType.STATUS:
        if not args:
            return ''
        else:
            _state, _path = args[0]

            if _state == '??':  # is mean untrack
                return git.diff(_path, tracked=False)
            elif _state.startswith('M'):
                return git.diff(_path, cached=True)
            else:
                return git.diff(_path)
    elif selected & SelectedType.COMMIT:
        if not args:
            return ''
        else:
            _commit_id = args[0][0]
            return git.commit_info(_commit_id)
    elif selected & SelectedType.BRANCH:
        if not args:
            return ''
        else:
            _branch = args[0]
            return git.branch_log(_branch)
    elif selected & SelectedType.STASH:
        # TODO:
        return 'Dont support display.'
    elif selected & SelectedType.STATE:
        return git.INTRODUCE


if __name__ == '__main__':
    from pprint import pprint
    t = {}
    create_git_tree(t)
    pprint(t)
    pass
