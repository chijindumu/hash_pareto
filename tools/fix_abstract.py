import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
# Fix Cell 3 (the title page abstract section)
# Replace the abstract with standardized format

new_abstract = """# HashPareto — a notebook-driven PPA explorer for an open SHA-256 core\n\n",
"Copyright 2026 Benjamin Joshua Chimbuchi\n",
"SPDX-License-Identifier: Apache-2.0\n",
"\n",
"| Name | Affiliation | IEEE Member | SSCS Member | Email |\n",
"|------|-------------|------------|-------------|-------|\n",
"| Benjamin Joshua Chimbuchi | University of Ibadan | No | No | joshuabenjamin852@gmail.com |\n",
"\n",
"## Abstract\n",
"\n",
"Unrolling the SHA-256 round loop is the textbook area↔throughput knob. We test this on an open RTL-to-GDS flow (LibreLane, SKY130) with a parameterized core (UNROLL ∈ {1,2,4,8,16}). We replace the usual closed-form model (`64/UNROLL` cycles/block) with cycle-accurate measurements of the synthesized RTL, which show the core becomes input-bound at ≈18 cycles/block (32-bit stream interface) for UNROLL ≥ 4. Hardening each variant at its own closed-timing clock reveals that unrolling beyond 4× incurs area overhead without throughput benefit — the knee of the Pareto curve is U4. All results (verification, cycle measurement, synthesis, Pareto analysis) are reproducible from committed data; the full flow runs on WSL2+LibreLane+SKY130. This notebook provides a three-tier framework (instant verification, measured performance, opt-in full flow) so judges can engage at their preferred depth.",
"\n",
"## Contents\n",
"\n",
"1. [Environment](#1-environment)\n",
"2. [Related work](#2-related-work)\n",
"3. [Design: one core, five variants](#3-the-design-one-core-five-variants)\n",
"4. [Functional verification: 25/25 bit-exact](#4-functional-verification-2525-bit-exact)\n",
"5. [Physical implementation: LibreLane on SKY130](#5-physical-implementation-librelane-on-sky130)\n",
"6. [Throughput and energy model](#6-throughput-and-energy-model)\n",
"7. [What the data says](#7-what-the-data-says)\n",
"8. [Conclusion](#8-conclusion)\n",
"9. [Limitations & future work](#9-limitations--future-work)\n",
"10. [How to reproduce everything](#10-how-to-reproduce-everything)\n",
"11. [References](#11-references)\n",
]
# Replace cells[3] source with new abstract
c = nb['cells'][3]
c['source'] = [line + '\n' for line in new_abstract.splitlines()]
print('Abstract updated')
" 2>&1 | tail -5