---
description: Execute an existing plan with wave-based parallelization and cost tracking.
argument-hint: [-y] [--phase=N] [--max-cost=N] [--quiet]
model: sonnet
---

<!--
CAPABILITY NOTE FOR CLAUDE:
All pseudocode in this file (SPAWN, parallel_spawn, etc.) maps to Claude Code tools:
- SPAWN agent → Task tool with subagent_type="autopilot:{agent}"
- parallel_spawn([...]) → Multiple Task tool calls in single message
- Read/Write files → Read, Write, Edit tools
- Bash commands → Bash tool

You CAN and SHOULD execute this workflow. See /CLAUDE.md for full mapping.
-->

# Autopilot: TAKEOFF Mode

// Project Autopilot - Takeoff Execution Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Execute** an existing flight plan created by `/autopilot:flightplan`. Handles wave-based parallel execution, validation, and cost tracking.

## Prerequisites

```
/autopilot:takeoff
    │
    ├── Has .autopilot/flightplan.md?
    │   ├── Yes → Execute the flight plan
    │   └── No  ─┬─→ Has .planning/ROADMAP.md? (GSD project)
    │            │   ├── Yes → Offer GSD import, then execute
    │            │   └── No  → Notify user, auto-transition to /autopilot:flightplan
    │
    └── Has -y flag?
        ├── Yes → Execute immediately (no approval needed)
        └── No  → Show clearance summary, wait for "approved"
```

### GSD Project Detection

