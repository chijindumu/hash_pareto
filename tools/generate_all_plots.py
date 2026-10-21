#!/usr/bin/env python3
"""Generate all possible plots for HashPareto submission richness."""
import json, os, sys
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RES = ROOT .parent / "results"

# Load data
met = pd.read_csv(RES / "metrics.csv")
cyc = pd.read_csv(DATA / "cycles.csv").set_index("unroll")["cycles_per_block"]
met["cycles_per_block"] = met["unroll"].map(cyc)
met["f_mhz"] = 1000.0 / met["clock_period_ns"]
met["throughput_Mhash_s"] = met["f_mhz"] / met["cycles_per_block"]
met["energy_nJ"] = met["power_W"] * met["cycles_per_block"] * met["clock_period_ns"]
met["area_um2"] = met["area_stdcell_um2"]

# Pick timing-closed runs for fair comparison
met_closed = met[met["setup_ws_worst_ns"].astype(float) >= 0].copy()

outputs = ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "data"

def save_fig(fig, name):
    fig.savefig(outputs / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {name}")

# 1. Pareto area vs throughput (already exist, regenerate for high-res)
fig, ax = plt.subplots(figsize=(7, 5))
for u in sorted(met_closed.unroll.unique()):
    subset = met_closed[met_closed.unroll == u]
    ax.plot(subset.throughput_Mhash_s, subset.area_um2 / 1e3, 'o-', label=f'U{u}', markersize=8, linewidth=2)
ax.plot([r.throughput_Mhash_s for r in json.load(open(ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "pareto.csv", ))], [r.area_um2 / 1e3 for r in json.load(open(ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "pareto.csv", )))], 'k--', alpha=0.5, lw=1)
ax.scatter([r.throughput_Mhash_s for r in json.load(open(ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "pareto.csv", )))], [r.area_um2 / 1e3 for r in json.load(open(ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "pareto.csv", )))], s=80, zorder=3, color='darkred')
for _, r in json.load(open(ROOT.parent / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "pareto.csv", )).iterrows():
    ax.annotate(f'U{int(r.unroll)}', (r.throughput_Mhash_s, r.area_um2 / 1e3), textcoords="offset points", xytext=(8, 4))
ax.set_xlabel("Throughput (Mhash/s)", fontsize=12)
ax.set_ylabel("Stdcell area (1k μm²)", fontsize=12)
ax.set_title("HashPareto: Area vs Throughput (SKY130, Timing-Closed)", fontsize=14, fontweight='bold')
ax.grid(alpha=0.3, linestyle='--')
ax.legend(fontsize=11)
save_fig(fig, "pareto_area_vs_throughput.png")

# 2. Pareto energy vs throughput
fig, ax = plt.subplots(figsize=(7, 5))
for u in sorted(met_closed.unroll.unique()):
    subset = met_closed[met_closed.unroll == u]
    ax.plot(subset.throughput_Mhash_s, subset.energy_nJ, 's-', label=f'U{u}', markersize=8, linewidth=2)
# Plot committed points
ref = pd.read_csv(ROOT / "submission" / "ISSCC27" / "submitted_notebooks" / "hashpareto" / "data" / "pareto.csv")
for _, r in ref.iterrows():
    ax.scatter(r.throughput_Mhash_s, r.energy_per_hash_nJ, s=80, zorder=3, color='darkred', marker='*')
for _, r in ref.iterrows():
    ax.annotate(f'U{int(r.unroll)}', (r.throughput_Mhash_s, r.energy_per_hash_nJ), textcoords="offset points", xytext=(8, 4))
ax.set_xlabel("Throughput (Mhash/s)", fontsize=12)
ax.set_ylabel("Energy per hash (nJ)", fontsize=12)
ax.set_title("HashPareto: Energy per Hash vs Throughput (SKY130, Timing-Closed)", fontsize=14, fontweight='bold')
ax.grid(alpha=0.3, linestyle='--')
ax.legend(fontsize=11)
save_fig(fig, "pareto_energy_vs_throughput.png")

