import sys
import os
from appsmiths.automata import Automata
from shutil import which
from pathlib import Path

is_nt = os.name == 'nt'


def pyexe():
    # search our system path, rather than spawn path
    return which('python')


def get_pipexe(PR):
    ext = '.exe' if os.name == 'nt' else ''
    if PR is None:
        return Path(f'pip3{ext}')

    bindir = 'Scripts' if is_nt else 'bin'
    pipexe = PR
    pipexe = pipexe / bindir
    return pipexe / f'pip3.6{ext}'


def install_pkgs(a, pkglist, PR):
    # import pip._internal
    # pip._internal.main(['install', *pkglist])
    print(f'pip installing prefix={PR}')
    pipe = get_pipexe(PR)
    pkgs = ' '.join(pkglist)
    a.run_string(f'{pipe} install --upgrade --prefix={PR} {pkgs}')


def install_ports(a, portlist, PR=None):
    drive = 'i:/' if is_nt else '/i'
    dir = Path(drive, 'ports', 'repo')

    for repname in portlist:
        repo = Path(dir, repname)

        os.chdir(str(repo))
        a.run_string(f'{pyexe()} setup.py install')


def install_virtualenv(a, PR=None):
    pkglist = ('virtualenv',)
    install_pkgs(a, pkglist, PR)


def install_our_pkgs(a, PR=None):

    # list of packages
    pkglist = ('docopt', 'rpyc')
    portlist = ('pypreprocessor',)

    install_pkgs(a, pkglist, PR)
    install_ports(a, portlist, PR)


def main(argv=None):
    if argv is not None:
        argv = sys.argv

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)
    install_our_pkgs(a)


if __name__ == '__main__':
    sys.exit(main())
