import os
import typing
from .gitoptions import (GIT_OPTIONS, is_branch_option, is_commit_option, is_conflict_option, is_fetch_option, is_index_option,
                         is_log_option, is_merge_option, is_push_option, is_remote_option, is_stash_option, is_tag_option, is_tree_option)
from .shared import run_shell, okey, warn, run_shell_with_resp, echo

_DIR = os.environ['HOME'] + '/.config/.pyzgit'

_TEMPLATE_ZSH = '''\
#compdef g

complete_g(){
local curcontext="$curcontext" state line ret=1
typeset -A opt_args

_alternative\\
  \'args:options arg:((\\
%s
  ))\'\\
  'files:filename:_files'
return ret
}

compdef _g g
'''

_TEMPLATE_BASH = '''\
#!/usr/env bash

_complete_g(){
  if [[ "${COMP_CWORD}" == "1" ]];then
    COMP_WORD="%s"
    COMPREPLY=($(compgen -W "$COMP_WORD" -- ${COMP_WORDS[${COMP_CWORD}]}))
  fi
} 

complete -F _complete_g g
'''


def get_current_shell() -> str:
    return run_shell_with_resp('echo $SHELL').split('/')[-1].strip()


def ensure_config_path(file_name: str) -> str:
    if not os.path.exists(_DIR):
        try:
            os.mkdir(_DIR)
            return '{}/{}'.format(_DIR, file_name)
        except Exception as e:
            pass
    else:
        return '{}/{}'.format(_DIR, file_name)


def generate_complete_script(template: str, fn: typing.Callable, name: str = '_g'):
    complete_src = fn()
    script_src = template % (complete_src)

    with open('./{}'.format(name), 'w') as f:
        for line in script_src:
            f.write(line)


def using_completion(file_name: str, path: str, config_path: str):
    run_shell('mv {} {}'.format(file_name, _DIR))
    run_shell('echo "source %s" >> %s ' % (path, config_path))
    okey('\nPlease run: source {}'.format(config_path))


def add_zsh_completion():
    _name = '_g'
    _path = ensure_config_path(_name)

    def gen_completion():
        avrs = []

        _type = ['Branch', 'Commit', 'Conflict', 'Fetch', 'Index', 'Log',
                 'Merge', 'Push', 'Remote', 'Stash', 'Tag', 'Working tree', 'Setting']

        for k in GIT_OPTIONS.keys():
            desc = GIT_OPTIONS[k]['help-msg']
            if not desc:
                desc = 'no description.'
            avrs.append('    {}\\:\"{}\"\\\n'.format(k, desc))

        return ('\n'.join(avrs)).rstrip()

    generate_complete_script(_TEMPLATE_ZSH, gen_completion, _name)

    using_completion(_name, _path, '~/.zshrc')


def add_bash_completion():
    _name = 'complete_script'
    _path = ensure_config_path(_name)

    def gen_completion():
        return ' '.join(GIT_OPTIONS.keys())

    generate_complete_script(_TEMPLATE_BASH, gen_completion, _name)

    using_completion(_name, _path, '~/.bashrc')


def add_completion():
    echo('\nTry to add completion ...')

    _shell = get_current_shell()
    if _shell == 'zsh':
        add_zsh_completion()
    elif _shell == 'bash':
        add_bash_completion()
    else:
        warn('Dont support completion of %s' % _shell)


if __name__ == '__main__':
    # generate_complete_script()
    add_completion()
    pass
