---
name: state-management
description: Lean session bridge for cross-session persistence. TRANSPONDER.md is the living memory (< 100 lines) that enables instant resumption.
---

# State Management

// Project Autopilot - State Management Skill
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Core Principle:** TRANSPONDER.md is the session bridge. Read FIRST, update LAST.

---

## TRANSPONDER.md Template

**Location:** `.autopilot/TRANSPONDER.md`
**Size Limit:** < 100 lines (enforced)

```markdown
# Project State

**Project:** {name}
**Updated:** {timestamp}

---

## Current Position

| Field | Value |
|-------|-------|
| Phase | {N} of {total} |
| Plan | {M} of {phase_total} |
| Status | {status} |
| Progress | {progress_bar} {percent}% |

**Last Activity:** {date} — {what happened}

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Plans completed | {N} |
| Avg duration | {X} min |
| Token efficiency | {percent}% |

---

## Accumulated Context

### Recent Decisions
- {Decision 1} — {outcome}
- {Decision 2} — {outcome}
- {Decision 3} — {outcome}

### Pending Todos
- [ ] {Todo 1}
- [ ] {Todo 2}

### Blockers
- {Blocker if any, prefixed with phase}

---

## Session Continuity

| Field | Value |
|-------|-------|
| Last session | {date} |
| Stopped at | {description} |
| Resume file | {path or "None"} |
| Next action | {command} |

---

## Quick Reference

- PROJECT.md: .autopilot/PROJECT.md
- flightplan.md: .autopilot/flightplan.md
- Current phase: .autopilot/phases/{phase}/
```

---

## Status Values

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `Ready to discuss` | Phase exists, no BRIEFING.md | `/autopilot:preflight` |
| `Ready to plan` | BRIEFING.md exists, no ROUTE.md | `/autopilot:takeoff --plan-only` |
| `Ready to execute` | ROUTE.md exists | `/autopilot:takeoff` or `/autopilot:cockpit` |
| `In progress` | Execution active | Continue or checkpoint |
| `Blocked` | Waiting on external | Resolve blocker |
| `Phase complete` | All plans done, verified | Transition to next phase |
| `Project complete` | All phases done | Archive/ship |

---

## Update Protocol

### When to Update TRANSPONDER.md

| Event | Update |
|-------|--------|
| Session start | Read TRANSPONDER.md FIRST |
| Task complete | Update position, log activity |
| Plan complete | Update plan count, metrics |
| Phase complete | Update phase, reset plan count |
| Decision made | Add to Recent Decisions (keep 3-5) |
| Blocker found | Add to Blockers |
| Blocker resolved | Remove from Blockers |
| Session end | Update Session Continuity |

### Update Rules

1. **Read FIRST** - Before any operation, load TRANSPONDER.md
2. **Update LAST** - After significant action, write TRANSPONDER.md
3. **Keep it small** - Prune old decisions, keep only 3-5
4. **Be specific** - "Completed auth API" not "Made progress"
5. **Include next action** - Always tell next session what to do

---

## Progress Bar Generation

```
Total tasks = sum of all plan tasks across all phases
Completed tasks = sum of completed plan tasks

percent = (completed / total) * 100
filled = floor(percent / 10)
empty = 10 - filled

bar = "█" * filled + "░" * empty
```

Examples:
- `██████████ 100%` - Complete
- `██████░░░░ 60%` - In progress
- `██░░░░░░░░ 20%` - Early stages
- `░░░░░░░░░░ 0%` - Not started

---

## Session Continuity

### Holding-Pattern Files

When execution interrupts mid-plan, create `.autopilot/holding-pattern.md`:

```markdown
---
phase: {phase_number}
plan: {plan_number}
task: {task_number}
total_tasks: {total}
status: in_progress
created: {timestamp}
---

## Current State
{Where exactly are we? Immediate context}

## Completed Work
| Task | Name | Commit | Status |
|------|------|--------|--------|
| 1 | {name} | {hash} | ✅ |
| 2 | {name} | {hash} | ✅ |
| 3 | {name} | — | 🔄 In progress |

## Remaining Work
- Task 3: {what's left}
- Task 4: {not started}
- Task 5: {not started}

## Decisions Made
{Why we chose X over Y - prevents re-debate}

## Blockers
{Anything stuck or waiting}

## Context
{Mental state, what you were thinking}

## Next Action
{The very first thing to do when resuming}
```

