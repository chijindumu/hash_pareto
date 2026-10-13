# HashPareto

**A reproducible, notebook-driven design-space explorer for an open-source SHA-256 core.**

HashPareto takes a verified SystemVerilog SHA-256 core, generates a family of
architectural variants (round-unrolling and multi-block pipelining), hardens each
one through the open-source LibreLane RTL-to-GDS flow on the SkyWater SKY130 PDK,
and reports which variant is best for **throughput**, **area**, and **energy per
hash** — with a Pareto analysis that explains *why*.

Target: IEEE SSCS **Code-a-Chip** travel-grant notebook submission (ISSCC 2027
cycle).

## Status

> Full phase-by-phase checklist with artifacts and step counts:
> **`docs/PROJECT_STATUS.md`** (updated 2026-10-13).

| Phase | Name | State | Steps left |
|------:|------|-------|:----------:|
| 0 + 0.5 | Environment, repo bring-up, residuals | ✅ complete | 0 |
| 1 | Parameterized RTL generator (`UNROLL`) + bit-exact verification | ✅ complete | 0 |
| 2 | SKY130 LibreLane hardening + PPA metrics | 🔄 in progress | 7 tasks / 4 runs |
| 3 | Energy + Pareto analysis | ⬜ | 5 |
| 4 | Notebook + reproducibility | ⬜ | 4 |
| 5 | Submission (PR to `sscs-ose`) | ⬜ | 4 |

Overall ≈ **45–55 %** (phases 0–1 done; the Phase 2 grid is running now:
U16@300 ns first, then U1/U2/U4/U8@100 ns — log `flow/grid.out.log`).

## Repository layout

```
.
|-- LICENSE                     Apache-2.0
|-- NOTICE                      third-party attribution
|-- README.md
|-- docs/
|   |-- phase0_environment.md   exact toolchain, hashes, reproduction steps
|   |-- phase1_verification.md  bit-exact verification results (25/25 PASS)
|   `-- PROJECT_STATUS.md       what's done / running / left, per phase
|-- rtl/
|   |-- original/               vendored nano_hash reference RTL + testbenches
|   `-- generated/              parameterized core + top (Phase 1)
|-- verif/
|   `-- cocotb/                 cocotb+Verilator golden-hash test harness
|-- flow/
|   |-- variants/u<U>/          per-unroll::{src, config.yaml, runs/}
|   `-- grid logs               grid.out.log / grid.err.log (Phase 2)
|-- tools/                      gen/run/slim/metrics helpers (Phase 1-2)
|-- results/                    collected PPA metrics.csv (Phase 2-3)
|-- notebook/                   the Code-a-Chip submission notebook (Phase 4)
`-- data/
    `-- vectors/                NIST SHA-256 test vectors
```

## Environment (summary)

The RTL-to-GDS flow runs under **WSL2 (Ubuntu 26.04)** on Windows 11, using the
**LibreLane v3.0.16** devshell AppImage (a Nix shell bundling Yosys, OpenROAD,
Magic, Netgen, KLayout, Verilator). The **SkyWater SKY130A/B** PDK is installed
via CIEL. No Docker is required. Full details and hashes: `docs/phase0_environment.md`.

Run a command in the flow, non-interactively:

```bash
tools/run_librelane.sh 'librelane --version'
```

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
