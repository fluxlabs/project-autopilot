---
description: Resume execution from checkpoint with quality validation and cost tracking
argument-hint: [--task=X.Y] [--phase=N] [--max-cost=N] [--max-tokens=N] [--project=NAME]
model: sonnet
---

<!--
CAPABILITY NOTE FOR CLAUDE:
All pseudocode in this file (SPAWN, parallel_spawn, etc.) maps to Claude Code tools:
- SPAWN agent → Task tool with subagent_type="autopilot:{agent}"
- parallel_spawn([...]) → Multiple Task tool calls in single message
- Read/Write files → Read, Write, Edit tools
- Bash commands → Bash tool

You CAN and SHOULD execute this workflow. See /CLAUDE.md for full mapping.
-->

# Autopilot: COCKPIT Mode

// Project Autopilot - Return to Cockpit Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Continue project execution from last waypoint with quality gate enforcement and token/cost tracking. Can resume projects from any directory using global history.

## Required Skills

**Read before resuming:**
1. `/autopilot/skills/user-experience/SKILL.md` - Consistent output patterns
2. `/autopilot/skills/state-management/SKILL.md` - TRANSPONDER.md session bridge
3. `/autopilot/skills/phase-ordering/SKILL.md` - Verify task order
4. `/autopilot/skills/quality-gates/SKILL.md` - Validation requirements
5. `/autopilot/skills/git-workflow/SKILL.md` - Commit standards
6. `/autopilot/skills/token-tracking/SKILL.md` - Cost monitoring
7. `/autopilot/skills/global-state/SKILL.md` - Cross-session state

## Required Agents

- `validator` - Verify waypoints and gate transitions
- `planner` - If task ordering questions arise
- `token-tracker` - Monitor costs and enforce limits
- `history-tracker` - Find resumable projects globally

---

## Options

### Project Selection
- `--project=NAME` - Resume specific project by name (from global history)
- `--list` - Show all resumable projects across all directories

### Execution Options
- `--task=X.Y` - Start from specific task (e.g., --task=2.3)
- `--phase=N` - Start from specific phase
- `--validate` - Run full validation before resuming

### Cost/Token Thresholds
- `--warn-cost=N` - Warning threshold in dollars
- `--alert-cost=N` - Alert/pause threshold in dollars
- `--max-cost=N` - Hard stop threshold in dollars
- `--warn-tokens=N` - Warning threshold in tokens
- `--alert-tokens=N` - Alert/pause threshold in tokens
- `--max-tokens=N` - Hard stop threshold in tokens
- `--no-cost-limit` - Disable all cost/token limits
- `--reset-alerts` - Reset alert acknowledgments (re-alert at thresholds)

### Execution Options
- `--task=X.Y` - Start from specific task (e.g., --task=2.3)
- `--phase=N` - Start from specific phase
- `--validate` - Run full validation before resuming
- `--quiet` - Suppress verbose output (CI mode)

### Examples
```bash
# Resume current directory project
/autopilot:cockpit

# List all resumable projects
/autopilot:cockpit --list

# Resume specific project from anywhere
/autopilot:cockpit --project=my-api

# Resume with increased budget
/autopilot:cockpit --max-cost=100

# Resume from specific task with new limits
/autopilot:cockpit --task=3.2 --max-cost=50 --warn-cost=25

# Resume without any limits
/autopilot:cockpit --no-cost-limit

# Resume and re-enable alerts
/autopilot:cockpit --reset-alerts

# Resume in quiet mode for CI
/autopilot:cockpit --quiet
```

### Quiet Mode (--quiet)

For CI/CD environments and automated runs:
- Suppress progress spinners and decorative output
- Only show errors and final status
- Machine-parseable output format
- Exit codes indicate success/failure

---

## Standard Output Format

### Command Banner

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 AUTOPILOT: COCKPIT
   Return to cockpit - resume flight from waypoint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Resume Startup

```
▶ Restoring Flight State

  Loading transponder...
    ✓ Found state: .autopilot/TRANSPONDER.md
    ✓ Last activity: 2 hours ago

  Validating state...
    ✓ Phase 3 of 6 in progress
    ✓ Task 3.2 pending (3.1 completed)
    ✓ Build still passes
    ✓ Tests still pass (47/47)

  Loading fuel status...
    ✓ Spent: $2.35 of $50.00
    ✓ Remaining: $47.65
    ✓ Estimate to complete: $4.15

─────────────────────────────────────────────────────────────
✅ READY TO RESUME
─────────────────────────────────────────────────────────────

  Position:    Phase 3, Task 3.2
  Progress:    42% complete (14/32 tasks)
  Next task:   Create order API endpoints

  Resuming flight...

─────────────────────────────────────────────────────────────
```

