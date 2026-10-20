#!/usr/bin/env bash
# Run inspect_slack.py
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/inspect_slack.py
