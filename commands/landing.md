---
description: Validate phase ordering, dependencies, and wave assignments before execution.
argument-hint: [--fix] [--strict] [--quiet]
model: sonnet
---

# Autopilot: LANDING Mode

// Project Autopilot - Final Approach Validation
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Validate** phase ordering, dependencies, and wave assignments to ensure correct execution order before running `/autopilot:takeoff`.

---

## Purpose

Catches ordering issues **before** execution:
- Phases depending on later phases (forward dependencies)
- Circular dependency chains
- Wave assignments that violate dependency order
- Missing prerequisite declarations
- Violations of canonical phase ordering rules

---

## Options

| Option | Description |
|--------|-------------|
| `--fix` | Auto-fix simple ordering issues where possible |
| `--strict` | Fail on warnings (not just errors) |
| `--quiet` | Minimal output (CI mode) - exit code only |
| `--phase=N` | Validate specific phase only |

---

## Required Skills

**MUST read before validation:**
- `/autopilot/skills/user-experience/SKILL.md` - Consistent output patterns
- `/autopilot/skills/phase-ordering/SKILL.md` - Canonical order and dependency rules

---

## Standard Output Format

### Command Banner

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛬 AUTOPILOT: LANDING
   Final approach - check phase ordering and dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Validation Checks

```
▶ Running Pre-Landing Checks

  Parsing phases...
    ✓ Found 6 phases in .autopilot/phases/

  Checking dependencies...
    ✓ No forward dependencies
    ✓ No circular dependencies

  Validating wave assignments...
    ✓ Wave 1: 2 phases (parallel)
    ✓ Wave 2: 3 phases (parallel)
    ✓ Wave 3: 1 phase (sequential)

  Checking canonical order...
    ✓ Setup → Database → Auth → API → Frontend → Testing

─────────────────────────────────────────────────────────────
✅ CLEARED TO LAND
─────────────────────────────────────────────────────────────

  Phases:       6 validated
  Waves:        3 (optimized for parallel execution)
  Dependencies: All resolved correctly

  Ready for takeoff: /autopilot:takeoff

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### On Validation Failure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛬 AUTOPILOT: LANDING
   Final approach - check phase ordering and dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▶ Running Pre-Landing Checks

  Parsing phases...
    ✓ Found 6 phases in .autopilot/phases/

  Checking dependencies...
    ✗ Forward dependency detected

─────────────────────────────────────────────────────────────
❌ LANDING ABORTED
─────────────────────────────────────────────────────────────

  Found 1 error that must be fixed:

  Error 1: FORWARD_DEPENDENCY
  ─────────────────────────────
  Location: .autopilot/phases/003/ROUTE.md
  Issue:    Phase 3 depends on Phase 5

  Why this matters:
    Phase 3 cannot run before Phase 5 completes.
    This would cause the flight to fail mid-execution.

  How to fix:
    • Edit Phase 3's depends_on to remove Phase 5
    • Or reorder phases so Phase 5 comes before Phase 3
    • Or run: /autopilot:landing --fix

─────────────────────────────────────────────────────────────

  Options:
    /autopilot:landing --fix    Auto-fix simple issues
    /autopilot:landing          Re-run after manual fix

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Validation Algorithm

### Step 1: Parse All Phase Routes

```
FUNCTION parsePhases():

    phases = []
    phaseDir = ".autopilot/phases/"

    IF NOT exists(phaseDir):
        ERROR "No phases found. Run /autopilot:flightplan first."
        EXIT 1

    FOR each directory in phaseDir (sorted numerically):
        phaseNum = extractNumber(directory)  # e.g., "001" → 1

        # Find all ROUTE.md files in phase directory
        routes = glob("{phaseDir}/{directory}/*.md")

        FOR each routeFile in routes:
            frontmatter = parseFrontmatter(routeFile)

            phase = {
                number: phaseNum,
                plan: frontmatter.plan or 1,
                wave: frontmatter.wave or 1,
                autonomous: frontmatter.autonomous or true,
                depends_on: frontmatter.depends_on or [],
                prerequisites: extractPrerequisites(routeFile),
                name: extractPhaseName(routeFile),
                file: routeFile
            }
            phases.append(phase)

    RETURN phases
