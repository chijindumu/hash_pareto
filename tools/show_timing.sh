#!/usr/bin/env bash
set -u
R="/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/runs/run_u1"
for c in nom_ff_n40C_1v95 nom_ss_100C_1v60 nom_tt_025C_1v80; do
  echo "== prePNR $c =="
  grep -E "period_min|fmax" "$R/12-openroad-staprepnr/$c/sta.log" | tr -d '\r' | tail -2
done
echo "== postPNR nom_tt =="
grep -E "period_min|fmax" "$R/56-openroad-stapostpnr/nom_tt_025C_1v80/sta.log" | tr -d '\r' | tail -2
echo "== postPNR nom_ss =="
grep -E "period_min|fmax" "$R/56-openroad-stapostpnr/nom_ss_100C_1v60/sta.log" | tr -d '\r' | tail -2