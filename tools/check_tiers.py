import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'markdown':
        s = ''.join(c['source'])
        if 'Tier' in s:
            print(f'Cell {i}: contains Tier text')
            print(s[:200])
            print('---')