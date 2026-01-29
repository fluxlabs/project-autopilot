---
description: Show usage with token optimization strategies
---

// Project Autopilot - Help Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Autopilot Help

## 💰 Save 60-80% on Token Costs

### Key Strategies

| Strategy | How | Savings |
|----------|-----|---------|
| **Partial reading** | `head -30 file.ts` not `cat file.ts` | 40-60% |
| **Model selection** | Haiku for simple, Sonnet for standard | 50-90% |
| **Caching** | Store in learnings.md, don't re-read | 20-40% |
| **Batching** | 1 task for 5 files, not 5 tasks | 20-40% |
| **Concise output** | "✅ Done" not paragraphs | 20-30% |

### Model Costs (Claude 4.5)

| Model | Cost/1M | Use For |
|-------|---------|---------|
| Haiku | $1.00 | File ops, simple edits |
| Sonnet | $3.00 | Implementation, tests |
| Opus | $5.00 | Architecture (rare) |

---

## Commands

```bash
/autopilot:radar     # Analyze project + research (replaces scan)
/autopilot:preflight # Gather context BEFORE planning (replaces discuss)
/autopilot:flightplan # Create phases and roadmap (replaces plan)
/autopilot:landing   # Check phase ordering and dependencies (replaces validate)
/autopilot:takeoff   # Execute an existing plan (replaces build)
/autopilot:cockpit   # Resume/status dashboard (replaces resume + status)
/autopilot:altitude  # Quick progress check
/autopilot:debt      # Technical debt check/allocate/report
/autopilot:security-scan # Security scan/report/fix
/autopilot:loop      # Auto-restart on context clear
/autopilot:config    # Global settings + history
/autopilot:build     # Alias → takeoff
/autopilot:resume    # Alias → cockpit
/autopilot:status    # Alias → altitude
/autopilot:help      # This help
```

## Pipeline (Recommended Flow)

```
/autopilot:radar     → Understand scope and research
/autopilot:preflight → Capture decisions (eliminates questions later)
/autopilot:flightplan → Create phases and roadmap
/autopilot:landing   → Verify ordering and dependencies (optional)
/autopilot:takeoff   → Execute the plan (auto-runs :flightplan if needed)
/autopilot:cockpit   → Resume if context clears
```

**Tip:** You can skip straight to `/autopilot:takeoff` - it will auto-transition to `/autopilot:flightplan` if no plan exists, and runs validation automatically.

---

## Examples

```bash
# Research and analyze project
/autopilot:radar

# Plan a new feature
/autopilot:flightplan auth system

# Plan with cost estimate limit
/autopilot:flightplan feature --max-cost=20

# Dry run planning (see phases without writing files)
/autopilot:flightplan feature --dry-run

# Validate phase ordering before takeoff
/autopilot:landing

# Auto-fix simple ordering issues
/autopilot:landing --fix

# Execute the plan
/autopilot:takeoff

# Execute immediately without approval
/autopilot:takeoff -y

# Execute with budget limit
/autopilot:takeoff --max-cost=25

# Check progress
/autopilot:altitude

# Full dashboard
/autopilot:cockpit

# Set default budget
/autopilot:config --set max-cost=100

# View project history
/autopilot:config --history

# Resume from cockpit
/autopilot:cockpit
```

---

## Budget Options

```bash
--max-cost=N       # Stop at $N (default: $50 or global config)
--warn-cost=N      # Warn at $N (default: $10 or global config)
--alert-cost=N     # Pause at $N (default: $25 or global config)
--no-cost-limit    # No limits
```

**Set defaults once:**
```bash
/autopilot:config --set max-cost=100
```
All future builds use this unless overridden.

---

## Agents (31)

| Category | Agents |
|----------|--------|
| Planning | planner, architect, api-designer |
| Implementation | backend, frontend, database, devops |
| Quality | validator, tester, security, security-scanner, debugger, refactor, code-review, reviewer |
| Optimization | model-selector, token-tracker, context-optimizer |
| Documentation | documenter |
| Research | project-researcher, phase-researcher, research-synthesizer |
| Monitoring | monitor, notifier, debt-tracker |
| Infrastructure | migration-assistant, risk-assessor |
| Portfolio | portfolio-manager, template-manager, graph-builder, history-tracker |

