# Autopilot MCP Server
# Project Autopilot - External tool integration for Claude Code
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

MCP (Model Context Protocol) server that provides external tool integration and project management capabilities for Project Autopilot.

## Features

### Tools

| Tool | Description |
|------|-------------|
| `create_project` | Create a new autopilot project |
| `update_project_status` | Update project status |
| `list_projects` | List all autopilot projects |
| `create_phase` | Create a new phase for a project |
| `update_phase_status` | Update phase status |
| `get_phase` | Get phase details |
| `update_task_status` | Update task status within a phase |
| `query_history` | Query project history for analytics |
| `get_analytics` | Get aggregated analytics across all projects |
| `add_learning` | Add a learning to the global learnings file |
| `search_learnings` | Search global learnings |
| `sync_jira` | Sync project with Jira* |
| `sync_linear` | Sync project with Linear* |
| `export_notion` | Export project documentation to Notion* |
| `notify_slack` | Send notification to Slack* |

*Requires API credentials (see External Integrations below)

### Resources

| Resource | Description |
|----------|-------------|
| `autopilot://learnings` | Global learnings and patterns |
| `autopilot://history` | Historical project data |
| `autopilot://project/{id}` | Individual project state |

### Prompts

| Prompt | Description |
|--------|-------------|
| `planning-template` | Template for project planning phase |
| `review-template` | Template for code review |
| `standup-template` | Template for daily standup summary |
| `handoff-template` | Template for developer handoff documentation |

---

## Installation

### Prerequisites

- Node.js >= 18.0.0
- npm or yarn

### Install Dependencies

```bash
cd mcp-server
npm install
```

### Build

```bash
npm run build
```

---

## Configuration

### Claude Code Configuration

Add to your Claude Code MCP settings (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "autopilot": {
      "command": "node",
      "args": ["/path/to/project-autopilot/mcp-server/dist/autopilot-server.js"]
    }
  }
}
```

Or for development:

```json
{
  "mcpServers": {
    "autopilot": {
      "command": "npx",
      "args": ["tsx", "/path/to/project-autopilot/mcp-server/autopilot-server.ts"]
    }
  }
}
```

### Data Storage

The server stores data in `~/.claude/autopilot/`:

```
~/.claude/autopilot/
├── global-learnings.md     # Cross-project learnings
├── project-history.json    # Completed project analytics
└── projects/               # Active project data
    └── proj-xxx/
        ├── state.json      # Project state
        └── phases/         # Phase data
            ├── phase-1.json
            └── phase-2.json
```

---

## Usage

### Creating a Project

```typescript
// Via MCP tool call
{
  "tool": "create_project",
  "arguments": {
    "name": "My New Project",
    "description": "A project to build something awesome",
    "totalPhases": 5,
    "estimatedCost": 50.00
  }
}
```

### Managing Phases

```typescript
// Create a phase
{
  "tool": "create_phase",
  "arguments": {
    "projectId": "proj-xxx",
    "phaseId": 1,
    "name": "Setup & Configuration",
    "tasks": [
      { "description": "Initialize project structure" },
      { "description": "Configure dependencies" },
      { "description": "Set up CI/CD" }
    ]
  }
}

// Update phase status
{
  "tool": "update_phase_status",
  "arguments": {
    "projectId": "proj-xxx",
    "phaseId": 1,
    "status": "in_progress"
  }
}
```

### Querying Analytics

```typescript
// Get project analytics
{
  "tool": "get_analytics",
  "arguments": {}
}

// Response:
{
  "analytics": {
    "totalProjects": 15,
    "completedProjects": 12,
    "activeProjects": 3,
    "totalCost": 450.25,
    "averageCost": 37.52,
    "averageSuccessRate": 94.5,
    "totalTokens": 2500000
  }
}
```

### Adding Learnings

```typescript
{
  "tool": "add_learning",
  "arguments": {
    "category": "patterns",
    "content": "Using wave-based parallel execution reduces total token usage by 15%",
    "projectId": "proj-xxx"
  }
}
```

---

## External Integrations

### Jira Integration

Set environment variables:

```bash
export JIRA_API_TOKEN="your-api-token"
export JIRA_BASE_URL="https://your-domain.atlassian.net"
```

Usage:

```typescript
{
  "tool": "sync_jira",
  "arguments": {
    "projectId": "proj-xxx",
    "jiraProjectKey": "PROJ",
    "action": "export"
  }
}
```

### Linear Integration

Set environment variables:

```bash
export LINEAR_API_KEY="your-api-key"
```

Usage:

```typescript
{
  "tool": "sync_linear",
  "arguments": {
    "projectId": "proj-xxx",
    "linearTeamId": "team-id",
    "action": "sync"
  }
}
```

### Notion Integration

Set environment variables:

```bash
export NOTION_API_KEY="your-api-key"
```

Usage:

```typescript
{
  "tool": "export_notion",
  "arguments": {
    "projectId": "proj-xxx",
    "notionPageId": "page-id",
    "includePhases": true,
    "includeLearnings": true
  }
}
```

### Slack Integration

Set environment variables:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/xxx"
```

Usage:

```typescript
{
  "tool": "notify_slack",
  "arguments": {
    "channel": "#project-updates",
    "message": "Phase 3 completed successfully!",
    "projectId": "proj-xxx"
  }
}
```

---

## Development

### Running in Development Mode

```bash
npm run dev
```

### Testing

```bash
# Run the server in one terminal
npm run dev

# In another terminal, use the MCP inspector
npx @modelcontextprotocol/inspector
```

### Building for Production

```bash
npm run build
npm start
```

---

## TypeScript Configuration

Create `tsconfig.json` if needed:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "strict": true,
    "outDir": "dist",
    "rootDir": ".",
    "declaration": true,
    "skipLibCheck": true
  },
  "include": ["*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Troubleshooting

### Server not connecting

1. Check Claude Code MCP settings path is correct
2. Ensure the server is built (`npm run build`)
3. Check Node.js version is >= 18

### Permission errors

Ensure the `~/.claude/autopilot/` directory exists and is writable:

```bash
mkdir -p ~/.claude/autopilot
chmod 755 ~/.claude/autopilot
```

### External integrations failing

1. Verify environment variables are set
2. Check API credentials are valid
3. Review rate limits for external services

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run linting: `npm run lint`
5. Build: `npm run build`
6. Submit a pull request

---

## License

MIT License - Copyright (c) 2026 Jeremy McSpadden
