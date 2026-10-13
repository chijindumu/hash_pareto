#!/usr/bin/env bash
set -u
R="/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/runs/run_u1"
cd "$R"
echo "=== last 12 run dirs ==="
ls -1 | tail -12
echo "=== final/ ==="
ls -1 final 2>/dev/null | head
echo "=== metrics timing (nom_tt) ==="
grep -E "timing__(setup|hold)__(ws|wns)__corner:nom_tt_025C_1v80|timing__setup_vio__count__corner:nom_tt_025C_1v80|design__instance__count|design__instance__area|power__total" final/metrics.json 2>/dev/null
echo "=== last Running steps ==="
grep -oE "Running '[^']+'" flow.log | tr -d '\r' | tail -10