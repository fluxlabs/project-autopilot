# Autopilot API Orchestrator
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Direct API-based orchestrator for continuous autonomous coding. Bypasses Claude Code CLI for full control over context, checkpointing, and execution.

## Quick Start (Recommended)

Use the simplified launcher from the project root:

```bash
# Start a new task
./autopilot run "Build a REST API with auth"

# Resume from checkpoint
./autopilot resume

# Check status
./autopilot status

# Continuous mode (auto-restarts on context fill)
./autopilot loop "Build a REST API"
```

The launcher auto-detects your API key from:
- `ANTHROPIC_API_KEY` environment variable
- `.env` file in project directory
- `~/.anthropic_key` file
- macOS Keychain (`anthropic-api-key`)

## Why Use This Instead of the Loop Script?

| Aspect | Loop Script | API Orchestrator |
|--------|-------------|------------------|
| Context control | Claude Code manages | You control exactly |
| Restart overhead | Full CLI startup each time | Just new API call |
| Cost tracking | Relies on plugin | Direct from API response |
| Tool execution | Claude Code's tools | Your implementations |
| Customization | Limited | Full control |
| Complexity | Simple bash | Python application |

## Manual Setup (Alternative)

```bash
# Install dependencies
cd scripts/orchestrator
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run
python main.py --project /path/to/project --task "Build a REST API with auth"

# Resume from checkpoint
python main.py --project /path/to/project --resume
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                         │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Context   │  │   Tools     │  │ Checkpoint  │     │
│  │   Manager   │  │   Engine    │  │   Manager   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │  Anthropic │                       │
│                    │    API     │                       │
│                    └───────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## Features

- **Smart context management** - Slides window, preserves critical info
- **Tool execution** - File ops, bash, search built-in
- **Automatic checkpointing** - Never lose progress
- **Cost tracking** - Real-time from API responses
- **Model selection** - Haiku/Sonnet/Opus per task complexity
- **Parallel tool calls** - Execute independent tools concurrently

## Configuration

```yaml
# config.yaml
model: sonnet  # Options: haiku, sonnet, opus
max_tokens: 8192
max_context_tokens: 150000  # Leave buffer from 200K limit
checkpoint_threshold: 0.6   # Checkpoint at 60% context

costs:
  max: 50.0
  warn: 10.0
  alert: 25.0

tools:
  enabled:
    - read_file
    - write_file
    - edit_file
    - bash
    - glob
    - grep
  bash:
    timeout: 120
    allowed_commands: ["git", "npm", "python", "pytest", "make"]
```

## Files

```
orchestrator/
├── main.py              # Entry point
├── orchestrator.py      # Core orchestration logic
├── context.py           # Context window management
├── tools.py             # Tool implementations
├── checkpoint.py        # State persistence
├── costs.py             # Cost tracking
├── config.yaml          # Configuration
└── requirements.txt     # Dependencies
```
