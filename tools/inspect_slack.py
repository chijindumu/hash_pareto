#!/usr/bin/env python3
"""Summarize worst setup slack per variant (audit A5)."""
import json, glob, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

PERIOD = {1: 100.0, 2: 100.0, 4: 100.0, 8: 100.0, 16: 300.0}

for u in (1, 2, 4, 8, 16):
    hits = glob.glob(f'flow/variants/u{u}/runs/*/final/metrics.json')
    if not hits:
        print(f'U{u}: NO final/metrics.json')
        continue
    run = hits[0].split('/')[3]
    d = json.load(open(hits[0]))
    ws = {k.split('__corner:')[1]: v for k, v in d.items()
          if k.startswith('timing__setup__ws__corner:')}
    if not ws:
        print(f'U{u} ({run}): no per-corner setup ws')
        continue
    worst_corner = min(ws, key=ws.get)
    worst = ws[worst_corner]
    nom = ws.get('nom_tt_025C_1v80', None)
    nom_ss = ws.get('nom_ss_100C_1v60', None)
    clk = PERIOD[u]
    fmax_wc = 1000.0 / (clk - worst) if clk - worst > 0 else float('inf')
    fmax_tt = 1000.0 / (clk - nom) if nom is not None and clk - nom > 0 else float('inf')
    print(f'U{u} run={run} clk={clk}ns worst_ws={worst:.2f}ns ({worst_corner}) '
          f'fmax_worst={fmax_wc:.1f}MHz nom_tt_ws={nom if nom is None else round(nom,2)} '
          f'nom_ss_ws={nom_ss if nom_ss is None else round(nom_ss,2)} fmax_tt={fmax_tt:.1f}MHz')
    # slew/cap/fanout at worst and nominal corners
    for kind in ('max_slew_violation', 'max_cap_violation', 'max_fanout_violation'):
        key = f'design__{kind}__count'
        if key in d:
            per = {k.split('__corner:')[1]: v for k, v in d.items()
                   if k.startswith(f'design__{kind}__count__corner:')}
            if per:
                mc = max(per, key=per.get)
                print(f'    {kind}: total={d[key]} worst_corner={mc} val={per[mc]} '
                      f'nom_tt={per.get("nom_tt_025C_1v80","-")}')
            else:
                print(f'    {kind}: total={d[key]} (no per-corner)')