```

### Step 2: Build Dependency Graph

```
FUNCTION buildDependencyGraph(phases):

    graph = new DirectedGraph()

    FOR each phase in phases:
        nodeId = "{phase.number}.{phase.plan}"
        graph.addNode(nodeId, phase)

        # Add edges for explicit depends_on
        FOR each dep in phase.depends_on:
            depId = "{phase.number}.{dep}"  # e.g., "3.01" depends on "3.02"
            graph.addEdge(depId, nodeId)

        # Add edges for prerequisite phases
        FOR each prereq in phase.prerequisites:
            prereqId = "{prereq}.1"  # Phase prereq, default plan 1
            graph.addEdge(prereqId, nodeId)

    RETURN graph
```

### Step 3: Detect Cycles

```
FUNCTION detectCycles(graph):

    cycles = []
    visited = {}
    recursionStack = {}

    FUNCTION dfs(node, path):
        visited[node] = true
        recursionStack[node] = true
        path.append(node)

        FOR each neighbor in graph.neighbors(node):
            IF NOT visited[neighbor]:
                result = dfs(neighbor, path.copy())
                IF result:
                    cycles.append(result)
            ELSE IF recursionStack[neighbor]:
                # Found cycle
                cycleStart = path.indexOf(neighbor)
                cycle = path.slice(cycleStart)
                cycle.append(neighbor)  # Complete the cycle
                RETURN cycle

        recursionStack[node] = false
        RETURN null

    FOR each node in graph.nodes:
        IF NOT visited[node]:
            dfs(node, [])

    RETURN cycles
```

### Step 4: Validate Ordering Rules

```
FUNCTION validateOrdering(phases):

    errors = []
    warnings = []

    # Load canonical order from phase-ordering skill
    canonicalOrder = {
        "Setup": 1,
        "Database": 2,
        "Infrastructure": 3,
        "Auth": 4,
        "API": 5,
        "Business Logic": 6,
        "Frontend": 7,
        "Features": 8,
        "Testing": 9,
        "Security": 10,
        "Documentation": 11,
        "DevOps": 12,
        "Polish": 13
    }

    # Hard dependency rules
    hardDeps = {
        "Database": ["Setup"],
        "Auth": ["Database"],
        "API": ["Infrastructure", "Auth"],
        "Business Logic": ["Database", "API"],
        "Frontend": ["API"],
        "Features": ["Business Logic", "Frontend"],
        "Testing": ["Features"],
        "Security": ["Features", "Testing"],
        "Documentation": ["Features"],
        "DevOps": ["Testing", "Security"],
        "Polish": ["all"]
    }

    FOR each phase in phases:
        phaseType = detectPhaseType(phase.name)

        # Rule 1: No forward dependencies
        FOR each dep in phase.depends_on:
            depPhase = findPhase(phases, phase.number, dep)
            IF depPhase AND depPhase.number > phase.number:
                errors.append({
                    type: "FORWARD_DEPENDENCY",
                    phase: phase.number,
                    plan: phase.plan,
                    depends_on: dep,
                    message: "Phase {phase.number} depends on later phase {depPhase.number}"
                })

        # Rule 2: Check canonical order
        IF phaseType AND canonicalOrder[phaseType]:
            expectedOrder = canonicalOrder[phaseType]
            IF phase.number < expectedOrder - 2:  # Allow some flexibility
                warnings.append({
                    type: "EARLY_PHASE",
                    phase: phase.number,
                    name: phase.name,
                    expected: expectedOrder,
                    message: "{phaseType} phase typically comes at position {expectedOrder}, found at {phase.number}"
                })

        # Rule 3: Check hard dependencies
        IF phaseType AND hardDeps[phaseType]:
            requiredDeps = hardDeps[phaseType]
            FOR each reqDep in requiredDeps:
                IF reqDep == "all":
                    CONTINUE  # Special case for Polish
                reqDepPhase = findPhaseByType(phases, reqDep)
                IF reqDepPhase AND reqDepPhase.number >= phase.number:
                    errors.append({
                        type: "MISSING_HARD_DEPENDENCY",
                        phase: phase.number,
                        name: phase.name,
                        requires: reqDep,
                        message: "{phaseType} requires {reqDep} to complete first"
                    })

        # Rule 4: Validate wave assignments
        FOR each dep in phase.depends_on:
            depPhase = findPhase(phases, phase.number, dep)
            IF depPhase AND depPhase.wave >= phase.wave:
                errors.append({
                    type: "INVALID_WAVE",
                    phase: phase.number,
                    plan: phase.plan,
                    wave: phase.wave,
                    dep_wave: depPhase.wave,
                    message: "Route {phase.plan} (wave {phase.wave}) depends on route {dep} (wave {depPhase.wave}) - dependency must be in earlier wave"
                })

    RETURN { errors, warnings }
