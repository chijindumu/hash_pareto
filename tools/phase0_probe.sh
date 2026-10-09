#!/usr/bin/env bash
# Phase 0 environment probe for HashPareto.
# Determines how to invoke LibreLane reproducibly on this machine.
set +e

APPIMAGE="$HOME/librelane-devshell-x86_64.AppImage"

echo "===== PHASE0 PROBE ====="
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "user: $(whoami)"
echo

echo "----- running AppImage / flow processes -----"
ps -eo pid,etime,rss,cmd | grep -iE 'appimage|librelane|openroad|yosys|magic|klayout' | grep -v grep
echo

echo "----- appimage help / options -----"
"$APPIMAGE" --appimage-help 2>&1 | head -40
echo

echo "----- attempt: pipe commands via pty (script) -----"
printf 'echo MARKER_INSIDE; command -v librelane; librelane --version; echo MARKER_DONE; exit\n' \
  | timeout 120 script -qec "$APPIMAGE" /dev/null 2>&1 | tr -d '\r' | sed -n '1,60p'
echo

echo "----- locale / pkg available for extraction -----"
command -v unsquashfs || echo "no unsquashfs"
echo

echo "----- sky130 pdk root -----"
find "$HOME/.ciel/ciel/sky130/versions" -maxdepth 2 -type d 2>/dev/null | sed -n '1,10p'
echo

echo "===== END PROBE ====="
