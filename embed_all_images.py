#!/usr/bin/env python3
"""Embed all images into notebook JSON using base64 data URIs so they display
in Jupyter without needing external files. This makes the notebook self-contained."""
import json
import base64
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
pkg_nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb')

nb = json.load(open(nb_path))

# Map of cell indices to image paths to embed
# Cell 21: layout displays (u1, u2, u4, u16)
# Cell 24: layout displays in sequence (u1, u2, u4, u16)
# Cell 26: Pareto plots (area vs throughput, energy vs throughput)

image_embeddings = {
    21: [
        ('data/layouts/u1.png', True),
        ('data/layouts/u2.png', True),
        ('data/layouts/u4.png', True),
        ('data/layouts/u16.png', True),
    ],
    24: [
        ('data/layouts/u1.png', True),
        ('data/layouts/u2.png', True),
        ('data/layouts/u4.png', True),
        ('data/layouts/u16.png', True),
    ],
    26: [
        ('data/pareto_area_vs_throughput.png', True),
        ('data/pareto_energy_vs_throughput.png', True),
    ],
}

embedded_count = 0

for cell_idx, images in image_embeddings.items():
    if cell_idx >= len(nb['cells']):
        print(f'Cell {cell_idx} out of range, skipping')
        continue
    
    target_cell = nb['cells'][cell_idx]
    source = ''.join(target_cell['source'])
    
    for img_path, should_emb in images:
        full_path = Path(img_path)
        if not full_path.exists():
            print(f'NOT FOUND: {img_path}')
            continue
        
        if not should_emb:
            continue
            
        # Read and base64 encode
        with open(full_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode()
        data_uri = f'data:image/png;base64,{b64_data}'
        
        # Replace the Image(filename=...) lines in this cell's source
        new_lines = []
        for line in source.split('\n'):
            if 'Image(filename' in line and 'width=' in line:
                # Replace the filename parameter with the data URI
                # The line format is: display(Image(filename='...', width=N))
                # We need to replace the filename part
                # Find the filename within the line
                import re
                match = re.search(r"filename='([^']+)'", line)
                if match:
                    old_filename = match.group(1)
                    # Replace old filename with data URI
                    new_line = line.replace(old_filename, data_uri)
                    new_lines.append(new_line)
                else:
                    # No filename found in quotes, try another pattern
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        target_cell['source'] = new_lines
        embedded_count += 1
        print(f'Cell {cell_idx}: embedded {full_path.name}')

# Save both notebooks
for path in [nb_path, pkg_nb_path]:
    with open(path, 'w') as f:
        json.dump(nb, f, indent=1)

orig_size = orig_size or 0
new_size = os.path.getsize(nb_path)
print(f'\nTotal images embedded: {embedded_count}')
print(f'Notebook size: {new_size/1024:.1f} KB')
print('Notebooks saved with base64-embedded images!')
import os