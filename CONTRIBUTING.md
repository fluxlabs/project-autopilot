# Contributing to Project Autopilot
# Project Autopilot
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Thank you for your interest in contributing to Project Autopilot!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature-name`

## Project Structure

```
project-autopilot/
├── agents/          # 31 specialized AI agents
├── commands/        # 40 slash commands
├── skills/          # 36 reusable skills
├── templates/       # Project scaffolding templates
├── mcp-server/      # MCP server integration
└── scripts/         # Automation scripts
```

## Development Guidelines

### Adding a New Agent

1. Create `agents/your-agent.md` following the template pattern
2. Include required sections:
   - YAML frontmatter with `name`, `description`, `model`
   - Copyright header
   - `## Required Skills` section
   - `## Core Principles` section

### Adding a New Skill

1. Create `skills/your-skill/SKILL.md`
2. Include YAML frontmatter with `name` and `description`
3. Add copyright header

### Adding a New Command

1. Create `commands/your-command.md`
2. Include YAML frontmatter with `description`
3. Add copyright header

## Code Style

- Use kebab-case for file names
- Include copyright headers in all files
- Follow existing patterns in similar files

## Testing

Before submitting:

1. Validate JSON files: `python3 -c "import json; json.load(open('file.json'))"`
2. Check shell scripts: `bash -n script.sh`
3. Check Python syntax: `python3 -m py_compile script.py`

## Pull Requests

1. Keep PRs focused on a single change
2. Update documentation as needed
3. Include a clear description of changes

## Questions?

Open an issue for questions or suggestions.
