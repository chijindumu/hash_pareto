import json
nb = json.load(open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb'))
# Cell 3 contains: title line + copyright code block + team table + Abstract heading + abstract text
# We need to replace only the abstract portion while keeping everything else

c = nb['cells'][3]
s = ''.join(c['source'])

# Find and replace the abstract text
# The abstract starts after "## Abstract" and ends before "## Contents"
import re
# Split on the TOC marker
parts = s.split('## Contents')
if len(parts) == 2:
    before_toc = parts[0]
    # The abstract is between "## Abstract" and the team table/data
    # Let's find the abstract text
    abstract_start = '## Abstract'
    # Rebuild: keep everything before abstract, new abstract, then TOC
    
    new_abstract = """>**Unrolling the SHA-256 round loop is the textbook area↔throughput knob.** We test this on an open RTL-to-GDS flow (LibreLane, SKY130) with a parameterized core (UNROLL ∈ {1,2,4,8,16}). We replace the usual closed-form model (`64/UNROLL` cycles/block) with **cycle-accurate measurements** of the synthesized RTL, which show the core becomes **input-bound at ≈18 cycles/block** (32-bit stream interface) for UNROLL ≥ 4. Hardening each variant at its own **closed-timing clock** reveals that unrolling beyond 4× incurs area overhead without throughput benefit — the **knee of the Pareto curve is U4**. All results (verification, cycle measurement, synthesis, Pareto analysis) are reproducible from committed data; the full flow runs on WSL2+LibreLane+SKY130. This notebook provides a **three-tier framework** (instant verification, measured performance, opt-in full flow) so judges can engage at their preferred depth."""
    
    # Replace the abstract section
    # Find "## Abstract" and new_abstract, then "## Contents"
    new_s = before_toc.replace(
        abstract_start + new_abstract + "## Contents",
        abstract_start + new_abstract
    )
    # Actually this is getting complicated. Let me just replace the specific abstract text.
    
    # Simpler: find the abstract text and replace it
    old_abstract_marker = '## Abstract\n\nHashPareto parameterizes a verified SystemVerilog SHA-256 core by round unrolling'
    new_abstract_text = '## Abstract\n\n**Unrolling the SHA-256 round loop is the textbook area↔throughput knob.** We test this on an open RTL-to-GDS flow (LibreLane, SKY130) with a parameterized core (UNROLL ∈ {1,2,4,8,16}). We replace the usual closed-form model (`64/UNROLL` cycles/block) with **cycle-accurate measurements** of the synthesized RTL, which show the core becomes **input-bound at ≈18 cycles/block** (32-bit stream interface) for UNROLL ≥ 4. Hardening each variant at its own **closed-timing clock** reveals that unrolling beyond 4× incurs area overhead without throughput benefit — the **knee of the Pareto curve is U4**. All results (verification, cycle measurement, synthesis, Pareto analysis) are reproducible from committed data; the full flow runs on WSL2+LibreLane+SKY130. This notebook provides a **three-tier framework** (instant verification, measured performance, opt-in full flow) so judges can engage at their preferred depth.'
    
    if old_abstract_marker in s:
        s = s.replace(old_abstract_marker, new_abstract_text)
        c['source'] = [line + '\n' for line in s.splitlines()]
        print('Abstract updated')
    else:
        print('Abstract marker not found, trying alternative')
        # Try finding any abstract text
        for i, line in enumerate(s.split('\n')):
            if 'HashPareto parameterizes' in line:
                print(f'Found at line {i}: {line[:80]}')
                break
else:
    print('Could not split on TOC')
    
with open('/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.ipynb','w') as f:
    json.dump(nb,f,indent=1)
print('done')