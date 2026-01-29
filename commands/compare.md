---
description: Compare estimated vs actual across projects
argument-hint: "[--project=name] [--all] [--by=phase|model|stack]"
model: haiku
---

# Autopilot: COMPARE Mode
# Project Autopilot - Estimation accuracy comparison
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Analyze estimation accuracy across projects to improve future estimates and identify patterns.

## Required Skills

**Read before comparing:**
1. `/autopilot/skills/global-state/SKILL.md` - Access historical data

## Required Agents

- `history-tracker` - Query project history

---

## Options

| Option | Description |
|--------|-------------|
| `--project=name` | Compare specific project |
| `--all` | Compare all completed projects |
| `--recent=N` | Compare last N projects (default: 10) |
| `--by=X` | Group comparison (phase\|model\|stack) |
| `--format=md\|json` | Output format |
| `--output=path` | Write to file |

---

## Behavior

```
FUNCTION compare(options):

    # 1. Load global history
    history = readJSON("~/.claude/autopilot/history.json")
    learnings = readJSON("~/.claude/autopilot/learnings.json")
    statistics = readJSON("~/.claude/autopilot/statistics.json")

    # 2. Filter projects
    IF args.autopilot:
        projects = findProject(history, args.autopilot)
    ELIF args.all:
        projects = history.autopilots.filter(p => p.status == "completed")
    ELSE:
        projects = history.autopilots.slice(-args.recent)

    # 3. Calculate comparisons
    comparisons = projects.map(p => {
        variance: calculateVariance(p.costs.estimated, p.costs.actual),
        accuracy: 100 - Math.abs(variance),
        phaseBreakdown: p.phaseCosts || null
    })

    # 4. Generate analysis
    analysis = {
        overall: aggregateStats(comparisons),
        byPhase: args.by == "phase" ? groupByPhase(comparisons) : null,
        byModel: args.by == "model" ? groupByModel(comparisons) : null,
        byStack: args.by == "stack" ? groupByStack(comparisons) : null,
        trends: calculateTrends(comparisons),
        recommendations: generateRecommendations(analysis)
    }

    # 5. Format and output
    RETURN format(analysis, args.format)
```

---

## Output Format (Default)

```markdown
# Estimation Comparison Report

**Generated:** [Timestamp]
**Projects Analyzed:** [N]
**Time Period:** [Start] to [End]

---

## Overall Accuracy

| Metric | Value |
|--------|-------|
| Average Accuracy | 94.2% |
| Average Variance | +5.8% |
| Best Estimate | -2% (project-x) |
| Worst Estimate | +32% (project-y) |

### Accuracy Distribution
```
90-100%: ████████████████ 12 projects (80%)
80-89%:  ████ 2 projects (13%)
70-79%:  █ 1 project (7%)
<70%:    0 projects (0%)
```

---

## Project Comparison

| Project | Est. | Actual | Variance | Accuracy |
|---------|------|--------|----------|----------|
| my-api | $4.50 | $4.85 | +7.8% | 92.2% ✅ |
| cli-tool | $2.00 | $1.85 | -7.5% | 92.5% ✅ |
| web-app | $8.00 | $9.12 | +14.0% | 86.0% ✅ |
| mobile-backend | $6.00 | $7.92 | +32.0% | 68.0% ⚠️ |
| ... | ... | ... | ... | ... |

### Variance by Project
```
my-api:          ██████████░░░░░░░░░░ +7.8%
cli-tool:        ████████░░░░░░░░░░░░ -7.5%
web-app:         ██████████████░░░░░░ +14.0%
mobile-backend:  ████████████████████████████████ +32.0%
```

---

## Trend Analysis

### Accuracy Over Time
```
Jan W1: ████████████████████ 95%
Jan W2: ██████████████████░░ 90%
Jan W3: ████████████████████ 96%
Jan W4: ██████████████████░░ 92%
```

**Trend:** Stable ✅

### Improvement Areas
| Factor | Impact |
|--------|--------|
| Historical calibration | +8% accuracy |
| Phase-type learning | +5% accuracy |
| Tech stack matching | +3% accuracy |

---

## Recommendations

Based on your estimation patterns:

1. **Add buffer to Frontend phases**
   - Average variance: +18%
   - Recommendation: Add 20% buffer to frontend estimates

2. **Setup phases consistently under**
   - Average variance: -15%
   - Recommendation: Reduce setup estimates by 10%

3. **New tech stacks need more buffer**
   - First project in stack: +25% avg variance
   - Recommendation: Add 30% buffer for unfamiliar stacks

---

## Quick Actions

```bash
# View detailed phase breakdown
/autopilot:compare --all --by=phase

