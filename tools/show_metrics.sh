#!/usr/bin/env bash
set -u
M="/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/runs/run_u1/final/metrics.json"
echo "=== DRC / LVS / antenna ==="
grep -E "drc__|lvs__|antenna__|magic__|klayout__|xor__" "$M" | head -40
echo "=== gds present? ==="
ls -la /mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/runs/run_u1/final/gds/