---
description: Execute an existing plan with wave-based parallelization and cost tracking.
argument-hint: [-y] [--phase=N] [--max-cost=N] [--quiet]
model: sonnet
---

# Autopilot: BUILD Mode

**Execute** an existing plan created by `/autopilot:plan`. Handles wave-based parallel execution, validation, and cost tracking.

## Prerequisites

```
/autopilot:build
    │
    ├── Has .autopilot/roadmap.md?
    │   ├── Yes → Execute the plan
    │   └── No  → Notify user, auto-transition to /autopilot:plan
    │
    └── Has -y flag?
        ├── Yes → Execute immediately (no approval needed)
        └── No  → Show scope summary, wait for "approved"
```

### Usage Examples

```bash
# Execute existing plan with approval
/autopilot:build

# Execute immediately (no approval)
/autopilot:build -y

# Execute starting from specific phase
/autopilot:build --phase=3

# Execute with cost limit
/autopilot:build --max-cost=25

# Execute in CI mode (quiet)
/autopilot:build -y --quiet
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
3. **`state-management`** - STATE.md session bridge (read first, update last)
4. **`global-state`** - Cross-session persistence
5. **`visual-style`** - Colors and icons for output
6. `phase-ordering` - Phase sequence
7. `quality-gates` - Validation
8. `checkpoint-protocol` - Save points

## Required Agents

### Core Coordination
- `orchestrator` - **PRIMARY** - Coordinates entire swarm, delegates to specialists
- `model-selector` - Choose Haiku/Sonnet/Opus per task (batch selection)
- `validator` - Quality gates (parallel validation)
- `token-tracker` - Monitor costs
- `history-tracker` - Cross-session persistence

### Domain Specialists (Spawned by Orchestrator)
| Phase Type | Primary Agent | Support Agents |
|------------|---------------|----------------|
| Database | `database` | `api-designer` |
| API | `backend`, `api-designer` | `tester` |
| Business Logic | `backend` | `database` |
| Frontend | `frontend` | `api-designer` |
| Testing | `tester` | `security` |
| Security | `security` | `tester` |
| Documentation | `documenter` | `api-designer` |
| DevOps | `devops` | `security` |

### Full Agent List (29 available)
All agents are routed through orchestrator based on task type:
- **Planning:** planner, architect
- **Implementation:** backend, frontend, database, api-designer
- **Quality:** tester, security, validator, debugger, refactor, code-review
- **Operations:** devops, deployer, monitor
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
```

### Quiet Mode (--quiet)

For CI/CD environments and automated runs:
- Suppress progress spinners and decorative output
- Only show errors and final status
- Machine-parseable output format
- Exit codes indicate success/failure

```bash
# CI example
/autopilot:build -y --quiet
echo "Exit code: $?"
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
| Implementation, tests | Sonnet | $3/1M |
| Architecture (rare) | Opus | $5/1M |
```

### Rule 3: Cache Everything

```
NEVER re-read files already in .autopilot/learnings.md
Reference learnings.md instead.
```

### Rule 4: Batch Work

```
❌ Task 1: Create user.route.ts
❌ Task 2: Create order.route.ts
❌ Task 3: Create product.route.ts

✅ Task 1: Create all route files (user, order, product)
```

### Rule 5: Concise Output

```
❌ "I will now proceed to create the UserService..."
✅ "Creating UserService."

❌ "I have successfully completed the task..."
✅ "✅ Done"
```

---

## Standard Output Format

Follow `/autopilot/skills/user-experience/SKILL.md` for all output. Key patterns:

### Command Banner (Always Show First)

```
╭─────────────────────────────────────────────────────────────╮
│  🚀 AUTOPILOT: BUILD                                        │
│  Execute project plan with wave-based parallelization       │
╰─────────────────────────────────────────────────────────────╯
```

### Startup Checks (Build Confidence)

```
▶ Startup Checks
  ✓ Project structure valid
  ✓ Phase ordering verified (6 phases, 3 waves)
  ✓ Dependencies resolved (no cycles)
  ✓ Global config loaded
  ✓ Budget available ($45.50 remaining)

Ready to proceed.
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

  📌 Checkpoint saved

─────────────────────────────────────────────────────────────
```

### Budget Dashboard (Show Periodically)

