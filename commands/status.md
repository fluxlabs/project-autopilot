---
description: Quick progress check with phase estimates vs actuals and budget status
argument-hint: [--global] [--detailed] [--compact]
model: sonnet
---

# Autopilot: STATUS Mode

Display current progress with phase-level estimates vs actuals comparison. Use `--global` for aggregate stats across all projects.

## Required Skills

- `/autopilot/skills/user-experience/SKILL.md` - Consistent output patterns

---

## Options

| Option | Description |
|--------|-------------|
| `--global` | Show aggregate stats across all projects |
| `--detailed` | Show full breakdown by model, agent, phase |
| `--compact` | Minimal output |

---

## Quick Read

### For Local Status (default)
Read these files:
- `.autopilot/progress.md` - Recent activity
- `.autopilot/checkpoint.md` - Current position
- `.autopilot/scope.md` - Phase overview with estimates
- `.autopilot/token-usage.md` - Cost details
- `.autopilot/phase-XXX.md` - Current phase

### For Global Status (--global)
Read these files:
- `~/.claude/autopilot/history.json` - All projects
- `~/.claude/autopilot/statistics.json` - Aggregate stats
- `~/.claude/autopilot/learnings.json` - Accuracy data

---

## Output Format

### Command Banner

```
╭─────────────────────────────────────────────────────────────╮
│  📊 AUTOPILOT: STATUS                                       │
│  Project progress and budget overview                       │
╰─────────────────────────────────────────────────────────────╯
```

### Standard Output

```markdown
# 📊 Autopilot Status

## Position
**Phase:** [X] of [Y] - [Phase Name]
**Task:** [XXX].Y - [Task Name]
**Progress:** [X]% complete

---

## 💰 Budget Status

### Overall
| Metric | Estimated | Actual | Remaining |
|--------|-----------|--------|-----------|
| Cost | $6.52 | $0.85 | $49.15 |
| Tokens | 1.2M | 245K | 1.76M |

```
Cost:   ██░░░░░░░░░░░░░░░░░░ 1.7% ($0.85 / $50.00)
Tokens: ████░░░░░░░░░░░░░░░░ 12% (245K / 2M)
```

### Thresholds
| Type | Limit | Current | Status |
|------|-------|---------|--------|
| Warning | $10.00 | $0.85 | ✅ 9% |
| Alert | $25.00 | $0.85 | ✅ 3% |
| Stop | $50.00 | $0.85 | ✅ 2% |

---

## 📋 Phase Progress (Estimates vs Actuals)

| Phase | Name | Est. | Actual | Variance | Status |
|-------|------|------|--------|----------|--------|
| 001 | Setup | $0.15 | $0.12 | -20% 🟢 | ✅ Complete |
| 002 | Database | $0.32 | $0.35 | +9% ✅ | ✅ Complete |
| 003 | Auth | $0.32 | $0.38 | +19% ✅ | ✅ Complete |
| 004 | API | $0.85 | $0.42 | - | 🔄 In Progress (49%) |
| 005 | Business | $1.10 | - | - | ⏳ Pending |
| 006 | Frontend | $1.40 | - | - | ⏳ Pending |
| 007 | Testing | $0.65 | - | - | ⏳ Pending |
| 008 | Security | $0.40 | - | - | ⏳ Pending |
| 009 | Docs | $0.35 | - | - | ⏳ Pending |
| 010 | DevOps | $0.50 | - | - | ⏳ Pending |

### Summary
| Metric | Value |
|--------|-------|
| Phases Complete | 3 of 10 |
| Est. for Complete | $0.79 |
| Actual for Complete | $0.85 |
| Overall Variance | +8% ✅ |

---

## 🔄 Current Phase Detail

### Phase 004: API Layer
**Status:** 🔄 In Progress
**Started:** 2024-01-15 14:00:00

#### Budget
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input | ~60K | 32K | - |
| Output | ~40K | 18K | - |
| **Cost** | **$0.85** | **$0.42** | **-51%** |

*Phase 49% complete - tracking under estimate*

#### Task Progress
| Task | Description | Est. | Actual | Status |
|------|-------------|------|--------|--------|
| 004.1 | User endpoints | $0.08 | $0.09 | ✅ +13% |
| 004.2 | Order endpoints | $0.12 | $0.11 | ✅ -8% |
| 004.3 | Product endpoints | $0.10 | $0.10 | ✅ 0% |
| 004.4 | Payment endpoints | $0.15 | $0.12 | ✅ -20% |
| 004.5 | Validation | $0.08 | - | 🔄 Current |
| 004.6 | Error handling | $0.07 | - | ⏳ |
| 004.7 | Middleware | $0.10 | - | ⏳ |
| 004.8 | Tests | $0.15 | - | ⏳ |

---

## 📈 Estimation Accuracy

### By Completed Phase
| Phase | Est. | Actual | Accuracy |
|-------|------|--------|----------|
| 001 Setup | $0.15 | $0.12 | 125% (under) |
| 002 Database | $0.32 | $0.35 | 91% |
| 003 Auth | $0.32 | $0.38 | 84% |
| **Average** | | | **100%** ✅ |

### Projection
**If current accuracy holds:**
- Remaining estimate: $5.25
- Projected actual: $5.25 × 1.00 = $5.25
- **Projected total:** $6.10

**Budget Status:**
- Maximum: $50.00
- Projected: $6.10
- **Headroom:** $43.90 (88%) ✅

---

## Recent Activity

### [Timestamp]
✅ Task 004.4 Complete - Payment endpoints
**Est:** $0.15 | **Actual:** $0.12 | **Variance:** -20% 🟢

### [Timestamp]
✅ Task 004.3 Complete - Product endpoints
**Est:** $0.10 | **Actual:** $0.10 | **Variance:** 0% ✅

---

## Next Steps

```bash
# Continue from checkpoint
/autopilot:resume

