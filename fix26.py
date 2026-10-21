#!/usr/bin/env python3
import json, base64
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
nb = json.load(open(nb_path))

# Fix cell 26 - Pareto plots
cell_idx = 26
c = nb['cells'][cell_idx]
s = ''.join(c['source'])

# The key lines are:
# display(Image(filename=str(DATA / 'pareto_area_vs_throughput.png'), width=600))
# display(Image(filename=str(DATA / 'pareto_energy_vs_throughput.png'), width=600))

# Read both images and create data URIs
imgs = [
    ('data/pareto_area_vs_throughput.png', True),
    ('data/pareto_energy_vs_throughput.png', True),
]

for img_path, _ in imgs:
    full_path = Path(img_path)
    if not full_path.exists():
        print(f'NOT FOUND: {img_path}')
        continue
    with open(full_path, 'rb') as f:
        b64_data = base64.b64encode(f.read()).decode()
    data_uri = f'data:image/png;base64,{b64_data}'
    
    # Replace the str(DATA / 'filename') pattern in the source
    new_source = ''
    for line in s.split('\n'):
        if img_path in line:
            # Replace str(DATA / 'filename') with data_uri
            new_line = line.replace(f"str(DATA / '{full_path.name}')", data_uri)
            if new_line == line:
                # Try without str()
                new_line = line.replace(f"DATA / '{full_path.name}'", data_uri)
            if new_line == line:
                # Last resort: just keep original
                new_line = line
            new_source += new_line + '\n'
        else:
            new_source += line + '\n'
    
    c['source'] = new_source.split('\n')
    
    # Save
    with open(nb_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print(f'Fixed: {img_path} in cell {cell_idx}')

# Verify
c = nb['cells'][cell_idx]
s2 = ''.join(c['source'])
has_b64 = 'base64' in s2.lower()
print(f'\nCell {cell_idx} now has base64: {has_b64}')

# Save final notebook
with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Done!')