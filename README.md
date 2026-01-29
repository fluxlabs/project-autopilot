# Autopilot Plugin for Claude Code

**One command to build entire projects.** Auto-scans existing code, generates execution phases, spawns specialized agents, tracks costs, and handles interruptions — all hands-off. Settings and history persist across sessions.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/fluxlabs/project-autopilot)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v2.0.12+-purple.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

## Installation

### Claude Code Plugin Manager

```bash
# Step 1: Add marketplace
/plugin marketplace add fluxlabs/project-autopilot

# Step 2: Install plugin
/plugin install autopilot
```

### Interactive Install

```bash
/plugin
```

Navigate: **Marketplaces** → Add `fluxlabs/project-autopilot` → **Discover** → Install **autopilot**

### Verify

```bash
/autopilot:help
```

---

## Quick Start

```bash
# Set your defaults once (optional)
/autopilot:config --set max-cost=100

# New project - describe what to build
/autopilot:takeoff "user authentication" -y          # Auto-execute, no approval

# Existing project - auto-scan and execute remaining work
/autopilot:takeoff -y                                # Scans, plans, executes

# Interactive mode (pause for approval)
/autopilot:takeoff "feature"                         # Shows scope, waits for approval

# Other commands
/autopilot:radar                                    # Analyze only (no execution)
/autopilot:altitude                                  # Check estimates vs actuals
/autopilot:altitude --global                         # Stats across all projects
/autopilot:cockpit --task=2.3                       # Continue from checkpoint
/autopilot:cockpit --list                           # See all resumable projects
/autopilot:config --history                        # View project history
```

---

## Features

### 💰 Token Optimization (60-80% Savings)

| Strategy | Savings | Description |
|----------|---------|-------------|
| Partial file reading | 40-60% | Read only needed lines, not entire files |
| Smart model selection | 50-90% | Haiku for simple tasks, Sonnet for standard |
| Caching | 20-40% | Store structure/types in learnings.md |
| Batching | 20-40% | Combine related files in one task |
| Concise output | 20-30% | Skip verbose explanations |

**Cost comparison:** $10-15 → $2.50-5 per project

### 🔄 Cross-Session Persistence

Settings and history persist across Claude Code sessions:

| Feature | Description |
|---------|-------------|
| **Global Config** | Set defaults once, apply to all projects |
| **Project History** | Track all projects built with costs and outcomes |
| **Smart Estimates** | Historical data improves future cost predictions |
| **Resume Anywhere** | List and resume projects from any directory |

```bash
/autopilot:config --set max-cost=100    # Set default budget
/autopilot:config --history             # View all projects
/autopilot:cockpit --list                # See resumable projects
/autopilot:altitude --global              # Aggregate stats
```

### 📊 Estimates vs Actuals

Track costs before and after execution:

```
| Phase | Est. | Actual | Variance |
|-------|------|--------|----------|
| 001   | $0.15| $0.12  | -20% 🟢  |
| 002   | $0.32| $0.35  | +9% ✅   |
| 003   | $0.55| -      | 🔄       |
```

### 🤖 31 Specialized Agents

| Category | Agents |
|----------|--------|
| **Planning** | planner, architect, api-designer |
| **Implementation** | backend, frontend, database, devops |
| **Quality** | validator, tester, security, security-scanner, debugger, refactor, code-review, reviewer |
| **Optimization** | model-selector, token-tracker, context-optimizer |
| **Documentation** | documenter |
| **Research** | project-researcher, phase-researcher, research-synthesizer |
| **Monitoring** | monitor, notifier, debt-tracker |
| **Infrastructure** | migration-assistant, risk-assessor |
| **Portfolio** | portfolio-manager, template-manager, graph-builder, history-tracker |

### 🎯 Goal-Backward Verification

Derive requirements from phase goals, verify against code:

```yaml
must_haves:
  truths:
    - "User can see messages"
    - "Messages persist across refresh"
  artifacts:
    - path: "src/components/Chat.tsx"
      min_lines: 30
  key_links:
    - from: "Chat.tsx" to: "/api/chat"
      pattern: "fetch.*api/chat"
```

Validator checks must_haves after execution. If gaps found → auto-generates gap-closure plans.

### ⚡ Wave-Based Parallel Execution

Plans grouped into waves. All plans in same wave run in parallel:

```
Phase 3
├── Wave 1 (parallel): API endpoints
├── Wave 2 (parallel): UI components
└── Wave 3 (sequential): Integration tests
```

### 💬 Discuss Before Plan (Reduces Questions)

```bash
/autopilot:preflight 3    # Identify gray areas before planning
```

Captures decisions upfront in CONTEXT.md. Downstream agents read decisions and execute autonomously - no mid-execution questions.

### 📚 36 Skills (Reference Guides)

| Category | Skills |
|----------|--------|
| **Core (Read First)** | token-optimization, state-management, checkpoint-protocol, user-experience |
| **Estimation** | cost-estimation, token-tracking, predictive-analytics |
| **Phase Management** | phase-template, phase-ordering, preflight-protocol, assumption-tracking |
| **Quality** | quality-gates, code-review, test-strategy, security-scanning |
| **Git & CI/CD** | git-workflow, git-integration, ci-cd-patterns, rollback-protocol |
| **Infrastructure** | deployment, environment-management, migration-patterns, notifications |
| **Analysis** | performance-analysis, dependency-visualization, risk-management, risk-assessment |
| **Documentation** | documentation-generation, templates, decision-logging |
| **Optimization** | context-optimization, refactoring-patterns, global-state |
| **Specialized** | accessibility, debug-sessions, visual-style |

---

## Commands (46 Total)

### Core Workflow

| Command | Description |
|---------|-------------|
| `/autopilot:radar` | Research and analyze project |
| `/autopilot:preflight` | Gather context and decisions before planning |
| `/autopilot:flightplan` | Create phases and roadmap |
| `/autopilot:landing` | Check phase ordering and dependencies |
| `/autopilot:takeoff` | Execute flight plan (`-y` for auto-execute) |
| `/autopilot:build` | Execute existing plan with wave parallelization |
| `/autopilot:cockpit` | Resume dashboard and session management |
| `/autopilot:altitude` | Quick progress check |
| `/autopilot:status` | Progress check with budget tracking |
| `/autopilot:loop` | Auto-restart loop for continuous execution |

### Configuration & Management

| Command | Description |
|---------|-------------|
| `/autopilot:config` | View/set global config, history, learnings |
| `/autopilot:init` | Initialize project from template |
| `/autopilot:estimate` | Cost estimate without execution |
| `/autopilot:compare` | Compare estimated vs actual across projects |
| `/autopilot:export` | Export plan as markdown or JSON |
| `/autopilot:graph` | Visualize phase dependencies and critical path |
| `/autopilot:help` | Usage and optimization tips |
| `/autopilot:update` | Check for and install updates |

### Quality & Review

| Command | Description |
|---------|-------------|
| `/autopilot:review` | Automated code review |
| `/autopilot:coverage` | Test coverage analysis with gap detection |
| `/autopilot:a11y` | Accessibility audit and WCAG compliance |
| `/autopilot:security-scan` | Security scanning for vulnerabilities |
| `/autopilot:perf` | Performance analysis and optimization |
| `/autopilot:refactor` | Intelligent refactoring suggestions |
| `/autopilot:debug` | Systematic debugging assistance |
| `/autopilot:risk` | Risk assessment and mitigation planning |

### DevOps & Infrastructure

| Command | Description |
|---------|-------------|
| `/autopilot:ci` | CI/CD pipeline generation |
| `/autopilot:deploy` | Deployment orchestration |
| `/autopilot:env` | Environment configuration management |
| `/autopilot:deps` | Dependency analysis and security auditing |
| `/autopilot:migrate` | Migration planning and execution |
| `/autopilot:rollback` | Revert to previous checkpoint |

