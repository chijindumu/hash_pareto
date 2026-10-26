#!/usr/bin/env python3
"""Generate Figures A4 and A5 for HashPareto appendix."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Data from metrics.csv (hard runs give tightest implied paths)
unrolls = [1, 2, 4, 16]
areas = [176750, 197497, 243908, 524671]   # um^2

# Implied critical path from hard runs (clock + |WNS| for failed runs)
# U1 hard20 @ 20ns WNS=-1.74 -> path ~21.7ns -> fmax ~46 MHz
# U2 hard35 @ 35ns WNS=-2.86 -> path ~37.9ns -> fmax ~26 MHz
# U4 hard70 @ 70ns WNS=-6.27 -> path ~76.3ns -> fmax ~13 MHz
# U16 grid300 @ 300ns WNS=+23.98 -> path ~276ns -> fmax ~3.6 MHz
fmax_mhz = [46.0, 26.0, 13.0, 3.6]

cycles = [67, 35, 19, 18]   # measured cycles per block

# Throughput at fmax: fmax_MHz / cycles (since Mhash/s = MHz / cycles_per_block)
throughput_at_fmax = [f / c for f, c in zip(fmax_mhz, cycles)]

# Fixed-100ns throughput for comparison
throughput_fixed = [0.149, 0.286, 0.526, 0.185]

colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b3']

# ============================================================
# FIGURE A4: Clock-normalized Pareto (throughput at fmax vs area)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: fixed-clock view (current published numbers)
ax = axes[0]
ax.scatter(throughput_fixed, [a / 1e3 for a in areas], s=150, c=colors,
           edgecolor='white', zorder=3, linewidth=2)
for u, t, a in zip(unrolls, throughput_fixed, areas):
    ax.annotate(f'U{u}', (t, a / 1e3), textcoords='offset points',
                xytext=(10, 4), fontweight='bold', fontsize=11)
ax.plot(throughput_fixed, [a / 1e3 for a in areas], '--', color='#9aa5b1', lw=1.5, alpha=0.6)
ax.set_xlabel('Throughput at 100 ns clock (Mhash/s)', fontsize=11)
ax.set_ylabel('Area (k µm²)', fontsize=11)
ax.set_title('Fixed-clock view (100 ns)', fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)

# Right: clock-normalized view (throughput at fmax)
ax = axes[1]
ax.scatter(throughput_at_fmax, [a / 1e3 for a in areas], s=150, c=colors,
           edgecolor='white', zorder=3, linewidth=2)
for u, t, a in zip(unrolls, throughput_at_fmax, areas):
    ax.annotate(f'U{u}', (t, a / 1e3), textcoords='offset points',
                xytext=(10, 4), fontweight='bold', fontsize=11)
ax.plot(throughput_at_fmax, [a / 1e3 for a in areas], '--', color='#9aa5b1', lw=1.5, alpha=0.6)
ax.set_xlabel('Throughput at fmax (Mhash/s)', fontsize=11)
ax.set_ylabel('Area (k µm²)', fontsize=11)
ax.set_title('Clock-normalized view (throughput at fmax)', fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)

fig.suptitle('Figure A4: Clock-normalized Pareto — throughput collapses above U4 once clock is relaxed',
             fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()

out_a4 = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/figures/fig_a4_clock_normalized.png'
os.makedirs(os.path.dirname(out_a4), exist_ok=True)
plt.savefig(out_a4, dpi=150, bbox_inches='tight')
print(f'Saved Figure A4: {out_a4}')

# ============================================================
# FIGURE A5: Per-variant fmax and clocking estimates
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

# Left: fmax by variant
ax = axes[0]
bars = ax.bar([f'U{u}' for u in unrolls], fmax_mhz, color=colors,
              edgecolor='black', alpha=0.85)
ax.set_ylabel('Fmax (MHz)', fontsize=11)
ax.set_title('Estimated fmax per variant', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, fmax_mhz):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f} MHz', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Middle: clock period required
clock_periods = [1000.0 / f for f in fmax_mhz]
ax = axes[1]
bars = ax.bar([f'U{u}' for u in unrolls], clock_periods, color=colors,
              edgecolor='black', alpha=0.85)
ax.set_ylabel('Clock period (ns)', fontsize=11)
ax.set_title('Clock period at fmax', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, clock_periods):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val:.0f} ns', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Right: throughput comparison (fixed clock vs fmax)
ax = axes[2]
x = range(len(unrolls))
w = 0.35
bars1 = ax.bar([i - w/2 for i in x], throughput_fixed, w, label='Fixed clock (100/300 ns)',
               color='#4c72b0', edgecolor='black', alpha=0.85)
bars2 = ax.bar([i + w/2 for i in x], throughput_at_fmax, w, label='At fmax',
               color='#c44e52', edgecolor='black', alpha=0.85)
ax.set_ylabel('Throughput (Mhash/s)', fontsize=11)
ax.set_title('Throughput: fixed clock vs fmax', fontsize=12, fontweight='bold')
ax.set_xticks(list(x))
ax.set_xticklabels([f'U{u}' for u in unrolls])
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars1, throughput_fixed):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar, val in zip(bars2, throughput_at_fmax):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

fig.suptitle('Figure A5: Clocking strategy — fmax drops sharply as unroll increases',
             fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()

out_a5 = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/data/figures/fig_a5_fmax_clocking.png'
plt.savefig(out_a5, dpi=150, bbox_inches='tight')
print(f'Saved Figure A5: {out_a5}')

print()
print('Summary data:')
for u, a, f, tf, taf in zip(unrolls, areas, fmax_mhz, throughput_fixed, throughput_at_fmax):
    print(f'  U{u}: area={a:,} um^2, fmax={f:.1f} MHz, fixed_throughput={tf:.3f} Mhash/s, fmax_throughput={taf:.3f} Mhash/s')