### Holding-Pattern Lifecycle

```
1. CREATION
   - Created when execution interrupts mid-plan
   - Created on context > 40%, user interrupt, error
   - Contains exact state for seamless resumption

2. USAGE
   - Cockpit command checks for holding-pattern.md FIRST
   - If exists, spawn fresh agent with:
     - Completed tasks table (for verification)
     - Remaining work list
     - Decisions already made
     - Next action to execute

3. DELETION
   - Auto-deleted after successful resume
   - NOT permanent storage (TRANSPONDER.md is permanent)
   - Just a handoff bridge between sessions
```

### Spawn Fresh, Don't Resume

When continuing from holding-pattern.md:

```
❌ WRONG: Resume previous agent
   - Agent state doesn't serialize across Task() boundaries
   - Previous context may be corrupted

✅ RIGHT: Spawn fresh agent with context
   - Read holding-pattern.md
   - Inline content into new agent prompt
   - Fresh agent knows exactly where to continue
   - No state serialization issues
```

### Holding-Pattern Template for Agents

```markdown
<objective>
Continue phase {N}, plan {M} from task {X} of {Y}
</objective>

<completed_tasks>
| Task | Name | Commit | Files |
| --- | --- | --- | --- |
| 1 | Create model | abc123 | src/model.ts |
| 2 | Create API | def456 | src/api.ts |
</completed_tasks>

<resume_context>
Current task: Task 3 - Create UI component
Previous work: Model and API complete, tested
Decisions: Using React Query for data fetching
</resume_context>

<next_action>
Create Dashboard.tsx component using the API from task 2
</next_action>
```

**Auto-delete** after successful resume.

---

## Migration from waypoint.md

If `.autopilot/waypoint.md` exists in old format, migrate to TRANSPONDER.md:

```
1. Read waypoint.md
2. Extract: phase, plan, status, progress
3. Create TRANSPONDER.md with extracted data
4. Move waypoint.md to .autopilot/archive/
5. Update cockpit.md to read TRANSPONDER.md
```

TRANSPONDER.md is leaner and faster to parse.

---

## Integration

### Takeoff Command
```
# At start
Read TRANSPONDER.md → know current position
Read BRIEFING.md → know user decisions

# During execution
Update TRANSPONDER.md after each plan

# At end
Update TRANSPONDER.md with completion status
```

### Cockpit Command
```
# At start
Read TRANSPONDER.md → instant context restoration
Check for holding-pattern.md → mid-plan resume

# Route based on status
Ready to discuss → suggest /autopilot:preflight
Ready to plan → suggest /autopilot:takeoff --plan-only
Ready to execute → continue execution
In progress → resume from holding-pattern.md
```

### Preflight Command
```
# At end
Update TRANSPONDER.md:
  Status: "Ready to plan"
  Last activity: "Discussed phase {N}"
```

---

## Example TRANSPONDER.md

```markdown
# Project State

**Project:** TaskFlow App
**Updated:** 2026-01-29T14:30:00Z

---

## Current Position

| Field | Value |
|-------|-------|
| Phase | 3 of 6 |
| Plan | 2 of 4 |
| Status | In progress |
| Progress | ████░░░░░░ 42% |

**Last Activity:** 2026-01-29 — Completed dashboard layout plan

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Plans completed | 8 |
| Avg duration | 12 min |
| Token efficiency | 73% |

---

## Accumulated Context

### Recent Decisions
- Hybrid sidebar layout — working well
- WebSocket for real-time — implemented
- Bottom nav on mobile — user approved

### Pending Todos
- [ ] Add error boundary to dashboard
- [ ] Write tests for auth flow

### Blockers
- None

---

## Session Continuity

| Field | Value |
|-------|-------|
| Last session | 2026-01-29 |
| Stopped at | Mid-plan 3.2, task 3 of 5 |
| Resume file | .autopilot/holding-pattern.md |
| Next action | /autopilot:cockpit |
```

