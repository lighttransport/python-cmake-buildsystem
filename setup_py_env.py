import sys
import os
import re
import print_site
from appsmiths.automata import Automata
from pathlib import Path

is_nt = os.name == 'nt'
bindir = 'Scripts' if is_nt else 'bin'
ext = '.exe' if is_nt else ''


def fix_activate_path(VRdir):

    new_lines = []
    fn = Path(VRdir) / bindir / 'activate'
    with open(fn, 'r') as fh:
        sexp = re.compile(r"VIRTUAL_ENV='(.+)'")
        for line in fh:
            # VIRTUAL_ENV='C:\Users\appsmith\asv\pyenv\glue-run-dbg'
            m = sexp.search(line)
            if m:
                # convert slashes
                the_path = str(Path(m.group(1)).as_posix())
                # fix drive letter
                fix_path = f'/{the_path[0].lower()}{the_path[2:]}'
                line = f"VIRTUAL_ENV='{fix_path}'\n"
            new_lines.append(line)

    with open(fn, 'w') as fh:
        print(''.join(new_lines), file=fh)


def pyexe(PR):
    return PR / bindir / f'python{ext}'


def ensure_pip(a, PR):
    pe = pyexe(PR)
    a.run_string(f'{pe} -s -m ensurepip --default-pip --upgrade --verbose')


def upgrade_pip(a, PR):
    pe = pyexe(PR)
    a.run_string(f'{pe} -s -m pip install --upgrade --verbose pip')


def compose_venv_root(PR):

    # where do we put the venv?
    drive = 'i:/' if is_nt else '/i'
    vext = 'dbg' if 'debug' in str(PR) else 'rel'
    return Path(drive, 'pyenv', f'glue-run-{vext}')


def make_venv(a, PR, VRdir):
    venvexe = PR / bindir / f'virtualenv{ext}'
    pyexe = PR / bindir / f'python{ext}'
    a.run_string(f'{venvexe} {VRdir} --python={pyexe} --verbose --always-copy --clear')

    if is_nt:
        fix_activate_path(VRdir)


def activate_venv(a, VR):

    # activate the venv - sets a few vars
    # https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
    activate_script = VR / bindir / 'activate_this.py'
    myglobals = dict(
        __file__=activate_script,
        __name__='__main__'
    )

    print(f'activating virtualenv={VR} with {activate_script}')
    with open(activate_script, 'rb') as f:
        code = compile(f.read(), activate_script, 'exec')
        exec(code, myglobals)

    print_site.print_site()


def install_pkgs(a, pkglist, PR, do_upgrade=True):
    pe = pyexe(PR)
    pkgs = ' '.join(pkglist)
    uparg = '' if not do_upgrade else '--upgrade'
    a.run_string(f'{pe} -s -m pip install {uparg} --verbose {pkgs}')


def install_ports(a, portlist, PR=None):
    drive = 'i:' if is_nt else '/i'
    portboy = Path(drive, 'ports', 'scripts', 'portboy.py')
    pe = pyexe(PR)
    repo_str = ' '.join(portlist)
    a.run_string(f'{pe} {portboy} {repo_str}')


def install_virtualenv(a, PR=None):
    pkglist = ('virtualenv==16.7.9',)
    install_pkgs(a, pkglist, PR, do_upgrade=False)


def install_our_pkgs(a, PR=None):

    # list of packages
    pkglist = (
        'docopt',
        'rpyc',
        'pyyaml',
        'sqlalchemy',
        'fdb',
        'graphql-core'
    )
    portlist = (
        'pypreprocessor',
        'region_profiler',
        'hypercorn'
    )

    install_pkgs(a, pkglist, PR)
    install_ports(a, portlist, PR)


def copy_python_exe(a, PR):

    pydir = PR / bindir

    # copy python to python3
    a.cp(
        pydir / f'python{ext}',
        pydir / f'python3{ext}')


def do_setup(a, PR):

    print('setup_py_env::do_setup')
    # on Windows, pip and such will fish in the registry
    # path still has various python versions first
    # better all be at same level!
    print_site.print_site()

    # install into our build
    copy_python_exe(a, PR)
    ensure_pip(a, PR)
    upgrade_pip(a, PR)
    install_virtualenv(a, PR)

    # create a virtualenv using python install
    VR = compose_venv_root(PR)
    make_venv(a, PR, VR)
    activate_venv(a, VR)
    upgrade_pip(a, VR)
    install_our_pkgs(a, VR)


def usage():
    msg = f"""\
Usage: python {__file__} python_root
"""
    print(msg)
    sys.exit(-1)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        usage()
        return -1

    # caller to pass pyroot
    PR = Path(argv[1])

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)

    do_setup(a, PR)

    return 0


if __name__ == '__main__':
    sys.exit(main())
