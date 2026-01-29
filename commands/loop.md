---
description: Start continuous autonomous execution loop that auto-restarts on context clear
argument-hint: [--background] [--max-iterations=N] [--cooldown=N] [--install]
model: sonnet
---

// Project Autopilot - Continuous Execution Loop
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Autopilot: LOOP Mode

Launch the continuous execution loop that automatically restarts Claude when context fills up. This enables fully autonomous project completion without manual intervention.

## Required Skills

**Read before starting:**
- `/autopilot/skills/token-optimization/SKILL.md` - Understand checkpoint triggers

---

## How It Works

```
┌─────────────────────────────────────────┐
│         autopilot-loop.sh               │
│                                         │
│  while not complete:                    │
│    ├─ claude -p "/autopilot:cockpit"    │
│    ├─ (Claude works until 40% context)  │
│    ├─ (Checkpoint saved, Claude exits)  │
│    ├─ sleep cooldown                    │
│    └─ restart loop                      │
│                                         │
└─────────────────────────────────────────┘
```

---

## Options

| Option | Description |
|--------|-------------|
| `--background` | Run loop in background (nohup), return control immediately |
| `--foreground` | Run loop in current terminal (default) |
| `--max-iterations=N` | Maximum restart cycles (default: 100) |
| `--cooldown=N` | Seconds between restarts (default: 3) |
| `--install` | Install loop script to ~/.local/bin for global access |
| `--status` | Check if loop is running |
| `--stop` | Stop background loop |
| `--quiet` | Suppress verbose output (CI mode) |

### Quiet Mode (--quiet)

For CI/CD environments and automated runs:
- Suppress progress spinners and decorative output
- Only show errors and final status
- Passes `--quiet` flag to spawned Claude sessions
- Machine-parseable log format

---

## Behavior

### Prerequisites Check

Before starting, verify:

```
1. ✓ Checkpoint exists (.autopilot/checkpoint.md)
   OR user provides --prompt="..." for new project
2. ✓ Loop script exists (scripts/autopilot-loop.sh)
3. ✓ claude CLI is available in PATH
```

### --install

Install the loop script globally:

```bash
mkdir -p ~/.local/bin
cp scripts/autopilot-loop.sh ~/.local/bin/autopilot-loop
chmod +x ~/.local/bin/autopilot-loop
```

Output:
```markdown
## Loop Script Installed

**Location:** ~/.local/bin/autopilot-loop

**Usage from anywhere:**
```bash
autopilot-loop /path/to/project
```

Make sure ~/.local/bin is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
```

### --background

Start loop in background and return control:

```bash
nohup ./scripts/autopilot-loop.sh . > autopilot-loop.log 2>&1 &
echo $! > .autopilot/loop.pid
```

Output:
```markdown
## Loop Started (Background)

**PID:** 12345
**Log:** autopilot-loop.log
**Project:** /path/to/project

Monitor progress:
```bash
tail -f autopilot-loop.log
```

Stop the loop:
```bash
/autopilot:loop --stop
# or
kill $(cat .autopilot/loop.pid)
```
```

### --foreground (default)

Since Claude cannot restart itself, provide clear instructions:

```markdown
## Start Continuous Loop

Run this command in your terminal:

```bash
./scripts/autopilot-loop.sh .
```

Or with custom settings:
```bash
MAX_ITERATIONS=50 COOLDOWN_SECONDS=5 ./scripts/autopilot-loop.sh .
```

**What happens:**
1. Claude starts with /autopilot:cockpit
2. Works until context reaches 40%
3. Saves checkpoint and exits
4. Script waits 3 seconds
5. Restarts Claude automatically
6. Repeats until project completes

Press Ctrl+C to stop the loop at any time.
```

### --status

Check if a background loop is running:

```bash
if [[ -f .autopilot/loop.pid ]]; then
    pid=$(cat .autopilot/loop.pid)
    if ps -p $pid > /dev/null 2>&1; then
        echo "Loop running (PID: $pid)"
    else
        echo "Loop not running (stale PID file)"
    fi
else
    echo "No loop running"
fi
```

### --stop

Stop a running background loop:

```bash
if [[ -f .autopilot/loop.pid ]]; then
    pid=$(cat .autopilot/loop.pid)
    kill $pid 2>/dev/null && echo "Loop stopped" || echo "Loop not running"
    rm -f .autopilot/loop.pid
fi
```

---

## Quick Start Examples

```bash
# See the command to run (default)
/autopilot:loop

# Start in background and continue working
/autopilot:loop --background

# Check if running
/autopilot:loop --status

# Stop background loop
/autopilot:loop --stop

# Install globally
/autopilot:loop --install

# Custom iteration limit
/autopilot:loop --max-iterations=50 --cooldown=5
```

---

## Integration with Takeoff

Typical workflow:

```bash
# 1. Start project interactively
/autopilot:takeoff Create a task management API

# 2. Review scope and approve
# 3. Work begins...

# 4. When ready to go fully autonomous:
/autopilot:loop --background

# 5. Check progress anytime
tail -f autopilot-loop.log
# or
/autopilot:altitude
```

---

## Troubleshooting

### "No checkpoint found"

```markdown
## Error: No Checkpoint

The loop requires an existing checkpoint to resume from.

**Fix:** Start a project first:
```bash
/autopilot:takeoff Your project description
```

Then run the loop after the first checkpoint is saved.
```

### "Loop script not found"

```markdown
## Error: Loop Script Missing

Expected: scripts/autopilot-loop.sh

**Fix:** The script should be in this repository. If missing:
```bash
# Check if in project-autopilot directory
ls scripts/

# Or install from the plugin
/autopilot:loop --install
```
```

### Loop exits immediately

Check the log file for errors:
```bash
cat autopilot-loop.log
```

Common causes:
- Missing `claude` CLI in PATH
- Invalid checkpoint file
- Permission issues

---

## Notes

- The loop uses `--yes` flag to auto-approve safe file operations
- Each iteration starts fresh context with full checkpoint restoration
- Progress is logged to `autopilot-loop.log`
- Background loops write PID to `.autopilot/loop.pid`
- Use `--max-iterations` as a safety limit for unattended runs
