import sys
import os
import site
import our_pkgs
from pathlib import Path
from appsmiths.automata import Automata

PATHSEP = ';' if os.name == 'nt' else ':'


def _print_env(env, name):
    val = env[name]
    sep = ';' if os.name == 'nt' else ':'
    lval = val.split(sep)
    print(f'{name}=[')
    for subval in lval:
        print(f"    '{subval}'")
    print(']')


def _prepend_path(env, ename, prepend_str):

    curpath = env.get(ename, None)
    oldpath = '' if not curpath else f'{PATHSEP}{curpath}'
    env[ename] = f'{prepend_str}{oldpath}'


def _set_py_env(PR, worklist):

    print('\nset_py_env')

    # modify copy of env
    env = os.environ.copy()

    for job in worklist:
        ename = job[0]
        vallist = job[1:]

        # update the env
        fpath = PATHSEP.join([str(val) for val in vallist])
        _prepend_path(env, ename, fpath)

        # report result
        _print_env(env, ename)

    return env


def set_unix_py_env(PR):

    pyvdir = 'python3.6'
    worklist = (
        ('PATH', Path(PR, 'bin')),  # exe
        ('LD_LIBRARY_PATH', Path(PR, 'lib')),  # .so
        ('PYTHONPATH', Path(PR, 'lib', f'{pyvdir}'), Path(PR, 'lib'))
    )
    return _set_py_env(PR, worklist)


def set_win_py_env(PR):

    worklist = (
        ('PATH', Path(PR, 'Scripts'), Path(PR, 'DLLs'), Path(PR)),  # .exe, .dll
        ('PYTHONPATH', Path(PR, 'lib'))
    )
    return _set_py_env(PR, worklist)


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
    if os.name != 'nt':
        print_env_path('LD_LIBRARY_PATH')


def usage():
    msg = \
f"""
Usage: python {__file__} python_root script_path
"""
    print(msg)
    sys.exit(-1)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        usage()

    # caller to pass pyroot
    PR = Path(argv[1])
    # and script name to run
    SCRIPT = argv[2]
    print('run_py_ver')
    print(f'PYTHONROOT={PR}')
    print(f'SCRIPT={SCRIPT}')

    logfile = 'log.txt'
    asi = os.environ['ASI']
    a = Automata(asi, log_name=logfile, showcmds=True, verbose=False)

    # print_site()

    # spawn python child env with corrected env
    pyexe = our_pkgs.pyexe(PR)
    a.run_string(f'{pyexe} -s {SCRIPT}')


if __name__ == '__main__':
    sys.exit(main())
