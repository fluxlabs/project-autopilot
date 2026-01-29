---
description: Show usage with token optimization strategies
---

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
/autopilot:scan      # Analyze project + estimate remaining work
/autopilot:discuss   # Gather context BEFORE planning (reduces questions)
/autopilot:plan      # Create phases and roadmap (scope only, no execution)
/autopilot:validate  # Check phase ordering and dependencies (NEW)
/autopilot:build     # Execute an existing plan
/autopilot:resume    # Continue from STATE.md
/autopilot:loop      # Auto-restart on context clear
/autopilot:status    # Estimates vs actuals
/autopilot:config    # Global settings + history
/autopilot:help      # This help
```

## Pipeline (Recommended Flow)

```
/autopilot:scan     → Understand scope and gaps
/autopilot:discuss  → Capture decisions (eliminates questions later)
/autopilot:plan     → Create phases and roadmap
/autopilot:validate → Verify ordering and dependencies (optional but recommended)
/autopilot:build    → Execute the plan (auto-runs :validate + :plan if needed)
/autopilot:resume   → Continue if context clears
```

**Tip:** You can skip straight to `/autopilot:build` - it will auto-transition to `/autopilot:plan` if no plan exists, and runs validation automatically.

---

## Examples

```bash
# Scan and estimate
/autopilot:scan

# Plan a new feature
/autopilot:plan auth system

# Plan with cost estimate limit
/autopilot:plan feature --max-cost=20

# Dry run planning (see phases without writing files)
/autopilot:plan feature --dry-run

# Validate phase ordering before build
/autopilot:validate

# Auto-fix simple ordering issues
/autopilot:validate --fix

# Execute the plan
/autopilot:build

# Execute immediately without approval
/autopilot:build -y

# Execute with budget limit
/autopilot:build --max-cost=25

# Check costs
/autopilot:status --detailed

# Global stats
/autopilot:status --global

# Set default budget
/autopilot:config --set max-cost=100

# View project history
/autopilot:config --history

# Resume from anywhere
/autopilot:resume --list
/autopilot:resume --project=my-api
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

## Agents (18)

| Role | Agents |
|------|--------|
| Optimization | **model-selector** (picks cheapest model) |
| Coordination | orchestrator, planner, validator, token-tracker |
| Persistence | **history-tracker** (cross-session state) |
| Design | architect, api-designer, database |
| Build | backend, frontend, devops |
| Quality | tester, security, debugger, refactor, documenter, code-review |

---

## Skills (10)

| Skill | Purpose |
|-------|---------|
| **token-optimization** | READ FIRST - saves 60-80% |
| **user-experience** | Consistent output patterns |
| **global-state** | Cross-session persistence |
| **visual-style** | Colors and icons for output |
| cost-estimation | Estimate tokens |
| phase-template | Phase format |
| phase-ordering | Correct sequence |
| quality-gates | Validation |
| git-workflow | Commits |
| token-tracking | Budgets |

---

## Agent Colors

| Agent | Icon | Role |
|-------|------|------|
| orchestrator | 🟣 | Coordination |
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
├── learnings.md      # CACHED (saves tokens!)
├── scope.md          # Estimates
├── phase-XXX.md      # Est + Actuals
├── token-usage.md    # Costs
└── checkpoint.md     # Resume
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
              Claude restarts with /autopilot:resume
                      ↓
              Repeat until project complete
```

---

## Cross-Session Features

### Global History
Your project history persists across Claude Code sessions:
- View history: `/autopilot:config --history`
- Resume any project: `/autopilot:resume --project=NAME`
- Global stats: `/autopilot:status --global`

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
