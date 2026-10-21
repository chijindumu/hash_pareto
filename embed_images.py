#!/usr/bin/env python3
"""Embed images into notebook JSON using base64 data URIs."""
import json, base64, os
from pathlib import Path

# Load the current notebook
nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
nb = json.load(open(nb_path))

# Images to embed (relative to notebook root)
images_to_embed = [
    ('data/layouts/u1.png', 'u1 layout'),
    ('data/layouts/u2.png', 'u2 layout'),
    ('data/layouts/u4.png', 'u4 layout'),
    ('data/layouts/u16.png', 'u16 layout'),
    ('data/pareto_area_vs_throughput.png', 'Pareto area vs throughput'),
    ('data/pareto_energy_vs_throughput.png', 'Pareto energy vs throughput'),
]

embedded_count = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        for img_path, desc in images_to_embed:
            full_path = Path(img_path)
            if full_path.exists():
                # Read and base64 encode
                with open(full_path, 'rb') as f:
                    b64 = base64.b64encode(f.read()).decode()
                # Get MIME type
                ext = full_path.suffix.lower()
                mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg'}.get(ext, 'application/octet-stream')
                # Build data URI
                data_uri = f'data:{mime};base64,{b64}'
                
                # Replace display(Image(filename=str(p), width=520)) 
                # with display(Image(filename=data_uri, width=520))
                old_text = "display(Image(filename=str(p), width=520))"
                # Find and replace - the str(p) part varies, so let's do a general replacement
                # The code cells have patterns like:
                # display(Image(filename=str(p), width=520))
                # We need to replace the entire line
                
                # Actually, let's find the specific pattern and replace
                # The source lines for image display are like:
                #     display(Image(filename=str(p), width=520))
                # where p = Path('data/layouts') / f'u{u}.png'
                
                # Let me just replace the whole cell source if it contains image display
                if 'display(Image(filename' in source:
                    # Replace all Image(filename=... patterns with base64
                    import re
                    # Pattern: display(Image(filename=str(p), width=520))
                    # We need to be careful - let's just replace the filename part
                    # Actually, the simplest approach: replace the specific line
                    
                    # Let me check what the actual source looks like
                    for line in source.split('\n'):
                        if 'Image(filename' in line and 'width=' in line:
                            # This is an image display line
                            # Replace with base64 version
                            new_line = line.replace(
                                'display(Image(filename=str(p), width=520))',
                                f"display(Image(filename='{data_uri}', width=520))"
                            )
                            source = source.replace(line, new_line)
                    
                    cell['source'] = source.split('\n')
                    embedded_count += 1
                    print(f'Embedded: {desc}')

# Save the modified notebook
with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

orig_size = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb').stat().st_size
print(f'Total cells modified: {embedded_count}')
print(f'Notebook size: {orig_size/1024:.1f} KB -> {os.path.getsize(nb_path)/1024:.1f} KB')
print('Done!')