# HashPareto — Project Status & Roadmap

**Updated: 2026-10-16.** This is the single source of truth for what is done,
what remains. Read-me-first summary in `README.md`.

## Legend
- ✅ **complete** — done, verified, artifacts on disk.
- 🔄 **partial** — done for the usable subset (see notes).
- ⬜ **todo** — not started.

---

## At a glance

| Phase | Name | State | Steps left |
|------:|------|-------|:----------:|
| 0 + 0.5 | Environment, repo bring-up, residuals | ✅ complete | **0** |
| 1 | Parameterized RTL + bit-exact verification | ✅ complete | **0** |
| 2 | SKY130 LibreLane grid + PPA metrics | ✅ complete (4/5; U8 documented) | **0** |
| 3 | Energy + Pareto analysis | ✅ complete (4 points) | **0** |
| 4 | Notebook + reproducibility | ✅ complete | **0** |
| 5 | Submission (PR to `sscs-ose`) | 🔄 package built → PR pending | **3** |

**Overall ≈ 90 % done.** The submission package
(`submission/ISSCC27/submitted_notebooks/hashpareto/`, 4.1 MB) is built and
verified — it runs standalone with only its committed `data/`. Remaining:
rubric audit, fork + copy + PR, deadline **2026-10-31**.

---

## Phase 0 + 0.5 — Environment & repo bring-up ✅

Done:
- WSL2 (Ubuntu 26.04) + Windows 11 hosts the whole flow; no Docker.
- LibreLane v3.0.16 devshell AppImage (Nix shell: Yosys 0.62, OpenROAD
  `dcf36133…`, Magic 8.3.623, Netgen 1.5.316, KLayout 0.30.7, Verilator 5.044).
  All versions + hashes pinned in `docs/phase0_environment.md`.
- SKY130 PDK via CIEL (`~/.ciel/…/sky130`).
- venv (`~/venv`): jupyterlab, numpy, pandas, matplotlib, cocotb 2.1.0.
- `.wslconfig` applied (6 GB RAM / 8 GB swap / 8 CPUs) — WSL now sees 5.8 GiB.
- Vendored `nano_hash` reference (Apache-2.0), `LICENSE`, `NOTICE`,
  `.gitignore`, `.gitattributes`, NIST vectors (`data/vectors/nist_sha256.json`).
- Git initialized + committed (Phase 0 / Phase 0.5).

---

## Phase 1 — Parameterized RTL + bit-exact verification ✅

Goal: one core, `#(parameter int UNROLL)`; prove every variant bit-exact vs
`hashlib.sha256`.

Done:
- `rtl/generated/sha256_core.sv` — UNROLL rounds/cycle (`NCHUNK=64/UNROLL`),
  in-cycle `ext[]` schedule chain, `kconst()` round constants.
- `rtl/generated/sha_top.sv` — same port list as the original, reuses the
  **untouched** vendored `message_padder` + `digest_buffer`.
- Synthesis fix: `digest_buffer` internal array renamed `digest_words`
  (Yosys frontend name clash) — `rtl/generated/digest_buffer.sv`.
- cocotb 2.1.0 + Verilator harness: `verif/cocotb/{test_sha256.py,run.py}`,
  5 suites (NIST/known vectors incl. 10⁶×`'a'`, boundary lengths, random,
  ingress bubbles, egress backpressure).
- **Result: 5 variants × 5 suites = 25/25 PASS** (2026-10-11), golden =
  `hashlib.sha256`. Documented in `docs/phase1_verification.md`.

Evidence on disk: `flow/runs/cocotb_u<UNROLL>/…` (results XML),
`docs/phase1_verification.md`.

---

## Phase 2 — SKY130 LibreLane grid + PPA metrics 🔄 (4/5 variants)

Hybrid clock policy (user-approved): **U1/U2/U4 @ 100 ns, U16 @ 300 ns**;
U8 was slated for 100 ns.

### Done
- **4/5 variants hardened end-to-end** (LibreLane RTL-to-GDS, DRC/LVS/antenna
  clean, WNS ≥ 0). One slimmed run each, keeping `final/` + logs:
  - `u1/runs/grid100` @ 100 ns — GDS 25.4 MB
  - `u2/runs/grid100` @ 100 ns — GDS 29.1 MB
  - `u4/runs/grid100` @ 100 ns — GDS 36.6 MB
  - `u16/runs/grid300` @ 300 ns — GDS 85.9 MB
- **U1 @10 ns counter-example** (deleted after recording): 77-step flow,
  DRC 0/LVS 0/antenna 0, but WNS −1.06 ns / 123 violations — proved the flow
  end-to-end and showed an over-aggressive clock fails timing. Numbers live in
  `results/metrics.csv` (`run=run_u1` row) and the git history; the 263 MB run
  dir was removed on 2026-10-16 to reclaim disk.
- Diagnostics that shaped the grid:
  - U16 **100 ns is impossible**: pre-PnR `period_min` = 132.5 ns (`nom_tt`),
    123.9 ns post-CTS → ~200 ns expected post-route. Repair tooling then
    runaway-looped 5 h → run killed, **hybrid clock chosen** (U16 @ 300 ns).
  - Disk hygiene: LibreLane keeps all 77 step outputs per run (~1.5–4.7 GB/run)
    → `tools/slim_run.sh` trims finished runs to `final/` + logs (~0.3–0.9 GB).

