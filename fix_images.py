#!/usr/bin/env python3
import json, base64
from pathlib import Path

nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb')
nb = json.load(open(nb_path))

# Load images
images_b64 = []
for img_file in ['data/layouts/u1.png', 'data/layouts/u2.png', 'data/layouts/u4.png', 'data/layouts/u16.png']:
    with open(img_file, 'rb') as f:
        images_b64.append(base64.b64encode(f.read()).decode())

pareto1_b64 = base64.b64encode(open('data/pareto_area_vs_throughput.png', 'rb').read()).decode()
pareto2_b64 = base64.b64encode(open('data/pareto_energy_vs_throughput.png', 'rb').read()).decode()

# Fix cell 21
c21 = nb['cells'][21]
c21['source'] = [
    "# Display the four hardened layouts.\n",
    "from IPython.display import Image, display\n",
    "from base64 import b64decode\n",
    "\n",
    "img_data = [\n",
    "    '" + images_b64[0] + "',\n",
    "    '" + images_b64[1] + "',\n",
    "    '" + images_b64[2] + "',\n",
    "    '" + images_b64[3] + "',\n",
    "]\n",
    "\n",
    "for i, u in enumerate([1, 2, 4, 16]):\n",
    "    print(f'UNROLL = {u}')\n",
    "    if img_data[i]:\n",
    "        display(Image(data=b64decode(img_data[i]), width=520))\n",
    "    print()\n",
]

# Fix cell 24
c24 = nb['cells'][24]
c24['source'] = [
    "# Display all four hardened layouts in sequence.\n",
    "from IPython.display import Image, display\n",
    "from base64 import b64decode\n",
    "\n",
    "img_data = [\n",
    "    '" + images_b64[0] + "',\n",
    "    '" + images_b64[1] + "',\n",
    "    '" + images_b64[2] + "',\n",
    "    '" + images_b64[3] + "',\n",
    "]\n",
    "\n",
    "for i, u in enumerate([1, 2, 4, 16]):\n",
    "    print(f'=== UNROLL = {u} (KLayout GDS render) ===')\n",
    "    if img_data[i]:\n",
    "        display(Image(data=b64decode(img_data[i]), width=600))\n",
    "    print()\n",
]

# Fix cell 26
c26 = nb['cells'][26]
c26['source'] = [
    "# Render the two Pareto plots.\n",
    "from IPython.display import Image, display\n",
    "from base64 import b64decode\n",
    "\n",
    "print('### Area vs throughput')\n",
    "display(Image(data=b64decode('" + pareto1_b64 + "'), width=650))\n",
    "\n",
    "print('\\n### Energy per hash vs throughput')\n",
    "display(Image(data=b64decode('" + pareto2_b64 + "'), width=650))\n",
]

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

pkg_nb_path = Path('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb')
with open(pkg_nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Done')