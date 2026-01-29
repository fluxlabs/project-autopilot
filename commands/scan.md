---
description: Scan project to assess completion status with cost estimates for remaining work.
argument-hint: [--phase=N]
model: sonnet
---

# Autopilot: SCAN Mode

Analyze this project and generate a completion status report with cost estimates, enhanced by historical data from similar projects.

## Required Skills

**Read for cost estimation:**
- `/autopilot/skills/cost-estimation/SKILL.md` - Token estimation guidelines
- `/autopilot/skills/global-state/SKILL.md` - Historical data access

## Required Agents

- `history-tracker` - Find similar projects for estimation

## Your Task

### Step 0: Load Historical Context (FIRST)

```
FUNCTION loadHistoricalContext():

    # 1. Load global state if available
    globalDir = expandPath("~/.claude/autopilot/")
    IF exists(globalDir):
        config = readJSON(globalDir + "config.json")
        history = readJSON(globalDir + "history.json")
        learnings = readJSON(globalDir + "learnings.json")

        # 2. Detect tech stack
        techStack = detectTechStack(currentDir)

        # 3. Find similar projects
        similarProjects = SPAWN history-tracker → getSimilarProjects(techStack)

        IF similarProjects.length > 0:
            LOG "Found {N} similar projects in history"
            estimationData = {
                hasSimilar: true,
                projects: similarProjects,
                avgCost: calculateAvgCost(similarProjects),
                avgPhases: calculateAvgPhases(similarProjects),
                accuracy: learnings.estimationAccuracy.overall
            }
        ELSE:
            estimationData = { hasSimilar: false }

    ELSE:
        estimationData = { hasSimilar: false }
        LOG "No global history found. Using base estimates."
        LOG "Tip: Run /autopilot:config to set up cross-session persistence"

    RETURN estimationData
```

### Step 1: Read project configuration

- Check for `.autopilot/` folder (existing autopilot state)
- Read CLAUDE.md, package.json, configs
- Understand the tech stack

### Step 2: Analyze codebase

- Scan all source files
- Identify implemented features
- Find TODOs, FIXMEs, incomplete code
- Check test coverage

### Step 3: Estimate remaining work (with historical adjustment)

- Calculate tasks needed per feature
- Apply cost estimation guidelines
- **Apply historical accuracy adjustment if available**
- Sum to project total

### Step 4: Generate scan report (with historical comparison)

Create `.autopilot/scan-report.md` with:

```markdown
# Project Scan Report: [Project Name]
**Scanned:** [Date/Time]

---

## Project Overview
- **Type:** [Web app, API, CLI, etc.]
- **Stack:** [Technologies detected]
- **Size:** [File count, LOC estimate]

---

## 📊 Historical Context

*If similar projects found:*

### Similar Projects in History
| Project | Stack Match | Cost | Phases | Variance |
|---------|-------------|------|--------|----------|
| my-api | 90% | $4.85 | 8 | -7% |
| auth-service | 85% | $3.20 | 6 | +5% |
| user-mgmt | 80% | $5.10 | 9 | +12% |

**Historical Average:** $4.38 for similar projects
**Your Estimation Accuracy:** 94% (based on 12 projects)

### Adjusted Estimates
Estimates below are adjusted by your historical accuracy (+6% buffer)

*If no similar projects:*

### No Historical Data
This appears to be a new tech stack combination.
Run `/autopilot:config` to enable cross-session learning.

---

## 💰 Cost Estimate Summary

### Remaining Work Estimate
| Category | Tasks | Est. Tokens | Base Est. | Adjusted | Confidence |
|----------|-------|-------------|-----------|----------|------------|
| New Features | [N] | [X]K | $[Y] | $[Y*adj] | Medium |
| Bug Fixes | [N] | [X]K | $[Y] | $[Y*adj] | High |
| Tests | [N] | [X]K | $[Y] | $[Y*adj] | Medium |
| Documentation | [N] | [X]K | $[Y] | $[Y*adj] | High |
| Tech Debt | [N] | [X]K | $[Y] | $[Y*adj] | Low |
| **Total** | **[N]** | **[X]K** | **$[Y]** | **$[Y*adj]** | |

*Adjusted estimates include historical accuracy factor*

### Recommended Budget
| Type | Amount | Reasoning |
|------|--------|-----------|
| Adjusted Estimate | $[X] | Base + accuracy adjustment |
| Buffer (1.25x) | $[Y] | For unknowns |
| **Recommended** | **$[Z]** | Set --max-cost |
| Historical Avg | $[H] | Similar projects averaged |

---

## ✅ Completed Work

### [Feature Area]
| Feature | Status | Files | Evidence |
|---------|--------|-------|----------|
| [Feature] | ✅ Done | `file.ts` | Has tests, documented |

---

## 🟡 Partial Work

### [Feature Area]
| Feature | Status | Files | What's Missing | Est. Cost |
|---------|--------|-------|----------------|-----------|
| [Feature] | 🟡 ~60% | `file.ts` | No validation | $0.05 |

---

## ⏳ Remaining Work

### [Feature Area]
| Feature | Priority | Complexity | Tasks | Est. Cost |
|---------|----------|------------|-------|-----------|
| [Feature] | High | Medium | 4 | $0.15 |
| [Feature] | Medium | Simple | 2 | $0.05 |

### Estimated Phase Breakdown
| Phase | Description | Tasks | Est. Cost |
|-------|-------------|-------|-----------|
| Database | Schema changes | 3 | $0.12 |
| API | New endpoints | 5 | $0.25 |
| Frontend | UI components | 8 | $0.45 |
| Testing | Coverage | 6 | $0.20 |
| **Total** | | **22** | **$1.02** |

---

## Technical Debt
| Issue | Location | Severity | Est. Fix Cost |
|-------|----------|----------|---------------|
| [Issue] | `file:line` | High | $0.03 |
| [Issue] | `file:line` | Medium | $0.02 |

---

## Recommendations

### Do First
1. [Critical item] - Est: $[X]

### Short Term
1. [Important item] - Est: $[X]

---

## Next Steps

```bash
# Create plan from scan results (dry run first)
/autopilot:plan --from-scan --dry-run

# Create plan from scan with budget
/autopilot:plan --from-scan --max-cost=[recommended]

# Create the plan, then execute
/autopilot:plan --from-scan
/autopilot:build

# Execute immediately without approval
/autopilot:build -y
```

**Recommended budget:** `--max-cost=$[Z]` based on estimates
```

### Step 5: Present findings

- Show the scan report with cost estimates
- Compare with historical data if available
- Recommend appropriate budget
- Offer to generate phase files for remaining work

### Tips Based on History

*If historical data available:*

```markdown
## 💡 Tips from Similar Projects

Based on your history with [tech stack]:

1. **Setup Phase** - Usually 15% under estimate (you're efficient here)
2. **Frontend Phase** - Often 18% over estimate (add buffer)
3. **Common Issues:**
   - Missing env vars (happened 5x) - Add .env.example early
   - Type errors (happened 3x) - Use strict TS config

**Recommended approach:** Based on auth-service project pattern
```

---

## Historical Learning Integration

After scan completes, learnings are automatically applied:

| Phase Type | Your Avg Variance | Adjustment Applied |
|------------|-------------------|-------------------|
| Setup | -15% | Use base estimate |
| Database | +8% | +8% buffer |
| Auth | +12% | +12% buffer |
| API | +5% | +5% buffer |
| Frontend | +18% | +18% buffer |
| Testing | -5% | Use base estimate |

This improves estimate accuracy from ~85% to ~95% over time.

$ARGUMENTS