```
FUNCTION detectAndHandleGSD():
    """
    Detect GSD project and offer import before takeoff.
    """

    # Check if this is a GSD project
    IF exists(".planning/ROADMAP.md") AND NOT exists(".autopilot/flightplan.md"):
        LOG "📁 Detected GSD project structure (.planning/)"
        LOG ""

        # Count GSD artifacts
        gsd = {
            project: exists(".planning/PROJECT.md"),
            roadmap: exists(".planning/ROADMAP.md"),
            phases: glob(".planning/phases/*.md").length,
            plans: glob(".planning/phases/*/PLAN.md").length,
            contexts: glob(".planning/phases/*/CONTEXT.md").length
        }

        LOG "Found:"
        IF gsd.project: LOG "  • PROJECT.md"
        IF gsd.roadmap: LOG "  • ROADMAP.md"
        IF gsd.phases > 0: LOG "  • {gsd.phases} phase definitions"
        IF gsd.plans > 0: LOG "  • {gsd.plans} execution plans"
        IF gsd.contexts > 0: LOG "  • {gsd.contexts} context files"
        LOG ""

        LOG "Options:"
        LOG "  1. 'import' - Import GSD to Autopilot format (recommended)"
        LOG "  2. 'gsd' - Run in GSD compatibility mode"
        LOG "  3. 'new' - Ignore GSD, create new Autopilot flight plan"
        LOG ""

        response = waitForUserResponse()

        SWITCH response:
            CASE "import":
                RETURN importGSDProject()

            CASE "gsd":
                RETURN executeGSDCompatMode()

            CASE "new":
                LOG "Transitioning to /autopilot:flightplan..."
                TRANSITION to /autopilot:flightplan
                RETURN

            DEFAULT:
                LOG "Please choose: import, gsd, or new"
                RETRY

FUNCTION importGSDProject():
    """
    Full GSD to Autopilot import.
    """
    LOG "🔄 Importing GSD project to Autopilot format..."
    LOG ""

    # Create .autopilot structure
    ensureDir(".autopilot/")
    ensureDir(".autopilot/phases/")

    imported = {phases: 0, plans: 0, contexts: 0}

    # 1. Import PROJECT.md → clearance.md
    IF exists(".planning/PROJECT.md"):
        project = parseGSDProjectFile(".planning/PROJECT.md")
        writeFile(".autopilot/clearance.md", formatAutopilotScope(project))
        LOG "  ✓ PROJECT.md → .autopilot/clearance.md"

    # 2. Import ROADMAP.md → flightplan.md
    IF exists(".planning/ROADMAP.md"):
        roadmap = parseGSDRoadmapFile(".planning/ROADMAP.md")
        writeFile(".autopilot/flightplan.md", formatAutopilotRoadmap(roadmap))
        LOG "  ✓ ROADMAP.md → .autopilot/flightplan.md"

    # 3. Import phase files
    phase_files = glob(".planning/phases/*.md")
    FOR each file IN phase_files:
        phase = parseGSDPhaseFile(file)
        phase_dir = ".autopilot/phases/{pad(phase.number, 3)}/"
        ensureDir(phase_dir)

        # Convert phase format
        writeFile(phase_dir + "PHASE.md", formatAutopilotPhase(phase))
        imported.phases += 1

        # Copy PLAN.md → ROUTE.md if exists
        gsd_plan = ".planning/phases/{phase.number}/PLAN.md"
        IF exists(gsd_plan):
            plan = parseGSDPlanFile(gsd_plan)
            writeFile(phase_dir + "ROUTE.md", formatAutopilotPlan(plan))
            imported.plans += 1

        # Copy CONTEXT.md → BRIEFING.md if exists
        gsd_context = ".planning/phases/{phase.number}/CONTEXT.md"
        IF exists(gsd_context):
            copyFile(gsd_context, phase_dir + "BRIEFING.md")
            imported.contexts += 1

        LOG "  ✓ Phase {phase.number}: {phase.name}"

    # 4. Create TRANSPONDER.md
    createFile(".autopilot/TRANSPONDER.md", formatInitialState(imported.phases))
    LOG "  ✓ Created TRANSPONDER.md"

    LOG ""
    LOG "╔══════════════════════════════════════════╗"
    LOG "║  ✅ GSD Import Complete                  ║"
    LOG "╠══════════════════════════════════════════╣"
    LOG "║  Phases: {pad(imported.phases, 3)}                           ║"
    LOG "║  Routes:  {pad(imported.plans, 3)}                           ║"
    LOG "║  Briefings: {pad(imported.contexts, 3)}                      ║"
    LOG "╠══════════════════════════════════════════╣"
    LOG "║  Original files preserved in .planning/  ║"
    LOG "╚══════════════════════════════════════════╝"
    LOG ""

    RETURN {success: true, imported: imported}

FUNCTION executeGSDCompatMode():
    """
    Execute GSD plan without full import.
    Maps GSD structure to Autopilot execution.
    """
    LOG "🔄 Running in GSD compatibility mode..."
    LOG ""
    LOG "Note: For full Autopilot features, run with 'import' option."
    LOG ""

    # Load GSD roadmap
    roadmap = parseGSDRoadmapFile(".planning/ROADMAP.md")

    # Map to execution structure
    execution = {
        phases: [],
        total_tasks: 0
    }

    FOR each gsd_phase IN roadmap.phases:
        phase = {
            number: gsd_phase.number,
            name: gsd_phase.name,
            goal: gsd_phase.goal,
            plan: loadGSDPlanIfExists(gsd_phase.number),
            context: loadGSDContextIfExists(gsd_phase.number)
        }
        execution.phases.add(phase)

    # Execute using standard protocol
    RETURN executePhases(execution)
```

### Usage Examples

```bash
# Execute existing flight plan with approval
/autopilot:takeoff

# Execute immediately (no approval)
/autopilot:takeoff -y

# Execute starting from specific phase
/autopilot:takeoff --phase=3

# Execute with cost limit
/autopilot:takeoff --max-cost=25

# Execute in CI mode (quiet)
/autopilot:takeoff -y --quiet
```

## FIRST: Read Optimization Skill

```
BEFORE ANY WORK:
Read /autopilot/skills/token-optimization/SKILL.md
Apply ALL strategies throughout execution
```

## Required Skills