### U8 note (10/16/2026)
U8 (grid100) failed at OpenROAD Global Routing with **GRT-0116 (congestion)**
after reaching step 42. Attempts to resume from GlobalRouting did not complete.
Given time and disk, results are reported for U1/U2/U4/U16 (4 usable Pareto
points). The failed run dir was deleted 2026-10-16; the partial set still
demonstrates the unrolling tradeoff (area increases, energy/hash drops,
throughput scales sublinearly at very high unroll due to longer critical paths
and the chosen hybrid clocking for U16).

---

## Phase 3 — Energy + Pareto analysis ✅ (4 points)

1. Throughput per variant at its clock: `blocks/s = UNROLL / 64 / period`.
2. Energy per hash: `power__total` (vectorless STA power) × time-per-hash.
3. Harvest: `python3 tools/collect_metrics.py` → `results/metrics.csv`
   (one row per finished run).
4. Pareto table `results/pareto.csv` + plots `results/pareto_*.png`
   (area vs throughput, energy/hash vs throughput), 4 points annotated.
5. Result summary:
   | UNROLL | Area (µm²) | Throughput (Mhash/s) | Energy/hash (pJ) |
   |-------:|-----------:|---------------------:|-----------------:|
   | 1 | 176 750 | 0.16 | 16 184 |
   | 2 | 197 497 | 0.31 | 8 211 |
   | 4 | 243 908 | 0.62 | 4 176 |
   | 16 | 524 671 | 0.83 | 1 099 |

---

## Phase 4 — Notebook + reproducibility ✅ (draft)

- `notebook/hashpareto.ipynb` rewritten (10/16): full narrative — env pins,
  RTL explanation, verification table, flow + clocking strategy, derived
  metrics + both Pareto charts (regenerated in-notebook), observations,
  limitations (U8/U16/STA power caveats), reproduce guide. Builder:
  `tools/build_notebook.py`; validator: `tools/verify_notebook.sh` (executes
  all code cells in the pinned venv — passes).
- `tools/collect_metrics.py`, `tools/slim_run.sh`, `tools/run_variant.sh`,
  `tools/run_grid.sh`, `tools/make_plots.py` make the flow rerunnable
  (fixed run tags, pinned env). `make_plots.py` replaces the throwaway
  `/tmp` heredoc and fixes the energy-label bug (per-row annotation).
- `README.md` rewritten (10/16): results-at-a-glance table, current phase
  states, known limitations, 3-command reproduce guide.

### Self-contained notebook + submission package (10/16)
The notebook no longer depends on `flow/runs/` (2.1 GB, gitignored). It
locates its data by searching CWD + parents for `data/` (submission) or
`results/` (dev repo), so it runs identically in both layouts.

- **Layout renders:** `tools/render_layout.sh` + `tools/render_gds.rb` use
  KLayout (inside the devshell) to turn each hardened GDS into a small PNG →
  `results/layouts/u{1,2,4,16}.png` (340–460 KB each). Copied into the
  package as `data/layouts/`.
- **Notebook re-executed** with `jupyter nbconvert --execute` so GitHub shows
  all plots/tables/images without the reviewer running anything. Energy
  cross-check vs committed `pareto.csv`: **0.000 % deviation**.
- **Package:** `submission/ISSCC27/submitted_notebooks/hashpareto/` (4.1 MB)
  = notebook + `data/` + `rtl/` + `verif/` + `flow/` (configs+src only) +
  `tools/` + `docs/` + LICENSE/NOTICE/README. **Verified to execute standalone
  inside the package** (0 errors, 6 embedded images, resolves `data/`).

---

## Phase 5 — Submission 🔄 (3 steps left)

Package is built; what remains is the PR mechanics:

1. Re-verify license/compliance: Apache-2.0 for our work, `NOTICE` for vendored
   `nano_hash` + PDK/tool attributions. *(NOTICE present in package — re-read
   before submitting.)*
2. Audit against the Code-a-Chip rubric (reproducibility, clarity,
   open-sourcing, originality) + read `howtoapply.md` in the target repo.
3. **Submit:** fork `sscs-ose/sscs-ose-code-a-chip.github.io` → copy
   `submission/ISSCC27/submitted_notebooks/hashpareto/` into
   `ISSCC27/submitted_notebooks/hashpareto/` in the fork → PR before
   **2026-10-31 11:59 AM Pacific**. Do not touch files outside that dir.

---

## Housekeeping / open threads
- Disk (2026-10-16 cleanup, user-approved): slimmed `u16/grid300`,
  `u4/grid100`, `u2/grid100`, `u1/grid100`; deleted failed `u8/runs/grid100`
  (1.3 GB) and the `u1/runs/run_u1` reference run (263 MB). `flow/` down
  12 GB → 1.9 GB; C: free 13.9 GB → 21.7 GB. Keep `tools/slim_run.sh` in the
  loop after every completed run.
- Obsolete Oct-10 parallel-attempt artifacts were **deleted** earlier
  (user-approved): split-core `rtl/generated/vN_*`, `flow/verify`,
  `flow/runs/verify`, stray `waveform.vcd`.
- Throwaway probe scripts **removed** (10/16): `resume_u1.sh`,
  `inspect_run.sh`, `show_metrics.sh`, `show_timing.sh`, `yosys_probe*.sh`,
  `_state_check.sh`, `_du_probe.sh`, `_metrics_probe.sh`, `poll_run.sh`,
  plus junk `notebook/hashpareto_{final,summary}.ipynb`. `tools/` now holds
  only the scripts the docs reference.
- The `submission/` package is a **copy** — after editing any source file
  (RTL/docs/notebook), re-copy it into the package before opening the PR.
