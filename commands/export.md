---
description: Export project plan as markdown or JSON
argument-hint: "[--format=md|json] [--output=path] [--include=all|scope|phases|costs]"
model: haiku
---

# Autopilot: EXPORT Mode
# Project Autopilot - Plan export functionality
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Export project plans, roadmaps, and cost data for documentation, sharing, or integration with external tools.

## Required Skills

**Read before exporting:**
1. `/autopilot/skills/global-state/SKILL.md` - Access project data

---

## Options

| Option | Description |
|--------|-------------|
| `--format=md\|json` | Output format (default: md) |
| `--output=path` | Write to file (default: stdout) |
| `--include=X` | What to include (see below) |
| `--no-actuals` | Exclude actual costs (estimates only) |

### Include Options

| Value | Contents |
|-------|----------|
| `all` | Everything (default) |
| `scope` | Scope and summary only |
| `phases` | Phase breakdown only |
| `costs` | Cost tracking only |
| `roadmap` | Roadmap visualization |

---

## Behavior

```
FUNCTION export(options):

    # 1. Verify project exists
    IF NOT exists(".autopilot/"):
        ERROR "No project found. Run /autopilot:takeoff (auto-creates plan) or /autopilot:flightplan first."
        RETURN

    # 2. Read project files
    scope = readFile(".autopilot/scope.md")
    roadmap = readFile(".autopilot/roadmap.md")
    tokenUsage = readFile(".autopilot/token-usage.md")
    phases = glob(".autopilot/phases/*.md")
    state = readFile(".autopilot/STATE.md")

    # 3. Build export data
    exportData = {
        meta: extractMeta(scope, state),
        summary: extractSummary(scope),
        phases: extractPhases(phases),
        costs: extractCosts(tokenUsage),
        progress: extractProgress(state)
    }

    # 4. Filter by include option
    IF args.include != "all":
        exportData = filterByInclude(exportData, args.include)

    # 5. Format output
    IF args.format == "json":
        output = formatJSON(exportData)
    ELSE:
        output = formatMarkdown(exportData)

    # 6. Write or display
    IF args.output:
        writeFile(args.output, output)
        LOG "Exported to {args.output}"
    ELSE:
        DISPLAY output
```

---

## Output Format (Markdown)

```markdown
# Project Export: [Project Name]

**Exported:** [Timestamp]
**Status:** [In Progress / Complete]
**Progress:** [X]% ([N] of [M] phases)

---

## Overview

**Description:** [Project description]
**Tech Stack:** [node, typescript, postgres]
**Started:** [Date]
**Last Updated:** [Date]

---

## Budget Summary

| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Total Cost | $6.52 | $2.85 | -56% |
| Input Tokens | 1.2M | 520K | -57% |
| Output Tokens | 450K | 195K | -57% |

### Cost Status
```
Progress: ████████░░░░░░░░░░░░ 44%
Budget:   ██████░░░░░░░░░░░░░░ 6% ($2.85 / $50.00)
```

---

## Phase Roadmap

```
Phase 001: Setup ✅
    ↓
Phase 002: Database ✅
    ↓
Phase 003: Auth ✅
    ↓
Phase 004: API 🔄 (In Progress)
    ↓
Phase 005: Business Logic ⏳
    ↓
Phase 006: Frontend ⏳
    ↓
Phase 007: Testing ⏳
    ↓
Phase 008: Documentation ⏳
```

---

## Phase Details

### Phase 001: Setup ✅
**Status:** Complete
**Cost:** Est. $0.15 → Actual $0.12 (-20%)

| Task | Description | Status | Cost |
|------|-------------|--------|------|
| 001.1 | Initialize project | ✅ | $0.02 |
| 001.2 | Configure TypeScript | ✅ | $0.03 |
| 001.3 | Setup testing | ✅ | $0.04 |
| 001.4 | Configure linting | ✅ | $0.03 |

### Phase 002: Database ✅
**Status:** Complete
**Cost:** Est. $0.32 → Actual $0.35 (+9%)

[... more phases ...]

---

## Cost Tracking

### By Phase
| Phase | Estimated | Actual | Variance | Status |
|-------|-----------|--------|----------|--------|
| 001 | $0.15 | $0.12 | -20% | ✅ |
| 002 | $0.32 | $0.35 | +9% | ✅ |
| 003 | $0.45 | $0.48 | +7% | ✅ |
| 004 | $0.85 | $0.42 | -51% | 🔄 |
| 005-008 | $4.75 | - | - | ⏳ |

### By Model
| Model | Operations | Tokens | Cost |
|-------|------------|--------|------|
| Haiku | 45 | 125K | $0.31 |
| Sonnet | 89 | 390K | $2.54 |
| Opus | 0 | 0 | $0.00 |

---

## Resume Information

**Current Position:** Phase 4, Task 4.5
**Checkpoint:** .autopilot/STATE.md

```bash
# Resume this project
/autopilot:cockpit

