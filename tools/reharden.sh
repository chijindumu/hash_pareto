#!/usr/bin/env bash
# A2 re-hardening: run each of U1/U2/U4 at a tightened clock to measure its own
# fmax-closed point. Sequential (one LibreLane job at a time: ~5.8 GiB RAM host).
# Writes runs into flow/variants/uN/runs/hard<period>/
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOGDIR="$ROOT/flow/redhard_logs"
mkdir -p "$LOGDIR"

run_one() {
  local U="$1" PERIOD="$2"
  local D="$ROOT/flow/variants/u$U"
  local TAG="hard${PERIOD//./p}"
  echo "==== U$U @ ${PERIOD} ns -> tag $TAG  ($(date -Is)) ===="
  # stage config
  sed -e "s/^CLOCK_PERIOD:.*/CLOCK_PERIOD: ${PERIOD}/" "$D/config.yaml" > "$D/config_${TAG}.yaml"
  cd "$D"
  bash "$ROOT/tools/run_librelane.sh" \
      "librelane config_${TAG}.yaml --run-tag $TAG --condensed" \
      > "$LOGDIR/u${U}_${TAG}.log" 2>&1
  local rc=$?
  echo "exit_code=$rc"
  echo "==== U$U @ ${PERIOD} ns done rc=$rc ($(date -Is)) ===="
  return $rc
}

# Order: cheapest / most informative first.
run_one 1 20 || true
run_one 2 35 || true
run_one 4 70 || true
run_one 1 30 || true
echo "ALL_DONE $(date -Is)"
