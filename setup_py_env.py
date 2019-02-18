import os
import sys
from appsmiths.automata import Automata
import make_pip
import our_pkgs
import make_venv
import run_py_ver
from pathlib import Path


def setup_py_env(a, PR):

    is_nt = os.name == 'nt'
    bindir = 'Scripts' if is_nt else 'bin'
    ext = '.exe' if is_nt else ''
    pydir = PR if is_nt else PR / bindir

    # copy over python
    a.cp(str(pydir / f'python{ext}'),
         str(pydir / f'python3{ext}'))

    # find pip location reletive to running interpreter
    pipexe = PR / bindir
    pipexe = pipexe / f'pip3.6{ext}'

    make_pip.make_pip(a, pipexe)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)

    run_py_ver.print_site()

    # install into our build
    if os == 'nt':
        PR = Path(sys.executable).parents[0]
    else:
        PR = Path(sys.executable).parents[1]  # allow for bin
    setup_py_env(a, PR)
    our_pkgs.install_virtualenv(a, PR)
    our_pkgs.install_our_pkgs(a, PR)

    # install a virtualenv
    VR = make_venv.compose_venv_root(a)
    make_venv.make_venv(a, VR)
    make_venv.activate_venv(a, VR)
    our_pkgs.install_our_pkgs(a, VR)


if __name__ == '__main__':
    sys.exit(main())