```

### Step 5: Generate Report

```
FUNCTION generateReport(phases, cycles, errors, warnings):

    report = []

    # Header
    report.append("# 🛬 Landing Validation Report")
    report.append("")
    report.append("**Project:** " + getProjectName())
    report.append("**Validated:** " + timestamp())
    report.append("")

    # Summary
    hasErrors = cycles.length > 0 OR errors.length > 0
    hasWarnings = warnings.length > 0

    IF NOT hasErrors AND NOT hasWarnings:
        report.append("## ✅ Cleared to Land")
        report.append("")
        report.append("All phases are correctly ordered with valid dependencies.")
    ELSE IF hasErrors:
        report.append("## ❌ Landing Aborted")
        report.append("")
        report.append("Found {errors.length + cycles.length} error(s) that must be fixed before takeoff.")
    ELSE:
        report.append("## ⚠️ Cleared with Caution")
        report.append("")
        report.append("Found {warnings.length} warning(s). Use --strict to treat as errors.")

    report.append("")
    report.append("---")
    report.append("")

    # Phase Overview
    report.append("## 📋 Phase Overview")
    report.append("")
    report.append("| Phase | Name | Wave | Dependencies | Status |")
    report.append("|-------|------|------|--------------|--------|")

    FOR each phase in phases:
        deps = phase.depends_on.join(", ") or "None"
        status = getPhaseStatus(phase, errors, warnings)
        report.append("| {phase.number}.{phase.plan} | {phase.name} | {phase.wave} | {deps} | {status} |")

    report.append("")

    # Dependency Graph (visual)
    report.append("## 🔗 Dependency Graph")
    report.append("")
    report.append("```")
    report.append(generateAsciiGraph(phases))
    report.append("```")
    report.append("")

    # Errors
    IF cycles.length > 0:
        report.append("## 🔴 Circular Dependencies")
        report.append("")
        FOR each cycle in cycles:
            report.append("**Cycle Detected:**")
            report.append("```")
            report.append(cycle.join(" → ") + " → " + cycle[0])
            report.append("```")
            report.append("")

    IF errors.length > 0:
        report.append("## 🔴 Errors (Must Fix)")
        report.append("")
        report.append("| # | Type | Location | Issue |")
        report.append("|---|------|----------|-------|")
        FOR i, error in errors:
            report.append("| {i+1} | {error.type} | Phase {error.phase} | {error.message} |")
        report.append("")

        # Fix suggestions
        report.append("### How to Fix")
        report.append("")
        FOR each error in errors:
            report.append(generateFixSuggestion(error))

    # Warnings
    IF warnings.length > 0:
        report.append("## 🟡 Warnings")
        report.append("")
        report.append("| # | Type | Location | Issue |")
        report.append("|---|------|----------|-------|")
        FOR i, warning in warnings:
            report.append("| {i+1} | {warning.type} | Phase {warning.phase} | {warning.message} |")
        report.append("")

    # Wave Execution Order
    report.append("## 🌊 Wave Execution Order")
    report.append("")
    waves = groupByWave(phases)
    FOR waveNum in sorted(waves.keys()):
        report.append("### Wave {waveNum}")
        report.append("")
        waveRoutes = waves[waveNum]
        autonomous = filter(waveRoutes, p => p.autonomous)
        checkpoints = filter(waveRoutes, p => NOT p.autonomous)

        IF autonomous.length > 0:
            report.append("**Parallel (autonomous):**")
            FOR each route in autonomous:
                report.append("- Phase {route.number}, Route {route.plan}: {route.name}")

        IF checkpoints.length > 0:
            report.append("")
            report.append("**Sequential (waypoints):**")
            FOR each route in checkpoints:
                report.append("- Phase {route.number}, Route {route.plan}: {route.name}")

        report.append("")

    # Next Steps
    report.append("---")
    report.append("")
    report.append("## Next Steps")
    report.append("")
    IF hasErrors:
        report.append("```bash")
        report.append("# Fix the errors above, then re-validate:")
        report.append("/autopilot:landing")
        report.append("")
        report.append("# Or auto-fix simple issues:")
        report.append("/autopilot:landing --fix")
        report.append("```")
    ELSE:
        report.append("```bash")
        report.append("# Validation passed! Ready for takeoff:")
        report.append("/autopilot:takeoff")
        report.append("")
        report.append("# Or takeoff with auto-approval:")
        report.append("/autopilot:takeoff -y")
        report.append("```")

    RETURN report.join("\n")
