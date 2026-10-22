#!/usr/bin/env python3
import json, base64

nb_path = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'
nb = json.load(open(nb_path))

# Read the new chart as base64
with open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/pareto_rich_bar_charts.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

# Fix cell 26 - Replace Pareto plots with rich bar charts
c26 = nb['cells'][26]
c26['source'] = [
    "# Render rich PPA bar chart gallery.\n",
    "from IPython.display import Image, display\n",
    "from base64 import b64decode\n",
    "\n",
    "# Rich bar charts (cycles, throughput, energy, power, area, knee analysis)\n",
    "bar_img = '" + b64 + "'\n",
    "\n",
    "if bar_img:\n",
    "    display(Image(data=b64decode(bar_img), width=700))\n",
    "\n",
    "print('---')\n",
    "print('Key observations from the charts:')\n",
    "print('1. Cycles per block drop rapidly: 67 (U1) to 35 (U2) to 19 (U4) to 18+ (U8/U16)')\n",
    "2. Throughput peaks at U4 (0.526 Mhash/s) then drops at U16 (0.185 Mhash/s)')\n",
    "3. Energy per hash improves 3.4x from U1 to U4, then plateaus at ~4.95 nJ')\n",
    "4. Area grows +38% U1 to U4, then +115% U1 to U16')\n",
    "5. Power stays ~2.5-2.6 mW across U1-U4, then drops at U16')\n",
    "6. **U4 is the knee of the Pareto curve**: optimal unroll factor',
]

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

pkg_nb_path = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/submission/ISSCC27/submitted_notebooks/hashpareto/hashpareto.ipynb'
with open(pkg_nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Fixed cell 26 with rich bar charts')