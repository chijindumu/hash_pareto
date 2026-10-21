#!/usr/bin/env python3
"""Embed base64 images into notebook JSON cells."""
import json
import base64
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
pkg_nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb')

# Load the package notebook (which is the one we'll modify)
nb = json.load(open(nb_path))

# Images to embed with their display code patterns
image_embeddings = [
    # (image_path, cell_index_target, replacement_text)
    # The replacement_text replaces the line with display(Image(filename='data:...'))
    ('data/layouts/u1.png', 21, "display(Image(filename='data:image/png;base64,"),
    ('data/layouts/u2.png', 21, "display(Image(filename='data:image/png;base64,"),
    ('data/layouts/u4.png', 21, "display(Image(filename='data:image/png;base64,"),
    ('data/layouts/u16.png', 21, "display(Image(filename='data:image/png;base64,"),
    ('data/pareto_area_vs_throughput.png', 26, "display(Image(filename='data:image/png;base64,"),
    ('data/pareto_energy_vs_throughput.png', 26, "display(Image(filename='data:image/png;base64,"),
]

embedded = 0
for img_path, cell_idx, replacement in image_embeddings:
    full_path = Path(img_path)
    if full_path.exists():
        with open(full_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode()
        mime_type = 'image/png'
        data_uri = f'data:{mime_type};base64,{b64_data}'
        
        target_cell = nb['cells'][cell_idx]
        source = ''.join(target_cell['source'])
        
        # Find the display line and replace
        # The lines look like: display(Image(filename=str(p), width=520))
        # We need to replace the filename=str(p) part with the data URI
        
        # Let's find and replace the specific Image display lines
        new_lines = []
        for line in source.split('\n'):
            if 'Image(filename' in line and 'width=' in line:
                # Replace the whole line with base64 version
                # Original: display(Image(filename=str(p), width=520))
                # New: display(Image(filename='data:image/png;base64,..., width=520))
                # But we need to keep the width parameter
                # Let's construct the new line
                new_line = line.replace(
                    "display(Image(filename=str(p), width=520))",
                    f"display(Image(filename='{data_uri}', width=520))"
                )
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        target_cell['source'] = new_lines
        embedded += 1
        print(f'Embedded: {img_path} -> cell {cell_idx}')
    else:
        print(f'Not found: {img_path}')

# Save both notebooks
for path in [nb_path, pkg_nb_path]:
    with open(path, 'w') as f:
        json.dump(nb, f, indent=1)

orig_size = orig_size or 0
new_size = path.stat().st_size if 'path' in dir() else 0
print(f'\nNotebooks updated. Size: check manually.')
print(f'Total images embedded: {embedded}')