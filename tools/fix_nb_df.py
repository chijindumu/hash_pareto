import json

nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        src = ''.join(c['source'])
        if 'energy_per_hash_J' in src:
            src = src.replace('energy_per_hash_J', 'energy_nJ/1e9 if "energy_nJ" in chk else 0')
            c['source'] = src.splitlines(keepends=True)
json.dump(nb, open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb','w'), indent=1)
print('done')
