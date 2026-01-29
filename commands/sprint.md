---
description: Sprint planning, tracking, and retrospective management
argument-hint: "[--plan] [--status] [--complete] [--retro] [--velocity]"
model: sonnet
---

# Autopilot: SPRINT Mode
# Project Autopilot - Sprint planning and tracking
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Sprint planning, tracking, and retrospective management for agile development.

## Required Skills

**Read before planning:**
1. `/autopilot/skills/global-state/SKILL.md` - Historical data access

## Required Agents

- `planner` - Sprint planning
- `history-tracker` - Velocity tracking

---

## Options

| Option | Description |
|--------|-------------|
| `--plan` | Plan a new sprint |
| `--status` | Current sprint status |
| `--complete` | Complete current sprint |
| `--retro` | Generate retrospective |
| `--velocity` | Show velocity metrics |
| `--backlog` | View and prioritize backlog |

---

## Usage

### Plan New Sprint

```bash
/autopilot:sprint --plan
```

Output:
```markdown
## Sprint Planning: Sprint 12

**Duration:** 2 weeks (Jan 29 - Feb 12, 2026)
**Team Velocity:** 42 points (avg last 3 sprints)

---

### Available Capacity

| Resource | Days | Capacity |
|----------|------|----------|
| Development | 10 | 40 points |
| Testing | 5 | 10 points |
| Buffer (20%) | - | -10 points |
| **Available** | - | **40 points** |

---

### Backlog (Prioritized)

| ID | Story | Points | Priority |
|----|-------|--------|----------|
| #45 | User authentication OAuth | 8 | 🔴 High |
| #46 | Dashboard redesign | 13 | 🔴 High |
| #47 | API rate limiting | 5 | 🟠 Medium |
| #48 | Email notifications | 8 | 🟠 Medium |
| #49 | Admin panel | 13 | 🟡 Low |
| #50 | Performance optimization | 5 | 🟡 Low |

---

### Recommended Sprint Scope

Based on velocity (42) and capacity (40):

| ID | Story | Points |
|----|-------|--------|
| #45 | User authentication OAuth | 8 |
| #46 | Dashboard redesign | 13 |
| #47 | API rate limiting | 5 |
| #48 | Email notifications | 8 |
| | **Total** | **34 points** |

**Buffer:** 6 points for unexpected work

---

### Sprint Goal

> Deliver core user authentication with OAuth and begin
> dashboard redesign while maintaining API stability.

---

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OAuth complexity | Medium | High | Spike early |
| Design dependency | Low | Medium | Use existing components |

**Confirm sprint plan? (y/n)**
```

### Sprint Status

```bash
/autopilot:sprint --status
```

Output:
```markdown
## Sprint 12 Status

**Progress:** Day 6 of 10 (60%)
**Burndown:**

```
Points Remaining
40 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
35 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░ Ideal
30 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░
25 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░
20 │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░ Actual
15 │▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
10 │▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 5 │▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 0 └──────────────────────────────────────────
    Day 1  2  3  4  5  6  7  8  9  10
```

**Status:** On Track ✅

---

### Story Status

| ID | Story | Points | Status | Assignee |
|----|-------|--------|--------|----------|
| #45 | User auth OAuth | 8 | ✅ Done | - |
| #46 | Dashboard redesign | 13 | 🔄 In Progress (70%) | - |
| #47 | API rate limiting | 5 | 🔄 In Progress (30%) | - |
| #48 | Email notifications | 8 | ⏳ Not Started | - |

---

### Blockers

| Story | Blocker | Impact | Action |
|-------|---------|--------|--------|
| #46 | Design assets pending | Medium | Follow up with design |

---

### Daily Summary

**Yesterday:**
- ✅ Completed OAuth integration
- ✅ Started dashboard layout

**Today:**
- 🎯 Continue dashboard components
- 🎯 Begin rate limiting implementation

**Tomorrow:**
- 🎯 Complete dashboard MVP
- 🎯 Start notification service
```

### Complete Sprint

```bash
/autopilot:sprint --complete
```

Output:
```markdown
## Sprint 12 Complete

### Summary

| Metric | Planned | Actual | Status |
|--------|---------|--------|--------|
| Points Committed | 34 | 34 | ✅ 100% |
| Stories Committed | 4 | 4 | ✅ 100% |
| Days | 10 | 10 | ✅ |

### Completed Stories

| ID | Story | Points | Notes |
|----|-------|--------|-------|
| #45 | User auth OAuth | 8 | ✅ |
| #46 | Dashboard redesign | 13 | ✅ |
| #47 | API rate limiting | 5 | ✅ |
| #48 | Email notifications | 8 | ✅ |

### Velocity Update

```
Sprint     Points
Sprint 9   ████████████████████████████████████████ 40
Sprint 10  ████████████████████████████████████████████ 44
Sprint 11  ██████████████████████████████████████████ 42
Sprint 12  ██████████████████████████████████████ 34 ← Current
           ────────────────────────────────────────────