### Project List (--list)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 AUTOPILOT: COCKPIT --list
   View all resumable flights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 2 resumable flights:

  ┌─────────────────────────────────────────────────────────┐
  │ 1. my-api                                               │
  │    Path:     ~/projects/my-api                          │
  │    Progress: ████████████░░░░░░░░ 60% (4/6 phases)      │
  │    Paused:   Task 5.2 - Frontend components             │
  │    Fuel:     $3.20 / Est: $5.50                         │
  │    Last:     2 hours ago                                │
  │                                                         │
  │    Resume: /autopilot:cockpit --project=my-api          │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ 2. auth-service                                         │
  │    Path:     ~/projects/auth-service                    │
  │    Progress: ██████░░░░░░░░░░░░░░ 30% (2/6 phases)      │
  │    Paused:   Task 3.1 - Auth middleware                 │
  │    Fuel:     $1.15 / Est: $4.00                         │
  │    Last:     1 day ago                                  │
  │                                                         │
  │    Resume: /autopilot:cockpit --project=auth-service    │
  └─────────────────────────────────────────────────────────┘
```

---

## Startup Sequence

### 0. Determine Project to Resume

```
FUNCTION determineProject():

    # Option 1: --project flag specified
    IF args.autopilot:
        project = SPAWN history-tracker → findProjectByName(args.autopilot)
        IF NOT project:
            ERROR "Project '{args.autopilot}' not found in history"
            SHOW "Run /autopilot:cockpit --list to see resumable flights"
            RETURN null
        RETURN project

    # Option 2: --list flag - show all resumable
    IF args.list:
        projects = SPAWN history-tracker → getResumableProjects()
        displayResumableProjects(projects)
        RETURN null  # Don't auto-resume

    # Option 3: Check current directory
    IF exists(".autopilot/TRANSPONDER.md"):
        RETURN { path: currentDir, source: "local" }

    # Option 4: Check global history for current directory
    project = SPAWN history-tracker → findProjectByPath(currentDir)
    IF project AND project.status IN ["in_progress", "paused"]:
        RETURN project

    # Option 5: No project found - show available
    projects = SPAWN history-tracker → getResumableProjects()
    IF projects.length > 0:
        displayResumableProjects(projects)
        PROMPT "Enter project name to resume, or run from project directory"
    ELSE:
        ERROR "No resumable flights found"
        SHOW "Start a flight with /autopilot:takeoff [description]"

    RETURN null
```

### Display Resumable Projects (--list)

```markdown
## Resumable Flights

| # | Project | Path | Progress | Fuel | Remaining | Last Active |
|---|---------|------|----------|------|-----------|-------------|
| 1 | my-api | ~/projects/my-api | ███░░ 60% | $2.45 | ~$1.65 | 2 hours ago |
| 2 | cli-tool | ~/projects/cli | ██░░░ 40% | $1.20 | ~$1.80 | 2 days ago |
| 3 | web-app | ~/work/web-app | █░░░░ 20% | $1.50 | ~$6.00 | 5 days ago |

**To resume:**
```bash
# Resume most recent
/autopilot:cockpit --project=my-api

# Or navigate to project directory
cd ~/projects/my-api && /autopilot:cockpit
```
```

### 1. Read State

```
# Local state
.autopilot/TRANSPONDER.md   → Current position + token state
.autopilot/learnings.md     → Accumulated knowledge
.autopilot/progress.md      → Activity history
.autopilot/token-usage.md   → Previous token usage
.autopilot/phase-XXX.md     → Current phase details

# Global state (for defaults)
~/.claude/autopilot/config.json → User preferences
~/.claude/autopilot/history.json → Project record
```

### 2. Restore Token State

Load from waypoint:
- Previous total tokens
- Previous total cost
- Alert acknowledgment status
- Warning shown status

**Priority for thresholds:**
1. CLI arguments (highest)
2. Waypoint values
3. Global config defaults (lowest)

```
FUNCTION resolveThresholds(args, waypoint, globalConfig):

    RETURN {
        maxCost: args.maxCost OR waypoint.maxCost OR globalConfig.defaults.maxCost,
        warnCost: args.warnCost OR waypoint.warnCost OR globalConfig.defaults.warnCost,
        alertCost: args.alertCost OR waypoint.alertCost OR globalConfig.defaults.alertCost,
        // ... same for tokens
    }
