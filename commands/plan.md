---
description: Project scoping and phase planning with aggressive token optimization (saves 60-80%).
argument-hint: [feature] [--dry-run] [--max-cost=N] [--from-scan]
model: sonnet
---

# Autopilot: PLAN Mode

**Token-optimized** project scoping and phase planning. Creates executable plans for `/autopilot:build`.

## Smart Detection

```
/autopilot:plan [description] [options]
    │
    ├── Has description?
    │   ├── Yes → Plan phases for that specific feature
    │   └── No  → Auto-scan project, plan phases for ALL remaining work
    │
    └── Output
        → Creates .autopilot/scope.md
        → Creates .autopilot/roadmap.md
        → Creates .autopilot/phases/{N}/PLAN.md files
        → Ready for /autopilot:build
```

### Usage Examples

```bash
# Plan a new feature
/autopilot:plan "user authentication"

# Plan based on existing scan
/autopilot:plan --from-scan

# Scan project and plan all remaining work
/autopilot:plan

# Dry run (just show what would be planned)
/autopilot:plan "payments" --dry-run

# Set cost estimate limit
/autopilot:plan "feature" --max-cost=25
```

## FIRST: Read Optimization Skill

```
BEFORE ANY WORK:
Read /autopilot/skills/token-optimization/SKILL.md
Apply ALL strategies throughout planning
```

## Required Skills

1. **`token-optimization`** - READ FIRST, apply always
2. **`user-experience`** - Consistent output patterns
3. **`state-management`** - STATE.md session bridge (read first, update last)
4. **`global-state`** - Cross-session persistence
5. **`visual-style`** - Colors and icons for output
6. `phase-ordering` - Phase sequence
7. `cost-estimation` - Estimates
8. `phase-template` - File format

## Required Agents

- `model-selector` - Choose Haiku/Sonnet/Opus per task
- `planner` - Create phases with estimates
- `history-tracker` - Cross-session persistence

---

## Standard Output Format

### Command Banner

```
╭─────────────────────────────────────────────────────────────╮
│  📋 AUTOPILOT: PLAN                                         │
│  Create execution phases for your project                   │
╰─────────────────────────────────────────────────────────────╯
```

### Planning Progress

```
▶ Analyzing Project

  Scanning codebase...
    ✓ Detected: TypeScript + React + Node.js
    ✓ Found 45 source files
    ✓ Existing coverage: 72%

  Loading historical data...
    ✓ Found 3 similar projects in history
    ✓ Average cost for this stack: $4.38
    ✓ Your estimation accuracy: 94%

  Generating phases...
    ✓ Phase 1: Project Setup ($0.15)
    ✓ Phase 2: Database Foundation ($0.35)
    ✓ Phase 3: Authentication ($0.55)
    ✓ Phase 4: API Layer ($0.85)
    ✓ Phase 5: Frontend ($1.20)
    ✓ Phase 6: Testing ($0.65)

─────────────────────────────────────────────────────────────
✅ PLAN CREATED
─────────────────────────────────────────────────────────────

  Phases:    6 phases, 3 waves
  Tasks:     32 total
  Estimate:  $4.75 (±15%, High confidence)

  Wave breakdown:
    Wave 1: Setup, Database (parallel)
    Wave 2: Auth, API, Frontend (parallel)
    Wave 3: Testing (sequential)

  Files created:
    ✓ .autopilot/scope.md
    ✓ .autopilot/roadmap.md
    ✓ .autopilot/phases/001/PLAN.md
    ✓ .autopilot/phases/002/PLAN.md
    ✓ .autopilot/phases/003/PLAN.md
    ✓ .autopilot/phases/004/PLAN.md
    ✓ .autopilot/phases/005/PLAN.md
    ✓ .autopilot/phases/006/PLAN.md

─────────────────────────────────────────────────────────────

  🔗 Next Steps

    • Review plan:    cat .autopilot/roadmap.md
    • Validate:       /autopilot:validate
    • Start build:    /autopilot:build
    • Auto-execute:   /autopilot:build -y

╰─────────────────────────────────────────────────────────────╯
```

---

## Options

```bash
--dry-run          # Show plan summary only, don't write files
--from-scan        # Use existing scan-report.md (skip auto-scan)
--max-cost=N       # Budget limit for estimates (default: $50)
--verbose          # Show detailed planning output
```

---

## OPTIMIZATION RULES (Apply Always)

### Rule 1: Partial File Reading

