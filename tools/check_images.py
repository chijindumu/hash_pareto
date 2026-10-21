import json, re
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        s = ''.join(c['source'])
        if 'png' in s.lower() or 'Image' in s or 'display' in s:
            print(f'Cell {i}: has image references')
            matches = re.findall(r'[\"\\']?([^\"\\']*\.(?:png|PNG))[\"\\']?', s)
            if matches:
                print(f'  PNG refs: {matches[:3]}')
" 2>&1