#!/usr/bin/env python3
import json, sys

nb = json.load(open('notebook/hashpareto.ipynb'))
def src(c): return ''.join(c.get('source',[]))
def set_src(c, s):
    c['source'] = s if isinstance(s, list) else s.splitlines(keepends=True)
changed = 0
for i,c in enumerate(nb['cells']):
    if c['cell_type'] != 'markdown': continue
    s = src(c)
    if 'slower clock slashes dynamic power' in s:
        # replace entire paragraph in that cell
        new = """**Energy/hash** is reported using the **vectorless STA power estimate** as `P_total × cycles_per_block / f_clk`. We measure cycles per block from RTL simulation (not the closed form 64/UNROLL): **67, 35, 19, 18, 18** for UNROLL 1, 2, 4, 8, 16. With the published clocks, energy/hash falls from ~16.9 nJ (U1) to ~5.0 nJ (U4/U16). Energy per hash is largely clock-independent at fixed voltage; the vectorless numbers should be read as **relative estimates across variants**, not absolute silicon energy.
"""
        set_src(c, new)
        changed += 1
    if 'Cycles per 512-bit block' in s and '`64 / UNROLL`' in s and 'measured' not in s.lower():
        set_src(c, [l.replace('`64 / UNROLL`  (SHA-256 has 64 rounds)',
                              '`64 / UNROLL` (SHA-256 has 64 rounds), plus 2 idle/digest cycles. Because the 32-bit AXI-Stream ingest overlaps, the **measured steady-state** is **67, 35, 19, 18, 18** cycles/block for U1–U16.') for l in c['source']])
        changed += 1
json.dump(nb, open('notebook/hashpareto.ipynb','w'), indent=1)
print('changed', changed)