Average:   40 points
```

### Sprint Marked Complete ✅

**Next:** Run `/autopilot:sprint --retro` for retrospective
```

### Sprint Retrospective

```bash
/autopilot:sprint --retro
```

Output:
```markdown
## Sprint 12 Retrospective

### What Went Well 🎉

1. **OAuth implementation ahead of schedule**
   - Good documentation available
   - Reused patterns from previous auth work

2. **Team collaboration**
   - Quick blocker resolution
   - Good communication on dependencies

3. **Quality**
   - Zero bugs escaped to production
   - Test coverage maintained

### What Could Improve 🔧

1. **Design dependencies**
   - Waited 2 days for design assets
   - Impact: Dashboard started late

2. **Estimation**
   - Rate limiting simpler than expected (-2 points)
   - Could have added more to sprint

3. **Documentation**
   - OAuth setup not documented
   - Will slow future team members

### Action Items 📋

| Action | Owner | Due |
|--------|-------|-----|
| Create OAuth setup guide | - | Sprint 13 |
| Establish design asset SLA | - | Next week |
| Review estimation for infra work | - | Sprint planning |

### Metrics

| Metric | Sprint 12 | Trend |
|--------|-----------|-------|
| Velocity | 34 | ↓ 8 |
| Commitment | 100% | → |
| Quality | 0 bugs | → |
| Estimation | -6% | ↑ |

### Team Feedback

> "Good sprint overall. Need better design coordination."

> "OAuth went smoothly. Happy with the outcome."
```

### Velocity Analysis

```bash
/autopilot:sprint --velocity
```

Output:
```markdown
## Velocity Analysis

### Historical Velocity

```
Sprint     Points
Sprint 7   ████████████████████████████████████ 36
Sprint 8   ██████████████████████████████████████ 38
Sprint 9   ████████████████████████████████████████ 40
Sprint 10  ████████████████████████████████████████████ 44
Sprint 11  ██████████████████████████████████████████ 42
Sprint 12  ██████████████████████████████████████ 34
```

### Statistics

| Metric | Value |
|--------|-------|
| Average (All) | 39 points |
| Average (Last 3) | 40 points |
| Highest | 44 points (Sprint 10) |
| Lowest | 34 points (Sprint 12) |
| Trend | Stable (±5%) |

### Commitment vs Delivery

| Sprint | Committed | Delivered | % |
|--------|-----------|-----------|---|
| Sprint 10 | 42 | 44 | 105% |
| Sprint 11 | 40 | 42 | 105% |
| Sprint 12 | 34 | 34 | 100% |

### Recommended Next Sprint

Based on velocity analysis:
- **Conservative:** 34 points
- **Moderate:** 40 points
- **Aggressive:** 44 points

**Recommendation:** 38-40 points (moderate)
```

---

## Behavior

```
FUNCTION sprint(options):

    IF options.plan:
        velocity = calculateVelocity()
        capacity = calculateCapacity()
        backlog = getBacklog()

        recommended = recommendScope(backlog, velocity, capacity)
        risks = identifyRisks(recommended)

        DISPLAY sprintPlan(recommended, risks)

        IF confirm():
            createSprint(recommended)

    ELIF options.status:
        sprint = getCurrentSprint()
        burndown = calculateBurndown(sprint)
        blockers = getBlockers(sprint)

        DISPLAY sprintStatus(sprint, burndown, blockers)

    ELIF options.complete:
        sprint = getCurrentSprint()
        summary = generateSummary(sprint)
        updateVelocity(sprint)

        DISPLAY sprintComplete(summary)

    ELIF options.retro:
        sprint = getLastSprint()
        retro = generateRetrospective(sprint)

        DISPLAY retrospective(retro)

    ELIF options.velocity:
        history = getSprintHistory()
        analysis = analyzeVelocity(history)

        DISPLAY velocityAnalysis(analysis)
```

---

## Quick Examples

```bash
# Plan new sprint
/autopilot:sprint --plan

# Check current sprint status
/autopilot:sprint --status

# Complete sprint
/autopilot:sprint --complete

# Run retrospective
/autopilot:sprint --retro

# View velocity metrics
/autopilot:sprint --velocity

# View and prioritize backlog
/autopilot:sprint --backlog
```

$ARGUMENTS