```bash
# ❌ NEVER
Read entire file: src/services/userService.ts

# ✅ ALWAYS
ls src/services/                              # List first
head -30 src/services/userService.ts          # Imports only
grep -n "functionName" src/services/*.ts      # Find location
sed -n '45,60p' src/services/userService.ts   # Specific lines
```

### Rule 2: Model Selection

Before EVERY agent spawn:

```
Spawn model-selector FIRST (runs on Haiku, cheap)
  ↓
Get recommended model
  ↓
Spawn actual agent on recommended model
```

```
| Task Type | Model | Cost |
|-----------|-------|------|
| File ops, simple edits | Haiku | $1/1M |
| Planning, reasoning | Sonnet | $3/1M |
| Architecture (rare) | Opus | $5/1M |
```

### Rule 3: Cache Everything

First task of session:
```
1. Read project structure → Cache in learnings.md
2. Read key types → Cache in learnings.md
3. Read conventions → Cache in learnings.md

NEVER re-read these files. Reference learnings.md instead.
```

### Rule 4: Concise Output

```
❌ "I will now proceed to analyze the project structure..."
✅ "Analyzing structure."

❌ "I have successfully completed the planning phase..."
✅ "✅ Plan complete"
```

---

## Phase 0: Load Global State (FIRST)

Before any work, load global configuration and historical data:

```
FUNCTION loadGlobalState():

    # 1. Check if global state exists
    globalDir = expandPath("~/.claude/autopilot/")
    IF NOT exists(globalDir):
        initializeGlobalState()  # Create default files

    # 2. Load user configuration
    config = readJSON(globalDir + "config.json")

    # Apply config defaults to this session:
    - maxCost = config.defaults.maxCost (unless --max-cost provided)
    - preferredModel = config.defaults.preferredModel

    # 3. Load historical data for estimation
    history = readJSON(globalDir + "history.json")
    learnings = readJSON(globalDir + "learnings.json")

    # 4. Find similar projects for better estimates
    techStack = detectTechStack(currentDir)
    similarProjects = findSimilarProjects(history, techStack)

    IF similarProjects.length > 0:
        LOG "Found {N} similar projects for estimation reference"
        estimationAdjustment = calculateAdjustment(similarProjects, learnings)
    ELSE:
        estimationAdjustment = 1.0

    # 5. Register this project in history (status: planning)
    projectId = SPAWN history-tracker → recordProjectStart({
        path: currentDir,
        description: [description] OR "Auto-scanned project",
        techStack: techStack,
        status: "planning"
    })

    STORE projectId for later updates
```

### Global Config Override

CLI arguments override global config:

| Argument | Overrides |
|----------|-----------|
| `--max-cost=N` | config.defaults.maxCost |

---

## Phase 1: Discovery (OPTIMIZED)

### 1.0 Smart Detection (FIRST)

```
IF no [description] provided:
    │
    ├── Check for .autopilot/scan-report.md
    │   ├── Exists AND --from-scan → Use existing scan
    │   └── Otherwise → Run full project scan (like /autopilot:scan)
    │
    └── Extract remaining work from scan
        → Use as implicit [description]

IF [description] provided:
    → Plan phases for that specific feature only
```

**Auto-scan output:** Creates `.autopilot/scan-report.md` with:
- Completed vs remaining work
- Cost estimates for remaining tasks
- Recommended phases

### 1.1 Minimal Analysis

```bash
# Step 1: Structure only (no content)
ls -la src/
find . -name "*.ts" -type f | head -20

# Step 2: Key files only
cat package.json | jq '.dependencies'
head -50 CLAUDE.md  # If exists

# Step 3: ONE example of each type
head -50 src/services/example.service.ts
head -30 src/routes/example.routes.ts

# Step 4: Cache findings
Write to .autopilot/learnings.md
```

### 1.2 Spawn Planner (Minimal Context)

```markdown
## Spawning: planner (via model-selector)

**Model:** Sonnet (planning needs reasoning)
**Task:** Create phases for [feature]
**Context:**
  - Stack: Node/TS (from package.json)
  - Pattern: See learnings.md

[NO file contents - planner reads what it needs]
```

### 1.3 Create Concise Scope (with Historical Context)

```markdown
# Scope: [Name]

## Historical Context
*Based on {N} similar projects*
| Metric | Historical Avg | This Project |
|--------|----------------|--------------|
| Total Cost | $3.50 | $2.50 (est) |
| Phases | 7 | 6 |
| Accuracy | 94% | - |

## Budget
| Phase | Est. | Historical |
|-------|------|------------|
| 001 | $0.15 | $0.12 avg |
| 002 | $0.32 | $0.35 avg |
| **Total** | **$2.50** | **$3.50 avg** |

*Estimates adjusted by historical accuracy factor*
```