```

### 3. Display Resume Summary

```markdown
## Resuming Flight

**Position:** Phase [X], Task [XXX].Y
**Last Waypoint:** [Timestamp]

### Previous Fuel Usage
| Metric | Value |
|--------|-------|
| Input Tokens | [X] |
| Output Tokens | [Y] |
| Total Cost | $[Z] |

### Current Thresholds
| Type | Limit | Used | Remaining |
|------|-------|------|-----------|
| Warning | $[X] | $[Y] | $[Z] |
| Alert | $[X] | $[Y] | $[Z] |
| Stop | $[X] | $[Y] | $[Z] |

### Fuel Status
💰 Cost: $[Y] / $[max] ([X]%)
████████░░░░░░░░░░░░ [X]%
```

### 4. Validate State

**Spawn validator agent:**

```markdown
## Spawning: validator agent

**Task:** Verify resume state is valid
**Input:** TRANSPONDER.md, token-usage.md, recent git commits

**Verify:**
1. Last completed task matches git history
2. Prerequisites for next task are satisfied
3. No broken state from previous run
4. Build currently passes
5. Tests currently pass
6. Token state is consistent
```

### 5. Pre-Resume Checks

```bash
# Must all pass before resuming
git status              # Clean working directory
npm run build           # Build works
npm run lint            # No lint errors
npm test                # Tests pass
```

If any fail, fix before resuming.

### 6. Log Resume and Update Global History

```markdown
### [Timestamp]
▶️ **Leg [N+1] Started** - Resuming from waypoint

**Position:** Phase [X], Task [XXX].Y
**Context:** ~10%
**Validated:** Build ✅ | Tests ✅ | Lint ✅

**Token State Restored:**
- Previous: [X] tokens / $[Y]
- Thresholds: Warn $[A] | Alert $[B] | Stop $[C]
- Fuel remaining: $[Z]
```

```
# Update global history
SPAWN history-tracker → markProjectResumed(projectId)
```

---

## Execution Loop with Token Tracking

```
RESTORE token state from waypoint
APPLY new thresholds if provided via CLI

WHILE project not complete:

    # Check thresholds BEFORE starting
    CHECK token-tracker thresholds
    IF STOP triggered → already at limit, halt immediately
    IF ALERT triggered AND not acknowledged → pause for confirmation

    CHECK context usage
    IF context > 40%:
        → Finish current task
        → SPAWN validator (verify task complete)
        → Save waypoint with token state
        → STOP: "Run /autopilot:cockpit to continue"

    FOR each task (in dependency order):

        # Pre-task threshold check
        CHECK token-tracker thresholds
        IF STOP → save waypoint, halt
        IF ALERT → pause, await confirmation
        IF WARNING → log, continue

        # Pre-task validation
        CHECK task prerequisites satisfied
        IF not → find and complete blocking tasks

        # Task execution
        CHECK task model → Sonnet for reviews, Opus for implementation
        LOG start in progress.md
        READ only relevant files
        IMPLEMENT one small change

        # Post-task validation
        RUN build → must pass
        RUN lint → must pass
        RUN tests → must pass
        IF any fail → FIX immediately, do not proceed

        # Log with token info
        UPDATE token-usage.md
        COMMIT with conventional message
        UPDATE phase file task status
        LOG completion in progress.md with token info

        # Save waypoint after task complete
        Save waypoint (reason: "task_complete")

        # Post-task threshold check
        CHECK token-tracker thresholds
        IF any triggered → handle appropriately

    # Phase exit validation
    IF phase complete:
        SPAWN validator → verify phase gate
        RUN integration tests
        CHECK coverage ≥80%
        LOG phase cost summary
        MARK phase complete
        Save waypoint (reason: "phase_complete")
        LOG: "📌 Phase complete - waypoint saved"
```

---

## Threshold Handling During Resume

### Immediate Stop (Already at Limit)

If resuming and already at/over max threshold:

```markdown
## 🛑 Cannot Resume - Fuel Exhausted

**Current Cost:** $50.23
**Maximum:** $50.00

You've already reached the maximum fuel budget from the previous session.

