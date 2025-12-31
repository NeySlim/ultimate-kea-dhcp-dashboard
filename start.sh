#!/bin/bash
# Start Ultimate Dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASHBOARD_BIN="$SCRIPT_DIR/bin/ultimate-dashboard"

if [ ! -f "$DASHBOARD_BIN" ]; then
    echo "Error: Dashboard script not found at $DASHBOARD_BIN"
    exit 1
fi

echo "Starting Ultimate Dashboard..."
python3 "$DASHBOARD_BIN"