```

---

## Auto-Fix Mode (--fix)

When `--fix` is specified, attempt to automatically repair:

```
FUNCTION autoFix(phases, errors):

    fixed = []
    unfixable = []

    FOR each error in errors:
        SWITCH error.type:

            CASE "INVALID_WAVE":
                # Fix: Increment wave number of dependent route
                route = findPlan(phases, error.phase, error.plan)
                newWave = error.dep_wave + 1
                updatePlanFrontmatter(route.file, { wave: newWave })
                fixed.append({
                    error: error,
                    fix: "Updated wave from {error.wave} to {newWave}"
                })

            CASE "FORWARD_DEPENDENCY":
                # Cannot auto-fix - requires manual review
                unfixable.append({
                    error: error,
                    reason: "Forward dependencies require manual restructuring"
                })

            CASE "MISSING_HARD_DEPENDENCY":
                # Fix: Add prerequisite to phase file
                route = findPlan(phases, error.phase, error.plan)
                addPrerequisite(route.file, error.requires)
                fixed.append({
                    error: error,
                    fix: "Added prerequisite: {error.requires}"
                })

            DEFAULT:
                unfixable.append({
                    error: error,
                    reason: "Cannot auto-fix this error type"
                })

    RETURN { fixed, unfixable }
```

---

## Output Formats

### Default Output

```markdown
# 🛬 Landing Validation Report

**Project:** my-app
**Validated:** 2026-01-29 10:30:00

## ✅ Cleared to Land

All phases are correctly ordered with valid dependencies.

---

## 📋 Phase Overview

| Phase | Name | Wave | Dependencies | Status |
|-------|------|------|--------------|--------|
| 1.01 | Project Setup | 1 | None | ✅ |
| 2.01 | Database Schema | 1 | None | ✅ |
| 3.01 | User API | 2 | 01, 02 | ✅ |
| 3.02 | Order API | 2 | 01, 02 | ✅ |
| 4.01 | Dashboard UI | 3 | 01, 02, 03 | ✅ |

## 🔗 Dependency Graph

