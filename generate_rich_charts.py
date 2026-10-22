#!/usr/bin/env python3
"""Generate rich bar charts for HashPareto notebook."""
import json, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Key data from HashPareto
unrolls = [1, 2, 4, 16]
areas = [176750, 197497, 243908, 524671]   # μm²
throughputs = [0.149, 0.286, 0.526, 0.185]  # Mhash/s
energies = [16.94, 8.98, 4.96, 4.95]         # nJ
cycles = [67, 35, 19, 18]                    # cycles/block
power = [2.53, 2.57, 2.61, 0.92]             # mW

colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b3']

# Create figure with 2x3 subplot layout
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# --- Chart 1: Cycles per block ---
ax = axes[0, 0]
bars = ax.bar(unrolls, cycles, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('UNROLL', fontsize=11)
ax.set_ylabel('Cycles/block', fontsize=11)
ax.set_title('Steady-State Cycles per Block', fontsize=13, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, cycles):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(val), ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Chart 2: Throughput ---
ax = axes[0, 1]
bars = ax.bar(unrolls, throughputs, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('UNROLL', fontsize=11)
ax.set_ylabel('Throughput (Mhash/s)', fontsize=11)
ax.set_title('Throughput by Unroll Factor', fontsize=13, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, throughputs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Chart 3: Energy per hash ---
ax = axes[0, 2]
bars = ax.bar(unrolls, energies, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('UNROLL', fontsize=11)
ax.set_ylabel('Energy/hash (nJ)', fontsize=11)
ax.set_title('Energy per Hash by Unroll', fontsize=13, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, energies):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val:.2f} nJ', ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Chart 4: Area ---
ax = axes[1, 0]
area_k = [a/1000 for a in areas]
bars = ax.bar(unrolls, area_k, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('UNROLL', fontsize=11)
ax.set_ylabel('Area (kμm²)', fontsize=11)
ax.set_title('Standard-Cell Area by Unroll', fontsize=13, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, area_k):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Chart 5: Power ---
ax = axes[1, 1]
bars = ax.bar(unrolls, power, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('UNROLL', fontsize=11)
ax.set_ylabel('Power (mW)', fontsize=11)
ax.set_title('Power Consumption by Unroll', fontsize=13, fontweight='bold')
ax.set_xticks(unrolls)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, power):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f} mW', ha='center', va='bottom', fontsize=10, fontweight='bold')

# --- Chart 6: Knee point annotation ---
ax = axes[1, 2]
ax.annotate('KNEE\nU4 = optimal\n(unrolling beyond 4×\ndoes not pay)',
            xy=(4, 0.526), xytext=(2, 5.5),
            arrowprops=dict(arrowstyle='->', color='#c44e52', lw=2.5),
            fontsize=11, fontweight='bold', color='#c44e52',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#c44e52', alpha=0.9))
ax.set_xlim(0.5, 16.5)
ax.set_ylim(0, 6)
ax.set_xticks(unrolls)
ax.set_xlabel('UNROLL', fontsize=10)
ax.set_ylabel('Metric Value', fontsize=10)
ax.grid(alpha=0.3)

# Overall title
plt.suptitle('HashPareto: PPA Characterization by Unroll Factor', fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save to correct path
output_path = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/pareto_rich_bar_charts.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f'Saved rich bar charts: {output_path} ({Path(output_path).stat().st_size/1024:.1f} KB)')