### Documentation & Communication

| Command | Description |
|---------|-------------|
| `/autopilot:docs` | Auto-generate documentation from code |
| `/autopilot:handoff` | Generate context for developer handoff |
| `/autopilot:pr` | Create pull request with phase context |
| `/autopilot:standup` | Generate daily standup summary |
| `/autopilot:sprint` | Sprint planning and tracking |
| `/autopilot:notify` | Configure notification webhooks |

### Portfolio & Advanced

| Command | Description |
|---------|-------------|
| `/autopilot:portfolio` | Manage multiple projects |
| `/autopilot:sync` | Sync with external project management tools |
| `/autopilot:insights` | Deep analytics and pattern detection |
| `/autopilot:forecast` | Predictive cost and time estimation |
| `/autopilot:learn` | Extract learnings across projects |
| `/autopilot:prompt` | Prompt template management |
| `/autopilot:resume` | Resume execution from checkpoint |
| `/autopilot:debt` | Technical debt tracking |

### Recommended Pipeline

```bash
/autopilot:radar        # 1. Research and understand scope
/autopilot:preflight 1  # 2. Capture decisions (optional but reduces questions)
/autopilot:flightplan   # 3. Create phases and roadmap
/autopilot:landing      # 4. Verify phase ordering (optional)
/autopilot:takeoff -y   # 5. Execute the plan
/autopilot:cockpit      # 6. Resume if context clears
```

### Build Options

```bash
-y, --yes          # Auto-execute without approval (key for automation)
--dry-run          # Plan only, don't execute
--from-scan        # Use existing scan-report.md instead of auto-scanning
--skip-validation  # Skip phase ordering validation (not recommended)
```

### Validation Options

```bash
/autopilot:landing            # Check phase ordering and dependencies
/autopilot:landing --fix      # Auto-fix simple ordering issues
/autopilot:landing --strict   # Fail on warnings too
/autopilot:landing --quiet    # CI mode (exit code only)
```

### Budget Options

```bash
--max-cost=N       # Hard stop (default: $50)
--warn-cost=N      # Warning threshold (default: $10)
--alert-cost=N     # Pause for confirmation (default: $25)
--max-tokens=N     # Hard stop by token count
--no-cost-limit    # Disable all limits
--reset-alerts     # Re-enable alerts after acknowledgment
```

---

## How It Works

### 1. Scan (Optional)

```bash
/autopilot:radar
/autopilot:radar --phase=2    # Scan specific phase only
```

**Note:** `/autopilot:takeoff` auto-scans when no description is provided. Use `/autopilot:radar` only when you want analysis without execution.

Creates `.autopilot/scan-report.md` with:
- Project structure and tech stack
- Completed, partial, and remaining work breakdown
- Cost estimates with confidence levels
- Recommended budget

### 2. Build (Smart Detection)

```bash
# With description → builds that specific feature
/autopilot:takeoff "user authentication" -y --max-cost=20

# Without description → auto-scans project, builds ALL remaining work
/autopilot:takeoff -y
```

**Smart detection logic:**
- Has description? → Plan phases for that feature
- No description? → Auto-scan project, plan phases for remaining work
- Has `-y`? → Execute immediately
- No `-y`? → Pause for approval

Applies token optimization (partial file reads, model selection, caching, batching).
Creates scope with phase estimates:

```
## Budget Summary
| Phase | Est. Cost | Confidence |
|-------|-----------|------------|
| 001 Setup | $0.15 | High |
| 002 Database | $0.32 | Medium |
| 003 Auth | $0.55 | Medium |
| **Total** | **$1.02** | |

# With -y flag: executes immediately
# Without -y: displays "Reply 'approved' to start."
```

### 3. Execute

Each task:
1. Selects optimal model (Haiku/Sonnet/Opus)
2. Reads only necessary files
3. Executes with minimal context
4. Records actual tokens/cost
5. Updates variance tracking