```
Phase 1 ─┬─► Phase 3.01 ─┬─► Phase 4.01
         │               │
Phase 2 ─┴─► Phase 3.02 ─┘
```

## 🌊 Wave Execution Order

### Wave 1
**Parallel (autonomous):**
- Phase 1, Route 01: Project Setup
- Phase 2, Route 01: Database Schema

### Wave 2
**Parallel (autonomous):**
- Phase 3, Route 01: User API
- Phase 3, Route 02: Order API

### Wave 3
**Sequential (waypoints):**
- Phase 4, Route 01: Dashboard UI

---

## Next Steps

```bash
# Validation passed! Ready for takeoff:
/autopilot:takeoff

# Or takeoff with auto-approval:
/autopilot:takeoff -y
```
```

### Error Output

```markdown
# 🛬 Landing Validation Report

**Project:** my-app
**Validated:** 2026-01-29 10:30:00

## ❌ Landing Aborted

Found 2 error(s) that must be fixed before takeoff.

---

## 🔴 Circular Dependencies

**Cycle Detected:**
```
3.01 → 3.02 → 3.01
```

## 🔴 Errors (Must Fix)

| # | Type | Location | Issue |
|---|------|----------|-------|
| 1 | FORWARD_DEPENDENCY | Phase 2 | Phase 2 depends on later phase 3 |
| 2 | INVALID_WAVE | Phase 3.02 | Route 02 (wave 1) depends on route 01 (wave 1) - dependency must be in earlier wave |

### How to Fix

**Error 1: FORWARD_DEPENDENCY**
Phase 2 cannot depend on Phase 3. Either:
- Move the dependency to Phase 3 (make Phase 3 depend on Phase 2)
- Reorder the phases so Phase 3 comes before Phase 2
- Remove the dependency if not actually required

**Error 2: INVALID_WAVE**
Route 3.02 depends on Route 3.01 but they're in the same wave.
Fix: Change Route 3.02 to wave 2 (or higher)

```yaml
# In .autopilot/phases/003/route-02.md
---
wave: 2  # Changed from 1
depends_on: ["01"]
---
```

---

## Next Steps

```bash
# Fix the errors above, then re-validate:
/autopilot:landing

# Or auto-fix simple issues:
/autopilot:landing --fix
```
```

### Quiet Mode Output (--quiet)

```
✅ Cleared to land (5 phases, 3 waves)
```

Or on failure:

```
❌ Landing aborted: 2 errors, 1 warning
  - CIRCULAR_DEPENDENCY: 3.01 → 3.02 → 3.01
  - FORWARD_DEPENDENCY: Phase 2 depends on Phase 3
  - EARLY_PHASE: Auth at position 2, expected 4
```

---

## Integration with Takeoff

The `/autopilot:takeoff` command should call landing first:

```
# In takeoff.md, add to Phase 0: Startup Validation

### 0.0 Validate Phase Order (NEW)

FUNCTION validateBeforeTakeoff():

    result = CALL /autopilot:landing --quiet

    IF result.errors > 0:
        LOG "❌ Phase validation failed. Run /autopilot:landing for details."
        LOG ""
        LOG "Fix errors before takeoff, or use --skip-validation to override."
        EXIT 1

    IF result.warnings > 0:
        LOG "⚠️ {result.warnings} validation warnings. Proceeding anyway."
        LOG "   Use /autopilot:landing for details."
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed (no errors) |
| 1 | Validation failed (has errors) |
| 2 | No phases found |
| 3 | Parse error in phase files |

---

## Examples

```bash
# Basic validation
/autopilot:landing

# Validate and auto-fix simple issues
/autopilot:landing --fix

# Strict mode (fail on warnings too)
/autopilot:landing --strict

# CI mode (quiet, exit code only)
/autopilot:landing --quiet

# Validate specific phase
/autopilot:landing --phase=3
```

$ARGUMENTS
