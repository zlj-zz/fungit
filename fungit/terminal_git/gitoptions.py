import re

from fungit.commands import run_cmd
from .shared import warn


class GitOptionState:
    NO = 0
    ONE = 1
    MULTI = 1 << 1
    INTERC = 1 << 2
    FUNC = 1 << 3
    STRING = 1 << 4


def add(args: list):
    if args:
        args_str = " ".join(args)
    else:
        args_str = " ."

    run_cmd("git add " + args_str)


def fetch_remote_branch(args: list):
    branch = args[0] if len(args) > 1 else None

    if branch:
        run_cmd(f"git fetch origin {branch}:{branch} ")
    else:
        warn("This option need a branch name.")


def set_email_and_username(args: list):
    __global = re.compile(r"\-\-global")
    res = []
    for i in args:
        r = __global.search(i)
        if r is not None:
            res.append(i)
    if res:
        other = " --global "
    else:
        other = " "

    name = input("Please input username:")
    run_cmd(GIT_OPTIONS["user"]["command"] + other + name)
    email = input("Please input email:")
    run_cmd(GIT_OPTIONS["email"]["command"] + other + email)


def process_func(c: str, args: list):
    fn = GIT_OPTIONS[c]["command"]
    fn(args)


def process_origin_command(c: str, args: list):
    origin_command = GIT_OPTIONS[c]["command"]

    if args:
        args_str = " ".join(args)
        command = " ".join([origin_command, args_str])
    else:
        command = origin_command

    warn(command)
    run_cmd(command)


def process(c: str, args: list = None):
    try:
        state = GIT_OPTIONS[c]["state"]
    except Exception:
        print("Don't support this command, please try ", end="")
        warn("g --show-commands")
        raise SystemExit(0)

    if state & GitOptionState.FUNC:
        process_func(c, args)
    elif state & GitOptionState.STRING:
        process_origin_command(c, args)


TYPES = [
    "Branch",
    "Commit",
    "Conflict",
    "Fetch",
    "Index",
    "Log",
    "Merge",
    "Push",
    "Remote",
    "Stash",
    "Tag",
    "Working tree",
    "Setting",
]

