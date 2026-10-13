#!/usr/bin/env bash
# Poll a running librelane variant run until final/metrics.json appears,
# the process dies, or a wallclock limit is reached.
# usage: tools/poll_run.sh <run_dir> <process_match> [max_polls]
set -u
RUN="$1"
MATCH="$2"
MAX="${3:-20}"
i=0
while [ "$i" -lt "$MAX" ]; do
  i=$((i + 1))
  if [ -f "$RUN/final/metrics.json" ]; then
    echo "POLL: DONE -- final/metrics.json present"
    break
  fi
  if ! pgrep -f "$MATCH" >/dev/null 2>&1; then
    echo "POLL: no process matching '$MATCH'"
    break
  fi
  STEP=$(ls "$RUN" 2>/dev/null | grep -E '^[0-9]' | tail -1)
  echo "POLL $(date +%H:%M:%S): ${STEP:-<listing empty>}"
  sleep 45
done
if [ -f "$RUN/final/metrics.json" ]; then
  echo "--- final metrics excerpt ---"
  grep -E '"design__instance__count__stdcell"|"design__instance__area__stdcell"|"power__total"|"timing__setup__wns"' \
    "$RUN/final/metrics.json" | tr -d '\r'
fi