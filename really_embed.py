#!/usr/bin/env python3
"""Embed base64 images into ALL notebook code cells that display images."""
import json
import base64
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
pkg_nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb')

nb = json.load(open(nb_path))

# Define all image embeddings: (image_relative_path, target_cell_index)
# Cell indices where images are displayed
image_cells = {
    # Layout display cells
    21: ['data/layouts/u1.png', 'data/layouts/u2.png', 'data/layouts/u4.png', 'data/layouts/u16.png'],
    # Pareto plot cells
    26: ['data/pareto_area_vs_throughput.png', 'data/pareto_energy_vs_throughput.png'],
    # Additional cells that may have image references
    11: None,  # import cell, no images to embed
}

embedded_total = 0

for cell_idx, img_paths in image_cells.items():
    if cell_idx >= len(nb['cells']):
        print(f'Cell {cell_idx} out of range')
        continue
    
    target_cell = nb['cells'][cell_idx]
    source = ''.join(target_cell['source'])
    
    if img_paths is None:
        continue
    
    for img_path in img_paths:
        full_path = Path(img_path)
        if not full_path.exists():
            print(f'Not found: {img_path}')
            continue
        
        with open(full_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode()
        data_uri = f'data:image/png;base64,{b64_data}'
        
        # Replace all Image(filename=... lines in this cell
        new_lines = []
        for line in source.split('\n'):
            if 'Image(filename' in line and 'width=' in line:
                # Replace the filename parameter with data URI
                new_line = line.replace(
                    "display(Image(filename=str(p), width=520))",
                    f"display(Image(filename='{data_uri}', width=520))"
                )
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        target_cell['source'] = new_lines
        embedded_total += 1
        print(f'Cell {cell_idx}: embedded {full_path.name}')

# Save both notebooks
for path in [nb_path, pkg_nb_path]:
    with open(path, 'w') as f:
        json.dump(nb, f, indent=1)

print(f'\nTotal images embedded: {embedded_total}')
print('Notebooks saved.')