1. **`token-optimization`** - READ FIRST, apply always
2. **`user-experience`** - Consistent output patterns (READ THIS)
3. **`state-management`** - TRANSPONDER.md session bridge (read first, update last)
4. **`global-state`** - Cross-session persistence
5. **`visual-style`** - Colors and icons for output
6. `phase-ordering` - Phase sequence
7. `quality-gates` - Validation
8. `checkpoint-protocol` - Save points

## Required Agents

### Core Coordination
- `model-selector` - Choose Haiku/Sonnet/Opus per task (batch selection)
- `validator` - Quality gates (parallel validation)
- `token-tracker` - Monitor costs
- `history-tracker` - Cross-session persistence

### Domain Specialists (Direct Spawning)
| Phase Type | Primary Agent | Support Agents | Parallel? |
|------------|---------------|----------------|-----------|
| Database | `database` | `api-designer` | No |
| API | `backend`, `api-designer` | `tester` | Yes |
| Business Logic | `backend` | `database` | Yes |
| Frontend | `frontend` | `api-designer` | Yes |
| Testing | `tester` | `security` | Yes |
| Security | `security` | `tester` | Yes |
| Documentation | `documenter` | `api-designer` | Yes |
| DevOps | `devops` | `security` | Yes |

### Full Agent List
Route directly based on task type:
- **Planning:** planner, architect
- **Implementation:** backend, frontend, database, api-designer
- **Quality:** tester, security, validator, debugger, refactor, code-review
- **Operations:** devops, monitor
- **Documentation:** documenter
- **Optimization:** model-selector, token-tracker, context-optimizer
- **Persistence:** history-tracker
- **Analysis:** risk-assessor, debt-tracker, graph-builder, migration-assistant

---

## Options

```bash
-y, --yes          # Auto-execute without approval
--phase=N          # Start from specific phase
--task=X.Y         # Start from specific task
--max-cost=N       # Budget limit (default: $50)
--warn-cost=N      # Warning (default: $10)
--alert-cost=N     # Pause for confirmation (default: $25)
--no-cost-limit    # Disable all limits
--quiet            # Suppress verbose output (CI mode)
--validate-only    # Run validation without execution
--skip-validation  # Skip phase ordering validation (not recommended)
--security-scan    # Run security-scanner at end of each phase
--debt-check       # Run debt-tracker summary at completion
```

### Quiet Mode (--quiet)

For CI/CD environments and automated runs:
- Suppress progress spinners and decorative output
- Only show errors and final status
- Machine-parseable output format
- Exit codes indicate success/failure

```bash
# CI example
/autopilot:takeoff -y --quiet
echo "Exit code: $?"
```

---

## OPTIMIZATION RULES (Apply Always)

**READ AND APPLY:** `/autopilot/skills/token-optimization/SKILL.md`

Key rules (see skill for full details):
1. **Partial file reading** - Never read entire files
2. **Model selection** - Use model-selector for each task
3. **Cache everything** - Check learnings.md first
4. **Batch work** - Combine related files in one task
5. **Concise output** - "✅ Done" not paragraphs

---

## Standard Output Format

Follow `/autopilot/skills/user-experience/SKILL.md` for all output. Key patterns:

### Command Banner (Always Show First)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛫 AUTOPILOT: TAKEOFF
   Execute flight plan with wave-based parallelization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Startup Checks (Build Confidence)

```
▶ Pre-Flight Checks
  ✓ Flight plan valid
  ✓ Phase ordering verified (6 phases, 3 waves)
  ✓ Dependencies resolved (no cycles)
  ✓ Global config loaded
  ✓ Fuel budget available ($45.50 remaining)

Cleared for takeoff.
```

### Phase Progress

```
─────────────────────────────────────────────────────────────
📋 PHASE 1 OF 6: Project Setup
─────────────────────────────────────────────────────────────

  ┌─ Task 1.1: Initialize project structure
  │  🔄 Creating package.json...
  │  🔄 Setting up TypeScript config...
  │  ✓ Completed in 12s | $0.04
  └────────────────────────────────────────
```

