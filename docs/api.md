# Project Autopilot API Reference
# Project Autopilot
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

## Overview

Project Autopilot provides a comprehensive API through slash commands, agents, and skills.

## Commands API

All commands are invoked via `/autopilot:<command>` syntax.

### Core Commands

| Command | Description |
|---------|-------------|
| `/autopilot:takeoff` | Initialize and start project execution |
| `/autopilot:preflight` | Run pre-execution checks and planning |
| `/autopilot:radar` | Scan codebase and assess current state |
| `/autopilot:cockpit` | View project dashboard and status |
| `/autopilot:landing` | Complete phase and validate results |
| `/autopilot:flightplan` | View/edit project roadmap |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/autopilot:help` | Show available commands |
| `/autopilot:init` | Initialize new project |
| `/autopilot:estimate` | Get cost estimates |
| `/autopilot:loop` | Run continuous execution |

## Agent API

Agents are spawned via the Task tool with `subagent_type` parameter.

### Example

```
Task tool call:
  subagent_type: "autopilot:backend"
  prompt: "Create user authentication service"
  model: "sonnet"
```

### Available Agents

See [CLAUDE.md](../CLAUDE.md) for the complete list of 31 agents.

## State Files

Autopilot maintains state in `.autopilot/` directory:

| File | Purpose |
|------|---------|
| `TRANSPONDER.md` | Session state bridge |
| `clearance.md` | Project scope |
| `flightplan.md` | Roadmap with phases |
| `token-usage.md` | Cost tracking |

## MCP Server

The MCP server provides external tool integration.

### Installation

```bash
cd mcp-server
npm install
npm run build
```

### Configuration

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "autopilot": {
      "command": "node",
      "args": ["path/to/mcp-server/dist/autopilot-server.js"]
    }
  }
}
```

## See Also

- [README.md](../README.md) - Project overview
- [INSTALL.md](../INSTALL.md) - Installation guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guide