```
─────────────────────────────────────────────────────────────
💰 BUDGET STATUS
─────────────────────────────────────────────────────────────

  Progress: ████████░░░░░░░░░░░░░░░░░░░░░░ 27%

  Spent:     $2.35 of $50.00
  Remaining: $47.65
  Estimate:  $8.50 total (17% of budget)

  ✅ On track - well within budget
─────────────────────────────────────────────────────────────
```

### Build Complete

```
╭─────────────────────────────────────────────────────────────╮
│  🎉 BUILD COMPLETE                                          │
╰─────────────────────────────────────────────────────────────╯

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
    • View history:     /autopilot:status --global
    • Start new task:   /autopilot:build "next feature"

╰─────────────────────────────────────────────────────────────╯
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
    result = CALL /autopilot:validate --quiet

    IF result.errors > 0:
        LOG "❌ Phase validation failed"
        LOG ""
        LOG "Found {result.errors} ordering/dependency error(s):"
        FOR each error in result.errorDetails:
            LOG "  - {error.type}: {error.message}"
        LOG ""
        LOG "Fix errors before building:"
        LOG "  /autopilot:validate        # See full report"
        LOG "  /autopilot:validate --fix  # Auto-fix simple issues"
        LOG ""
        LOG "Or skip validation (not recommended):"
        LOG "  /autopilot:build --skip-validation"
        EXIT 1

    IF result.warnings > 0:
        LOG "⚠️ {result.warnings} validation warning(s) - proceeding anyway"
        LOG "   Run /autopilot:validate for details"

    LOG "✅ Phase ordering validated"
```

### 0.1 Verify Plan Exists

```
FUNCTION verifyPlanExists():

    IF NOT exists(".autopilot/roadmap.md") OR NOT exists(".autopilot/phases/"):
        LOG "📋 No plan found for this project."
        LOG ""
        LOG "Transitioning to /autopilot:plan to create one..."
        LOG ""

        # Pass through any arguments that apply to planning
        TRANSITION to /autopilot:plan with:
            - description (if provided)
            - --max-cost (if provided)

        # After plan completes, prompt to continue
        LOG ""
        LOG "✅ Plan created. Run /autopilot:build to execute."
        EXIT 0

    # Count phases
    phaseCount = countDirectories(".autopilot/phases/")
    IF phaseCount == 0:
        LOG "📋 Plan exists but has no phases."
        LOG "Transitioning to /autopilot:plan to regenerate..."
        TRANSITION to /autopilot:plan
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
            description: readProjectName(".autopilot/scope.md"),
            status: "executing"
        })
```

### 0.3 Load Local State

```
FUNCTION loadLocalState():

    # Read STATE.md
    state = read(".autopilot/STATE.md")

    IF state.status == "complete":
        LOG "Project already complete."
        SHOW "Run /autopilot:plan to start a new feature."
        EXIT 0

    IF state.status == "executing":
        LOG "Resuming from previous execution..."
        RETURN state.position

    IF state.status != "planned":
        ERROR "Invalid state: {state.status}"
        EXIT 1

    RETURN { phase: 1, task: 1 }
```

### 0.4 Display Scope Summary

```markdown
## Build Summary

**Project:** [name from scope.md]
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
    → Display: "Reply 'approved' to start execution."
    → WAIT for user approval
    → On "approved" → Proceed to execution
```

---

## Phase 1: Execution Loop

### Pre-Execution: Load State

```
# 1. Read STATE.md FIRST (session bridge)
IF .autopilot/STATE.md exists:
    Load current position, metrics, decisions
    Log: "📂 Restored state: Phase {N}, Task {M}"

# 2. Read CONTEXT.md (user decisions) if exists
IF .autopilot/phases/{phase}/CONTEXT.md exists:
    Load implementation decisions
    Load "Claude's Discretion" areas
    Log: "📋 Loaded context for phase {N}"

# 3. Extract wave numbers from plans
Group phases by wave number (from frontmatter)
Sort waves: 1, 2, 3...
```

### Execution Loop (Orchestrator-Coordinated)

**CRITICAL:** Delegate to orchestrator for maximum parallelization.

```
FUNCTION executeProject():

    # SPAWN ORCHESTRATOR as central coordinator
    # See /autopilot/agents/orchestrator.md for full protocol

    SPAWN orchestrator → coordinateSwarm({
        phases: loadPhases(),
        state: loadState(),
        config: {
            parallelTasks: true,      # Enable task-level parallelization
            parallelValidation: true, # Enable parallel quality gates
            batchModelSelection: true # Pre-select models for efficiency
        }
    })
```

