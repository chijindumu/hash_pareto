#!/usr/bin/env bash
set -u
SRC=/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/src
for f in "$SRC"/digest_buffer.sv "$SRC"/message_padder.sv "$SRC"/sha256_core.sv "$SRC"/sha_top.sv; do
    echo "==== $(basename "$f") ===="
    out=$(timeout 180 yosys -Q -p "read_verilog -sv $f; hierarchy -auto-top" 2>&1)
    rc=$?
    echo "rc=$rc"
    echo "$out" | tr -d '\r' | grep -Ei 'error|Traceback|IndexError|exception|deriving|module `' | tail -10
done