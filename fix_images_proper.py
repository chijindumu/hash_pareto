#!/usr/bin/env python3
"""Fix notebook to properly display all images with base64 embedding."""
import json
import base64
from pathlib import Path

# Load notebook
nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
nb = json.load(open(nb_path))

# Images to embed
images_to_embed = {}
img_files = [
    'data/layouts/u1.png',
    'data/layouts/u2.png',
    'data/layouts/u4.png',
    'data/layouts/u16.png',
    'data/pareto_area_vs_throughput.png',
    'data/pareto_energy_vs_throughput.png',
]

# Load all images as base64
for img_path in img_files:
    full_path = Path(img_path)
    if full_path.exists():
        with open(full_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        images_to_embed[img_path] = f'data:image/png;base64,{b64}'
        print(f'Loaded {img_path}')
    else:
        print(f'MISSING {img_path}')
        images_to_embed[img_path] = ''

# Fix cell 21 - display layouts with proper formatting
c21 = nb['cells'][21]
c21['source'] = [
    "# Display the four hardened layouts. Falls back gracefully if images absent.\n",
    "from IPython.display import Image, display\n",
    "\n",
    "# Base64-embedded layout images (KLayout GDS renders)\n",
    f"img_u1 = '{images_to_embed['data/layouts/u1.png']}'\n",
    f"img_u2 = '{images_to_embed['data/layouts/u2.png']}'\n",
    f"img_u4 = '{images_to_embed['data/layouts/u4.png']}'\n",
    f"img_u16 = '{images_to_embed['data/layouts/u16.png']}'\n",
    "\n",
    "for u, img in [(1, img_u1), (2, img_u2), (4, img_u4), (16, img_u16)]:\n",
    "    print(f'UNROLL = {u}')\n",
    "    if img:\n",
    "        display(Image(filename=img, width=520))\n",
    "    print()\n",
]

# Fix cell 24
c24 = nb['cells'][24]
c24['source'] = [
    "# Display all four hardened layouts in sequence (KLayout GDS renders).\n",
    "from IPython.display import Image, display\n",
    "\n",
    "# Base64-embedded layout images\n",
    f"img_list = [('u1', '{images_to_embed['data/layouts/u1.png']}'), ('u2', '{images_to_embed['data/layouts/u2.png']}'), ('u4', '{images_to_embed['data/layouts/u4.png']}'), ('u16', '{images_to_embed['data/layouts/u16.png']}')]\n",
    "\n",
    "for name, img_data in img_list:\n",
    "    if img_data:\n",
    "        print(f'=== UNROLL = {name[1:]} (KLayout GDS render) ===')\n",
    "        display(Image(filename=img_data, width=600))\n",
    "        print()\n",
]

# Fix cell 26
c26 = nb['cells'][26]
c26['source'] = [
    "# Render the two Pareto plots from committed data.\n",
    "from IPython.display import Image, display\n",
    "\n",
    "# Base64-embedded Pareto plots\n",
    f"pareto_area = '{images_to_embed['data/pareto_area_vs_throughput.png']}'\n",
    f"pareto_energy = '{images_to_embed['data/pareto_energy_vs_throughput.png']}'\n",
    "\n",
    "print('### Area vs throughput')\n",
    "if pareto_area:\n",
    "    display(Image(filename=pareto_area, width=650))\n",
    "print()\n",
    "\n",
    "print('### Energy per hash vs throughput')\n",
    "if pareto_energy:\n",
    "    display(Image(filename=pareto_energy, width=650))\n",
]

# Save both notebooks
with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

pkg_nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb')
with open(pkg_nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Notebook updated with properly formatted base64 images')
print('Saved to both notebook/ and submission/ directories')
