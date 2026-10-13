#!/usr/bin/env bash
set -u
mkdir -p /tmp/yprobe
cp /mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/src/digest_buffer.sv /tmp/yprobe/db_renamed.sv
sed -i 's/\bdigest_buffer\b/wbuf/g' /tmp/yprobe/db_renamed.sv
sed -i 's/^module wbuf/module digest_buffer/' /tmp/yprobe/db_renamed.sv
echo "--- head of renamed ---"
head -13 /tmp/yprobe/db_renamed.sv
echo "--- yosys ---"
yosys -Q -p "read_verilog -sv /tmp/yprobe/db_renamed.sv; hierarchy -auto-top" 2>&1 | tr -d '\r' | grep -Ei 'error|IndexError|exception|Generating RTLIL|abort' | tail -8
echo "--- original for comparison ---"
yosys -Q -p "read_verilog -sv /mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/flow/variants/u1/src/digest_buffer.sv; hierarchy -auto-top" 2>&1 | tr -d '\r' | grep -Ei 'error|IndexError|exception|Generating RTLIL|abort' | tail -8