**Options:**
1. Increase limit: `/autopilot:cockpit --max-cost=75`
2. Remove limit: `/autopilot:cockpit --no-cost-limit`
3. Review usage: Check `.autopilot/token-usage.md`
```

### Alert Acknowledgment Persistence

If alert was acknowledged in previous session, don't re-alert unless:
- `--reset-alerts` flag provided
- New, lower threshold provided

```markdown
### Alert Status
**Previous alert at $25 was acknowledged**
**Will not re-alert until $50 (stop threshold)**

To re-enable alerts: `/autopilot:cockpit --reset-alerts`
```

### New Threshold Application

When new thresholds provided:

```markdown
### Threshold Update

**Previous:**
- Warning: $10 | Alert: $25 | Stop: $50

**New (from CLI):**
- Warning: $15 | Alert: $40 | Stop: $100

**Applied:** New thresholds active for this session
```

---

## Progress Log Format with Tokens

```markdown
### [YYYY-MM-DD HH:MM:SS]
✅ **Task [XXX].Y Complete** - [Task Name]
**Context:** ~[X]%
**Model:** Opus/Sonnet

**Token Usage:**
- This task: +3,245 in / +1,892 out = $0.05
- Session total: 348,067 tokens = $4.36
- Fuel: 44% of $10.00 warning | 17% of $25.00 alert

**Change:** [One sentence description]
**Files:** `file1.ts`, `file2.ts`
**Verified:** Build ✅ | Tests ✅ | Lint ✅
**Commit:** `abc1234` feat(scope): description [XXX.Y]
```

---

## Waypoint Save with Token State

Waypoints are saved at these trigger points:

| Trigger | Reason | Description |
|---------|--------|-------------|
| Task completes | `task_complete` | After every task finishes successfully |
| Phase completes | `phase_complete` | After phase validation passes |
| Context > 40% | `context_threshold` | Before context window fills |
| User interrupts | `user_interrupt` | Ctrl+C or manual stop |
| Cost threshold | `cost_limit` | Max fuel budget reached |
| Error | `error` | Unrecoverable error |

### Update `.autopilot/TRANSPONDER.md`:

```markdown
# Flight Waypoint
**Saved:** [Timestamp]
**Reason:** [task_complete | phase_complete | context_threshold | ...]
**Leg:** [N]

## Current State
- **Phase:** [X] of [Y] - [Phase Name]
- **Last Task Completed:** [XXX].Y
- **Next Task:** [XXX].Z
- **Context Used:** ~50%

## Fuel State
| Metric | Value |
|--------|-------|
| Input Tokens | 348,067 |
| Output Tokens | 142,891 |
| Total Cost | $4.36 |

### Thresholds
| Type | Limit | Used | Remaining | Status |
|------|-------|------|-----------|--------|
| Warning | $10.00 | $4.36 | $5.64 | ✅ |
| Alert | $25.00 | $4.36 | $20.64 | ✅ |
| Stop | $50.00 | $4.36 | $45.64 | ✅ |

### Alert Acknowledgments
- Warning shown: Yes
- Alert acknowledged: No

## Validation State
- Build: ✅ Pass
- Tests: ✅ Pass (coverage: 85%)
- Lint: ✅ Pass

## Git State
- Branch: [branch-name]
- Last commit: `abc1234`
- Clean working directory: Yes

## Resume Instructions
```bash
# Standard resume
/autopilot:cockpit

# With increased fuel budget
/autopilot:cockpit --max-cost=75

# From specific task
/autopilot:cockpit --task=[XXX].Z
```
```

---

## Status Display

Include token info in status checks:

```markdown
## Flight Status

**Position:** Phase 3, Task 3.4
**Progress:** 34% complete

### Fuel Usage
💰 Cost: $4.36 / $50.00 (9%)
📊 Tokens: 490,958 / 2,000,000 (25%)
████░░░░░░░░░░░░░░░░ 9%

### Thresholds
| Type | Status |
|------|--------|
| Warning ($10) | ✅ 44% |
| Alert ($25) | ✅ 17% |
| Stop ($50) | ✅ 9% |

### Projection
**Estimated remaining fuel:** $8-12
**Projected total:** $12-16
**Within budget:** ✅ Yes
```

---

## Error Recovery

[Previous error recovery, plus:]

### Token State Corruption

```markdown
## Token State Invalid

**Issue:** token-usage.md is corrupted or missing

**Recovery:**
1. Check git history for previous version
2. Estimate from progress.md timestamps
3. Reset to conservative estimate
4. Continue with monitoring

**Action:** Resetting token state to $0 (monitor closely)
```

---

## Code Review Tasks (Sonnet)

[Same as before, plus token logging]

$ARGUMENTS
