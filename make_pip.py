import sys
import os
import ensurepip
from pathlib import Path
from appsmiths.automata import Automata

is_nt = os.name == 'nt'
bindir = 'Scripts' if is_nt else 'bin'
ext = '.exe' if is_nt else ''


def make_pip(a, PR):

    pydir = PR / bindir

    # put pip in current environment, without internet
    #print(f'ensurepip {sys.executable}')
    #ensurepip.bootstrap(upgrade=True, default_pip=True, verbosity=10)
    pyexe = Path(pydir, f'python{ext}')
    print(f'ensurepip {pyexe}')
    a.run_string(f'{pyexe} -s -m ensurepip --default-pip --upgrade --verbose')
    # a.run_string(f'{pyexe} -s -m ensurepip --default-pip --upgrade --verbose --root {PR}')

    # via internet
    # run the pip we just installed
    # https://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip/53870246#53870246
    print('pip upgrade')
    # import pip
    # pip._internal.main(['install', '--upgrade', 'pip'])

    pip = Path(pydir, f'pip3.6{ext}')
    # a.run_string(f'{pip} install -vvv --upgrade pip')
    a.run_string(f'{pip} install -vvv --upgrade --prefix {PR} pip')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)
    make_pip(a)


if __name__ == '__main__':
    sys.exit(main())
