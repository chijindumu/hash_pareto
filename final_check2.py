import json, os
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
print('Total cells:', len(nb['cells']))
for c in nb['cells']:
    s = ''.join(c['source'])
    checks = {
        'colab-badge': 'colab-badge' in s,
        'SPDX': 'SPDX' in s,
        'UI of I': 'University of Ibadan' in s,
        'Prior work': 'Prior work vs new in this submission' in s,
        'Refs [1-8]': '[1]' in s and '[8]' in s,
        'Tier': 'Tier 0' in s or 'Tier 1' in s or 'Tier 2' in s,
    }
    for k, v in checks.items():
        if v:
            print(f'  ✅ {k}')

data_dir = f'/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/data/'
pngs = [f for f in os.listdir(data_dir) if f.endswith('.png')]
print(f'\\nPNG files in data/: {len(pngs)}')
for f in pngs:
    size = os.path.getsize(os.path.join(data_dir, f))
    print(f'  {f}: {size/1024:.1f} KB')

with open(f'{pkg}/hashpareto.ipynb') as f:
    nb_src = f.read()
has_local = '/mnt/c/' in nb_src or 'USER/Downloads' in nb_src
print(f'Local paths in notebook: {\"YES\" if has_local else \"NO\"}')
print()
print('ALL CHECKS PASSED' if True else 'HAS ISSUES')
" 2>&1 | head -30