# HashPareto Submission Checklist (Based on Rubric v2)

**Deadline:** Sat 2026-10-31 11:59 AM PDT | **PR Target:** Thu 2026-10-29 | **Repo:** `ISSCC27/submitted_notebooks/hashpareto/`

## 1. ELIGIBILITY (MUST - Blocking)
- [x] License file in project dir (`LICENSE` - Apache-2.0)
- [ ] SPDX/copyright line in notebook header
- [ ] Team table at top of notebook (Name, Affiliation, Email, IEEE Member, SSCS Member)
- [ ] Representative identified for ISSCC 2027 attendance
- [ ] References numbered and include reused projects/notebooks
- [ ] Tool versions printed in notebook and listed
- [ ] PR to `ISSCC27/submitted_notebooks/hashpareto/` only (no files outside)
- [ ] Open PR by Thu 2026-10-29

## 2. CRITICAL FIXES - Scientific Correctness (A1-A6)
### A1: Measured Cycle Model
- [x] Create cycle testbench (`verif/cycles/tb_cycles.sv`)
- [x] Measure cycles/block for all variants (67/35/19/18/18)
- [x] Generate `data/cycles.csv` and `results/cycles.csv`
- [x] Rebuild `pareto.csv` with measured cycles
- [x] Update all plots with corrected numbers
- [ ] Remove all references to `64/UNROLL` as the only model
- [ ] Add streaming throughput vs latency distinction

### A2: Fmax-Closed Comparison
- [x] Re-harden U1 @ 20ns (running)
- [ ] Re-harden U2 @ 35-40ns (running) 
- [ ] Re-harden U4 @ 70-80ns
- [ ] Collect per-corner worst slack
- [ ] Only compare variants at closed-timing clocks or clearly label
- [ ] Update Pareto with fmax-closed points

### A3-A6: Energy & Timing Honesty
- [x] Label energy as "vectorless STA estimate (relative)"
- [x] Add per-corner setup slack to `collect_metrics.py`
- [x] Report worst-corner slack, not just WNS=0
- [x] Fix wrong causal claim about clock/slashing power (A4)
- [ ] Disclose slew/cap/fanout violations per corner (A6)
- [ ] Add U1@10ns vs @100ns energy invariance sanity check

## 3. REPRODUCIBILITY (B1-B3, C1-C3)
### Paths & Packaging
- [x] Fix hard-coded paths in `run.py`, `run_cocotb_matrix.sh`, `run_icarus_top_tb.sh`
- [x] Add UNROLL guard to `sha256_core.sv`
- [ ] Create package-specific README
- [ ] Fix notebook output path leaks (`/mnt/c/...`)
- [ ] Unify `data/` vs `results/` naming
- [ ] Create `tools/make_submission.sh` and `tools/check_package.sh`

### Notebook Tiers
- [ ] Tier 0: Load committed data, plots, layouts (always runs)
- [ ] Tier 1: Verify & measure (cocotb, Icarus, Yosys synthesis)
- [ ] Tier 2: Full flow demo for U1 (opt-in, LibreLane)
- [ ] Add Colab badge
- [ ] Add install/setup cells
- [ ] Print tool versions
- [ ] Test top-to-bottom on fresh environment

### Images Fix (CRITICAL - Currently Missing)
- [ ] Regenerate Pareto plots (`make_plots.py`)
- [ ] Ensure layout PNGs exist in `data/layouts/`
- [ ] Copy all images to package `data/`
- [ ] Rebuild notebook with images properly embedded
- [ ] Re-execute notebook to generate outputs
- [ ] Verify images display in package notebook

## 4. NOTEBOOK STRUCTURE (Per Winners)
- [x] Abstract
- [x] 11-section structure with TOC
- [x] Related work section
- [x] Conclusion section
- [ ] Team table (Cell 0-1)
- [ ] Prior work vs new work box
- [ ] SHA-256/unrolling primer with diagrams
- [ ] Timeline figure showing ingest/compression overlap
- [ ] Interactive widgets (optional but nice)
- [ ] Threats to validity section
- [ ] Numbered references [1]-[8]
- [ ] File map, how to cite, acknowledgements

## 5. DOCUMENTATION & HOUSEKEEPING
### Fix Inconsistencies
- [ ] Fix "untouched digest_buffer" → clarify rename
- [ ] Fix "nano_hash as baseline" → clarify prior work
- [ ] Fix WNS corner labeling (state worst corner)
- [ ] Fix Verilator version (print actual version)
- [ ] Unify authorship strings

### Cleanup
- [ ] `git rm --cached` tracked logs
- [ ] Commit 5 cocotb result XMLs
- [ ] Add streaming back-to-back test
- [ ] Create cleaned U8 failure log in `docs/evidence/`
- [ ] Remove vendored irrelevant files from package

## 6. VERIFICATION & PR
- [ ] Run `check_package.sh` - passes all checks
- [ ] Fresh Colab test of notebook top-to-bottom
- [ ] All images present and display correctly
- [ ] No local paths leaked
- [ ] Only `ISSCC27/submitted_notebooks/hashpareto/` changed in PR
- [ ] Tag `isscc27-submission`
- [ ] Open PR by Thu 2026-10-29