### Phase Completion

```
─────────────────────────────────────────────────────────────
✅ PHASE 1 COMPLETE
─────────────────────────────────────────────────────────────

  Tasks:     3/3 completed
  Duration:  1m 24s
  Cost:      $0.08 (estimate: $0.10, -20% under 🟢)

  Quality Gate:
    ✓ Build passes
    ✓ Lint clean (0 errors)
    ✓ Tests pass (12/12)

  📌 Waypoint saved

─────────────────────────────────────────────────────────────
```

### Budget Dashboard (Show Periodically)

```
─────────────────────────────────────────────────────────────
💰 FUEL STATUS
─────────────────────────────────────────────────────────────

  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░ 27%

  Spent:     $2.35 of $50.00
  Remaining: $47.65
  Estimate:  $8.50 total (17% of budget)

  ✅ On track - well within budget
─────────────────────────────────────────────────────────────
```

### Flight Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛬 FLIGHT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Project:   my-awesome-app
  Duration:  45m 12s
  Cost:      $4.85 (estimate: $6.00, -19% under budget 🟢)

─────────────────────────────────────────────────────────────

📊 Summary

  Phases completed:  6/6 ✅
  Tasks completed:   24/24 ✅
  Tests passing:     156/156 ✅
  Coverage:          87%
  Git commits:       12

─────────────────────────────────────────────────────────────

🔗 Next Steps

  • Run your app:     npm run dev
  • View history:     /autopilot:altitude --global
  • Start new task:   /autopilot:takeoff "next feature"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 0: Startup Validation

### 0.0 Validate Phase Order (Run First)

```
FUNCTION validatePhaseOrder():

    # Skip if --skip-validation flag
    IF "--skip-validation" in arguments:
        LOG "⚠️ Skipping validation (--skip-validation flag)"
        RETURN

    # Run validation in quiet mode
    result = CALL /autopilot:landing --quiet

    IF result.errors > 0:
        LOG "❌ Phase validation failed"
        LOG ""
        LOG "Found {result.errors} ordering/dependency error(s):"
        FOR each error in result.errorDetails:
            LOG "  - {error.type}: {error.message}"
        LOG ""
        LOG "Fix errors before takeoff:"
        LOG "  /autopilot:landing        # See full report"
        LOG "  /autopilot:landing --fix  # Auto-fix simple issues"
        LOG ""
        LOG "Or skip validation (not recommended):"
        LOG "  /autopilot:takeoff --skip-validation"
        EXIT 1

    IF result.warnings > 0:
        LOG "⚠️ {result.warnings} validation warning(s) - proceeding anyway"
        LOG "   Run /autopilot:landing for details"

    LOG "✅ Phase ordering validated"
```

### 0.1 Verify Flight Plan Exists

```
FUNCTION verifyPlanExists():

    IF NOT exists(".autopilot/flightplan.md") OR NOT exists(".autopilot/phases/"):
        LOG "📋 No flight plan found for this project."
        LOG ""
        LOG "Transitioning to /autopilot:flightplan to create one..."
        LOG ""

        # Pass through any arguments that apply to planning
        TRANSITION to /autopilot:flightplan with:
            - description (if provided)
            - --max-cost (if provided)

        # After plan completes, prompt to continue
        LOG ""
        LOG "✅ Flight plan filed. Run /autopilot:takeoff to execute."
        EXIT 0

    # Count phases
    phaseCount = countDirectories(".autopilot/phases/")
    IF phaseCount == 0:
        LOG "📋 Flight plan exists but has no phases."
        LOG "Transitioning to /autopilot:flightplan to regenerate..."
        TRANSITION to /autopilot:flightplan
        EXIT 0

    LOG "Found {phaseCount} phases to execute"
```

### 0.2 Load Global State