---

## Three-Level Threshold State

### Threshold State Storage

```
.autopilot/state/thresholds.json
```

### Structure

```json
{
  "current_values": {
    "cost": 26.50,
    "context_percent": 35,
    "variance_percent": 18,
    "error_count": 1
  },
  "levels_triggered": {
    "cost": "alert",
    "context": "warning",
    "variance": null,
    "errors": null
  },
  "last_check": "2026-01-29T14:30:00Z"
}
```

### Update Protocol

```
FUNCTION updateThresholdState(type, value, level):
    """
    Update threshold state after check.
    """
    state = loadThresholdState()

    state.current_values[type] = value
    state.levels_triggered[type] = level
    state.last_check = now()

    saveThresholdState(state)
```

---

## Acknowledgment State Management

### Acknowledgment Storage

```
.autopilot/state/acknowledgments.json
```

### Structure

```json
{
  "acknowledgments": {
    "cost": {
      "acknowledged_at": "2026-01-29T14:30:00Z",
      "value_at_acknowledgment": 26.50,
      "threshold_level": "alert",
      "session_id": "session-abc123",
      "user_note": "Acknowledged cost increase due to complex feature"
    },
    "context": {
      "acknowledged_at": "2026-01-29T15:00:00Z",
      "value_at_acknowledgment": 42,
      "threshold_level": "alert",
      "session_id": "session-def456",
      "user_note": null
    }
  },
  "acknowledgment_history": [
    {
      "type": "cost",
      "value": 12.00,
      "acknowledged_at": "2026-01-28T10:00:00Z",
      "reset_at": "2026-01-29T08:00:00Z"
    }
  ],
  "last_reset": "2026-01-29T08:00:00Z"
}
```

### Acknowledgment Functions

```
FUNCTION isAcknowledged(type):
    """
    Check if an alert type has been acknowledged.
    """
    acks = loadAcknowledgments()

    IF type IN acks.acknowledgments:
        ack = acks.acknowledgments[type]
        # Check if acknowledgment is still valid
        # (not reset since acknowledged)
        IF acks.last_reset AND ack.acknowledged_at < acks.last_reset:
            RETURN false
        RETURN true

    RETURN false

FUNCTION acknowledge(type, value, note=null):
    """
    Record user acknowledgment of an alert.
    """
    acks = loadAcknowledgments()

    acks.acknowledgments[type] = {
        acknowledged_at: now(),
        value_at_acknowledgment: value,
        threshold_level: "alert",
        session_id: getCurrentSessionId(),
        user_note: note
    }

    saveAcknowledgments(acks)

    LOG "✅ Acknowledged: {type} at {value}"
    IF note:
        LOG "   Note: {note}"

FUNCTION resetAcknowledgments(types=null):
    """
    Reset acknowledgments. If types provided, only reset those.
    """
    acks = loadAcknowledgments()

    IF types == null:
        # Reset all
        # Move current to history first
        FOR type, ack IN acks.acknowledgments:
            acks.acknowledgment_history.add({
                type: type,
                value: ack.value_at_acknowledgment,
                acknowledged_at: ack.acknowledged_at,
                reset_at: now()
            })

        acks.acknowledgments = {}
        acks.last_reset = now()
        LOG "✅ All acknowledgments reset"
    ELSE:
        # Reset specific types
        FOR type IN types:
            IF type IN acks.acknowledgments:
                acks.acknowledgment_history.add({
                    type: type,
                    value: acks.acknowledgments[type].value_at_acknowledgment,
                    acknowledged_at: acks.acknowledgments[type].acknowledged_at,
                    reset_at: now()
                })
                delete acks.acknowledgments[type]
                LOG "✅ Reset acknowledgment: {type}"

    saveAcknowledgments(acks)
```

### Acknowledgment Persistence Across Sessions

