from pathlib import Path
t = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/tools/build_notebook.py').read_text()
if '64 / UNROLL' in t:
    print('has64')
else:
    print('no64')
