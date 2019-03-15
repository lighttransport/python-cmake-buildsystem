import sys
import os
import ensurepip
import pathlib
from appsmiths.automata import Automata


def make_pip(a, pip_path='pip3'):

    # put pip in current environment, without internet
    print(f'ensurepip {sys.executable}')
    ensurepip.bootstrap(upgrade=True, default_pip=True, verbosity=10)

    # via internet
    # run the pip we just installed
    # https://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip/53870246#53870246
    print('pip upgrade')
    # import pip
    # pip._internal.main(['install', '--upgrade', 'pip'])

    a.run_string(f'{pip_path} install -vvv --upgrade pip')
    # a.run_string(
    #     f'{pip_path} install -vvv --upgrade --root {PR} pip')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)
    make_pip(a)


if __name__ == '__main__':
    sys.exit(main())
