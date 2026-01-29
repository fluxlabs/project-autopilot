#!/bin/bash
# Autopilot Continuous Execution Loop
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>
#
# Wraps Claude Code to enable autonomous context-clearing and resumption.
# When Claude checkpoints and exits, this script automatically restarts.

set -e

# Configuration
PROJECT_DIR="${1:-.}"
MAX_ITERATIONS="${MAX_ITERATIONS:-100}"
COOLDOWN_SECONDS="${COOLDOWN_SECONDS:-3}"
LOG_FILE="${LOG_FILE:-autopilot-loop.log}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# State
ITERATION=0
STARTED_AT=$(date +%s)

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "$msg"
    echo "$msg" >> "$LOG_FILE"
}

cleanup() {
    log "${YELLOW}Loop interrupted. Ran $ITERATION iterations.${NC}"
    local ended_at=$(date +%s)
    local duration=$((ended_at - STARTED_AT))
    log "Total runtime: $((duration / 60))m $((duration % 60))s"
    exit 0
}

trap cleanup SIGINT SIGTERM

check_prerequisites() {
    if ! command -v claude &> /dev/null; then
        log "${RED}Error: 'claude' CLI not found in PATH${NC}"
        exit 1
    fi

    if [[ ! -d "$PROJECT_DIR" ]]; then
        log "${RED}Error: Project directory '$PROJECT_DIR' not found${NC}"
        exit 1
    fi
}

get_checkpoint_status() {
    local checkpoint_file="$PROJECT_DIR/.autopilot/checkpoint.md"
    if [[ -f "$checkpoint_file" ]]; then
        grep -E "^## (Phase|Task)" "$checkpoint_file" 2>/dev/null | head -2 || echo "Unknown"
    else
        echo "No checkpoint"
    fi
}

run_claude() {
    local mode="$1"
    local prompt=""

    case "$mode" in
        "start")
            prompt="$AUTOPILOT_PROMPT"
            ;;
        "resume")
            prompt="/autopilot:cockpit"
            ;;
    esac

    log "${BLUE}Starting Claude (mode: $mode)${NC}"
    log "Checkpoint: $(get_checkpoint_status)"

    # Run Claude and capture exit code
    # Using --yes to auto-approve safe operations
    cd "$PROJECT_DIR"

    if claude --yes -p "$prompt" 2>&1 | tee -a "$LOG_FILE"; then
        return 0
    else
        return $?
    fi
}

detect_completion() {
    # Check if project is marked complete
    local checkpoint_file="$PROJECT_DIR/.autopilot/checkpoint.md"
    if [[ -f "$checkpoint_file" ]]; then
        if grep -q "Status: completed" "$checkpoint_file" 2>/dev/null; then
            return 0
        fi
    fi

    # Check global history for completion
    local history_file="$HOME/.claude/autopilot/history.json"
    if [[ -f "$history_file" ]]; then
        local project_name=$(basename "$PROJECT_DIR")
        if grep -q "\"$project_name\".*\"completed\"" "$history_file" 2>/dev/null; then
            return 0
        fi
    fi

    return 1
}

main() {
    check_prerequisites

    log "${GREEN}=== Autopilot Continuous Loop ===${NC}"
    log "Project: $PROJECT_DIR"
    log "Max iterations: $MAX_ITERATIONS"
    log "Cooldown: ${COOLDOWN_SECONDS}s"
    log ""

    # Determine starting mode
    local mode="resume"
    if [[ ! -f "$PROJECT_DIR/.autopilot/checkpoint.md" ]]; then
        if [[ -z "$AUTOPILOT_PROMPT" ]]; then
            log "${RED}No checkpoint found and AUTOPILOT_PROMPT not set.${NC}"
            log "Either:"
            log "  1. Run /autopilot:takeoff first to create initial checkpoint"
            log "  2. Set AUTOPILOT_PROMPT='your project description'"
            exit 1
        fi
        mode="start"
    fi

    while [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
        ITERATION=$((ITERATION + 1))

        log ""
        log "${GREEN}━━━ Iteration $ITERATION/$MAX_ITERATIONS ━━━${NC}"

        # Run Claude
        run_claude "$mode"
        local exit_code=$?

        log "Claude exited with code: $exit_code"

        # Check if project completed
        if detect_completion; then
            log "${GREEN}✓ Project completed!${NC}"
            break
        fi

        # After first run, always resume
        mode="resume"

        # Cooldown before restart
        log "Cooling down for ${COOLDOWN_SECONDS}s..."
        sleep "$COOLDOWN_SECONDS"
    done

    if [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
        log "${YELLOW}Reached maximum iterations ($MAX_ITERATIONS)${NC}"
    fi

    log ""
    log "${GREEN}=== Loop Complete ===${NC}"
    log "Total iterations: $ITERATION"
}

# Show usage if --help
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    cat << 'EOF'
Autopilot Continuous Execution Loop

Usage:
    ./autopilot-loop.sh [project_dir]

Environment Variables:
    AUTOPILOT_PROMPT    Initial prompt for /autopilot:takeoff (required if no checkpoint)
    MAX_ITERATIONS      Maximum loop iterations (default: 100)
    COOLDOWN_SECONDS    Pause between iterations (default: 3)
    LOG_FILE            Log file path (default: autopilot-loop.log)

Examples:
    # Resume existing project
    ./autopilot-loop.sh /path/to/project

    # Start new project
    AUTOPILOT_PROMPT="Build a REST API with user auth" ./autopilot-loop.sh .

    # With custom limits
    MAX_ITERATIONS=50 COOLDOWN_SECONDS=5 ./autopilot-loop.sh .

The loop will:
    1. Run Claude with /autopilot:cockpit (or initial prompt)
    2. When Claude exits (context full/checkpoint), wait and restart
    3. Repeat until project completes or max iterations reached

Press Ctrl+C to stop the loop gracefully.
EOF
    exit 0
fi

main "$@"