# View live status
/autopilot:altitude
```

---

*Exported by Autopilot v2.0*
```

---

## Output Format (JSON)

```json
{
  "export": {
    "version": "2.0",
    "timestamp": "2026-01-29T12:00:00Z",
    "format": "json"
  },
  "project": {
    "name": "my-project",
    "description": "Task management API",
    "path": "/path/to/project",
    "techStack": ["node", "typescript", "postgres"],
    "status": "in_progress",
    "progress": 44,
    "started": "2026-01-28T10:00:00Z",
    "updated": "2026-01-29T12:00:00Z"
  },
  "budget": {
    "estimated": {
      "totalCost": 6.52,
      "inputTokens": 1200000,
      "outputTokens": 450000
    },
    "actual": {
      "totalCost": 2.85,
      "inputTokens": 520000,
      "outputTokens": 195000
    },
    "limits": {
      "maxCost": 50,
      "warnCost": 10,
      "alertCost": 25
    },
    "variance": {
      "percentage": -56,
      "status": "under_budget"
    }
  },
  "phases": [
    {
      "id": "001",
      "name": "Setup",
      "status": "complete",
      "estimated": 0.15,
      "actual": 0.12,
      "variance": -20,
      "tasks": [
        {
          "id": "001.1",
          "description": "Initialize project",
          "status": "complete",
          "cost": 0.02
        }
      ]
    }
  ],
  "resume": {
    "currentPhase": 4,
    "currentTask": "004.5",
    "checkpointPath": ".autopilot/STATE.md"
  }
}
```

---

## Include Filters

### --include=scope

```markdown
# Project: [Name]

**Description:** [Description]
**Tech Stack:** [Stack]
**Status:** [Status]
**Progress:** [X]%

## Summary
| Metric | Value |
|--------|-------|
| Phases | [N] |
| Tasks | [M] |
| Est. Cost | $[X] |
```

### --include=costs

```markdown
# Cost Report: [Name]

## Summary
| Metric | Estimated | Actual |
|--------|-----------|--------|
| Total | $6.52 | $2.85 |

## By Phase
[Phase cost table]

## By Model
[Model cost table]

## Projections
[Remaining cost estimates]
```

### --include=roadmap

```markdown
# Roadmap: [Name]

## Visual Roadmap
[ASCII/text roadmap visualization]

## Phase Dependencies
[Dependency list]

## Critical Path
[Longest path through phases]
```

---

## Quick Start Examples

```bash
# Export everything to stdout
/autopilot:export

# Export to markdown file
/autopilot:export --output=PROJECT-EXPORT.md

# Export as JSON for tooling
/autopilot:export --format=json --output=project.json

# Export just the roadmap
/autopilot:export --include=roadmap

# Export costs only (for reporting)
/autopilot:export --include=costs --output=cost-report.md

# Export estimates only (hide actuals)
/autopilot:export --no-actuals --output=scope.md
```

---

## Integration Use Cases

### CI/CD Pipeline
```bash
# Generate JSON for pipeline metrics
/autopilot:export --format=json --include=costs > metrics.json
```

### Documentation
```bash
# Include in project README
/autopilot:export --include=scope >> README.md
```

### Reporting
```bash
# Weekly cost report
/autopilot:export --include=costs --output=reports/week-$(date +%U).md
```

### External Tools
```bash
# Feed to dashboard
/autopilot:export --format=json | curl -X POST https://dashboard/api/projects -d @-
```

---

## No Project Found

If `.autopilot/` doesn't exist:

```markdown
## Error: No Project Found

No Autopilot project exists in this directory.

**Start a project:**
```bash
/autopilot:takeoff "Your feature description"
```

**Or export from a specific project:**
```bash
cd /path/to/project && /autopilot:export
```
```

$ARGUMENTS