# Global command dictionary, including attributes:
#     command type,
#     complete command,
#     help information
GIT_OPTIONS = {
    # Branch
    "b": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git branch ",
        "help-msg": "lists, creates, renames, and deletes branches.",
    },
    "bc": {
        "state": GitOptionState.STRING | GitOptionState.ONE,
        "command": "git checkout -b ",
        "help-msg": "creates a new branch.",
    },
    "bl": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git branch -vv ",
        "help-msg": "lists branches and their commits.",
    },
    "bL": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git branch --all -vv ",
        "help-msg": "lists local and remote branches and their commits.",
    },
    "bs": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git show-branch ",
        "help-msg": "lists branches and their commits with ancestry graphs.",
    },
    "bS": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git show-branch --all ",
        "help-msg": "lists local and remote branches and their commits with ancestry graphs.",
    },
    "bm": {
        "state": GitOptionState.STRING | GitOptionState.ONE,
        "command": "git branch --move ",
        "help-msg": "renames a branch.",
    },
    "bM": {
        "state": GitOptionState.STRING | GitOptionState.ONE,
        "command": "git branch --move --force ",
        "help-msg": "renames a branch even if the new branch name already exists.",
    },
    # Commit
    "c": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git commit --verbose ",
        "help-msg": "records changes to the repository.",
    },
    "ca": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git commit --verbose --all ",
        "help-msg": "commits all modified and deleted files.",
    },
    "cA": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git commit --verbose --patch ",
        "help-msg": "commits all modified and deleted files interactivly.",
    },
    "cm": {
        "state": GitOptionState.STRING | GitOptionState.ONE,
        "command": "git commit --verbose --message ",
        "help-msg": "commits with the given message.",
    },
    "co": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git checkout ",
        "help-msg": "checks out a branch or paths to the working tree.",
    },
    "cO": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git checkout --pathc ",
        "help-msg": "checks out hunks from the index or the tree interactively.",
    },
    "cf": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git commit --amend --reuse-message HEAD ",
        "help-msg": "amends the tip of the current branch reusing the same log message as HEAD.",
    },
    "cF": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git commit --verbose --amend ",
        "help-msg": "amends the tip of the current branch.",
    },
    "cr": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git revert ",
        "help-msg": "reverts existing commits by reverting patches and recording new commits.",
    },
    "cR": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": 'git reset "HEAD^" ',
        "help-msg": "removes the HEAD commit.",
    },
    "cs": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": 'git show --pretty=format:"%C(bold yellow)commit %H%C(auto)%d%n%C(bold)Author: %C(blue)%an <%ae> %C(reset)%C(cyan)%ai (%ar)%n%C(bold)Commit: %C(blue)%cn <%ce> %C(reset)%C(cyan)%ci (%cr)%C(reset)%n%+B"',
        "help-msg": "shows one or more objects (blobs, trees, tags and commits).",
    },
    # Conflict(C)
    "Cl": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git --no-pager diff --diff-filter=U --name-only ",
        "help-msg": "lists unmerged files.",
    },
    "Ca": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git add git --no-pager diff --diff-filter=U --name-only ",
        "help-msg": "adds unmerged file contents to the index.",
    },
    "Ce": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git mergetool git --no-pager diff --diff-filter=U --name-only ",
        "help-msg": "executes merge-tool on all unmerged files.",
    },
    "Co": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git checkout --ours -- ",
        "help-msg": "checks out our changes for unmerged paths.",
    },
    "CO": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git checkout --ours -- git --no-pager diff --diff-filter=U --name-only ",
        "help-msg": "checks out our changes for all unmerged paths.",
    },
    "Ct": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git checkout --theirs -- ",
        "help-msg": "checks out their changes for unmerged paths.",
    },
    "CT": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": "git checkout --theirs -- git --no-pager diff --diff-filter=U --name-only ",
        "help-msg": "checks out their changes for all unmerged paths.",
    },
    # Fetch(f)
    "f": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git fetch ",
        "help-msg": "downloads objects and references from another repository.",
    },
    "fc": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git clone ",
        "help-msg": "clones a repository into a new directory.",
    },
    "fC": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git clone --depth=1 ",
        "help-msg": "clones a repository into a new directory clearly(depth:1).",
    },
    "fm": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git pull ",
        "help-msg": "fetches from and merges with another repository or local branch.",
    },
    "fr": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git pull --rebase ",
        "help-msg": "fetches from and rebase on top of another repository or local branch.",
    },
    "fu": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git fetch --all --prune && git merge --ff-only @{u} ",
        "help-msg": "removes un-existing remote-tracking references, fetches all remotes and merges.",
    },
    "fb": {
        "state": GitOptionState.FUNC | GitOptionState.ONE,
        "command": fetch_remote_branch,
        "help-msg": "fetch other branch to local as same name.",
    },
    # Index(i)
    "ia": {
        "state": GitOptionState.FUNC | GitOptionState.MULTI,
        "command": add,
        "help-msg": "adds file contents to the index(default: all files).",
    },
    "iA": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git add --patch ",
        "help-msg": "adds file contents to the index interactively.",
    },
    "iu": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git add --update ",
        "help-msg": "adds file contents to the index (updates only known files).",
    },
    "id": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git diff --no-ext-diff --cached ",
        "help-msg": "displays changes between the index and a named commit (diff).",
    },
    "iD": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git diff --no-ext-diff --cached --word-diff ",
        "help-msg": "displays changes between the index and a named commit (word diff).",
    },
    "ir": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git reset ",
        "help-msg": "resets the current HEAD to the specified state.",
    },
    "iR": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git reset --patch ",
        "help-msg": "resets the current index interactively.",
    },
    "ix": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git rm --cached -r ",
        "help-msg": "removes files from the index (recursively).",
    },
    "iX": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git rm --cached -rf ",
        "help-msg": "removes files from the index (recursively and forced).",
    },
    # Log(l)
    "l": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git log --graph --all --decorate ",
        "help-msg": "displays the log with good format.",
    },
    "l1": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git log --graph --all --decorate --oneline ",
        "help-msg": "",
    },
    "ls": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": 'git log --topo-order --stat --pretty=format:"%C(bold yellow)commit %H%C(auto)%d%n%C(bold)Author: %C(blue)%an <%ae> %C(reset)%C(cyan)%ai (%ar)%n%C(bold)Commit: %C(blue)%cn <%ce> %C(reset)%C(cyan)%ci (%cr)%C(reset)%n%+B" ',
        "help-msg": "displays the stats log.",
    },
    "ld": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": 'git log --topo-order --stat --patch --pretty=format:"%C(bold yellow)commit %H%C(auto)%d%n%C(bold)Author: %C(blue)%an <%ae> %C(reset)%C(cyan)%ai (%ar)%n%C(bold)Commit: %C(blue)%cn <%ce> %C(reset)%C(cyan)%ci (%cr)%C(reset)%n%+B" ',
        "help-msg": "displays the diff log.",
    },
    "lv": {
        "state": GitOptionState.STRING | GitOptionState.NO,
        "command": 'git log --topo-order --show-signature --pretty=format:"%C(bold yellow)commit %H%C(auto)%d%n%C(bold)Author: %C(blue)%an <%ae> %C(reset)%C(cyan)%ai (%ar)%n%C(bold)Commit: %C(blue)%cn <%ce> %C(reset)%C(cyan)%ci (%cr)%C(reset)%n%+B" ',
        "help-msg": "displays the log, verifying the GPG signature of commits.",
    },
    "lc": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git shortlog --summary --numbered ",
        "help-msg": "displays the commit count for each contributor in descending order.",
    },
    "lr": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git reflog ",
        "help-msg": "manages reflog information.",
    },
    # Merge(m)
    "m": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge ",
        "help-msg": "joins two or more development histories together.",
    },
    "ma": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge --abort ",
        "help-msg": "aborts the conflict resolution, and reconstructs the pre-merge state.",
    },
    "mC": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge --no-commit ",
        "help-msg": "performs the merge but does not commit.",
    },
    "mF": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge --no-ff ",
        "help-msg": "creates a merge commit even if the merge could be resolved as a fast-forward.",
    },
    "mS": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge -S ",
        "help-msg": "performs the merge and GPG-signs the resulting commit.",
    },
    "mv": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git merge --verify-signatures ",
        "help-msg": "verifies the GPG signature of the tip commit of the side branch being merged.",
    },
    "mt": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git mergetool ",
        "help-msg": "runs the merge conflict resolution tools to resolve conflicts.",
    },
    # Push(p)
    "p": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push ",
        "help-msg": "updates remote refs along with associated objects.",
    },
    "pf": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push --force-with-lease ",
        "help-msg": 'forces a push safely (with "lease").',
    },
    "pF": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push --force ",
        "help-msg": "forces a push. ",
    },
    "pa": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push --all ",
        "help-msg": "pushes all branches.",
    },
    "pA": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push --all && git push --tags ",
        "help-msg": "pushes all branches and tags.",
    },
    "pt": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git push --tags ",
        "help-msg": "pushes all tags.",
    },
    "pc": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": 'git push --set-upstream origin "$(git symbolic-ref -q --short HEAD 2> /dev/null)" ',
        "help-msg": "pushes the current branch and adds origin as an upstream reference for it.",
    },
    "pp": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": 'git pull origin "$(git symbolic-ref -q --short HEAD 2> /dev/null)" && git push origin "$(git symbolic-ref -q --short HEAD 2> /dev/null)" ',
        "help-msg": "pulls and pushes the current branch from origin to origin.",
    },
    # Remote(R)
    "R": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote ",
        "help-msg": "manages tracked repositories.",
    },
    "Rl": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote --verbose ",
        "help-msg": "lists remote names and their URLs.",
    },
    "Ra": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote add ",
        "help-msg": "adds a new remote.",
    },
    "Rx": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote rm ",
        "help-msg": "removes a remote.",
    },
    "Rm": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote rename ",
        "help-msg": "renames a remote.",
    },
    "Ru": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote update ",
        "help-msg": "fetches remotes updates.",
    },
    "Rp": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote prune ",
        "help-msg": "prunes all stale remote tracking branches.",
    },
    "Rs": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote show ",
        "help-msg": "shows information about a given remote.",
    },
    "RS": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git remote set-url ",
        "help-msg": "changes URLs for a remote.",
    },
    # Stash(s)
    "s": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git stash ",
        "help-msg": "stashes the changes of the dirty working directory.",
    },
    "sp": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git stash pop ",
        "help-msg": "removes and applies a single stashed state from the stash list.",
    },
    "sl": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git stash list ",
        "help-msg": "lists stashed states.",
    },
    "sd": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git stash show",
        "help-msg": "",
    },
    "sD": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git stash show --patch --stat",
        "help-msg": "",
    },
    # 'sr': {
    #     'state': GitOptionState.STRING | GitOptionState.MULTI,
    #     'command': '_git_stash_recover ',
    #     'help-msg': '',
    # },
    # 'sc': {
    #     'state': GitOptionState.STRING | GitOptionState.MULTI,
    #     'command': '_git_clear_stash_interactive',
    #     'help-msg': '',
    # },
    # Tag (t)
    "t": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git tag ",
        "help-msg": "creates, lists, deletes or verifies a tag object signed with GPG.",
    },
    "ta": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git tag -a ",
        "help-msg": "create a new tag.",
    },
    "tx": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git tag --delete ",
        "help-msg": "deletes tags with given names.",
    },
    # Working tree(w)
    "ws": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git status --short ",
        "help-msg": "displays working-tree status in the short format.",
    },
    "wS": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git status ",
        "help-msg": "displays working-tree status.",
    },
    "wd": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git diff --no-ext-diff ",
        "help-msg": "displays changes between the working tree and the index (diff).",
    },
    "wD": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git diff --no-ext-diff --word-diff ",
        "help-msg": "displays changes between the working tree and the index (word diff).",
    },
    "wr": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git reset --soft ",
        "help-msg": "resets the current HEAD to the specified state, does not touch the index nor the working tree.",
    },
    "wR": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git reset --hard ",
        "help-msg": "resets the current HEAD, index and working tree to the specified state.",
    },
    "wc": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git clean --dry-run ",
        "help-msg": "cleans untracked files from the working tree (dry-run).",
    },
    "wC": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git clean -d --force ",
        "help-msg": "cleans untracked files from the working tree.",
    },
    "wm": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git mv ",
        "help-msg": "moves or renames files.",
    },
    "wM": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git mv -f ",
        "help-msg": "moves or renames files (forced).",
    },
    "wx": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git rm -r ",
        "help-msg": "removes files from the working tree and from the index (recursively).",
    },
    "wX": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git rm -rf ",
        "help-msg": "removes files from the working tree and from the index (recursively and forced).",
    },
    # Setting
    "savepd": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git config credential.helper store ",
        "help-msg": "Remember your account and password.",
    },
    "ue": {
        "state": GitOptionState.FUNC | GitOptionState.NO,
        "command": set_email_and_username,
        "help-msg": "set email and username interactively.",
    },
    "user": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git config user.name ",
        "help-msg": "",
    },
    "email": {
        "state": GitOptionState.STRING | GitOptionState.MULTI,
        "command": "git config user.email ",
        "help-msg": "",
    },
    # 'clear': {
    #     'state': GitOptionState.STRING | GitOptionState.MULTI,
    #     'command': '_git_clear ${@:2:$((${#@}))} ',
    #     'help-msg': '',
    # },
    # 'ignore': {
    #     'state': GitOptionState.STRING | GitOptionState.MULTI,
    #     'command': '_git_ignore_files ${@:2:$((${#@}))} ',
    #     'help-msg': '',
    # },
}


def is_branch_option(x):
    return x.startswith("b")


def is_commit_option(x):
    return x.startswith("c")


def is_conflict_option(x):
    return x.startswith("C")


def is_fetch_option(x):
    return x.startswith("f")


def is_index_option(x):
    return x.startswith("i")


def is_log_option(x):
    return x.startswith("l")


def is_merge_option(x):
    return x.startswith("m")


def is_push_option(x):
    return x.startswith("p")


def is_remote_option(x):
    return x.startswith("R")


def is_stash_option(x):
    return x.startswith("s")


def is_tag_option(x):
    return x.startswith("t")


def is_tree_option(x):
    return x.startswith("w")


def detect_option_type(k: str) -> str:
    pass
