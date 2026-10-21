import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i in [3, 22, 23]:
    c = nb['cells'][i]
    s = ''.join(c['source'])
    print(f'=== Cell {i} ===')
    print(s[:600])
    print('---')