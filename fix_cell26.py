#!/usr/bin/env python3
import json, base64, re
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
nb = json.load(open(nb_path))

# Fix cell 26
cell_idx = 26
c = nb['cells'][cell_idx]
s = ''.join(c['source'])

new_lines = []
for line in s.split('\n'):
    if 'Image(filename' in line and 'width=' in line:
        match = re.search(r"filename='([^']+)'", line)
        if match:
            old_filename = match.group(1)
            full_path = Path(old_filename)
            if full_path.exists():
                with open(full_path, 'rb') as f:
                    b64_data = base64.b64encode(f.read()).decode()
                data_uri = f'data:image/png;base64,{b64_data}'
                new_line = line.replace(old_filename, data_uri)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

c['source'] = new_lines

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Cell 26 fixed')