```
FUNCTION loadGlobalState():

    globalDir = expandPath("~/.claude/autopilot/")

    # Initialize if needed
    IF NOT exists(globalDir):
        initializeGlobalState()

    config = readJSON(globalDir + "config.json")

    # Apply config defaults:
    - maxCost = config.defaults.maxCost (unless --max-cost provided)
    - warnCost = config.defaults.warnCost (unless --warn-cost provided)
    - alertCost = config.defaults.alertCost (unless --alert-cost provided)

    # Load historical data
    history = readJSON(globalDir + "history.json")
    learnings = readJSON(globalDir + "learnings.json")

    # Find this project in history (or register it)
    projectId = findProjectByPath(history, currentDir)
    IF NOT projectId:
        # Register project now (plan may have been created manually)
        projectId = SPAWN history-tracker → recordProjectStart({
            path: currentDir,
            description: readProjectName(".autopilot/clearance.md"),
            status: "executing"
        })
```

### 0.3 Load Local State

```
FUNCTION loadLocalState():

    # Read TRANSPONDER.md
    state = read(".autopilot/TRANSPONDER.md")

    IF state.status == "complete":
        LOG "Project already complete."
        SHOW "Run /autopilot:flightplan to start a new feature."
        EXIT 0

    IF state.status == "executing":
        LOG "Resuming from previous execution..."
        RETURN state.position

    IF state.status != "planned":
        ERROR "Invalid state: {state.status}"
        EXIT 1

    RETURN { phase: 1, task: 1 }
```

### 0.4 Display Clearance Summary

```markdown
## Flight Clearance Summary

**Project:** [name from clearance.md]
**Phases:** N
**Estimated Cost:** $X.XX

| Phase | Name | Tasks | Est. Cost |
|-------|------|-------|-----------|
| 001 | Setup | 3 | $0.15 |
| 002 | Core | 5 | $0.32 |
| 003 | Tests | 4 | $0.18 |

**Total:** $0.65 estimated
```

### 0.5 Approval Gate

```
IF -y/--yes flag:
    → Log: "Auto-approved (-y flag)"
    → Proceed to execution immediately

IF --validate-only flag:
    → Run validation checks
    → STOP (do not execute)

ELSE:
    → Display: "Reply 'approved' to commence takeoff."
    → WAIT for user approval
    → On "approved" → Proceed to execution
```

---

## Phase 1: Execution Loop

### Pre-Execution: Load State

```
# 1. Read TRANSPONDER.md FIRST (session bridge)
IF .autopilot/TRANSPONDER.md exists:
    Load current position, metrics, decisions
    Log: "📂 Restored state: Phase {N}, Task {M}"

# 2. Read BRIEFING.md (user decisions) if exists
IF .autopilot/phases/{phase}/BRIEFING.md exists:
    Load implementation decisions
    Load "Claude's Discretion" areas
    Log: "📋 Loaded briefing for phase {N}"

# 3. Extract wave numbers from routes
Group phases by wave number (from frontmatter)
Sort waves: 1, 2, 3...
```

### Execution Loop (Direct Coordination)

**The main Claude context coordinates directly** - no intermediary agent needed.

```
FUNCTION executeProject():

    # Load phases and state
    phases = loadPhases()
    state = loadState()

    # Configuration
    config = {
        parallelTasks: true,      # Enable task-level parallelization
        parallelValidation: true, # Enable parallel quality gates
        batchModelSelection: true # Pre-select models for efficiency
    }

    # Execute wave by wave
    waves = groupPhasesByWave(phases)
    FOR each wave in waves:
        executeWave(wave, config)
```

### Wave-Based Execution (Phase Level)

