---
name: state-management
description: Lean session bridge for cross-session persistence. STATE.md is the living memory (< 100 lines) that enables instant resumption.
---

# State Management

// Project Autopilot - State Management Skill
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Core Principle:** STATE.md is the session bridge. Read FIRST, update LAST.

---

## STATE.md Template

**Location:** `.autopilot/STATE.md`
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
- ROADMAP.md: .autopilot/roadmap.md
- Current phase: .autopilot/phases/{phase}/
```

---

## Status Values

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `Ready to discuss` | Phase exists, no CONTEXT.md | `/autopilot:discuss` |
| `Ready to plan` | CONTEXT.md exists, no PLAN.md | `/autopilot:build --plan-only` |
| `Ready to execute` | PLAN.md exists | `/autopilot:build` or `/autopilot:resume` |
| `In progress` | Execution active | Continue or checkpoint |
| `Blocked` | Waiting on external | Resolve blocker |
| `Phase complete` | All plans done, verified | Transition to next phase |
| `Project complete` | All phases done | Archive/ship |

---

## Update Protocol

### When to Update STATE.md

| Event | Update |
|-------|--------|
| Session start | Read STATE.md FIRST |
| Task complete | Update position, log activity |
| Plan complete | Update plan count, metrics |
| Phase complete | Update phase, reset plan count |
| Decision made | Add to Recent Decisions (keep 3-5) |
| Blocker found | Add to Blockers |
| Blocker resolved | Remove from Blockers |
| Session end | Update Session Continuity |

### Update Rules

1. **Read FIRST** - Before any operation, load STATE.md
2. **Update LAST** - After significant action, write STATE.md
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

### Continue-Here Files

When execution interrupts mid-plan, create `.autopilot/continue-here.md`:

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

### Continue-Here Lifecycle

```
1. CREATION
   - Created when execution interrupts mid-plan
   - Created on context > 40%, user interrupt, error
   - Contains exact state for seamless resumption

2. USAGE
   - Resume command checks for continue-here.md FIRST
   - If exists, spawn fresh agent with:
     - Completed tasks table (for verification)
     - Remaining work list
     - Decisions already made
     - Next action to execute

3. DELETION
   - Auto-deleted after successful resume
   - NOT permanent storage (STATE.md is permanent)
   - Just a handoff bridge between sessions
```

### Spawn Fresh, Don't Resume

When continuing from continue-here.md:

```
❌ WRONG: Resume previous agent
   - Agent state doesn't serialize across Task() boundaries
   - Previous context may be corrupted

✅ RIGHT: Spawn fresh agent with context
   - Read continue-here.md
   - Inline content into new agent prompt
   - Fresh agent knows exactly where to continue
   - No state serialization issues
```

### Continue-Here Template for Agents

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

## Migration from checkpoint.md

If `.autopilot/checkpoint.md` exists, migrate to STATE.md:

```
1. Read checkpoint.md
2. Extract: phase, plan, status, progress
3. Create STATE.md with extracted data
4. Move checkpoint.md to .autopilot/archive/
5. Update resume.md to read STATE.md
```

STATE.md is leaner and faster to parse.

---

## Integration

### Build Command
```
# At start
Read STATE.md → know current position
Read CONTEXT.md → know user decisions

# During execution
Update STATE.md after each plan

# At end
Update STATE.md with completion status
```

### Resume Command
```
# At start
Read STATE.md → instant context restoration
Check for continue-here.md → mid-plan resume

# Route based on status
Ready to discuss → suggest /autopilot:discuss
Ready to plan → suggest /autopilot:build --plan-only
Ready to execute → continue execution
In progress → resume from continue-here.md
```

### Discuss Command
```
# At end
Update STATE.md:
  Status: "Ready to plan"
  Last activity: "Discussed phase {N}"
```

---

## Example STATE.md

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
| Resume file | .autopilot/continue-here.md |
| Next action | /autopilot:resume |
```
