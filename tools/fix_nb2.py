#!/usr/bin/env python3
import json

nb = json.load(open('notebook/hashpareto.ipynb'))
def src(c): return ''.join(c.get('source',[]))
def set_src(c, s):
    c['source'] = s if isinstance(s, list) else s.splitlines(keepends=True)
for c in nb['cells']:
    if c['cell_type'] != 'markdown': continue
    s = src(c)
    if 'setup WNS = 0 ns' in s and 'worst' not in s:
        new = """**Sign-off (published runs):** DRC/LVS/antenna clean; **setup WNS = 0 ns** at the chosen clock by the standard metric (worst-negative slack clamped to 0). We report **worst-corner setup slack** and estimated fmax per run below (from `final/metrics.json` / `timing__setup__ws__corner:*`). Slew/cap/fanout violations remain in non-nominal corners on several variants (see table) and are documented as present. An earlier deliberately tight run (U1 @ 10 ns) failed timing — evidence that 100 ns was conservative for U1/U2/U4.\n"""
        set_src(c, new)
        break
json.dump(nb, open('notebook/hashpareto.ipynb','w'), indent=1)
print('done')
