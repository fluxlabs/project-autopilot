---
description: Deep analytics and pattern detection across projects and portfolio
argument-hint: "[--scope=project|portfolio] [--period=week|month|all] [--export]"
model: sonnet
---

# Autopilot: INSIGHTS Mode
# Project Autopilot - Deep analytics and patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Deep analytics and pattern detection for projects and portfolio-wide insights.

## Required Skills

**Read before analyzing:**
1. `/autopilot/skills/global-state/SKILL.md` - Historical data access
2. `/autopilot/skills/predictive-analytics/SKILL.md` - ML patterns

## Required Agents

- `history-tracker` - Access project history
- `debt-tracker` - Technical debt analysis

---

## Options

| Option | Description |
|--------|-------------|
| `--scope=scope` | Analysis scope: project, portfolio |
| `--period=period` | Time period: week, month, quarter, all |
| `--export` | Export report to file |
| `--trends` | Show trend analysis |
| `--costs` | Focus on cost analysis |
| `--efficiency` | Focus on efficiency metrics |

---

## Usage

### Project Insights

```bash
/autopilot:insights --scope=project
```

Output:
```markdown
## Project Insights: my-saas-app

### Summary
| Metric | Value | vs Average |
|--------|-------|------------|
| Total Cost | $4.85 | +8% |
| Phases | 8 | +0.5 |
| Tasks | 52 | +15% |
| Accuracy | 91% | -3% |

---

### Cost Analysis

#### Cost by Phase Type
```
Setup          ████░░░░░░░░░░░░░░░░ $0.12 (2%)
Database       ██████░░░░░░░░░░░░░░ $0.38 (8%)
Auth           ████████░░░░░░░░░░░░ $0.65 (13%)
API            ██████████████░░░░░░ $0.92 (19%)
Frontend       ████████████████████ $1.45 (30%)
Testing        ██████████░░░░░░░░░░ $0.68 (14%)
Other          ██████░░░░░░░░░░░░░░ $0.65 (14%)
```

#### Cost Variance by Phase
| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Setup | $0.15 | $0.12 | -20% ✅ |
| Database | $0.35 | $0.38 | +9% ✅ |
| Auth | $0.55 | $0.65 | +18% ⚠️ |
| API | $0.85 | $0.92 | +8% ✅ |
| Frontend | $1.20 | $1.45 | +21% ⚠️ |

#### Insight: Auth & Frontend phases consistently over-estimate
**Recommendation:** Apply 1.2x multiplier for these phases

---

### Efficiency Metrics

#### Task Completion Rate
```
Week 1: ██████████████████████████████ 100%
Week 2: █████████████████████████████░ 95%
Week 3: ████████████████████████░░░░░░ 80%
```

#### Cost per Task
| Phase | Tasks | Cost | Cost/Task |
|-------|-------|------|-----------|
| Setup | 3 | $0.12 | $0.04 |
| Database | 5 | $0.38 | $0.08 |
| Auth | 8 | $0.65 | $0.08 |
| API | 12 | $0.92 | $0.08 |
| Frontend | 18 | $1.45 | $0.08 |

**Insight:** Consistent cost per task (~$0.08) indicates good estimation

---

### Patterns Detected

1. **Frontend phases take 20% longer than estimated**
   - Confidence: High (5 data points)
   - Action: Increase frontend estimates by 20%

2. **Testing catch-up at end of project**
   - Pattern: Testing tasks spike in final phases
   - Action: Integrate testing throughout

3. **Model selection inefficiency**
   - 15% of Sonnet tasks could use Haiku
   - Potential savings: $0.35 (7%)

---

### Technical Debt Indicators

| Indicator | Level | Trend |
|-----------|-------|-------|
| Code complexity | Medium | → |
| Test coverage | Good (85%) | ↑ |
| Dependency age | Low | → |
| Documentation | Poor | ↓ |

**Recommended Focus:** Improve documentation before it becomes a blocker
```

### Portfolio Insights

```bash
/autopilot:insights --scope=portfolio
```

