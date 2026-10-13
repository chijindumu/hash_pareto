#!/usr/bin/env bash
RD=/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto
echo "now: $(date '+%F %T %z')"
echo "--- librelane/openroad/wsl processes ---"
pgrep -fa 'run-tag|openroad|config.yaml' | grep -v "bash -lc" | cut -c1-140
echo "--- any python under nix store? ---"
pgrep -fa 'python3.*librelane' | grep -v grep | cut -c1-140
echo "--- grid.out.log last 8 (strip ansi) ---"
tail -8 "$RD/flow/grid.out.log" | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g;s/\x1b\]8;;[^\x1b]*\x1b\\//g' | grep -v '^\s*$' | tr -d '\r' | tail -8
echo "--- grid.err.log last 4 ---"
tail -4 "$RD/flow/grid.err.log" | tr -d '\r'
echo "--- step dirs in grid300 ---"
ls "$RD/flow/variants/u16/runs/grid300" | grep -E '^[0-9]' | tail -3
echo "--- 44 dir mtimes ---"
stat -c '%y %n' "$RD"/flow/variants/u16/runs/grid300/44-*/openroad-detailedrouting.log 2>/dev/null
echo "--- final? ---"
test -f "$RD/flow/variants/u16/runs/grid300/final/metrics.json" && echo FINAL_DONE || echo no_final_yet