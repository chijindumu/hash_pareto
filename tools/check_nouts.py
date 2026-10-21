import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        nouts = len(c.get('outputs', []))
        print(i, nouts)
