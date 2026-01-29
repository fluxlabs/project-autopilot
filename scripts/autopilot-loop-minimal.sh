#!/bin/bash
# Minimal Autopilot Loop - bare bones version
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "Starting autopilot loop in: $PROJECT_DIR"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "--- $(date) ---"

    # Run Claude with resume command
    claude --yes -p "/autopilot:resume"

    # Check if completed
    if grep -q "Status: completed" .autopilot/checkpoint.md 2>/dev/null; then
        echo "Project completed!"
        break
    fi

    echo "Restarting in 3s..."
    sleep 3
done
