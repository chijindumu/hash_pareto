import json
nb=json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
count=0
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        for o in c.get('outputs', []):
            d=o.get('data', {})
            if 'image/png' in d:
                count+=1
print(count)