```
FUNCTION loadSessionState():
    """
    Load complete session state including acknowledgments.
    """
    state = {
        position: loadPosition(),           # From TRANSPONDER.md
        metrics: loadMetrics(),             # From TRANSPONDER.md
        thresholds: loadThresholdState(),   # From thresholds.json
        acknowledgments: loadAcknowledgments(),  # From acknowledgments.json
        holding_pattern: loadHoldingPattern()   # If exists
    }

    # Restore acknowledged alerts
    FOR type, ack IN state.acknowledgments.acknowledgments:
        LOG "📝 Alert acknowledged ({type}): {ack.value_at_acknowledgment} on {ack.acknowledged_at}"

    RETURN state

FUNCTION saveSessionState(state):
    """
    Save complete session state.
    """
    savePosition(state.position)
    saveMetrics(state.metrics)
    saveThresholdState(state.thresholds)
    saveAcknowledgments(state.acknowledgments)

    IF state.interrupted:
        saveHoldingPattern(state.holding_pattern)
```

---

## Session State Integration

### TRANSPONDER.md with Thresholds Section

```markdown
# Project State

**Project:** TaskFlow App
**Updated:** 2026-01-29T14:30:00Z

---

## Current Position

| Field | Value |
|-------|-------|
| Phase | 3 of 6 |
| Plan | 2 of 4 |
| Status | In progress |
| Progress | ████░░░░░░ 42% |

---

## Thresholds

| Type | Current | Warning | Alert | Stop | Status |
|------|---------|---------|-------|------|--------|
| Cost | $26.50 | $10 ⚠️ | $25 🔶 ACK | $50 | Alert (ack) |
| Context | 35% | 30% ⚠️ | 40% | 50% | Warning |
| Variance | 18% | 20% | 30% | 50% | OK |
| Errors | 1 | 2 | 3 | 5 | OK |

**Acknowledged Alerts:**
- Cost @ $26.50 — acknowledged 2026-01-29T14:30

---

## Session Continuity

| Field | Value |
|-------|-------|
| Last session | 2026-01-29 |
| Stopped at | Mid-plan 3.2, task 3 of 5 |
| Resume file | .autopilot/holding-pattern.md |
| Next action | /autopilot:cockpit |
```

---

## Reset Alerts Flag

### Command Usage

```bash
# Reset all acknowledgments before resume
/autopilot:cockpit --reset-alerts

# Reset during takeoff
/autopilot:takeoff --reset-alerts

# Reset specific alert type
/autopilot:config --reset-alert=cost
```

### Reset Protocol

```
FUNCTION handleResetAlertsFlag():
    """
    Handle --reset-alerts flag from command.
    """
    LOG "🔄 Resetting alert acknowledgments..."

    resetAcknowledgments()

    LOG ""
    LOG "All alerts will trigger again if thresholds are exceeded."
    LOG "Current thresholds:"
    displayThresholds()
```

---

## Checkpoint Trigger State

### Trigger State Storage

```json
{
  "triggers": {
    "context_warning": {
      "last_triggered": "2026-01-29T14:00:00Z",
      "count": 2
    },
    "cost_alert": {
      "last_triggered": "2026-01-29T14:30:00Z",
      "count": 1,
      "acknowledged": true
    },
    "time_elapsed": {
      "session_start": "2026-01-29T14:00:00Z",
      "suggested_checkpoint": false
    }
  }
}
```

### Trigger Functions

```
FUNCTION triggerFired(trigger_type):
    """
    Record that a trigger was fired.
    """
    state = loadTriggerState()

    IF trigger_type NOT IN state.triggers:
        state.triggers[trigger_type] = {count: 0}

    state.triggers[trigger_type].last_triggered = now()
    state.triggers[trigger_type].count += 1

    saveTriggerState(state)

FUNCTION shouldTrigger(trigger_type, config):
    """
    Determine if trigger should fire based on config.
    """
    state = loadTriggerState()

    # Some triggers only fire once per session
    IF config.frequency == "once_per_session":
        IF state.triggers[trigger_type]?.last_triggered:
            RETURN false

    # Some triggers have cooldown
    IF config.cooldown:
        last = state.triggers[trigger_type]?.last_triggered
        IF last AND (now() - last) < config.cooldown:
            RETURN false

    RETURN true
```
