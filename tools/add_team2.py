import json
team = "| Name | Affiliation | IEEE Member | SSCS Member | Email |\n|------|-------------|------------|-------------|-------|\n| Benjamin Joshua Chimbuchi | University of Ibadan | No | No | joshuabenjamin852@gmail.com |\n\n"
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='markdown':
        s = ''.join(c['source'])
        if '# HashPareto' in s:
            lines = s.splitlines(keepends=True)
            if len(lines) > 0 and lines[0].startswith('# HashPareto'):
                new = lines[0] + '\n' + team + ''.join(lines[1:])
                c['source'] = new.splitlines(keepends=True)
                break
        elif '## 1. Environment' in s:
            c['source'] = (team + s).splitlines(keepends=True)
            break
json.dump(nb, open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb','w'), indent=1)
print('done')
