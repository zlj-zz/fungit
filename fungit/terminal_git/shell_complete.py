import os
import re
import typing

from .. import __HOME__, __FUNGITDIR__
from .gitoptions import GIT_OPTIONS
from .shared import run_shell, run_shell_with_resp, okay, warn, echo


_TEMPLATE_ZSH = """\
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

compdef complete_g g
"""

_TEMPLATE_BASH = """\
#!/usr/env bash

_complete_g(){
  if [[ "${COMP_CWORD}" == "1" ]];then
    COMP_WORD="%s"
    COMPREPLY=($(compgen -W "$COMP_WORD" -- ${COMP_WORDS[${COMP_CWORD}]}))
  fi
} 

complete -F _complete_g g
"""

_re = re.compile(r"\/\.config\/\.pyzgit/([^\s]+)")


def get_current_shell() -> str:
    """Gets the currently used shell"""
    return run_shell_with_resp("echo $SHELL").split("/")[-1].strip()


def ensure_config_path(file_name: str) -> str:
    if not os.path.exists(__FUNGITDIR__):
        try:
            os.mkdir(__FUNGITDIR__)
            return "{}/{}".format(__FUNGITDIR__, file_name)
        except Exception as e:
            pass
    else:
        return "{}/{}".format(__FUNGITDIR__, file_name)


def generate_complete_script(template: str, fn: typing.Callable, name: str = "_g"):
    complete_src = fn()
    script_src = template % (complete_src)

    with open("./%s" % (name), "w") as f:
        for line in script_src:
            f.write(line)


def using_completion(file_name: str, path: str, config_path: str):
    """Inject the load of completion script into the configuration of shell.
    If it exists in the configuration, the injection will not be repeated.

    Args:
        file_name: generated completion script.
        path: `fungit` configuration path.
        config_path: shell configuration path.
    """
    run_shell("mv {} {}".format(file_name, __FUNGITDIR__))

    with open(config_path) as f:
        conf = f.read()
        files = _re.findall(conf)

    has_injected = False
    if files:
        for file in files:
            if file == file_name:
                has_injected = True

    if not has_injected:
        run_shell('echo "source %s" >> %s ' % (path, config_path))
        okay("\nPlease run: source {}".format(config_path))
    else:
        warn("This configuration already exists.")


def add_zsh_completion():
    _name = "_g"
    _path = ensure_config_path(_name)

    def gen_completion():
        vars = []

        _type = [
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

        for k in GIT_OPTIONS.keys():
            desc = GIT_OPTIONS[k]["help-msg"]
            if not desc:
                desc = "no description."
            vars.append('    {}\\:"{}"\\\n'.format(k, desc))

        return ("\n".join(vars)).rstrip()

    generate_complete_script(_TEMPLATE_ZSH, gen_completion, _name)

    using_completion(_name, _path, __HOME__ + "/.zshrc")


def add_bash_completion():
    _name = "complete_script"
    _path = ensure_config_path(_name)

    def gen_completion():
        return " ".join(GIT_OPTIONS.keys())

    generate_complete_script(_TEMPLATE_BASH, gen_completion, _name)

    using_completion(_name, _path, __HOME__ + "/.bashrc")


def add_completion():
    echo("\nTry to add completion ...")

    _shell = get_current_shell()
    echo("Detect shell: %s" % _shell)
    if _shell == "zsh":
        add_zsh_completion()
    elif _shell == "bash":
        add_bash_completion()
    else:
        warn("Don't support completion of %s" % _shell)


if __name__ == "__main__":
    # generate_complete_script()
    add_completion()
    pass