Output:
```markdown
## Portfolio Insights

**Period:** All Time
**Projects:** 25
**Total Investment:** $89.45

---

### Portfolio Health

```
┌─────────────────────────────────────────────────────────────┐
│                    PORTFOLIO OVERVIEW                        │
├─────────────────────────────────────────────────────────────┤
│  Projects: 25     │  Success Rate: 92%  │  Avg Cost: $3.58  │
│  Active: 3        │  Accuracy: 94%      │  Total: $89.45    │
│  Completed: 22    │  Trend: +2.3%       │  Budget: $150     │
└─────────────────────────────────────────────────────────────┘
```

---

### Cost Efficiency

#### Cost by Tech Stack
| Stack | Projects | Avg Cost | vs Overall |
|-------|----------|----------|------------|
| Next.js + Supabase | 8 | $2.85 | -20% ✅ |
| Node + PostgreSQL | 6 | $3.45 | -4% ✅ |
| React + Firebase | 5 | $4.12 | +15% ⚠️ |
| Python + Django | 4 | $3.80 | +6% |
| Other | 2 | $4.50 | +26% ⚠️ |

**Insight:** Next.js + Supabase is most cost-efficient

#### Cost by Phase Type (Portfolio-Wide)
| Phase Type | Total Cost | Avg Variance |
|------------|------------|--------------|
| Setup | $2.45 | -12% |
| Database | $8.90 | +5% |
| Auth | $12.30 | +18% |
| API | $18.50 | +8% |
| Frontend | $28.90 | +22% |
| Testing | $10.40 | -5% |

**Insight:** Frontend phases consistently exceed estimates by 22%

---

### Estimation Accuracy Trends

```
Month  Accuracy
Jan    ████████████████████░░░░ 82%
Feb    █████████████████████░░░ 88%
Mar    ██████████████████████░░ 92%
Apr    ███████████████████████░ 94%
May    ███████████████████████░ 95%
```

**Trend:** Accuracy improving +3.25% per month

#### By Phase Type
| Phase Type | Accuracy | Samples | Confidence |
|------------|----------|---------|------------|
| Setup | 98% | 25 | High |
| Database | 95% | 22 | High |
| Auth | 82% | 20 | Medium |
| API | 92% | 25 | High |
| Frontend | 78% | 23 | Medium |
| Testing | 95% | 20 | High |

---

### Learning Patterns

#### Top Learnings Applied
| Learning | Times Applied | Success Rate |
|----------|---------------|--------------|
| Auth phase buffer 1.3x | 15 | 95% |
| Frontend parallel tasks | 12 | 88% |
| Early validation setup | 10 | 100% |

#### Common Failure Patterns
| Pattern | Occurrences | Impact |
|---------|-------------|--------|
| Missing env validation | 8 | High |
| Late test integration | 6 | Medium |
| Underestimated auth | 5 | Medium |

---

### Recommendations

1. **Standardize on Next.js + Supabase** for web projects
   - 20% cost savings vs average
   - Fastest time-to-completion

2. **Apply frontend estimation buffer**
   - Current: 22% average overrun
   - Recommended: 1.25x multiplier

3. **Address recurring auth estimation**
   - 5 projects overran auth by >20%
   - Create auth estimation template

4. **Improve documentation phase**
   - 40% of projects have documentation debt
   - Add documentation checkpoints
```

---

## Behavior

```
FUNCTION generateInsights(options):

    # 1. Load data based on scope
    IF options.scope == 'project':
        data = loadCurrentProject()
    ELSE:
        data = loadPortfolioData()

    # 2. Filter by period
    IF options.period:
        data = filterByPeriod(data, options.period)

    # 3. Calculate metrics
    metrics = {
        costs: calculateCostMetrics(data),
        efficiency: calculateEfficiencyMetrics(data),
        accuracy: calculateAccuracyMetrics(data),
        trends: calculateTrends(data)
    }

    # 4. Detect patterns
    patterns = detectPatterns(data, metrics)

    # 5. Generate recommendations
    recommendations = generateRecommendations(patterns, metrics)

    # 6. Compile report
    report = compileInsightsReport(metrics, patterns, recommendations)

    # 7. Export if requested
    IF options.export:
        writeReport(report, ".autopilot/insights-report.md")

    DISPLAY report
```

---

## Quick Examples

```bash
# Current project insights
/autopilot:insights --scope=project

# Portfolio-wide analysis
/autopilot:insights --scope=portfolio

# Last month trends
/autopilot:insights --scope=portfolio --period=month --trends

# Cost analysis export
/autopilot:insights --costs --export

# Efficiency metrics
/autopilot:insights --efficiency
```

$ARGUMENTS
