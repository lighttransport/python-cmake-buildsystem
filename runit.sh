declare pydir='python-debug'
declare pydir='python'
declare -r PR="${ASV_PLAT_PORTS}/${pydir}"

python run_py_ver.py ${PR} setup_py_env.py ${PR}
# python setup_py_env.py ${PR}
