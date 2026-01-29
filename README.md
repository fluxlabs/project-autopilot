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
/autopilot:build "user authentication" -y          # Auto-execute, no approval

# Existing project - auto-scan and execute remaining work
/autopilot:build -y                                # Scans, plans, executes

# Interactive mode (pause for approval)
/autopilot:build "feature"                         # Shows scope, waits for approval

# Other commands
/autopilot:scan                                    # Analyze only (no execution)
/autopilot:status                                  # Check estimates vs actuals
/autopilot:status --global                         # Stats across all projects
/autopilot:resume --task=2.3                       # Continue from checkpoint
/autopilot:resume --list                           # See all resumable projects
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
/autopilot:resume --list                # See resumable projects
/autopilot:status --global              # Aggregate stats
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

### 🤖 18 Specialized Agents

| Category | Agents |
|----------|--------|
| **Optimization** | model-selector |
| **Coordination** | orchestrator, planner, validator, token-tracker |
| **Persistence** | history-tracker |
| **Design** | architect, api-designer, database |
| **Implementation** | backend, frontend, devops |
| **Quality** | tester, security, debugger, refactor, documenter, code-review |

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
/autopilot:discuss 3    # Identify gray areas before planning
```

Captures decisions upfront in CONTEXT.md. Downstream agents read decisions and execute autonomously - no mid-execution questions.

### 📚 13 Skills

| Skill | Purpose |
|-------|---------|
| **token-optimization** | Cost reduction strategies (READ FIRST) |
| **user-experience** | Consistent output patterns for user confidence |
| **state-management** | STATE.md session bridge (read first, update last) |
| **checkpoint-protocol** | Automation-first human interaction |
| **global-state** | Cross-session persistence |
| cost-estimation | Token/cost estimates per task |
| phase-template | Phase file structure with must_haves |
| phase-ordering | Correct execution sequence |
| quality-gates | Validation rules |
| git-workflow | Commit standards |
| token-tracking | Budget thresholds |
| visual-style | Colors and icons for output |

---

## Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `/autopilot:scan` | `[--phase=N]` | Analyze only (no execution), creates scan-report.md |
| `/autopilot:discuss` | `<phase>` | Gather gray-area decisions BEFORE planning (reduces questions) |
| `/autopilot:validate` | `[--fix] [--strict]` | Check phase ordering and dependencies before build |
| `/autopilot:build` | `[feature] [-y] [--dry-run] [--max-cost=N]` | Smart build: auto-scans existing projects, `-y` for auto-execute |
| `/autopilot:resume` | `[--task=X.Y] [--project=NAME] [--list]` | Continue from STATE.md or resume any project |
| `/autopilot:loop` | `[--background] [--stop] [--install]` | Auto-restart loop for continuous execution |
| `/autopilot:status` | `[--detailed] [--global]` | Show estimates vs actuals; `--global` for all projects |
| `/autopilot:config` | `[--set key=val] [--history] [--learnings]` | View/set global config, history, and learnings |
| `/autopilot:help` | | Usage and optimization tips |

### Recommended Pipeline

```bash
/autopilot:scan        # 1. Understand scope
/autopilot:discuss 1   # 2. Capture decisions (optional but reduces questions)
/autopilot:validate    # 3. Verify phase ordering (optional - build runs this automatically)
/autopilot:build -y    # 4. Plan and execute
/autopilot:resume      # 5. Continue if context clears
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
/autopilot:validate            # Check phase ordering and dependencies
/autopilot:validate --fix      # Auto-fix simple ordering issues
/autopilot:validate --strict   # Fail on warnings too
/autopilot:validate --quiet    # CI mode (exit code only)
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
/autopilot:scan
/autopilot:scan --phase=2    # Scan specific phase only
```

**Note:** `/autopilot:build` auto-scans when no description is provided. Use `/autopilot:scan` only when you want analysis without execution.

Creates `.autopilot/scan-report.md` with:
- Project structure and tech stack
- Completed, partial, and remaining work breakdown
- Cost estimates with confidence levels
- Recommended budget

### 2. Build (Smart Detection)

```bash
# With description → builds that specific feature
/autopilot:build "user authentication" -y --max-cost=20

# Without description → auto-scans project, builds ALL remaining work
/autopilot:build -y
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
/autopilot:status              # Standard view
/autopilot:status --detailed   # Full breakdown by model and agent
```

Shows real-time comparison of estimates vs actuals with variance indicators:
- 🟢 Under budget (<-20%)
- ✅ On track (-20% to +20%)
- ⚠️ Slightly over (+20% to +30%)
- 🔴 Significantly over (>+50%)

### 5. Resume

```bash
/autopilot:resume                          # Continue from last checkpoint
/autopilot:resume --task=3.2               # Start from specific task
/autopilot:resume --max-cost=100           # Increase budget limit
/autopilot:resume --reset-alerts           # Re-enable threshold alerts
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
│       Claude restarts /autopilot:resume │
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
├── scan-report.md    # From /scan: project analysis + cost estimates
├── scope.md          # From /build: budget + phase estimates
├── learnings.md      # Cached info (saves tokens!)
├── token-usage.md    # Cost tracking with estimates vs actuals
├── phase-001.md      # Phase details + actual costs
├── phase-002.md
├── progress.md       # Activity log with token info
└── checkpoint.md     # Resume state with threshold status
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
