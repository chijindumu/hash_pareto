#!/usr/bin/env bash
set +e

echo "verilator: $(verilator --version 2>&1 | head -1)"
echo "iverilog:  $(iverilog -V 2>&1 | head -1)"
echo

~/venv/bin/python - <<'PY'
import cocotb
print("cocotb", cocotb.__version__)
try:
    import cocotb_tools.runner as r
    print("cocotb_tools.runner:", r.__file__)
    print("public:", [x for x in dir(r) if not x.startswith("_")])
except Exception as e:
    print("runner import failed:", repr(e))
try:
    from cocotb_tools.runner import get_runner
    import inspect
    print("get_runner sig:", inspect.signature(get_runner))
except Exception as e:
    print("get_runner failed:", repr(e))
try:
    from cocotb_tools.runner import Simulator
    print("Simulator:", [x.name for x in Simulator])
except Exception as e:
    print("Simulator failed:", repr(e))
PY
