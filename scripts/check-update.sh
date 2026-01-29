#!/bin/bash
# Project Autopilot - Version Check Script
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Get installed version from local plugin.json
PLUGIN_DIR="${CLAUDE_PLUGIN_DIR:-$HOME/.claude/plugins/autopilot}"
LOCAL_VERSION=$(grep -o '"version": *"[^"]*"' "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')

if [ -z "$LOCAL_VERSION" ]; then
  # Try alternate location
  LOCAL_VERSION=$(grep -o '"version": *"[^"]*"' "$PLUGIN_DIR/plugin.json" 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
fi

if [ -z "$LOCAL_VERSION" ]; then
  echo "autopilot: Could not determine installed version"
  exit 1
fi

# Fetch remote version from GitHub (raw plugin.json)
REMOTE_VERSION=$(curl -s --max-time 5 "https://raw.githubusercontent.com/fluxlabs/project-autopilot/main/.claude-plugin/plugin.json" 2>/dev/null | grep -o '"version": *"[^"]*"' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')

if [ -z "$REMOTE_VERSION" ]; then
  # Network issue or rate limit - skip silently
  exit 0
fi

# Compare versions
if [ "$LOCAL_VERSION" != "$REMOTE_VERSION" ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔄 Autopilot update available: v$LOCAL_VERSION → v$REMOTE_VERSION"
  echo "   Run: /plugin update autopilot"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
fi
