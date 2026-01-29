---
description: Generate daily standup summary with progress, blockers, and next steps
argument-hint: "[--yesterday] [--blockers] [--format=slack|md|json]"
model: haiku
---

# Autopilot: STANDUP Mode
# Project Autopilot - Daily progress summary
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Generate daily standup summaries with progress, blockers, and planned work.

## Required Skills

**Read before generating:**
1. `/autopilot/skills/global-state/SKILL.md` - Project state access

## Required Agents

- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--yesterday` | Show detailed yesterday activity |
| `--blockers` | Highlight blockers |
| `--format=fmt` | Output format: slack, md, json |
| `--since=date` | Activity since specific date |
| `--project=name` | Specific project standup |

---

## Usage

### Default Standup

```bash
/autopilot:standup
```

Output:
```markdown
## Daily Standup - Jan 29, 2026

### Yesterday ✅
- Completed Phase 4: API Development (32 tasks)
- Fixed authentication bug in login flow
- Merged PR #45: Rate limiting middleware

### Today 🎯
- Begin Phase 5: Frontend Integration
- Implement dashboard components
- Connect API to frontend services

### Blockers ⚠️
- Waiting on design assets for mobile views

### Metrics
| Metric | Value |
|--------|-------|
| Phase Progress | 4/10 (40%) |
| Cost Today | $0.85 |
| Cost Total | $4.23 |
```

### Slack Format

```bash
/autopilot:standup --format=slack
```

Output:
```
🧑‍💻 *Daily Standup - Jan 29, 2026*

*Yesterday* ✅
• Completed Phase 4: API Development (32 tasks)
• Fixed authentication bug in login flow
• Merged PR #45: Rate limiting middleware

*Today* 🎯
• Begin Phase 5: Frontend Integration
• Implement dashboard components
• Connect API to frontend services

*Blockers* ⚠️
• Waiting on design assets for mobile views

📊 Progress: 4/10 phases (40%) | 💰 Cost: $4.23
```

### Detailed Yesterday

```bash
/autopilot:standup --yesterday
```

Output:
```markdown
## Daily Standup - Jan 29, 2026

### Yesterday (Detailed) ✅

#### Phase 4: API Development
**Status:** ✅ Complete
**Tasks:** 32/32
**Cost:** $0.92

| Task | Status | Time |
|------|--------|------|
| User endpoints | ✅ | 14:30 |
| Order endpoints | ✅ | 15:45 |
| Auth middleware | ✅ | 16:20 |
| Rate limiting | ✅ | 17:15 |
| API tests | ✅ | 18:00 |

#### Bug Fixes
- **#142** Auth token refresh race condition
  - Fixed in `src/services/auth.ts:78`
  - Added token refresh queue

#### Pull Requests
| PR | Title | Status |
|----|-------|--------|
| #45 | Rate limiting middleware | ✅ Merged |
| #46 | Fix auth token refresh | 🔄 Review |

#### Commits
```
abc1234 feat: Add rate limiting middleware
def5678 fix: Token refresh race condition
ghi9012 test: Add API endpoint tests
```

### Today 🎯
- Begin Phase 5: Frontend Integration
- Implement dashboard components
- Connect API to frontend services

### Blockers ⚠️
- Waiting on design assets for mobile views
```

### Blockers Focus

```bash
/autopilot:standup --blockers
```

Output:
```markdown
## Blockers Report - Jan 29, 2026

### Active Blockers

#### 🔴 High Priority

**Design assets for mobile views**
- **Blocking:** Phase 5 - Mobile dashboard
- **Since:** Jan 28, 2026 (1 day)
- **Impact:** Cannot implement mobile UI
- **Action:** Follow up with design team
- **ETA:** Jan 30, 2026

#### 🟡 Medium Priority

**Third-party API rate limits**
- **Blocking:** Integration testing
- **Since:** Jan 29, 2026 (today)
- **Impact:** Cannot run full test suite
- **Action:** Request limit increase
- **Workaround:** Mock responses for CI

### Resolved Today

| Blocker | Resolved | Duration |
|---------|----------|----------|
| Database connection pool | 10:30 | 2 hours |
| Missing env variables | 11:15 | 30 min |

### Blocker Statistics

| Metric | Value |
|--------|-------|
| Active | 2 |
| Resolved Today | 2 |
| Avg Resolution | 4 hours |
| Longest Active | 1 day |
```

### JSON Format (for automation)

```bash
/autopilot:standup --format=json
```

Output:
```json
{
  "date": "2026-01-29",
  "project": "my-saas-app",
  "yesterday": {
    "tasks_completed": 32,
    "phases_completed": 1,
    "cost": 0.85,
    "items": [
      "Completed Phase 4: API Development",
      "Fixed authentication bug",
      "Merged PR #45"
    ]
  },
  "today": {
    "planned_phase": 5,
    "planned_tasks": 18,
    "items": [
      "Begin Phase 5: Frontend Integration",
      "Implement dashboard components",
      "Connect API to frontend services"
    ]
  },
  "blockers": [
    {
      "id": "block-001",
      "description": "Design assets for mobile views",
      "priority": "high",
      "since": "2026-01-28",
      "impact": "Cannot implement mobile UI"
    }
  ],
  "metrics": {
    "phase_progress": "4/10",
    "cost_today": 0.85,
    "cost_total": 4.23
  }
}
```

---

## Behavior

```
FUNCTION standup(options):

    # 1. Load project state
    project = loadProjectState()
    history = loadActivityHistory()

    # 2. Analyze yesterday's activity
    IF options.since:
        since = parseDate(options.since)
    ELSE:
        since = getYesterday()

    activity = getActivitySince(history, since)

    # 3. Generate yesterday summary
    yesterday = summarizeActivity(activity)

    # 4. Plan today
    today = planToday(project.currentPhase, project.remainingTasks)

    # 5. Identify blockers
    blockers = getBlockers(project)

    IF options.blockers:
        DISPLAY blockersReport(blockers)
        RETURN

    # 6. Calculate metrics
    metrics = calculateMetrics(project, activity)

    # 7. Format output
    IF options.format == 'slack':
        DISPLAY slackFormat(yesterday, today, blockers, metrics)
    ELIF options.format == 'json':
        DISPLAY jsonFormat(yesterday, today, blockers, metrics)
    ELSE:
        DISPLAY markdownFormat(yesterday, today, blockers, metrics)
```

---

## Activity Detection

### What's Tracked

| Source | Activity Type |
|--------|---------------|
| `.autopilot/STATE.md` | Phase/task progress |
| Git commits | Code changes |
| Pull requests | Code reviews |
| `.autopilot/progress.md` | Detailed log |

### Yesterday Detection

```
FUNCTION getYesterday():
    now = Date.now()
    IF isWeekend(now):
        RETURN lastFriday()
    ELSE:
        RETURN yesterday()
```

---

## Quick Examples

```bash
# Default standup
/autopilot:standup

# Slack format
/autopilot:standup --format=slack

# Detailed yesterday
/autopilot:standup --yesterday

# Focus on blockers
/autopilot:standup --blockers

# JSON for automation
/autopilot:standup --format=json

# Since specific date
/autopilot:standup --since=2026-01-27

# Specific project
/autopilot:standup --project=my-saas-app
```

$ARGUMENTS