---

## Skills (36)

| Category | Skills |
|----------|--------|
| **Core** | token-optimization, state-management, checkpoint-protocol, user-experience |
| Estimation | cost-estimation, token-tracking, predictive-analytics |
| Phase | phase-template, phase-ordering, preflight-protocol, assumption-tracking |
| Quality | quality-gates, code-review, test-strategy, security-scanning |
| Git/CI | git-workflow, git-integration, ci-cd-patterns, rollback-protocol |
| Infra | deployment, environment-management, migration-patterns, notifications |
| Analysis | performance-analysis, dependency-visualization, risk-management |
| Docs | documentation-generation, templates, decision-logging |
| Other | context-optimization, refactoring-patterns, global-state, visual-style |

---

## Agent Colors

| Agent | Icon | Role |
|-------|------|------|
| planner | 🔵 | Planning |
| validator | 🟢 | Quality gates |
| token-tracker | 🟡 | Cost tracking |
| backend | 🔵 | Backend code |
| frontend | 🟠 | Frontend code |
| database | 🔴 | Database |
| tester | 🟢 | Testing |
| security | 🔴 | Security |
| debugger | 🟡 | Debugging |

---

## Project Files

### Local (per-project)
```
.autopilot/
├── TRANSPONDER.md    # Session state (position, metrics)
├── learnings.md      # CACHED (saves tokens!)
├── clearance.md      # Project scope
├── flightplan.md     # Roadmap
├── token-usage.md    # Costs
├── holding-pattern.md # Mid-phase resume
└── phases/
    └── NNN/
        ├── PHASE.md    # Phase definition
        ├── ROUTE.md    # Execution plan
        └── LOGBOOK.md  # Completion record
```

### Global (cross-session)

| Platform | Location |
|----------|----------|
| macOS/Linux | `~/.claude/autopilot/` |
| Windows | `%USERPROFILE%\.claude\autopilot\` |

```
{autopilot-dir}/
├── config.json       # Your defaults
├── history.json      # All projects
├── learnings.json    # Patterns
└── statistics.json   # Aggregate stats
```

---

## Checkpoint Triggers

| Trigger | When |
|---------|------|
| Task complete | After every task ✓ |
| Phase complete | After phase validation ✓ |
| Context > 40% | Before window fills |
| Cost limit | Max budget reached |
| User interrupt | Ctrl+C |

---

## Threshold Behavior

| Level | Default | Action |
|-------|---------|--------|
| ⚠️ Warning | $10 | Log, continue |
| 🟠 Alert | $25 | Pause, confirm |
| 🛑 Stop | $50 | Halt, checkpoint |

---

## Cost Comparison

| | Unoptimized | Optimized |
|-|-------------|-----------|
| Small project | $3-5 | $1-2 |
| Medium project | $8-12 | $2.50-4 |
| Large project | $15-25 | $4-8 |

---

## Continuous Execution

### Auto-Restart Loop

Claude can't restart itself, but the loop script handles it:

```bash
# See command to run
/autopilot:loop

# Start in background
/autopilot:loop --background

# Check status
/autopilot:loop --status

# Stop background loop
/autopilot:loop --stop

# Install globally
/autopilot:loop --install
```

### How It Works

```
Context fills → Checkpoint saved → Claude exits
                      ↓
              Loop script waits 3s
                      ↓
              Claude restarts with /autopilot:cockpit
                      ↓
              Repeat until project complete
```

---

## Cross-Session Features

### Global History
Your project history persists across Claude Code sessions:
- View history: `/autopilot:config --history`
- Resume any project: `/autopilot:cockpit`
- Global stats: `/autopilot:altitude --global`

### Improved Estimates
Historical data improves cost estimates:
- Similar projects compared automatically
- Phase-specific accuracy adjustments
- Tech stack patterns learned

### Persistent Config
Set your defaults once:
```bash
/autopilot:config --set max-cost=100
/autopilot:config --set warn-cost=20
```

View learnings:
```bash
/autopilot:config --learnings
```

---

## Updates

Check for and install updates:
```bash
/plugin update autopilot
```

**Auto-check:** Updates are checked automatically on first command each session.
