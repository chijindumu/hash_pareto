import json

paths = [
    '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb',
    '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb'
]
for p in paths:
    nb = json.load(open(p))
    imgs = 0
    errs = 0
    for c in nb['cells']:
        if c['cell_type'] == 'code':
            for o in c.get('outputs', []):
                if 'image/png' in o.get('data', {}):
                    imgs += 1
                if o.get('output_type') == 'error':
                    errs += 1
    name = p.split('/')[-1]
    print(name, 'cells=', len(nb['cells']), 'imgs=', imgs, 'errors=', errs)
