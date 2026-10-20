import json
nb=json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='markdown':
        s=''.join(c['source'])
        if '[1]' in s or '## 11' in s or 'References' in s:
            print('===',i,'len',len(s),'===')
            print(s[:400])
            print()
