# HashPareto — Project Status & Roadmap

**Updated: 2026-10-13.** This is the single source of truth for what is done,
what is running, and what remains. Read-me-first summary in `README.md`.

## Legend
- ✅ **complete** — done, verified, artifacts on disk.
- 🔄 **in progress** — running now (most are polled/backgrounded).
- ⬜ **todo** — not started.

---

## At a glance

| Phase | Name | State | Steps left |
|------:|------|-------|:----------:|
| 0 + 0.5 | Environment, repo bring-up, residuals | ✅ complete | **0** |
| 1 | Parameterized RTL + bit-exact verification | ✅ complete | **0** |
| 2 | SKY130 LibreLane grid + PPA metrics | 🔄 in progress | **7 tasks / 4 runs** |
| 3 | Energy + Pareto analysis | ⬜ todo | **5** |
| 4 | Notebook + reproducibility | ⬜ todo | **4** |
| 5 | Submission (PR to `sscs-ose`) | ⬜ todo | **4** |

**Overall ≈ 45–55 % done** (phases 0–1 complete, phase 2 mid-flight).

**Current action (right now):** `flow/variants/u16/runs/grid300/` is at step
44/77 (detailed routing) — U16@300 ns, run 1 of 5 in the background grid.

---

## Phase 0 + 0.5 — Environment & repo bring-up ✅ (0 steps left)

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
- Proven LibreLane reference run (`~/project/uart_first/…/RUN_2026-10-06/`).

---

## Phase 1 — Parameterized RTL + bit-exact verification ✅ (0 steps left)

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

Optional polish (not blocking): Icarus ≠ entry in `run.py` for the vendored TB
(simulator limitation, already documented).

---

## Phase 2 — SKY130 LibreLane grid + PPA metrics 🔄 (~40 % now)

### Done so far
- Full U1 validation run **@10 ns** (`flow/variants/u1/runs/run_u1/`, slimmed):
  77-step flow, GDS 25.9 MB, **DRC 0, LVS 0, antenna 0**; area 178 932 µm²,
  power 25.5 mW, post-PnR `nom_ss` period_min = 18.98 ns. Proved the flow end-to-end.
- U1 **@10 ns does NOT close setup** (WNS −1.06 ns, 123 violations) → deliberately
  kept as the "too-aggressive clock" counter-example for the notebook.
- Diagnostics that shaped the grid:
  - U16 **100 ns is impossible**: pre-PnR `period_min` = 132.5 ns (`nom_tt`),
    123.9 ns post-CTS → ~200 ns expected post-route. Repair tooling then
    runaway-looped 5 h → run killed, **hybrid clock chosen** (U1–U8 @ 100 ns,
    U16 @ 300 ns).
  - Disk hygiene: LibreLane keeps all 77 step outputs per run (~1.5–1.7 GB/run)
    → `tools/slim_run.sh` trims finished runs to `final/` + logs (~0.26 GB).
    4.2 GB reclaimed down to ~1.8 GB.

### Running now 🔄
- **U16 @ 300 ns** — `flow/variants/u16/runs/grid300/`, step 44/77.
- Queued automatically after it: U1, U2, U4, U8 @ **100 ns** (common clock),
  each `grid100` tag. Driver: `tools/run_grid.sh` (detached, sequential to stay
  within RAM). Log: `flow/grid.out.log`.

### Remaining tasks (7)
1. U16@300 finishes 77/77 → confirm `final/metrics.json`, DRC/LVS/antenna = 0.
2. U1/U2/U4/U8 @100 run to completion (each ≈ 30–45 min), same gates.
3. Slim every finished run (`bash tools/slim_run.sh <run_dir>`) — disk ≤ ~1.6 GB total.
4. Harvest: `python tools/collect_metrics.py` → `results/metrics.csv`  (one row/run;
   area, cells, power, WNS/TNS, per-corner `period_min`/`fmax`, DRC/antenna).
5. Timing review table: setup/hold clean at chosen clock per variant; record
   achieved `period_min` (`nom_ss`) for each.
6. Spot-check: GDS exists + one LVS/DRC re-confirmation from metrics.
7. **Contingency:** if an unroll misses its clock (unexpected U8 > 100 ns),
   re-bin that variant with margin and re-run; document it.

Deliverable when done: one clean run per variant (`final/gds/sha_top.gds` +
`metrics.json`) + `results/metrics.csv`.

---

## Phase 3 — Energy + Pareto analysis ⬜ todo (5 steps)

1. Throughput per variant at its clock: blocks/s = 1/(cycles_per_block × period);
   also measured cycles/hash from cocotb (latency + pading/session overhead).
2. Energy per hash: `power__total` (vectorless STA power at operating corner)
   × time-per-hash; report W, J/hash, and (optional) energy-delay product.
3. Document the power methodology (which corner/analysis, what it includes).
4. Pareto plots (matplotlib, in notebook): **area vs throughput,
   power vs throughput, energy per hash vs throughput**, all 5 UNROLL points
   annotated; explain U16's diminishing returns (critical-path-limited).
5. Save tables/plots into `results/` + `notebook/`.

---

## Phase 4 — Notebook + reproducibility ⬜ todo (4 steps)

1. Author `notebook/hashpareto.ipynb`: env pins → RTL generation → cocotb
   verification gate → LibreLane runs (with graceful skip if outputs exist) →
   metrics → Pareto analysis. All cells rerunnable in the pinned env.
2. Make every step deterministic: fixed run tags, fixed period policy
   (documented), pinned tool versions + hashes (from Phase 0).
3. Export README-style summary; add `docs/` pointers from notebooks.
4. Clean-room rerun pass on a fresh clone (best-effort; flag any manual bits).

---

## Phase 5 — Submission 🔄/⬜ (4 steps)

1. Re-verify license/compliance: Apache-2.0 for our work, `NOTICE` for vendored
   `nano_hash` + PDK/tool attributions.
2. Audit against the Code-a-Chip rubric (reproducibility, clarity,
   open-sourcing, originality).
3. Push `hash_pareto` repo public (GitHub) **after Phase 4 rerun**.
4. Open PR to `sscs-ose/sscs-ose-code-a-chip.github.io` under
   `ISSCC27/submitted_notebooks/<name>/` (deadline **2026-10-31**).

---

## Housekeeping / open threads
- Not yet committed (all Phase 1–2 work): `docs/phase1_verification.md`,
  `flow/`, `rtl/generated/`, `verif/`, `tools/*` (new .sh/.py), `results/`.
  Phase 0/0.5 are committed (`5a3c864`, `1272ae9`).
- Obsolete Oct-10 parallel-attempt artifacts were **deleted** (user-approved):
  the split-core `rtl/generated/vN_*` set, `flow/verify`, `flow/runs/verify`,
  stray `waveform.vcd`.
- Disk: keep `tools/slim_run.sh` in the loop after every completed run.
## U8 note (10/16/2026)
U8 (grid100) failed at OpenROAD Global Routing with GRT-0116 (congestion) after reaching step 42. Attempts to resume from GlobalRouting did not complete. Given time and disk, results are reported for U1,U2,U4,U16 (4 usable Pareto points). The partial set still demonstrates the unrolling tradeoff (area increases, energy/hash drops, throughput scales sublinearly at very high unroll due to longer critical paths and the chosen hybrid clocking for U16).