```
FOR each wave (1, 2, 3...):

    # Execute autonomous phases in this wave IN PARALLEL
    parallel_phases = []
    checkpoint_phases = []

    FOR each phase in wave:
        IF phase.autonomous == true:
            parallel_phases.append(phase)
        ELSE:
            checkpoint_phases.append(phase)

    # Execute parallel phases simultaneously
    IF parallel_phases.length > 0:
        parallel_spawn([
            executePhase(phase) FOR phase IN parallel_phases
        ])
        WAIT all

    # Handle checkpoint phases sequentially (require user input)
    FOR each checkpoint_phase:
        Execute with checkpoint protocol
        Present checkpoint to user
        Wait for approval/decision

    # Update TRANSPONDER.md after wave complete
    Update TRANSPONDER.md: "Wave {N} complete"
```

### Task-Level Parallelization (Within Phase)

**NEW:** Tasks within a phase can run in parallel if they don't modify the same files.

```
FUNCTION executePhase(phase):

    # 1. BATCH MODEL SELECTION (all tasks at once)
    all_tasks = phase.tasks
    models = SPAWN model-selector → batchSelect(all_tasks)
    Log: "✓ Model selection: {count} tasks → {breakdown}"

    # 2. ANALYZE TASK DEPENDENCIES
    task_groups = analyzeTaskDependencies(all_tasks)
    Log: "✓ Found {task_groups.length} parallel groups"

    # 3. ROUTE TO DOMAIN AGENTS
    domain_agents = routeToDomainAgents(phase.type)
    Log: "✓ Domain agents: {domain_agents}"

    # 4. EXECUTE TASK GROUPS
    FOR each group in task_groups:

        IF group.length == 1:
            # Single task - execute normally
            task = group[0]
            agent = domain_agents[task.type] OR task.agent
            SPAWN agent on models[task.id] → task

        ELSE:
            # Multiple independent tasks - PARALLEL execution
            parallel_tasks = []
            FOR each task in group:
                agent = domain_agents[task.type] OR task.agent
                spawned = SPAWN agent on models[task.id] → task
                parallel_tasks.append(spawned)

            # Wait for parallel group to complete
            WAIT parallel_tasks
            Log: "✓ Parallel group complete ({group.length} tasks)"

        # 5. PARALLEL VALIDATION after each group
        changed_files = collectChangedFiles(group)
        SPAWN validator → parallelValidate(changed_files)

        # 6. Save waypoint after group
        Save waypoint (reason: "task_group_complete")

    # 7. PARALLEL PHASE VALIDATION
    SPAWN validator → parallelPhaseGate(phase)
    Save waypoint (reason: "phase_complete")
    Log: "📌 Phase {phase.id} complete"
```

### Task Dependency Analysis

```
FUNCTION analyzeTaskDependencies(tasks):
    """
    Groups tasks that can run in parallel (no file conflicts).
    Returns list of groups, each group runs in parallel.
    """

    file_map = {}  # file -> [task_ids]
    task_files = {}  # task_id -> [files]

    # Build file modification map
    FOR each task in tasks:
        task_files[task.id] = task.files_modified OR []
        FOR each file in task.files_modified:
            file_map[file] = file_map[file] OR []
            file_map[file].append(task.id)

    # Group tasks by independence
    groups = []
    current_group = []
    current_files = Set()

    FOR each task in tasks:
        task_file_set = Set(task_files[task.id])

        # Check for conflicts with current group
        IF task_file_set.intersection(current_files).isEmpty():
            # No conflict - add to current group
            current_group.append(task)
            current_files = current_files.union(task_file_set)
        ELSE:
            # Conflict - start new group
            IF current_group.length > 0:
                groups.append(current_group)
            current_group = [task]
            current_files = task_file_set

    # Don't forget last group
    IF current_group.length > 0:
        groups.append(current_group)

    RETURN groups
```

### Domain Agent Routing

