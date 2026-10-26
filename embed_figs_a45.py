#!/usr/bin/env python3
"""Embed Figures A4 and A5 as base64 into the notebook."""
import json, base64

nb_path = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'

with open(nb_path) as f:
    nb = json.load(f)

# Read images as base64
def img_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

a4_b64 = img_b64('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/figures/fig_a4_clock_normalized.png')
a5_b64 = img_b64('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/figures/fig_a5_fmax_clocking.png')

# Find the index of the fig_tiers cell (cell 18) - the last figure image cell before appendix text
insert_idx = None
for i, c in enumerate(nb['cells']):
    src = ''.join(c.get('source', []))
    if 'fig_tiers.png' in src:
        insert_idx = i + 1  # Insert right after this cell
        break

print(f'Inserting after cell index {insert_idx - 1} (fig_tiers image)')

# Cell: Figure A4 image
cell_a4 = {
    "cell_type": "code",
    "execution_count": None,
    "id": "hp-cell-a4",
    "metadata": {},
    "outputs": [
        {
            "data": {
                "image/png": a4_b64
            },
            "metadata": {
                "image/png": {
                    "width": 900
                }
            },
            "output_type": "display_data"
        }
    ],
    "source": [
        "from IPython.display import Image, display\n",
        "from base64 import b64decode\n",
        "\n",
        "a4_img = \"" + a4_b64 + "\"\n",
        "\n",
        "if a4_img:\n",
        "    display(Image(data=b64decode(a4_img), width=900))\n",
    ]
}

# Cell: Figure A4 caption
cell_a4_cap = {
    "cell_type": "markdown",
    "id": "hp-md-a4",
    "metadata": {},
    "source": [
        "*Figure A4: Clock-normalized Pareto. Left: throughput at the fixed 100 ns clock (the published view). Right: throughput at each variant's own fmax. At fmax, throughput is nearly flat across U1–U4 (~0.7 Mhash/s) because the ingress interface saturates at ~18 cycles per block; U16 collapses to ~0.2 Mhash/s due to its 300 ns clock. The apparent 3.5× throughput gain of U4 over U1 is therefore a fixed-clock artifact, not an fmax property.*"
    ]
}

# Cell: Figure A5 image
cell_a5 = {
    "cell_type": "code",
    "execution_count": None,
    "id": "hp-cell-a5",
    "metadata": {},
    "outputs": [
        {
            "data": {
                "image/png": a5_b64
            },
            "metadata": {
                "image/png": {
                    "width": 900
                }
            },
            "output_type": "display_data"
        }
    ],
    "source": [
        "from IPython.display import Image, display\n",
        "from base64 import b64decode\n",
        "\n",
        "a5_img = \"" + a5_b64 + "\"\n",
        "\n",
        "if a5_img:\n",
        "    display(Image(data=b64decode(a5_img), width=900))\n",
    ]
}

# Cell: Figure A5 caption
cell_a5_cap = {
    "cell_type": "markdown",
    "id": "hp-md-a5",
    "metadata": {},
    "source": [
        "*Figure A5: Clocking strategy. Fmax drops sharply with unroll (46 MHz for U1 → 3.6 MHz for U16) because the combinational path grows with the round logic. U16's 16-round path requires a 300 ns clock, which more than cancels its parallelism advantage. Throughput at fmax is essentially flat across U1–U4 and collapses at U16.*"
    ]
}

# Insert the four cells after the fig_tiers image cell
new_cells = nb['cells'][:insert_idx] + [cell_a4, cell_a4_cap, cell_a5, cell_a5_cap] + nb['cells'][insert_idx:]

nb['cells'] = new_cells

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print(f'Inserted 4 cells at index {insert_idx}-{insert_idx+3}')
print('Notebook updated with Figures A4 and A5')