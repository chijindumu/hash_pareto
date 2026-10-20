from pathlib import Path
DATA = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data')
for u in (1,2,4,16):
    p = DATA/'layouts'/f'u{u}.png'
    print(p.exists(), p.stat().st_size if p.exists() else 0)
