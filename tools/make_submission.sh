#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKG="$ROOT/submission/ISSCC27/submitted_notebooks/hashpareto"
rm -rf "$PKG" && mkdir -p "$PKG"
rsync -a --exclude='runs/' --exclude='*.log' --exclude='__pycache__/' \
  "$ROOT/LICENSE" "$ROOT/NOTICE" "$ROOT/requirements.txt" "$ROOT/docs" "$ROOT/rtl" \
  "$ROOT/verif" "$ROOT/flow" "$ROOT/tools" "$PKG/"
mkdir -p "$PKG/data"; cp -r "$ROOT/results/"* "$PKG/data/"; cp -r "$ROOT/data/vectors" "$PKG/data/"
cp "$ROOT/notebook/hashpareto.ipynb" "$PKG/hashpareto.ipynb"
cp "$ROOT/docs/PACKAGE_README.md" "$PKG/README.md"
echo "package built -> $PKG"