### Wave-Based Execution (Phase Level)

```
FOR each wave (1, 2, 3...):

    # Spawn all autonomous plans in this wave IN PARALLEL
    parallel_agents = []
    FOR each phase in wave:
        IF phase.autonomous == true:
            agent = SPAWN orchestrator → executePhase(phase)
            parallel_agents.append(agent)
        ELSE:
            checkpoint_phases.append(phase)

    # Wait for all parallel agents to complete
    WAIT parallel_agents

    # Handle checkpoint phases sequentially
    FOR each checkpoint_phase:
        Execute with checkpoint protocol
        Present checkpoint to user
        Wait for approval/decision

    # Update STATE.md after wave complete
    Update STATE.md: "Wave {N} complete"
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

        # 6. Save checkpoint after group
        Save checkpoint (reason: "task_group_complete")

    # 7. PARALLEL PHASE VALIDATION
    SPAWN validator → parallelPhaseGate(phase)
    Save checkpoint (reason: "phase_complete")
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
📌 Checkpoint saved (task_complete)
```

**Phase completion:**
```markdown
🟢 validator → Phase 003 Gate
   ✓ Build passes
   ✓ Tests pass (47/47)
   ✓ Coverage 87%
   ✅ APPROVED
📌 Checkpoint saved (phase_complete)
```

**Cost updates:**
```markdown
💰 Cost: $4.36 / $50.00 (9%)
⚠️ Warning threshold reached ($10.00)
```

---

## Phase 2: Cost Monitoring

### Threshold Handling

```
FUNCTION checkThresholds(currentCost):

    IF currentCost >= maxCost:
        LOG "🛑 Maximum cost reached ($[max])"
        Save checkpoint (reason: "cost_limit")
        EXIT with instructions to increase limit

    IF currentCost >= alertCost AND NOT alertAcknowledged:
        LOG "⚠️ Alert threshold reached ($[alert])"
        PAUSE for user confirmation
        SET alertAcknowledged = true

    IF currentCost >= warnCost AND NOT warningShown:
        LOG "💡 Warning: Approaching budget ($[warn])"
        SET warningShown = true
```

### Cost Display

```markdown
## Cost Status

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

### On Project Pause/Checkpoint

```
IF context > 40% OR user interrupts:

    # Update STATE.md (session bridge)
    Update STATE.md:
        Status: "executing"
        Stopped at: "{current task description}"
        Resume file: ".autopilot/continue-here.md" (if mid-phase)
        Next action: "/autopilot:resume"

    # Create continue-here.md if mid-phase
    IF mid_phase:
        Create .autopilot/continue-here.md with:
            - Completed tasks table
            - Remaining work
            - Decisions made
            - Next action

    # Also update global history
    SPAWN history-tracker → recordProjectPause(projectId, "context_limit")

    LOG "📌 State saved to STATE.md"
    LOG "Resume with /autopilot:resume"
```

### On Project Success

```
IF all phases complete:

    # Update STATE.md
    Update STATE.md:
        Status: "complete"
        Completed at: [timestamp]

    SPAWN history-tracker → recordProjectComplete(projectId, "success")

    # Show summary with historical comparison
    LOG "
    ## ✅ Build Complete!

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
□ Context at 40%? (checkpoint time)
```

---

## Output Files

### Updated by /autopilot:build
```
.autopilot/
├── STATE.md          # Session bridge - status: "executing" → "complete"
├── token-usage.md    # Cost tracking (created/updated)
├── progress.md       # Compact execution log
├── continue-here.md  # Mid-phase resume (auto-deleted on complete)
└── phases/
    └── {phase}/
        ├── PLAN.md       # Updated with actual costs
        └── SUMMARY.md    # Created on phase completion
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
       - Save checkpoint
       - Display error details
       - PAUSE for user intervention
    4. On user fix confirmation → resume
```

### Context Overflow

```
IF context > 40%:
    1. Finish current task
    2. Save checkpoint
    3. Log: "📌 Context limit - checkpoint saved"
    4. Log: "Resume with /autopilot:resume"
    5. EXIT cleanly
```

$ARGUMENTS
