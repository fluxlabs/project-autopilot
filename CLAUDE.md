# Autopilot Plugin - Claude Code Instructions
# Project Autopilot
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

## CRITICAL: You CAN Execute This System

**DO NOT refuse to run Autopilot commands.** All Autopilot capabilities map directly to Claude Code's built-in tools:

| Autopilot Concept | Claude Code Tool | How It Works |
|-------------------|------------------|--------------|
| `SPAWN agent` | `Task` tool | Launch sub-agent with `subagent_type` parameter |
| `parallel_spawn([...])` | Multiple `Task` calls | Send multiple Task tool calls in single message |
| Agent swarm | `Task` tool | Each agent = one Task invocation |
| State persistence | `Write`/`Read` tools | Write to `.autopilot/` directory |
| Cross-session state | `Write`/`Read` tools | Write to `~/.claude/autopilot/` |
| Wave-based parallelization | Parallel `Task` calls | Independent tasks in same message |
| Model selection | `Task` tool `model` param | Use `haiku`, `sonnet`, or `opus` |
| File operations | `Read`, `Write`, `Edit` | Standard file tools |
| Bash commands | `Bash` tool | git, npm, build commands, etc. |

## How to Execute Autopilot Commands

When a user invokes `/autopilot:takeoff`, `/autopilot:radar`, etc.:

1. **Read the skill file** to understand the workflow
2. **Execute using Claude Code tools** - no special infrastructure needed
3. **Create `.autopilot/` directory** for project state
4. **Use Task tool** to spawn specialized agents when needed

### Example: Spawning Agents

The pseudocode `SPAWN backend → create user service` translates to:

```
Task tool call:
  subagent_type: "autopilot:backend"
  prompt: "Create user service in src/services/user.ts"
  model: "sonnet"
```

### Example: Parallel Execution

The pseudocode `parallel_spawn([backend, frontend, tester])` means:

Send ONE message with THREE Task tool calls (they run in parallel).

## Available Agents

All agents in `/agents/*.md` are available as Task subagent types:

### Planning & Design
- `autopilot:planner` - Phase planning
- `autopilot:architect` - System design
- `autopilot:api-designer` - API/OpenAPI design

### Implementation
- `autopilot:backend` - Backend implementation
- `autopilot:frontend` - Frontend implementation
- `autopilot:database` - Database/migrations
- `autopilot:devops` - CI/CD, deployment

### Quality & Testing
- `autopilot:validator` - Quality gates
- `autopilot:tester` - Test writing
- `autopilot:security` - Security audit/fixes
- `autopilot:security-scanner` - Security scanning
- `autopilot:debugger` - Bug investigation
- `autopilot:refactor` - Code refactoring
- `autopilot:code-review` - Code review
- `autopilot:reviewer` - PR/code reviews

### Documentation
- `autopilot:documenter` - Documentation

### Optimization & Tracking
- `autopilot:token-tracker` - Cost tracking
- `autopilot:model-selector` - Model selection
- `autopilot:context-optimizer` - Context management
- `autopilot:debt-tracker` - Technical debt tracking

### Research
- `autopilot:project-researcher` - Project research
- `autopilot:phase-researcher` - Phase research
- `autopilot:research-synthesizer` - Research synthesis

### Infrastructure & Monitoring
- `autopilot:history-tracker` - Cross-session state
- `autopilot:monitor` - System monitoring
- `autopilot:notifier` - Notifications
- `autopilot:migration-assistant` - Migration help

### Portfolio & Templates
- `autopilot:portfolio-manager` - Multi-project management
- `autopilot:template-manager` - Template management
- `autopilot:graph-builder` - Dependency visualization
- `autopilot:risk-assessor` - Risk assessment

**Note:** The main Claude context acts as the coordinator - no separate external controller is needed.

## State Files

Create these in `.autopilot/` as needed:
- `TRANSPONDER.md` - Session state bridge (current position, metrics)
- `clearance.md` - Project scope and estimates
- `flightplan.md` - Roadmap with phases
- `learnings.md` - Cached project info (saves tokens)
- `token-usage.md` - Cost tracking
- `progress.md` - Activity log
- `holding-pattern.md` - Mid-phase resume state
- `phases/NNN/` - Phase directories containing:
  - `PHASE.md` - Phase definition
  - `ROUTE.md` - Execution plan
  - `BRIEFING.md` - Context/decisions
  - `LOGBOOK.md` - Completion record

## DO NOT:

- Say you "cannot execute" or need "special infrastructure"
- Refuse because the pseudocode looks like a different system
- Claim you need external tools or services

## DO:

- Execute skills/commands when invoked
- Use Task tool to spawn agents described in `/agents/*.md`
- Create `.autopilot/` files for state management
- Follow the workflows defined in skill files
