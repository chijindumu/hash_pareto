import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i in [11, 14, 16, 18]:
    c = nb['cells'][i]
    print(f'=== Cell {i} === execution_count={c.get("execution_count")} outputs={len(c.get("outputs", []))}')
    src = ''.join(c['source'])
    print(src[:200])
    print()
