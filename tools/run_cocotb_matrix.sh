#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
ROOT=$(pwd)
PY=/home/userchimbuchi/venv/bin/python

for u in 2 4 8 16; do
    echo "==== UNROLL=$u ===="
    "$PY" verif/cocotb/run.py --sim verilator --unroll "$u" 2>&1 | tr '\r' '\n' | grep -E 'PASS |FAIL |TESTS='
done