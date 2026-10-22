# HashPareto

**A reproducible, notebook-driven design-space explorer for an open-source SHA-256 core.**

HashPareto takes a verified SystemVerilog SHA-256 core, generates a family of
architectural variants (round-unrolling), hardens each one through the
open-source LibreLane RTL-to-GDS flow on the SkyWater SKY130 PDK, and reports
which variant is best for **throughput**, **area**, and **energy per hash** —
with a Pareto analysis that explains *why*.

Target: IEEE SSCS **Code-a-Chip** travel-grant notebook submission (ISSCC 2027
cycle). Deadline: **2026-10-31**.

## Results at a glance

4 of 5 variants hardened end-to-end (DRC/LVS/antenna clean, setup WNS = 0):

| UNROLL | Area (µm²) | Throughput (Mhash/s) | Energy/hash (nJ) | Power (mW) | Clock |
|-------:|-----------:|---------------------:|-----------------:|-----------:|------:|
| 1 | 176 750 | 0.149 | 16.94 | 2.53 | 100 ns |
| 2 | 197 497 | 0.286 | 8.98 | 2.57 | 100 ns |
| 4 | 243 908 | 0.526 | 4.96 | 2.61 | 100 ns |
| 16 | 524 671 | 0.185 | 4.95 | 0.92 | 300 ns |

**Takeaway:** unroll to 4 for the best area-energy tradeoff: 3.4× lower
energy per hash than U1 for only +38 % area, at the highest throughput of the
set. Unroll to 16 only with a wider ingress interface, since it adds 115 %
area over U4 without raising throughput or lowering energy. Functional
verification: **25/25 PASS** (5 variants × 5 cocotb suites vs
`hashlib.sha256`).

Full story in **`notebook/hashpareto.ipynb`** (the submission deliverable).

## Status

> Phase-by-phase checklist with artifacts and step counts:
> **`docs/PROJECT_STATUS.md`** (updated 2026-10-16).

| Phase | Name | State |
|------:|------|-------|
| 0 + 0.5 | Environment, repo bring-up, residuals | ✅ complete |
| 1 | Parameterized RTL generator (`UNROLL`) + bit-exact verification | ✅ complete (25/25 PASS) |
| 2 | SKY130 LibreLane hardening + PPA metrics | ✅ complete (4/5 variants; U8 blocked by congestion) |
| 3 | Energy + Pareto analysis | ✅ complete (4 points) |
| 4 | Notebook + reproducibility | ✅ complete (self-contained, outputs pre-rendered) |
| 5 | Submission (PR to `sscs-ose`) | 🔄 audited → PR pending |

Overall ≈ **95 %**. The submission package is built, audited against the
Code-a-Chip `howtoapply.md`, and verified to run standalone.

## Submission package

`submission/ISSCC27/submitted_notebooks/hashpareto/` (6.0 MB) is the exact
tree to push for the Code-a-Chip PR. It is **self-contained**: the notebook
runs using only its committed `data/` (metrics CSVs, rendered figures, and
GDS layout renders) —
the multi-GB `flow/runs/` artifacts stay local and are regenerable. Verified
to execute standalone with 0 errors.

To submit (deadline **2026-10-31, 11:59 AM Pacific**):

1. Fork `sscs-ose/sscs-ose-code-a-chip.github.io`.
2. Copy `submission/ISSCC27/submitted_notebooks/hashpareto/` → fork's
   `ISSCC27/submitted_notebooks/hashpareto/` (touch nothing outside it).
3. Open the PR, then watch it for reviewer questions.

Notes on the measured set:
- **U8 (UNROLL = 8 @ 100 ns)** did not complete OpenROAD global routing
  (`GRT-0116`, congestion); the four hardened points still span the unrolling
  tradeoff.
- **U16 runs at 300 ns**, not 100 ns: its 16-round combinational path cannot
  close timing at 100 ns (pre-CTS critical path alone was 132 ns). Every U16
  number uses that clock.

## Repository layout

```
.
|-- LICENSE                     Apache-2.0
|-- NOTICE                      third-party attribution
|-- README.md
|-- docs/
|   |-- phase0_environment.md   exact toolchain versions + hashes
|   |-- phase1_verification.md  bit-exact verification results (25/25 PASS)
|   `-- PROJECT_STATUS.md       what's done / left, per phase
|-- rtl/
|   |-- original/               vendored nano_hash reference RTL (untouched)
|   `-- generated/              parameterized core + top (UNROLL parameter)
|-- verif/
|   `-- cocotb/                 cocotb+Verilator golden-hash test harness
|-- flow/
|   |-- variants/u<U>/          per-unroll: src/, config.yaml, runs/
|   `-- runs/cocotb_u<U>/       simulation build + results per variant
|-- tools/                      gen / run / slim / metrics / plots helpers
|-- results/
|   |-- metrics.csv             harvested PPA metrics (one row per run)
|   `-- pareto.csv              measured throughput + energy per hash
|-- notebook/
|   `-- hashpareto.ipynb        the Code-a-Chip submission notebook
`-- data/
    |-- cycles.csv              measured cycles per block
    |-- figures/                Pareto, PPA, and layout figures
    |-- layouts/                GDS-to-PNG renders
    `-- vectors/                NIST SHA-256 test vectors
```

## Reproduce in three commands

Assumes the one-time environment setup from `docs/phase0_environment.md`
(WSL2 + LibreLane devshell AppImage + SKY130 via CIEL + `~/venv`) is done.

```bash
# 1. Verify the RTL is bit-exact (~2 min)
for u in 1 2 4 8 16; do ~/venv/bin/python verif/cocotb/run.py --sim verilator --unroll $u; done

# 2. Harden one variant (~30-45 min)
tools/run_variant.sh 2 test_u2

# 3. Harvest metrics + regenerate plots
~/venv/bin/python tools/collect_metrics.py
~/venv/bin/python tools/make_plots.py
```

## Environment (summary)

The RTL-to-GDS flow runs under **WSL2 (Ubuntu 26.04)** on Windows 11, using
**LibreLane v3.0.16** (devshell AppImage: Yosys 0.62, OpenROAD, Magic 8.3.623,
Netgen 1.5.316, KLayout 0.30.7, Verilator 5.044). The **SKY130A/B** PDK is
installed via CIEL. No Docker required. Full versions and hashes:
`docs/phase0_environment.md`.

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
