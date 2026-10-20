import json

nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for c in nb['cells']:
    if c['cell_type'] != 'markdown': continue
    s = ''.join(c['source'])
    if '| Name |' in s and '| Benjamin' in s:
        new = """| Name | Affiliation | IEEE Member | SSCS Member | Email |
|------|-------------|------------|-------------|-------|
| Benjamin Joshua Chimbuchi | University of Ibadan | No | No | joshuabenjamin852@gmail.com |
"""
        c['source'] = new.splitlines(keepends=True)
        break
json.dump(nb, open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb','w'), indent=1)
print('done')
