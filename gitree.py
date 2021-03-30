from select import select
import commands as git
from shared import SelectedType, GIT_TREE, SELECTED


def create_git_tree(tree: dict):
    tree['state'] = git.state()
    tree['status'] = git.status()
    tree['branch'], tree['current_branch'] = git.branchs()
    tree['commit'] = git.commits()
    tree['stash'] = git.stashs()
    tree['content'] = ''


def fetch_content():
    selected = SELECTED['selected']

    if selected & SelectedType.STATUS:
        args = GIT_TREE['status']
        if not args:
            return ''
        else:
            _state, _path = args[SELECTED['status']]

            if _state == '??':  # is mean untrack
                return git.diff(_path, tracked=False)
            elif _state.startswith('M'):
                return git.diff(_path, cached=True)
            else:
                return git.diff(_path)
    elif selected & SelectedType.COMMIT:
        args = GIT_TREE['commits']
        if not args:
            return ''
        else:
            _commit_id = args[SELECTED['commit']][0]
            return git.commit_info(_commit_id)
    elif selected & SelectedType.BRANCH:
        args = GIT_TREE['branchs']
        if not args:
            return ''
        else:
            _branch = args[SELECTED['branch']]
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
