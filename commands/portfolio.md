---
description: Manage multiple projects
argument-hint: "[--list] [--costs] [--switch project] [--compare] [--summary]"
model: sonnet
---

# Autopilot: PORTFOLIO Mode
# Project Autopilot - Multi-project management
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Manage multiple Autopilot projects, view aggregate statistics, compare costs, and coordinate resources.

## Required Skills

**Read before managing portfolio:**
1. `/autopilot/skills/global-state/SKILL.md` - Project history access

## Required Agents

- `portfolio-manager` - Multi-project coordination
- `history-tracker` - Project data access

---

## Options

| Option | Description |
|--------|-------------|
| `--list` | List all projects with status |
| `--costs` | Show aggregate cost breakdown |
| `--switch project` | Change active project context |
| `--compare` | Compare projects side-by-side |
| `--summary` | Show portfolio summary |
| `--archive project` | Archive completed project |
| `--export` | Export portfolio report |

---

## Usage

### List Projects (--list)

```bash
/autopilot:portfolio --list
```

Output:
```markdown
## Project Portfolio

┌─────────────────────────────────────────────────────────────────────┐
│                         PROJECT PORTFOLIO                            │
├─────────────────────────────────────────────────────────────────────┤
│ Project          │ Status    │ Phase │ Cost    │ Variance │ Last    │
├──────────────────┼───────────┼───────┼─────────┼──────────┼─────────┤
│ my-saas-app      │ 🔄 Active │ 5/10  │ $4.23   │ -12% 🟢  │ 2h ago  │
│ mobile-backend   │ ⏸️ Paused │ 3/8   │ $2.15   │ +5% ✅   │ 2d ago  │
│ cli-tool         │ ✅ Done   │ 5/5   │ $1.87   │ -8% 🟢   │ 5d ago  │
│ api-service      │ ✅ Done   │ 6/6   │ $3.87   │ +3% ✅   │ 1w ago  │
│ web-dashboard    │ ❌ Failed │ 4/10  │ $5.12   │ +45% 🔴  │ 2w ago  │
├──────────────────┴───────────┴───────┴─────────┴──────────┴─────────┤
│ Total: 5 projects | Active: 1 | Paused: 1 | Done: 2 | Failed: 1     │
│ Total Spent: $17.24 | Avg per Project: $3.45                        │
└─────────────────────────────────────────────────────────────────────┘

### Quick Actions
```bash
# Resume paused project
/autopilot:cockpit --project=mobile-backend

# View specific project
/autopilot:portfolio --switch my-saas-app

# Compare projects
/autopilot:portfolio --compare
```
```

### Cost Summary (--costs)

```bash
/autopilot:portfolio --costs
```

Output:
```markdown
## Portfolio Cost Analysis

### Overall Statistics
| Metric | Value |
|--------|-------|
| Total Projects | 5 |
| Total Spent | $17.24 |
| Total Estimated | $19.50 |
| Overall Variance | -11.6% 🟢 |
| Avg per Project | $3.45 |
| Avg Accuracy | 92% |

### Cost by Project
```
my-saas-app    ████████████████░░░░ $4.23 (25%)
api-service    ███████████░░░░░░░░░ $3.87 (22%)
web-dashboard  ██████████████░░░░░░ $5.12 (30%)
mobile-backend ██████░░░░░░░░░░░░░░ $2.15 (12%)
cli-tool       █████░░░░░░░░░░░░░░░ $1.87 (11%)
```

### Cost by Status
| Status | Projects | Total Cost | Avg Cost |
|--------|----------|------------|----------|
| ✅ Completed | 2 | $5.74 | $2.87 |
| 🔄 Active | 1 | $4.23 | $4.23 |
| ⏸️ Paused | 1 | $2.15 | $2.15 |
| ❌ Failed | 1 | $5.12 | $5.12 |

### Cost by Tech Stack
| Stack | Projects | Total Cost | Avg Cost |
|-------|----------|------------|----------|
| Node + TypeScript | 3 | $9.97 | $3.32 |
| Python + FastAPI | 1 | $3.87 | $3.87 |
| React Native | 1 | $2.15 | $2.15 |

### Monthly Trend
```
Jan W1: ████████░░ $3.50
Jan W2: ██████████ $4.20
Jan W3: ███████░░░ $3.15
Jan W4: ██████████ $4.39
```
```

### Project Comparison (--compare)

```bash
/autopilot:portfolio --compare
```

Output:
```markdown
## Project Comparison

### Side-by-Side
| Metric | my-saas-app | mobile-backend | cli-tool |
|--------|-------------|----------------|----------|
| Status | 🔄 Active | ⏸️ Paused | ✅ Done |
| Phases | 5/10 | 3/8 | 5/5 |
| Tasks | 32/65 | 18/48 | 25/25 |
| Cost | $4.23 | $2.15 | $1.87 |
| Estimate | $6.50 | $4.80 | $2.00 |
| Variance | -12% 🟢 | +5% ✅ | -8% 🟢 |
| Duration | 4.5h | 2h | 1.5h |
| Start | Jan 25 | Jan 20 | Jan 15 |

### Efficiency Comparison
```
                Cost Efficiency (lower is better)
