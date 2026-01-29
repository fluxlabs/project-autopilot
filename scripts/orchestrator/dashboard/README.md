# Autopilot Dashboard
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Web-based dashboard for managing autonomous coding projects with real-time streaming, project management, and cost visualization.

## Features

- **Real-time streaming** - Watch Claude's output and tool calls live via WebSocket
- **Project management** - Create, start, stop, resume multiple projects
- **Cost visualization** - Charts showing cost breakdown by model, token usage, budget progress
- **Modern UI** - Dark theme, responsive design with Tailwind CSS

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Start services
docker-compose up -d

# Open dashboard
open http://localhost:3000
```

### Option 2: Manual

**Backend:**
```bash
cd backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python server.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (React)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Dashboard                                        │  │
│  │  ├── Project List                                │  │
│  │  ├── Real-time Output                            │  │
│  │  ├── Cost Charts                                 │  │
│  │  └── Task History                                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP + WebSocket
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │  REST API                                         │  │
│  │  ├── POST /api/projects (create)                 │  │
│  │  ├── GET  /api/projects (list)                   │  │
│  │  ├── POST /api/projects/:id/start                │  │
│  │  ├── POST /api/projects/:id/stop                 │  │
│  │  └── GET  /api/stats                             │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  WebSocket /ws/:project_id                       │  │
│  │  ├── output (text)                               │  │
│  │  ├── tool_start / tool_end                       │  │
│  │  ├── cost_update                                 │  │
│  │  └── complete / error                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   Orchestrator                          │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ Context │ │  Tools  │ │Checkpoint│ │   Costs     │  │
│  └────┬────┘ └────┬────┘ └────┬─────┘ └──────┬──────┘  │
│       └───────────┼───────────┴───────────────┘        │
│                   ▼                                     │
│            Anthropic API                                │
└─────────────────────────────────────────────────────────┘
```

## API Reference

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create a new project |
| GET | `/api/projects/:id` | Get project details |
| DELETE | `/api/projects/:id` | Delete a project |
| POST | `/api/projects/:id/start` | Start/resume project |
| POST | `/api/projects/:id/stop` | Stop project |
| GET | `/api/projects/:id/history` | Get execution history |

### Global

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get global statistics |
| GET | `/api/config` | Get configuration |
| PUT | `/api/config` | Update configuration |
| GET | `/api/health` | Health check |

### WebSocket

Connect to `ws://localhost:8000/ws/:project_id` for real-time updates.

**Server → Client Messages:**
```typescript
{ type: "output", text: "...", timestamp: "..." }
{ type: "tool_start", tool_name: "read_file", tool_input: {...} }
{ type: "tool_end", tool_name: "read_file", result: "...", is_error: false }
{ type: "cost_update", level: "warning", cost: 10.5 }
{ type: "checkpoint", timestamp: "..." }
{ type: "complete", timestamp: "..." }
{ type: "error", error: "...", timestamp: "..." }
```

**Client → Server Messages:**
```typescript
{ type: "start" }
{ type: "stop" }
{ type: "help_response", response: "..." }
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | Your Anthropic API key |
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Backend URL for frontend |

### Backend Config

Edit `config.yaml` in the orchestrator directory:

```yaml
model: sonnet  # Options: haiku, sonnet, opus
max_tokens: 8192
max_context_tokens: 150000

costs:
  warn: 10.0    # Show warning
  alert: 25.0   # Pause for confirmation
  max: 50.0     # Hard stop
```

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Type Checking

```bash
# Frontend
cd frontend && npm run lint

# Backend
cd backend && mypy .
```

## Screenshots

### Dashboard
![Dashboard](docs/dashboard.png)

### Cost Charts
![Costs](docs/costs.png)

### Real-time Output
![Output](docs/output.png)

## Troubleshooting

### WebSocket connection fails

1. Ensure backend is running on port 8000
2. Check CORS settings if using different origins
3. Try `ws://127.0.0.1:8000/ws/:id` instead of localhost

### Project won't start

1. Verify project path exists and is accessible
2. Check `ANTHROPIC_API_KEY` is set
3. Look at backend logs for errors

### High memory usage

1. Clear old output from terminal view
2. Limit history entries loaded
3. Close unused project connections

## License

MIT