# Compare by tech stack
/autopilot:compare --all --by=stack

# Export for analysis
/autopilot:compare --all --format=json --output=comparison.json

# View specific project
/autopilot:compare --project=mobile-backend
```
```

---

## Grouped Comparisons

### --by=phase

```markdown
## Comparison by Phase Type

| Phase Type | Projects | Avg Est. | Avg Actual | Variance | Accuracy |
|------------|----------|----------|------------|----------|----------|
| Setup | 15 | $0.15 | $0.13 | -13% | 87% 🟢 |
| Database | 12 | $0.35 | $0.38 | +9% | 91% ✅ |
| Auth | 10 | $0.45 | $0.52 | +16% | 84% ✅ |
| API | 14 | $0.85 | $0.89 | +5% | 95% ✅ |
| Business | 11 | $1.10 | $1.25 | +14% | 86% ✅ |
| Frontend | 9 | $1.40 | $1.65 | +18% | 82% ⚠️ |
| Testing | 13 | $0.65 | $0.62 | -5% | 95% ✅ |
| Security | 8 | $0.40 | $0.42 | +5% | 95% ✅ |
| Docs | 12 | $0.35 | $0.30 | -14% | 86% 🟢 |
| DevOps | 10 | $0.50 | $0.55 | +10% | 90% ✅ |

### Insights

**Under-estimated phases:** Frontend (+18%), Auth (+16%)
**Over-estimated phases:** Setup (-13%), Docs (-14%)

### Calibration Factors

Apply these multipliers to improve accuracy:

| Phase Type | Multiplier |
|------------|------------|
| Frontend | ×1.18 |
| Auth | ×1.16 |
| Business | ×1.14 |
| DevOps | ×1.10 |
| Database | ×1.09 |
| API | ×1.05 |
| Security | ×1.05 |
| Testing | ×0.95 |
| Setup | ×0.87 |
| Docs | ×0.86 |
```

### --by=model

```markdown
## Comparison by Model

| Model | Operations | Est. Tokens | Actual | Variance | Cost Accuracy |
|-------|------------|-------------|--------|----------|---------------|
| Haiku | 342 | 450K | 420K | -7% | 93% ✅ |
| Sonnet | 567 | 1.8M | 1.95M | +8% | 92% ✅ |
| Opus | 23 | 120K | 145K | +21% | 79% ⚠️ |

### Insights

- **Haiku:** Consistently accurate, slight over-estimation
- **Sonnet:** Reliable estimates, small under-estimation
- **Opus:** Under-estimated by 21%, add buffer for Opus tasks
```

### --by=stack

```markdown
## Comparison by Tech Stack

| Tech Stack | Projects | Avg Est. | Avg Actual | Variance | Accuracy |
|------------|----------|----------|------------|----------|----------|
| node-typescript-postgres | 5 | $4.50 | $4.38 | -3% | 97% ✅ |
| react-nextjs | 3 | $6.20 | $6.85 | +10% | 90% ✅ |
| python-fastapi | 2 | $3.10 | $3.25 | +5% | 95% ✅ |
| electron-react | 1 | $5.00 | $6.50 | +30% | 70% ⚠️ |

### Insights

- **Best estimates:** node-typescript-postgres (97% accuracy)
- **Needs calibration:** electron-react (+30% variance)
- **Tip:** First project in a new stack averages +25% variance
```

