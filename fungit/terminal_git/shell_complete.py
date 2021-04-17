import os
import re
import typing
import logging

from .. import __HOME__, __FUNGITDIR__
from ..commands.exec import run_cmd, run_cmd_with_resp
from .gitoptions import GIT_OPTIONS
from .shared import okay, warn, echo, exit_

LOG = logging.getLogger(__name__)


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

_re = re.compile(r"\/\.config\/fungit/([^\s]+)")


def get_current_shell() -> str:
    """Gets the currently used shell.

    Returns:
        shell_: Current shell string.
    """
    shell_ = ""
    _, resp = run_cmd_with_resp("echo $SHELL")
    if resp:
        shell_ = resp.split("/")[-1].strip()
    return shell_


def ensure_config_path(file_name: str) -> str:
    """Check config path.

    Check whether the configuration directory exists, if not, try to create
    it. Failed to exit, successfully returned to complete the file path.

    Args:
        file_name: Completion prompt script name.

    Returns:
        file_path: Full path of completion prompt script.
    """
    LOG.debug(f"{__FUNGITDIR__}, {file_name}")
    if not os.path.exists(__FUNGITDIR__):
        try:
            os.mkdir(__FUNGITDIR__)
            return "{}/{}".format(__FUNGITDIR__, file_name)
        except Exception as e:
            exit_(1, e)
    else:
        file_path = "{}/{}".format(__FUNGITDIR__, file_name)
        return file_path


def generate_complete_script(template: str, fn: typing.Callable, name: str = "_g"):
    """Generate completion scirpt.

    Generate the completion script of the corresponding shell according to
    the template.

    Args:
        template: Script template.
        fn: Method of generating script content.
        name: Completion script name.
    """
    complete_src = fn()
    script_src = template % (complete_src)

    try:
        with open("./%s" % (name), "w") as f:
            for line in script_src:
                f.write(line)
    except Exception as e:
        exit_(1, e)


def using_completion(file_name: str, path: str, config_path: str):
    """Try using completion script.

    Inject the load of completion script into the configuration of shell.
    If it exists in the configuration, the injection will not be repeated.

    Args:
        file_name: generated completion script.
        path: `fungit` configuration path.
        config_path: shell configuration path.
    """
    try:
        run_cmd("mv {} {}".format(file_name, __FUNGITDIR__))
        with open(config_path) as f:
            shell_conf = f.read()
            files = _re.findall(shell_conf)
    except Exception as e:
        exit_(1, e)

    has_injected = False
    if files:
        for file in files:
            if file == file_name:
                has_injected = True
    LOG.debug(f"has_injected: {has_injected}")

    if not has_injected:
        try:
            run_cmd('echo "source %s" >> %s ' % (path, config_path))
        except Exception as e:
            exit_(1, e)
        okay("\nPlease run: source {}".format(config_path))
    else:
        warn("This configuration already exists.")


def add_zsh_completion():
    """Add Zsh completion prompt script."""

    _name = "_g"
    _path = ensure_config_path(_name)

    def gen_completion():
        vars = []

        for k in GIT_OPTIONS.keys():
            desc = GIT_OPTIONS[k]["help-msg"]
            if not desc:
                desc = "no description."
            vars.append('    {}\\:"{}"\\\n'.format(k, desc))

        return ("\n".join(vars)).rstrip()

    generate_complete_script(_TEMPLATE_ZSH, gen_completion, _name)

    using_completion(_name, _path, __HOME__ + "/.zshrc")


def add_bash_completion():
    """Add Bash completion prompt script."""

    _name = "complete_script"
    _path = ensure_config_path(_name)

    def gen_completion():
        return " ".join(GIT_OPTIONS.keys())

    generate_complete_script(_TEMPLATE_BASH, gen_completion, _name)

    using_completion(_name, _path, __HOME__ + "/.bashrc")


def add_completion():
    """Add completion prompt script."""
    echo("\nTry to add completion ...")

    _shell = get_current_shell()
    echo("Detect shell: %s" % _shell)
    if _shell == "zsh":
        add_zsh_completion()
    elif _shell == "bash":
        add_bash_completion()
    else:
        warn("Don't support completion of %s" % _shell)
