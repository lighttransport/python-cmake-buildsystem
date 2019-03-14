import sys
import os
import pathlib
from appsmiths.automata import Automata
import run_py_ver
from pathlib import Path

is_nt = os.name == 'nt'


def compose_venv_root(a):
    pdir = pathlib.Path(sys.executable).parents[0]

    # where do we put the venv?
    drive = 'i:/' if is_nt else '/i'
    vext = 'dbg' if 'debug' in str(pdir) else 'rel'
    return Path(drive, 'pyenv', f'glue-run-{vext}')


def make_venv(a, VR):

    # delete the old one
    a.rm(str(VR))

    # make a fresh venv
    print(f'creating virtualenv={VR}')
    # import virtualenv
    # virtualenv.create_environment(VR)
    a.run_string(f'virtualenv {VR} --verbose --always-copy')


def activate_venv(a, VR):
    bindir = 'Scripts' if is_nt else 'bin'

    # active the venv - sets a few vars
    # https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
    activate_script = f'{VR}/{bindir}/activate_this.py'
    myglobals = dict(
        __file__=activate_script,
        __name__='__main__'
    )

    print(f'activating virtualenv={VR} with {activate_script}')
    with open(activate_script, 'rb') as f:
        code = compile(f.read(), activate_script, 'exec')
        exec(code, myglobals)

    run_py_ver.print_site()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)
    make_venv(a)


if __name__ == '__main__':
    sys.exit(main())
