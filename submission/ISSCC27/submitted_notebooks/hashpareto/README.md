# HashPareto — a notebook-driven PPA explorer for an open SHA-256 core

**IEEE SSCS Code-a-Chip travel-grant submission · ISSCC 2027 cycle**

Start here: **[`hashpareto.ipynb`](hashpareto.ipynb)** — the complete notebook
(design → verification → hardening → Pareto analysis → limitations → reproduce).

**Open the notebook first.** Its §5–§6 run anywhere with `pandas` +
`matplotlib` using only the small files in `data/`. §8 explains how to
reproduce the full RTL-to-GDS flow if you have the toolchain.

## What this project does

Takes a verified SystemVerilog SHA-256 core, generates a family of
architectural variants by **round-unrolling** (`UNROLL` = 1, 2, 4, 8, 16),
hardens each through the open-source **LibreLane** RTL-to-GDS flow on the
**SkyWater SKY130** PDK, and reports which variant is best for **throughput**,
**area**, and **energy per hash** — with a Pareto analysis that explains *why*.

### Headline results (4 of 5 variants hardened)

| UNROLL | Area (µm²) | Throughput (Mhash/s) | Energy/hash (nJ) | Power (mW) | Clock |
|-------:|-----------:|---------------------:|-----------------:|-----------:|------:|
| 1 | 176 750 | 0.156 | 16.18 | 2.53 | 100 ns |
| 2 | 197 497 | 0.313 | 8.21 | 2.57 | 100 ns |
| 4 | 243 908 | 0.625 | 4.18 | 2.61 | 100 ns |
| 16 | 524 671 | 0.833 | 1.10 | 0.92 | 300 ns |

Functional verification: **25/25 PASS** (5 variants × 5 cocotb suites vs
`hashlib.sha256`). Sign-off: **DRC 0 / LVS clean / antenna 0 / setup WNS 0**
for every hardened variant.

**Takeaway:** unroll to 4 for the best area-energy tradeoff (4× lower energy
than U1 for only +38 % area); unroll to 16 if absolute energy matters more
than area.

Honest limitations: U8 (UNROLL = 8) failed global routing (`GRT-0116`
congestion); U16 runs at 300 ns because its 16-round combinational path cannot
close 100 ns. Both are explained in notebook §7.

## Package contents

```
hashpareto/
|-- hashpareto.ipynb          the submission notebook (outputs pre-rendered)
|-- LICENSE                   Apache-2.0
|-- NOTICE                    third-party attribution (nano_hash, PDK, tools)
|-- README.md                 this file
|-- data/                     small files the notebook needs (committed)
|   |-- metrics.csv           harvested PPA metrics, one row per finished run
|   |-- pareto.csv            derived throughput + energy per hash
|   |-- layouts/*.png         GDS→PNG renders of the 4 hardened variants
|   `-- vectors/              NIST SHA-256 test vectors
|-- rtl/
|   |-- generated/            parameterized core + top (UNROLL parameter)
|   `-- original/rtl/core/    vendored nano_hash reference (untouched)
|-- verif/cocotb/             cocotb + Verilator golden-hash test harness
|-- flow/variants/u<N>/       per-variant: src/ + 4-line config.yaml
|-- tools/                    gen / run / slim / metrics / plots / render
`-- docs/                     environment pins, verification, project status
```

Large physical-design run artifacts (`flow/runs/`, ~2 GB per variant) are
intentionally **not** included — they are reproducible with the flow scripts
and would blow up the repository. Their *results* (metrics, layouts) are in
`data/`.

## Reproduce from scratch

One-time environment setup (Windows 11 + WSL2, no Docker) is documented in
[`docs/phase0_environment.md`](docs/phase0_environment.md): LibreLane 3.0.16
devshell AppImage, SKY130 via CIEL, and a Python venv with cocotb/pandas/
matplotlib/Jupyter.

```bash
# 1. Functional verification (~2 min)
for u in 1 2 4 8 16; do ~/venv/bin/python verif/cocotb/run.py --sim verilator --unroll $u; done

# 2. Harden one variant (~30-45 min, ~4 GB RAM)
tools/run_variant.sh 2 test_u2
tools/slim_run.sh flow/variants/u2/runs/test_u2

# 3. Harvest metrics + regenerate plots
~/venv/bin/python tools/collect_metrics.py
~/venv/bin/python tools/make_plots.py

# 4. Re-execute this notebook
~/venv/bin/jupyter nbconvert --to notebook --execute --inplace hashpareto.ipynb
```

## License

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
