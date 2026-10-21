import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
# Print all markdown cells
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'markdown':
        s = ''.join(c['source'])
        # find first line
        first_line = s.split('\n')[0] if s else ''
        print(f'Cell {i}: {first_line}')
        print(s[:200])
        print('---')