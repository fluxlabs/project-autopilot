---
description: Analyze and track technical debt across the project
argument-hint: "[--check --threshold=N] [--allocate --budget=20%] [--report --format=release]"
model: sonnet
---

# Autopilot: DEBT Mode

Technical debt assessment powered by the `debt-tracker` agent.

## Required Agents
- `debt-tracker` - Technical debt identification and scoring
- `model-selector` - Choose optimal model (optional)

## Usage

```bash
# Fail CI if debt score exceeds threshold
/autopilot:debt --check --threshold=50

# Allocate debt budget for the sprint
/autopilot:debt --allocate --budget=20%

# Generate release-ready debt summary
/autopilot:debt --report --format=release
```

## Behavior

```
FUNCTION debt(options):
    ensureDir('.autopilot/')

    IF options.check:
        SPAWN debt-tracker → checkDebt(threshold=options.threshold)
    IF options.allocate:
        SPAWN debt-tracker → allocateBudget(budget=options.budget)
    IF options.report:
        SPAWN debt-tracker → generateReport(format=options.format)
```