# 3. Cycles per block bar chart
fig, ax = plt.subplots(figsize=(6, 4))
unrolls = sorted(met.unroll.unique())
cycles = [met[met.unroll == u].cycles_per_block.mean() for u in unrolls]
ax.bar(unrolls, cycles, color=['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860'][::len(unrolls)//5])
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Cycles per 512-bit block", fontsize=12)
ax.set_title("Measured Cycles per Block by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(cycles):
    ax.text(unrolls[i], v + 0.5, f'{v:.1f}', ha='center', fontsize=11, fontweight='bold')
save_fig(fig, "cycles_per_block_bar.png")

# 4. Throughput comparison bar chart
fig, ax = plt.subplots(figsize=(6, 4))
throughputs = [met_closed[met_closed.unroll == u].throughput_Mhash_s.mean() for u in unrolls]
ax.bar(unrolls, throughputs, color=['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860'][::len(unrolls)//5])
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Throughput (Mhash/s)", fontsize=12)
ax.set_title("Timing-Closed Throughput by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(throughputs):
    ax.text(unrolls[i], v + 0.02, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
save_fig(fig, "throughput_bar.png")

# 5. Energy per hash bar chart
fig, ax = plt.subplots(figsize=(6, 4))
energies = [met_closed[met_closed.unroll == u].energy_nJ.mean() for u in unrolls]
ax.bar(unrolls, energies, color=['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860'][::len(unrolls)//5])
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Energy per hash (nJ)", fontsize=12)
ax.set_title("Timing-Closed Energy per Hash by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(energies):
    ax.text(unrolls[i], v + 0.1, f'{v:.2f}', ha='center', fontsize=11, fontweight='bold')
save_fig(fig, "energy_bar.png")

# 6. Power comparison bar chart
fig, ax = plt.subplots(figsize=(6, 4))
powers = [met_closed[met_closed.unroll == u].power_W.mean() * 1000 for u in unrolls]  # mW
ax.bar(unrolls, powers, color=['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860'][::len(unrolls)//5])
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Power (mW)", fontsize=12)
ax.set_title("Timing-Closed Power by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(powers):
    ax.text(unrolls[i], v + 0.5, f'{v:.1f}', ha='center', fontsize=11, fontweight='bold')
save_fig(fig, "power_bar.png")

# 7. Area comparison bar chart
fig, ax = plt.subplots(figsize=(6, 4))
areas = [met_closed[met_closed.unroll == u].area_um2.mean() for u in unrolls]
ax.bar(unrolls, areas, color=['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860'][::len(unrolls)//5])
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Area (μm²)", fontsize=12)
ax.set_title("Timing-Closed Area by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(areas):
    ax.text(unrolls[i], v + 5000, f'{v/1e3:.1f}k', ha='center', fontsize=11, fontweight='bold')
save_fig(fig, "area_bar.png")

# 8. Critical path vs UNROLL (estimated from timing data)
fig, ax = plt.subplots(figsize=(6, 4))
# Estimate critical period from worst slack
periods = met_closed.groupby('unroll')['clock_period_ns'].first().values
ws = met_closed.groupby('unroll')['setup_ws_worst_ns'].first().values
ax.plot(unrolls, periods, 'o-', color='#4c72b0', markersize=8, linewidth=2, label='Clock period')
ax.set_xlabel("UNROLL", fontsize=12)
ax.set_ylabel("Clock period (ns)", fontsize=12)
ax.set_title("Critical Path: Clock Period by Unroll", fontsize=14, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3, linestyle='--')
for i, v in enumerate(periods):
    ax.text(unrolls[i], v + 2, f'{v:.1f} ns', ha='center', fontsize=11, fontweight='bold')
ax.legend()
save_fig(fig, "critical_path.png")

# 9. SHA-256 round structure diagram (text-based visual)
# Create a simple visual showing 64 rounds organized by unroll
fig, ax = plt.subplots(figsize=(8, 2))
colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b3', '#937860']
for i, u in enumerate(unrolls):
    nchunks = 64 // u
    # Draw rounds as horizontal blocks
    for r in range(nchunks):
        ax.add_patch(plt.Rectangle((r * 0.12, 0.3), 0.1, 0.4, facecolor=colors[i % len(colors)], edgecolor='black'))
    # Label
    ax.text(0.02, 0.5 - i * 0.6, f'U{u}: {64//u} rounds/cycle', fontsize=10, fontweight='bold', va='center')
ax.set_xlim(0, 2.5)
ax.set_ylim(0, 3)
ax.axis('off')
ax.set_title('SHA-256 Round Structure by Unroll', fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "sha256_round_structure.png")

# 10. Three-tier framework illustration
fig, ax = plt.subplots(figsize=(8, 3))
# Tier 0 - Instant
ax.add_patch(plt.Rectangle((0, 2), 2, 0.8, facecolor='#4c72b0', edgecolor='black'))
ax.text(1, 2.4, 'TIER 0\nInstant', ha='center', fontsize=11, fontweight='bold', color='white')
ax.add_patch(plt.Rectangle((3, 2), 2, 0.8, facecolor='#55a868', edgecolor='black'))
ax.text(4, 2.4, 'TIER 1\nVerify & Measure', ha='center', fontsize=11, fontweight='bold', color='white')
ax.add_patch(plt.Rectangle((6, 2), 2, 0.8, facecolor='#c44e52', edgecolor='black'))
ax.text(7, 2.4, 'TIER 2\nFull Flow', ha='center', fontsize=11, fontweight='bold', color='white')
# Arrows
ax.annotate('', xy=(2.5, 2.4), xytext=(2.5, 2.7), arrowprops=dict(arrowstyle='->', color='black'))
ax.annotate('', xy=(4.5, 2.4), xytext=(4.5, 2.7), arrowprops=dict(arrowstyle='->', color='black'))
ax.set_xlim(0, 9)
ax.set_ylim(0, 4)
ax.axis('off')
ax.set_title('HashPareto Three-Tier Reproducibility Framework', fontsize=13, fontweight='bold', pad=20)
save_fig(fig, "three_tier_framework.png")

# 11. Timeline: ingest vs compression overlap (for U4 example)
fig, ax = plt.subplots(figsize=(8, 2))
u = 4
cycles_per_block = met_closed[met_closed.unroll == u].cycles_per_block.mean()
ingest_cycles = 18  # 16 beats + overhead
comp_cycles = 64 // u + 2  # round comb + control
total = cycles_per_block
# Draw overlapping bars
for b in range(3):  # show 3 blocks
    t0 = b * cycles_per_block
    ax.add_patch(plt.Rectangle((t0, 0.3), ingest_cycles, 0.4, facecolor='#55a868', alpha=0.7, label='Ingest' if b == 0 else ''))
    ax.add_patch(plt.Rectangle((t0 + ingest_cycles, 0.3), comp_cycles, 0.4, facecolor='#c44e52', alpha=0.7, label='Compression' if b == 0 else ''))
ax.set_xlabel('Cycles', fontsize=12)
ax.set_ylim(0, 1)
ax.set_title(f'SHA-256 Ingest/Compression Overlap (U={u}, {cycles_per_block} cycles/block)', fontsize=13, fontweight='bold')
ax.set_xticks(ticks=[0, cycles_per_block*1, cycles_per_block*2], labels=['Block 0', 'Block 1', 'Block 2'])
save_fig(fig, "ingest_compression_timeline.png")

print("\nAll plots generated successfully!")
print(f"Output directory: {outputs}")
PY
 2>&1