### 4. Track

```bash
/autopilot:altitude              # Standard view
/autopilot:altitude --detailed   # Full breakdown by model and agent
```

Shows real-time comparison of estimates vs actuals with variance indicators:
- 🟢 Under budget (<-20%)
- ✅ On track (-20% to +20%)
- ⚠️ Slightly over (+20% to +30%)
- 🔴 Significantly over (>+50%)

### 5. Resume

```bash
/autopilot:cockpit                          # Continue from last checkpoint
/autopilot:cockpit --task=3.2               # Start from specific task
/autopilot:cockpit --max-cost=100           # Increase budget limit
/autopilot:cockpit --reset-alerts           # Re-enable threshold alerts
```

Restores token state, validates quality gates (build/test/lint), and continues execution.

**Checkpoints are saved automatically:**

| Trigger | When |
|---------|------|
| Task complete | After every successful task |
| Phase complete | After phase validation passes |
| Context > 40% | Before context window fills |
| Cost limit | When max budget reached |
| User interrupt | On Ctrl+C |

### 6. Continuous Loop (Fully Autonomous)

Claude can't restart itself when context fills up, but a wrapper script handles this:

```bash
# From within Claude - see command to run
/autopilot:loop

# Start in background (returns control immediately)
/autopilot:loop --background

# Check if running
/autopilot:loop --status

# Stop background loop
/autopilot:loop --stop

# Install script globally
/autopilot:loop --install
```

**How it works:**

```
┌─────────────────────────────────────────┐
│  Context fills → Checkpoint → Exit      │
│                      ↓                  │
│            Script waits 3s              │
│                      ↓                  │
│       Claude restarts /autopilot:cockpit │
│                      ↓                  │
│         Repeat until complete           │
└─────────────────────────────────────────┘
```

Or run the script directly:

```bash
# In your terminal (not Claude)
./scripts/autopilot-loop.sh /path/to/project

# With custom settings
MAX_ITERATIONS=50 COOLDOWN_SECONDS=5 ./scripts/autopilot-loop.sh .
```

---

## Project Structure

### Local (per-project)

When autopilot runs, it creates:

```
.autopilot/
├── TRANSPONDER.md    # Session state (position, metrics, decisions)
├── clearance.md      # Project scope and estimates
├── flightplan.md     # Roadmap with phase breakdown
├── learnings.md      # Cached info (saves tokens!)
├── token-usage.md    # Cost tracking with estimates vs actuals
├── progress.md       # Activity log with token info
├── holding-pattern.md # Mid-phase resume state
└── phases/
    ├── 001/
    │   ├── PHASE.md    # Phase definition
    │   ├── ROUTE.md    # Execution plan
    │   ├── BRIEFING.md # Context/decisions
    │   └── LOGBOOK.md  # Completion record
    ├── 002/
    └── ...
```

### Global (cross-session)

Settings and history persist in:

| Platform | Location |
|----------|----------|
| macOS/Linux | `~/.claude/autopilot/` |
| Windows | `%USERPROFILE%\.claude\autopilot\` |

```
{autopilot-dir}/
├── config.json       # Your default thresholds and preferences
├── history.json      # All projects built (for resume from anywhere)
├── learnings.json    # Patterns for better cost estimates
└── statistics.json   # Aggregate stats across all projects
```

---

## Plugin Management

```bash
# Update
/plugin update autopilot

# Disable/Enable
/plugin disable autopilot
/plugin enable autopilot

# Uninstall
/plugin uninstall autopilot

# Check for errors
/plugin errors
```

---

## Requirements

- Claude Code v2.0.12 or higher
- Run `claude --version` to check

---

## License

MIT

---

## Links

- **Repository:** https://github.com/fluxlabs/project-autopilot
- **Issues:** https://github.com/fluxlabs/project-autopilot/issues
- **Claude Code Docs:** https://docs.anthropic.com/en/docs/claude-code
