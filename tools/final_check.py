import json
nb=json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb'))
imgs = 0
for c in nb['cells']:
    if c['cell_type']=='code':
        for o in c.get('outputs',[]):
            if o.get('output_type') in ['display_data','execute_result']:
                if 'image/png' in o.get('data',{}):
                    imgs += 1
print(len(nb['cells']), imgs)