```
FUNCTION routeToDomainAgents(phase_type):
    """
    Returns map of task types to specialized agents for this phase.
    """

    routing = {
        "database": {
            "schema": "database",
            "migration": "database",
            "seed": "database",
            "query": "database"
        },
        "devops": {
            "ci": "devops",
            "infrastructure": "devops",
            "deployment": "devops",
            "monitoring": "monitor",
            "alerts": "monitor"
        },
        "api": {
            "endpoint": "backend",
            "contract": "api-designer",
            "validation": "backend",
            "middleware": "backend"
        },
        "business_logic": {
            "service": "backend",
            "repository": "backend",
            "domain": "backend"
        },
        "frontend": {
            "component": "frontend",
            "page": "frontend",
            "hook": "frontend",
            "state": "frontend"
        },
        "testing": {
            "unit": "tester",
            "integration": "tester",
            "e2e": "tester",
            "security": "security"
        },
        "security": {
            "audit": "security",
            "fix": "security",
            "test": "tester"
        },
        "documentation": {
            "api": "documenter",
            "user": "documenter",
            "dev": "documenter"
        }
    }

    RETURN routing[phase_type] OR {}
```

### Batch Model Selection

```
FUNCTION batchModelSelect(tasks):
    """
    Pre-selects models for ALL tasks in one call.
    Saves ~2s per task vs individual calls.
    """

    # Build task descriptions for batch selection
    task_summaries = []
    FOR each task in tasks:
        task_summaries.append({
            id: task.id,
            type: task.type,
            complexity: task.complexity,
            files_count: task.files_modified.length
        })

    # Single call to model-selector
    SPAWN model-selector → batchSelect(task_summaries)

    # Returns: { task_id: "haiku"|"sonnet"|"opus", ... }
```

### Parallel Validation

```
FUNCTION parallelValidate(files):
    """
    Runs all quality checks in parallel.
    Saves 60-70% time vs sequential.
    """

    # All checks run simultaneously
    parallel_spawn([
        SPAWN validator → runBuild(),
        SPAWN validator → runLint(),
        SPAWN validator → runTypecheck(),
        SPAWN validator → runTests(files),
        SPAWN validator → runAudit()
    ])

    # Collect and merge results
    results = WAIT all
    RETURN mergeValidationResults(results)
```

### Progress Log (Visual Style)

Use icons from `/autopilot/skills/visual-style/SKILL.md`:

```markdown
### [Time]
🔵 backend → Creating AuthService
✅ 003.2 | AuthService | $0.04 | 2.1K tokens
📌 Waypoint saved (task_complete)
```

**Phase completion:**
```markdown
🟢 validator → Phase 003 Gate
   ✓ Build passes
   ✓ Tests pass (47/47)
   ✓ Coverage 87%
   ✅ APPROVED
📌 Waypoint saved (phase_complete)
```

**Cost updates:**
```markdown
💰 Fuel: $4.36 / $50.00 (9%)
⚠️ Warning threshold reached ($10.00)
```

---

## Phase 2: Cost Monitoring

### Threshold Handling

```
FUNCTION checkThresholds(currentCost):

    IF currentCost >= maxCost:
        LOG "🛑 Maximum fuel budget reached ($[max])"
        Save waypoint (reason: "cost_limit")
        EXIT with instructions to increase limit

    IF currentCost >= alertCost AND NOT alertAcknowledged:
        LOG "⚠️ Alert threshold reached ($[alert])"
        PAUSE for user confirmation
        SET alertAcknowledged = true

    IF currentCost >= warnCost AND NOT warningShown:
        LOG "💡 Warning: Approaching fuel budget ($[warn])"
        SET warningShown = true
```

### Cost Display

```markdown
## Fuel Status

💰 **Current:** $4.36 / $50.00 (9%)
████░░░░░░░░░░░░░░░░ 9%

| Threshold | Value | Status |
|-----------|-------|--------|
| Warning | $10.00 | ✅ 44% |
| Alert | $25.00 | ✅ 17% |
| Maximum | $50.00 | ✅ 9% |
```

---

## Phase 3: Completion

### Update Global State