If no similar projects found:

```markdown
# Scope: [Name]

## Budget
| Phase | Est. |
|-------|------|
| 001 | $0.15 |
| 002 | $0.32 |
| **Total** | **$2.50** |

*No similar projects in history - using base estimates*
```

### 1.4 Create Phase Plans

For each phase, create `.autopilot/phases/{N}/PLAN.md`:

```markdown
---
phase: N
name: Phase Name
wave: 1
autonomous: true
estimated_cost: $0.XX
estimated_tokens: XXXX
---

# Phase N: [Name]

## Goal
[What this phase accomplishes]

## Prerequisites
- Phase N-1 complete (if applicable)
- [Other dependencies]

## Tasks

### Task N.1: [Name]
- **Model:** Haiku/Sonnet
- **Files:** `path/to/file.ts`
- **Action:** [Specific action]

### Task N.2: [Name]
- **Model:** Haiku/Sonnet
- **Files:** `path/to/file.ts`
- **Action:** [Specific action]

## Validation
- [ ] Build passes
- [ ] Tests pass
- [ ] [Specific criteria]

## Estimated Cost
| Task | Model | Est. Tokens | Est. Cost |
|------|-------|-------------|-----------|
| N.1 | Haiku | 1000 | $0.00 |
| N.2 | Sonnet | 5000 | $0.02 |
| **Total** | - | 6000 | $0.02 |
```

### 1.5 Create Roadmap

Write `.autopilot/roadmap.md`:

```markdown
# Project Roadmap

## Overview
- **Feature:** [description]
- **Total Phases:** N
- **Estimated Cost:** $X.XX
- **Estimated Tokens:** XXX,XXX

## Phase Summary

| Phase | Name | Wave | Est. Cost | Dependencies |
|-------|------|------|-----------|--------------|
| 001 | Setup | 1 | $0.15 | None |
| 002 | Core | 1 | $0.32 | 001 |
| 003 | Tests | 2 | $0.18 | 002 |

## Execution Order
Phases are grouped into waves for parallel execution:
- **Wave 1:** 001, 002 (can run in parallel)
- **Wave 2:** 003 (depends on wave 1)

## Next Step
Run `/autopilot:build` to execute this plan.
```

### 1.6 Dry Run Output

If `--dry-run` flag:

```markdown
## Plan Summary (Dry Run)

**Feature:** [description]

### Phases
| # | Name | Tasks | Est. Cost |
|---|------|-------|-----------|
| 1 | Setup | 3 | $0.15 |
| 2 | Core Logic | 5 | $0.32 |
| 3 | Testing | 4 | $0.18 |

### Total Estimate
- **Phases:** 3
- **Tasks:** 12
- **Cost:** $0.65

*Dry run complete. Run without --dry-run to create plan files.*
```

---

## Output Files

### Created by /autopilot:plan
```
.autopilot/
├── STATE.md          # Session bridge - status: "planned"
├── scope.md          # Concise project scope
├── roadmap.md        # Phase breakdown with estimates
├── learnings.md      # Cached project knowledge
├── scan-report.md    # Auto-scan results (if no description)
└── phases/
    ├── 001/
    │   └── PLAN.md   # Phase 1 execution plan
    ├── 002/
    │   └── PLAN.md   # Phase 2 execution plan
    └── .../
```

### Global (cross-session)
```
~/.claude/autopilot/
├── config.json       # User preferences
├── history.json      # All projects (marked as "planning")
├── learnings.json    # Patterns
└── statistics.json   # Aggregate stats
```

---

## Completion

After planning completes:

```
FUNCTION finalizePlan():

    # 1. Update STATE.md
    Write STATE.md:
        Status: "planned"
        Phases: [count]
        Estimated cost: $X.XX
        Next action: "/autopilot:build"

    # 2. Update global history
    SPAWN history-tracker → updateProjectStatus(projectId, "planned")

    # 3. Display summary
    LOG "
    ## ✅ Plan Complete

    | Metric | Value |
    |--------|-------|
    | Phases | N |
    | Tasks | M |
    | Est. Cost | $X.XX |

    **Next:** Run `/autopilot:build` to execute the plan.
    "
```

---

## Expected Costs (Planning Only)

| Project Size | Planning Cost |
|--------------|---------------|
| Small | $0.10-0.25 |
| Medium | $0.25-0.50 |
| Large | $0.50-1.00 |

*Planning is cheap - execution is where costs accumulate.*

$ARGUMENTS