my-saas-app    ████████░░░░░░░░░░░░ $0.42/task
mobile-backend ██████████░░░░░░░░░░ $0.45/task
cli-tool       ██████░░░░░░░░░░░░░░ $0.30/task
```

### Tech Stack Comparison
| Project | Stack | Phase Cost (avg) |
|---------|-------|------------------|
| my-saas-app | Next.js + Supabase | $0.42 |
| mobile-backend | Node + MongoDB | $0.54 |
| cli-tool | Node + Commander | $0.37 |

### Lessons Learned
- **Best estimate accuracy:** cli-tool (-8% variance)
- **Most complex:** my-saas-app (65 tasks)
- **Fastest completion:** cli-tool (1.5h)
- **Stack recommendation:** Node + Commander for CLIs
```

### Switch Project (--switch)

```bash
/autopilot:portfolio --switch mobile-backend
```

Output:
```markdown
## Switching to: mobile-backend

**Path:** /Users/user/projects/mobile-backend
**Status:** ⏸️ Paused
**Position:** Phase 3, Task 3.5

### Project Details
| Metric | Value |
|--------|-------|
| Description | Mobile app backend API |
| Tech Stack | Node, TypeScript, MongoDB |
| Progress | 37.5% (3/8 phases) |
| Cost | $2.15 / $4.80 estimated |

### Resume
```bash
cd /Users/user/projects/mobile-backend
/autopilot:cockpit
```

Or resume from anywhere:
```bash
/autopilot:cockpit --project=mobile-backend
```
```

### Portfolio Summary (--summary)

```bash
/autopilot:portfolio --summary
```

Output:
```markdown
## Portfolio Summary

### At a Glance
```
┌────────────────────────────────────────────┐
│           AUTOPILOT PORTFOLIO              │
├────────────────────────────────────────────┤
│  📊 5 Projects  │  💰 $17.24 Total         │
│  ✅ 2 Complete  │  📈 92% Accuracy         │
│  🔄 1 Active    │  ⏱️ 12h Total Time       │
│  ⏸️ 1 Paused    │  📁 194 Tasks           │
└────────────────────────────────────────────┘
```

### Health Indicators
| Indicator | Status | Notes |
|-----------|--------|-------|
| Budget Health | ✅ Good | 11% under overall |
| Estimate Accuracy | ✅ Good | 92% average |
| Completion Rate | 🟡 Fair | 40% complete |
| Stale Projects | ⚠️ Warning | 1 project paused >7d |

### Recommendations
1. **Resume mobile-backend** - Paused for 2 days
2. **Review web-dashboard** - Over budget, may need re-scoping
3. **Consider archiving** - cli-tool, api-service complete

### Quick Actions
```bash
# Resume stale project
/autopilot:cockpit --project=mobile-backend

# Archive completed
/autopilot:portfolio --archive cli-tool

# View detailed costs
/autopilot:portfolio --costs
```
```

### Archive Project (--archive)

```bash
/autopilot:portfolio --archive cli-tool
```

Output:
```markdown
## Archive Project: cli-tool

**Status:** ✅ Completed (5/5 phases)
**Final Cost:** $1.87
**Duration:** 1.5 hours

### Archive Actions
- ✅ Marked as archived in history
- ✅ Statistics preserved
- ✅ Learnings retained

### Archived Data
```json
{
  "project": "cli-tool",
  "path": "/Users/user/projects/cli-tool",
  "archivedAt": "2026-01-29T12:00:00Z",
  "finalCost": 1.87,
  "phases": 5,
  "outcome": "success"
}
```

Project will no longer appear in active list.
View archived projects with:
```bash
/autopilot:portfolio --list --include-archived
```
```

---

## Export Portfolio Report

```bash
/autopilot:portfolio --export --output=portfolio-report.md
```

Creates a comprehensive report suitable for documentation or sharing.

---

## Behavior

```
FUNCTION portfolio(options):

    # Load global history
    history = readJSON("~/.claude/autopilot/history.json")
    statistics = readJSON("~/.claude/autopilot/statistics.json")
    learnings = readJSON("~/.claude/autopilot/learnings.json")

    IF options.list:
        DISPLAY projectList(history)

    ELIF options.costs:
        DISPLAY costAnalysis(history, statistics)

    ELIF options.compare:
        DISPLAY projectComparison(history)

    ELIF options.switch:
        switchProject(options.switch, history)

    ELIF options.summary:
        DISPLAY portfolioSummary(history, statistics, learnings)

    ELIF options.archive:
        archiveProject(options.archive, history)

    ELIF options.export:
        exportReport(history, statistics, options.output)

    ELSE:
        # Default: show summary
        DISPLAY portfolioSummary(history, statistics, learnings)
```

---

## No Projects Found

If no projects in history:

```markdown
## Empty Portfolio

No Autopilot projects found.

**Get started:**
```bash
# Create your first project
/autopilot:takeoff "Your project description"

# Or initialize from template
/autopilot:init nextjs-supabase --name=my-first-app
```

After completing projects, portfolio data will be available.
```

---

## Quick Start Examples

```bash
# View all projects
/autopilot:portfolio --list

# Cost breakdown
/autopilot:portfolio --costs

# Compare projects
/autopilot:portfolio --compare

# Portfolio health summary
/autopilot:portfolio --summary

# Switch to specific project
/autopilot:portfolio --switch my-project

# Archive completed project
/autopilot:portfolio --archive old-project

# Export full report
/autopilot:portfolio --export --output=report.md
```

$ARGUMENTS
