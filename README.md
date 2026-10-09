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

| Phase | Description | State |
|------:|-------------|-------|
| 0 | Environment + repo bring-up | **complete** (see `docs/phase0_environment.md`) |
| 1 | Parameterized RTL generator (`UNROLL`, `PIPE_STAGES`) + verification | not started |
| 2 | SKY130 LibreLane hardening of all variants | not started |
| 3 | PPA + energy/Pareto analysis | not started |
| 4 | Notebook assembly + reproducibility | not started |
| 5 | Submission (fork + PR to `sscs-ose`) | not started |

## Repository layout

```
.
|-- LICENSE                     Apache-2.0
|-- NOTICE                      third-party attribution
|-- README.md
|-- docs/
|   `-- phase0_environment.md   exact toolchain, hashes, reproduction steps
|-- rtl/
|   |-- original/               vendored nano_hash reference RTL + testbenches
|   `-- generated/              parameter-generated variants (Phase 1)
|-- flow/
|   |-- configs/                LibreLane YAML configs (Phase 2)
|   `-- runs/                   hardened-run outputs (gitignored)
|-- tools/
|   |-- run_librelane.sh        invoke LibreLane inside the devshell AppImage
|   |-- phase0_probe.sh         environment probe
|   `-- phase0_versions.sh      toolchain version capture
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
