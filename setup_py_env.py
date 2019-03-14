import os
import sys
from appsmiths.automata import Automata
import make_pip
import our_pkgs
import make_venv
import run_py_ver
from pathlib import Path

is_nt = os.name == 'nt'
bindir = 'Scripts' if is_nt else 'bin'
ext = '.exe' if is_nt else ''


def setup_py_env(a, PR):

    pydir = PR / bindir

    # copy over python
    a.cp(str(pydir / f'python{ext}'),
         str(pydir / f'python3{ext}'))

    # find pip location reletive to running interpreter
    pipexe = pydir / f'pip3.6{ext}'

    make_pip.make_pip(a, pipexe)


def usage():
    msg = \
f"""
Usage: python {__file__} python_root
"""
    print(msg)
    sys.exit(-1)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        usage()

    # caller to pass pyroot
    PR = Path(argv[1])

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)

    print('doing setup_py_env.py')
    run_py_ver.print_site()

    # install into our build
    setup_py_env(a, PR)
    our_pkgs.install_virtualenv(a, PR)
    our_pkgs.install_our_pkgs(a, PR)

    # install a virtualenv
    VR = make_venv.compose_venv_root(a)
    make_venv.make_venv(a, VR)
    # make_venv.activate_venv(a, VR)
    our_pkgs.install_our_pkgs(a, VR)


if __name__ == '__main__':
    sys.exit(main())
