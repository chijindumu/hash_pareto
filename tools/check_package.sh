#!/usr/bin/env bash
set -euo pipefail
T=$(mktemp -d); cp -r submission/ISSCC27/submitted_notebooks/hashpareto "$T/p"; cd "$T/p"
echo "=== Checking for local paths ==="
grep -rInE '/mnt/c/|/home/user|C:\\\\Users|USER/Downloads' . --exclude-dir=.git --exclude='*.png' || { echo "OK: no local path leak"; }
echo "=== Checking required files ==="
test -f LICENSE && test -f README.md && test -f requirements.txt && echo "OK: LICENSE + README.md + requirements.txt present"
echo "=== Checking notebook execution ==="
~/venv/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=3600 hashpareto.ipynb --output executed.ipynb 2>&1 | tail -3
echo "=== Package size ==="
du -sh .;
echo "PACKAGE OK"