```
FUNCTION updateGlobalState(outcome):

    # 1. Record completion in history
    SPAWN history-tracker → recordProjectComplete(projectId, {
        outcome: outcome,  # "success", "partial", "paused"
        phases: {
            total: totalPhases,
            completed: completedPhases
        },
        costs: {
            estimated: scopeEstimate,
            actual: tokenUsageActual
        },
        tokens: {
            input: totalInputTokens,
            output: totalOutputTokens
        },
        phaseCosts: phaseActuals
    })

    # 2. history-tracker automatically:
    #    - Updates learnings.json with patterns
    #    - Updates statistics.json with aggregates
    #    - Calculates estimation accuracy
```

### On Project Pause/Waypoint

```
IF context > 40% OR user interrupts:

    # Update TRANSPONDER.md (session bridge)
    Update TRANSPONDER.md:
        Status: "executing"
        Stopped at: "{current task description}"
        Resume file: ".autopilot/holding-pattern.md" (if mid-phase)
        Next action: "/autopilot:cockpit"

    # Create holding-pattern.md if mid-phase
    IF mid_phase:
        Create .autopilot/holding-pattern.md with:
            - Completed tasks table
            - Remaining work
            - Decisions made
            - Next action

    # Also update global history
    SPAWN history-tracker → recordProjectPause(projectId, "context_limit")

    LOG "📌 Position saved to TRANSPONDER.md"
    LOG "Resume with /autopilot:cockpit"
```

### On Project Success

```
IF all phases complete:

    # Update TRANSPONDER.md
    Update TRANSPONDER.md:
        Status: "complete"
        Completed at: [timestamp]

    SPAWN history-tracker → recordProjectComplete(projectId, "success")

    # Show summary with historical comparison
    LOG "
    ## 🛬 Flight Complete!

    | Metric | Estimated | Actual |
    |--------|-----------|--------|
    | Cost | $2.50 | $2.35 |
    | Phases | 6 | 6 |
    | Tasks | 24 | 24 |

    | Metric | This Project | Your Average |
    |--------|--------------|--------------|
    | Cost | $2.35 | $3.77 |
    | Accuracy | 94% | 91% |

    View history: /autopilot:config --history
    "
```

---

## Optimization Checklist

Before EVERY operation:

```
□ Reading minimum necessary? (partial files)
□ Model selected by model-selector?
□ Info already in learnings.md?
□ Can batch with related work?
□ Output will be concise?
□ Skipping redundant validation?
□ Context at 40%? (waypoint time)
```

---

## Output Files

### Updated by /autopilot:takeoff
```
.autopilot/
├── TRANSPONDER.md    # Session bridge - status: "executing" → "complete"
├── token-usage.md    # Cost tracking (created/updated)
├── progress.md       # Compact execution log
├── holding-pattern.md # Mid-phase resume (auto-deleted on complete)
└── phases/
    └── {phase}/
        ├── ROUTE.md      # Updated with actual costs
        └── LOGBOOK.md    # Created on phase completion
```

### Global (cross-session)
```
~/.claude/autopilot/
├── history.json      # Updated with completion data
├── learnings.json    # Updated with patterns
└── statistics.json   # Updated with aggregates
```

---

## Expected Costs

| Project Size | Planning | Execution | Total |
|--------------|----------|-----------|-------|
| Small | $0.15 | $0.85-1.85 | $1-2 |
| Medium | $0.35 | $2.15-3.65 | $2.50-4 |
| Large | $0.75 | $3.25-7.25 | $4-8 |

*Costs with optimization. Unoptimized can be 60-80% higher.*

---

## Error Recovery

### Build/Test Failure

```
IF build or tests fail:
    1. Log failure details
    2. Attempt auto-fix (up to 3 tries)
    3. If still failing:
       - Save waypoint
       - Display error details
       - PAUSE for user intervention
    4. On user fix confirmation → resume
```

### Context Overflow

```
IF context > 40%:
    1. Finish current task
    2. Save waypoint
    3. Log: "📌 Context limit - waypoint saved"
    4. Log: "Resume with /autopilot:cockpit"
    5. EXIT cleanly
```

$ARGUMENTS