# View detailed cost breakdown
cat .autopilot/token-usage.md

# View current phase details
cat .autopilot/phase-004.md
```
```

---

## Compact Mode

If minimal output needed:

```markdown
## Autopilot Status (Compact)

📍 Phase 4/10: API (Task 4.5)
💰 $0.85 / $50.00 (2%)
📊 Est: $6.52 | On track

Phases: ███░░░░░░░ 30%
Budget: █░░░░░░░░░ 2%
```

---

## Variance Indicators

| Variance | Icon | Meaning |
|----------|------|---------|
| < -20% | 🟢 | Under budget |
| -20% to +20% | ✅ | On track |
| +20% to +30% | ⚠️ | Slightly over |
| +30% to +50% | 🟠 | Over budget |
| > +50% | 🔴 | Significantly over |

---

## Detailed Mode (--detailed)

Show full breakdown:

```markdown
## Detailed Token Usage

### By Model
| Model | Operations | Input | Output | Cost |
|-------|------------|-------|--------|------|
| Sonnet | 142 | 201K | 79K | $2.79 |
| Opus | 3 | 12K | 5K | $0.56 |

### By Agent
| Agent | Tasks | Est. | Actual | Accuracy |
|-------|-------|------|--------|----------|
| planner | 3 | $0.15 | $0.12 | 125% |
| backend | 28 | $1.20 | $1.35 | 89% |
| tester | 15 | $0.65 | $0.58 | 112% |
| database | 8 | $0.32 | $0.35 | 91% |

### Variance Trend
| Phase | Variance |
|-------|----------|
| 001 | -20% 🟢 |
| 002 | +9% ✅ |
| 003 | +19% ✅ |
| 004 | -20% 🟢 (partial) |
| **Trend** | **Improving** ✅ |
```

---

## No Project Found

If no `.autopilot/` folder:

```markdown
# 📊 Autopilot Status

**No active project found in this directory.**

Start with:
- `/autopilot:scan` - Analyze existing project
- `/autopilot:build [description]` - Start new scope

Or view global stats:
- `/autopilot:status --global` - Stats across all projects
- `/autopilot:resume --list` - See resumable projects
```

---

## Global Status (--global)

Show aggregate stats across all projects:

```markdown
# 📊 Autopilot Global Status

**Since:** January 1, 2026 | **Last Project:** January 25, 2026

---

## Overview

| Metric | Value |
|--------|-------|
| Total Projects | 12 |
| Successful | 11 (92%) |
| In Progress | 1 |
| Failed | 0 |

---

## 💰 Costs

### Totals
| Metric | Value |
|--------|-------|
| Total Spent | $45.23 |
| Avg per Project | $3.77 |
| Avg per Phase | $0.52 |

### Visual
```
Total Spent:  ████████████████████ $45.23
Avg Project:  ████░░░░░░░░░░░░░░░░ $3.77
```

---

## 📈 Estimation Accuracy

### Overall
| Metric | Value |
|--------|-------|
| Accuracy | 94% |
| Avg Variance | +6% |
| Trend | Improving |

### By Phase Type
| Phase | Variance | Samples | Confidence |
|-------|----------|---------|------------|
| Setup | -15% 🟢 | 12 | High |
| Database | +8% ✅ | 10 | High |
| Auth | +12% ✅ | 8 | Medium |
| API | +5% ✅ | 15 | High |
| Frontend | +18% ✅ | 9 | Medium |
| Testing | -5% 🟢 | 11 | High |

---

## 🔄 Resumable Projects

| Project | Progress | Spent | Remaining |
|---------|----------|-------|-----------|
| cli-tool | 50% | $1.45 | ~$1.55 |

**Resume:** `/autopilot:resume --project=cli-tool`

---

## Recent Projects

| Project | Date | Cost | Variance | Outcome |
|---------|------|------|----------|---------|
| user-auth | Jan 25 | $4.85 | -7% 🟢 | ✅ |
| api-gateway | Jan 22 | $9.12 | +7% ✅ | ✅ |
| web-dashboard | Jan 18 | $11.50 | +15% ✅ | ✅ |

---

## Tech Stack Insights

### Most Used
1. **node-typescript-postgres** (5 projects) - Avg: $4.38
2. **react-nextjs** (3 projects) - Avg: $6.20
3. **python-fastapi** (2 projects) - Avg: $3.10

### Best Estimates
1. Setup phases (-15% avg) - You're efficient here
2. API phases (+5% avg) - Very accurate

### Needs Improvement
1. Frontend phases (+18% avg) - Consider adding buffer

---

## Quick Actions

```bash
# View specific project history
/autopilot:config --history

# View learnings
/autopilot:config --learnings

# Start new project
/autopilot:build [description]

# Resume in-progress project
/autopilot:resume --project=cli-tool
```
```

---

## Global Status (Compact)

With `--global --compact`:

```markdown
## Autopilot Global Stats

📊 12 projects | $45.23 total | 94% accuracy
🔄 1 resumable: cli-tool (50%)
📈 Trend: Improving (+2.3%)
```
