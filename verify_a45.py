import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

print('Total cells:', len(nb['cells']))
for i in range(47, 52):
    if i < len(nb['cells']):
        c = nb['cells'][i]
        src = ''.join(c.get('source', []))
        print('Cell', i, '(' + c['cell_type'] + '):')
        if c['cell_type'] == 'code':
            print('  Outputs:', len(c.get('outputs', [])))
            for o in c.get('outputs', []):
                if 'data' in o:
                    for fmt in o['data']:
                        if 'image' in fmt:
                            size = len(o['data'][fmt])
                            print('  Image format:', fmt, 'size:', size, 'bytes')
        print('  Source preview:', src[:80].replace(chr(10), ' | '))
        print()