---

## Single Project Comparison

With `--project=mobile-backend`:

```markdown
# Project Comparison: mobile-backend

**Path:** /Users/user/projects/mobile-backend
**Completed:** 2026-01-25
**Tech Stack:** node, typescript, mongodb

---

## Overall

| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Total Cost | $6.00 | $7.92 | +32% ⚠️ |
| Phases | 10 | 10 | - |
| Tasks | 65 | 72 | +11% |
| Duration | 4h | 5.5h | +38% |

---

## Phase Breakdown

| Phase | Est. | Actual | Variance | Notes |
|-------|------|--------|----------|-------|
| 001 Setup | $0.15 | $0.14 | -7% | ✅ On track |
| 002 Database | $0.35 | $0.42 | +20% | MongoDB new |
| 003 Auth | $0.45 | $0.58 | +29% | JWT + refresh |
| 004 API | $0.85 | $1.12 | +32% | Added endpoints |
| 005 Business | $1.10 | $1.45 | +32% | Complex logic |
| 006 Frontend | $1.40 | $1.85 | +32% | Mobile-specific |
| 007 Testing | $0.65 | $0.72 | +11% | Extra coverage |
| 008 Security | $0.40 | $0.52 | +30% | Mobile security |
| 009 Docs | $0.35 | $0.32 | -9% | ✅ |
| 010 DevOps | $0.50 | $0.80 | +60% | CI/CD complex |

---

## Root Cause Analysis

### Why +32% variance?

1. **New tech stack (MongoDB)**
   - First MongoDB project
   - Learning curve added ~15% overhead

2. **Scope expansion during execution**
   - Added 7 tasks mid-project
   - Mobile-specific requirements emerged

3. **DevOps complexity underestimated**
   - Multi-environment setup
   - CI/CD for mobile builds

### Learnings Captured

- [ ] MongoDB projects need +20% buffer
- [ ] Mobile backends need +15% for platform-specific code
- [ ] CI/CD for mobile apps needs +40% buffer

---

## Comparison to Similar Projects

| Project | Stack | Cost | Variance | Accuracy |
|---------|-------|------|----------|----------|
| **mobile-backend** | node-mongo | $7.92 | +32% | 68% |
| api-service | node-postgres | $3.87 | -8% | 92% |
| user-auth | node-postgres | $4.85 | -7% | 93% |

**Insight:** Node+Postgres projects are well-calibrated. Node+MongoDB needs adjustment.
```

---

## JSON Output

With `--format=json`:

```json
{
  "report": {
    "timestamp": "2026-01-29T12:00:00Z",
    "projectsAnalyzed": 15,
    "timeRange": {
      "start": "2026-01-01",
      "end": "2026-01-29"
    }
  },
  "overall": {
    "averageAccuracy": 94.2,
    "averageVariance": 5.8,
    "bestEstimate": { "project": "project-x", "variance": -2 },
    "worstEstimate": { "project": "project-y", "variance": 32 }
  },
  "projects": [
    {
      "name": "my-api",
      "estimated": 4.50,
      "actual": 4.85,
      "variance": 7.8,
      "accuracy": 92.2
    }
  ],
  "byPhase": { ... },
  "byModel": { ... },
  "byStack": { ... },
  "trends": {
    "direction": "stable",
    "weeklyAccuracy": [95, 90, 96, 92]
  },
  "recommendations": [
    {
      "area": "Frontend phases",
      "issue": "Average +18% variance",
      "recommendation": "Add 20% buffer"
    }
  ]
}
```

---

## No History Found

If no completed projects exist:

```markdown
## No Comparison Data Available

No completed projects found in history.

**Build your first project:**
```bash
/autopilot:build "Your feature description"
```

After completing projects, comparison data will be available.
```

$ARGUMENTS
