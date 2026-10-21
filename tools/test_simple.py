import json
print("json ok")
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
print("loaded", len(nb['cells']))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        nouts = len(c.get('outputs', []))
        ec = c.get('execution_count')
        print(i, 'outs=', nouts, 'exec=', ec)
