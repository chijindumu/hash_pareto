#!/usr/bin/env bash
# Capture exact tool versions + artifact hashes for the HashPareto reproducibility record.
set +e

APPIMAGE="$HOME/librelane-devshell-x86_64.AppImage"

echo "===== ARTIFACT HASHES ====="
echo "appimage_sha256: $(sha256sum "$APPIMAGE" | cut -d' ' -f1)"
echo "appimage_bytes:  $(stat -c %s "$APPIMAGE")"
echo "sky130_pdk_hash: $(basename "$(dirname "$(dirname "$(find "$HOME/.ciel/ciel/sky130/versions" -maxdepth 1 -mindepth 1 -type d | head -1)")")")"
echo

echo "===== TOOL VERSIONS (inside devshell) ====="
printf '%s\n' \
 'librelane --version 2>&1 | head -2' \
 'echo "---yosys---"; yosys -V' \
 'echo "---openroad---"; openroad -version' \
 'echo "---magic---"; magic --version 2>&1 | head -2' \
 'echo "---klayout---"; klayout -v 2>&1 | head -2' \
 'echo "---netgen---"; netgen -batch version 2>&1 | head -3' \
 'echo "---python---"; python3 --version' \
 'echo "---verilator---"; verilator --version 2>&1 | head -1' \
 'echo "---iverilog---"; iverilog -V 2>&1 | head -1' \
 'exit' \
 | timeout 180 script -qec "$APPIMAGE" /dev/null 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;?]*[a-zA-Z]//g'
echo
echo "===== END ====="
