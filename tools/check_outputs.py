import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        outs = c.get('outputs', [])
        if outs:
            print(f'=== Cell {i} ===')
            for o in outs:
                ot = o.get('output_type', '?')
                if ot == 'execute_result' or ot == 'display_data':
                    keys = list(o.get('data', {}).keys())
                    print(f'  {ot}: {keys}')
                elif ot == 'stream':
                    print(f'  stream: {o.get("text", "")[:100]}')
                elif ot == 'error':
                    print(f'  ERROR: {o.get("ename", "")}: {o.get("evalue", "")[:100]}')
                else:
                    print(f'  {ot}')
