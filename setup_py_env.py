import sys
import os
from appsmiths.automata import Automata
from pathlib import Path
import site

is_nt = os.name == 'nt'
bindir = 'Scripts' if is_nt else 'bin'
ext = '.exe' if is_nt else ''
PATHSEP = ';' if is_nt else ':'


def pyexe(PR):
    return PR / bindir / f'python{ext}'


def _print_env(env, name):
    val = env[name]
    lval = val.split(PATHSEP)
    print(f'{name}=[')
    for subval in lval:
        print(f"    '{subval}'")
    print(']')


def print_path(name, path_list):
    print(f'{name} = [')
    for pname in path_list:
        print(f'    {pname}')
    print(']')


def print_env_path(name):
    path = os.environ[name]
    path_list = path.split(PATHSEP)
    print_path(name, path_list)


def print_site():

    # site
    user_base = site.getuserbase()
    user_site = site.getusersitepackages()
    print_path('sys.path', sys.path)
    ube = 'exists' if os.path.isdir(user_base) else "doesn't exist"
    print(f'USER_BASE: {user_base} ({ube})')
    use = 'exists' if os.path.isdir(user_site) else "doesn't exist"
    print(f'USER_SITE: {user_site} ({use})')
    print(f'ENABLE_USER_SITE: {site.ENABLE_USER_SITE}')

    # other crap
    print_env_path('PATH')
    print_env_path('PYTHONPATH')
    if not is_nt:
        print_env_path('LD_LIBRARY_PATH')


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


def make_venv(a, PR, VR):
    a.rm(VR)  # danger!
    venv = PR / bindir / f'virtualenv{ext}'
    a.run_string(f'{venv} {VR} --verbose --always-copy')


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

    print_site()


def install_pkgs(a, pkglist, PR):
    pe = pyexe(PR)
    pkgs = ' '.join(pkglist)
    a.run_string(f'{pe} -s -m pip install --upgrade --verbose {pkgs}')


def install_ports(a, portlist, PR=None):
    drive = 'i:/' if is_nt else '/i'
    repo_dir = Path(drive, 'ports', 'repo')
    pe = pyexe(PR)

    for repname in portlist:
        repo_dir = Path(repo_dir, repname)

        os.chdir(repo_dir)
        a.run_string(f'{pe} setup.py install --prefix={PR}')


def install_virtualenv(a, PR=None):
    pkglist = ('virtualenv',)
    install_pkgs(a, pkglist, PR)


def install_our_pkgs(a, PR=None):

    # list of packages
    pkglist = ('docopt', 'rpyc', 'pyyaml', 'sqlalchemy', 'fdb')
    portlist = ('pypreprocessor', )

    install_pkgs(a, pkglist, PR)
    install_ports(a, portlist, PR)


def copy_python(a, PR):

    pydir = PR / bindir

    # copy python to python3
    a.cp(pydir / f'python{ext}',
         pydir / f'python3{ext}')


def do_setup(a, PR):

    print('doing do_setup.py')
    print_site()

    # install into our build
    copy_python(a, PR)
    ensure_pip(a, PR)
    upgrade_pip(a, PR)
    install_our_pkgs(a, PR)
    install_virtualenv(a, PR)

    # install a virtualenv
    VR = compose_venv_root(PR)
    make_venv(a, PR, VR)
    activate_venv(a, VR)
    upgrade_pip(a, PR)
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

    # caller to pass pyroot
    PR = Path(argv[1])

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)

    do_setup(a, PR)


if __name__ == '__main__':
    sys.exit(main())
