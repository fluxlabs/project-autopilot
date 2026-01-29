---
description: Cost estimate without execution
argument-hint: "[feature] - Description to estimate"
model: haiku
---

# Autopilot: ESTIMATE Mode
# Project Autopilot - Cost estimation without execution
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Generate cost and token estimates for a feature without executing any work. Useful for budget planning and scope validation.

## Required Skills

**Read before estimating:**
1. `/autopilot/skills/cost-estimation/SKILL.md` - Token estimation guidelines
2. `/autopilot/skills/phase-ordering/SKILL.md` - Phase dependencies
3. `/autopilot/skills/global-state/SKILL.md` - Historical data for accuracy

## Required Agents

- `planner` - Create phase breakdown with estimates
- `history-tracker` - Find similar projects for calibration

---

## Options

| Option | Description |
|--------|-------------|
| `--format=md\|json` | Output format (default: md) |
| `--output=path` | Write to file instead of console |
| `--detailed` | Show task-level breakdown |
| `--no-history` | Skip historical comparison |

---

## Behavior

### Input Processing

```
/autopilot:estimate [description]
    │
    └── Analyze description
        ├── Extract feature requirements
        ├── Identify tech stack (from project or description)
        └── Determine scope complexity
```

### Estimation Pipeline

```
FUNCTION estimate(description):

    # 1. Load historical data (if available)
    IF NOT args.noHistory:
        history = SPAWN history-tracker → findSimilarProjects(
            techStack: detectTechStack(currentDir),
            description: description
        )
        calibration = calculateCalibration(history)
    ELSE:
        calibration = 1.0

    # 2. Generate phase breakdown
    phases = SPAWN planner → createPhases({
        description: description,
        estimateOnly: true,  # No file creation
        calibration: calibration
    })

    # 3. Calculate totals
    totals = {
        phases: phases.length,
        tasks: sumTasks(phases),
        inputTokens: sumInputTokens(phases),
        outputTokens: sumOutputTokens(phases),
        estimatedCost: sumCosts(phases) * calibration,
        confidence: calculateConfidence(history, phases)
    }

    # 4. Generate output
    IF args.format == "json":
        RETURN formatJSON(phases, totals, history)
    ELSE:
        RETURN formatMarkdown(phases, totals, history)
```

---

## Output Format (Markdown)

```markdown
# Cost Estimate: [Feature Description]

**Generated:** [Timestamp]
**Tech Stack:** [Detected or specified]

---

## Summary

| Metric | Estimate | Confidence |
|--------|----------|------------|
| Phases | [N] | - |
| Tasks | [M] | - |
| Input Tokens | ~[X]K | [High/Med/Low] |
| Output Tokens | ~[Y]K | [High/Med/Low] |
| **Total Cost** | **$[Z]** | **[High/Med/Low]** |

### Cost Range
| Scenario | Cost |
|----------|------|
| Optimistic (-20%) | $[X] |
| **Expected** | **$[Y]** |
| Pessimistic (+30%) | $[Z] |

---

## Historical Context

*Based on [N] similar projects*

| Metric | Historical Avg | This Estimate |
|--------|----------------|---------------|
| Phases | [X] | [Y] |
| Total Cost | $[X] | $[Y] |
| Accuracy | [X]% | - |

**Calibration Applied:** [X]% adjustment based on historical variance

---

## Phase Breakdown

| Phase | Description | Est. Cost | Confidence |
|-------|-------------|-----------|------------|
| 001 | Setup | $0.15 | High |
| 002 | Database | $0.32 | Medium |
| 003 | Auth | $0.45 | Medium |
| ... | ... | ... | ... |
| **Total** | | **$X.XX** | |

---

## Task-Level Detail (--detailed)

### Phase 001: Setup
| Task | Description | Model | Est. Cost |
|------|-------------|-------|-----------|
| 001.1 | Initialize project | Haiku | $0.02 |
| 001.2 | Configure TypeScript | Haiku | $0.03 |
| ... | ... | ... | ... |

### Phase 002: Database
| Task | Description | Model | Est. Cost |
|------|-------------|-------|-----------|
| 002.1 | Design schema | Sonnet | $0.08 |
| ... | ... | ... | ... |

---

## Assumptions

- Stack: [Detected/Assumed tech stack]
- Complexity: [Simple/Medium/Complex]
- Testing: Standard coverage (80%)
- Documentation: Basic inline + README

---

## Next Steps

```bash
# Execute this scope
/autopilot:build [description] -y

# Export full plan
/autopilot:export --format=json

# Modify budget limits
/autopilot:build [description] --max-cost=[amount]
```
```

---

## Output Format (JSON)

With `--format=json`:

```json
{
  "estimate": {
    "description": "[Feature description]",
    "timestamp": "2026-01-29T00:00:00Z",
    "techStack": ["node", "typescript", "postgres"]
  },
  "summary": {
    "phases": 8,
    "tasks": 45,
    "inputTokens": 850000,
    "outputTokens": 320000,
    "estimatedCost": 4.52,
    "confidence": "medium",
    "range": {
      "optimistic": 3.62,
      "expected": 4.52,
      "pessimistic": 5.88
    }
  },
  "historical": {
    "similarProjects": 3,
    "avgCost": 4.15,
    "avgAccuracy": 94,
    "calibration": 1.05
  },
  "phases": [
    {
      "id": "001",
      "name": "Setup",
      "tasks": 4,
      "estimatedCost": 0.15,
      "confidence": "high"
    },
    ...
  ],
  "tasks": [
    {
      "id": "001.1",
      "phase": "001",
      "description": "Initialize project",
      "model": "haiku",
      "estimatedCost": 0.02
    },
    ...
  ]
}
```

---

## Confidence Levels

| Level | Conditions | Range |
|-------|------------|-------|
| High | Similar projects exist, standard tech stack | ±15% |
| Medium | Some similar projects, known patterns | ±25% |
| Low | No history, novel requirements | ±40% |

---

## Quick Start Examples

```bash
# Basic estimate
/autopilot:estimate "Add user authentication with JWT"

# Detailed breakdown
/autopilot:estimate "REST API for task management" --detailed

# Export to file
/autopilot:estimate "E-commerce checkout flow" --output=estimate.md

# JSON for tooling integration
/autopilot:estimate "Mobile app backend" --format=json --output=estimate.json

# Skip historical comparison
/autopilot:estimate "New experimental feature" --no-history
```

---

## No Execution Guarantee

This command is **read-only**:
- No files created
- No git operations
- No state changes
- No agent spawning for implementation
- No cost incurred beyond the estimate calculation itself

The estimate itself uses ~2-5K tokens (Haiku model).

$ARGUMENTS
