#!/usr/bin/env bash
# Verify the notebook's code cells execute cleanly in the pinned venv.
set -e
cd "$(dirname "$0")/.."
PY=~/venv/bin/python
"$PY" - <<'PYEOF'
import json
from pathlib import Path

nb = json.load(open("notebook/hashpareto.ipynb"))
code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
src = "\n\n".join("".join(c["source"]) for c in code_cells)

# Execute as if CWD were notebook/ (worst case for the ROOT fallback).
import os, tempfile
os.chdir("notebook")
try:
    exec(compile(src, "<notebook>", "exec"), {})
finally:
    os.chdir("..")
print("NOTEBOOK_CELLS_OK", len(code_cells), "code cells")
PYEOF
