---
description: View and manage global Autopilot configuration, history, and learnings.
argument-hint: [--set key=value] [--history] [--learnings] [--stats] [--reset]
model: haiku
---

# Autopilot: CONFIG Mode

Manage global Autopilot settings that persist across Claude Code sessions.

## Required Skills

**Read before operations:**
- `/autopilot/skills/global-state/SKILL.md` - File schemas and operations

## Required Agents

- `history-tracker` - For history and statistics operations

---

## Usage

```bash
# View current config
/autopilot:config

# Set a default value
/autopilot:config --set max-cost=75
/autopilot:config --set warn-cost=15
/autopilot:config --set preferred-model=haiku
/autopilot:config --set auto-approve=true

# View project history
/autopilot:config --history
/autopilot:config --history --limit=10

# View learnings
/autopilot:config --learnings

# View statistics
/autopilot:config --stats

# Export all data
/autopilot:config --export

# Reset to defaults
/autopilot:config --reset
/autopilot:config --reset-history
/autopilot:config --reset-learnings
```

---

## Options

### Configuration

| Option | Description |
|--------|-------------|
| `--set key=value` | Set a configuration value |
| `--reset` | Reset config to defaults (keeps history) |
| `--reset-all` | Reset everything (requires confirmation) |

### View Data

| Option | Description |
|--------|-------------|
| `--history` | Show project history |
| `--learnings` | Show extracted learnings |
| `--stats` | Show aggregate statistics |
| `--export` | Export all data to JSON |

### Filters

| Option | Description |
|--------|-------------|
| `--limit=N` | Limit history to N entries |
| `--since=DATE` | Show history since date |
| `--tech=STACK` | Filter by tech stack |

---

## Configurable Values

### Cost Thresholds

| Key | Default | Description |
|-----|---------|-------------|
| `max-cost` | 50 | Hard stop threshold ($) |
| `warn-cost` | 10 | Warning threshold ($) |
| `alert-cost` | 25 | Pause/confirm threshold ($) |

### Token Thresholds

| Key | Default | Description |
|-----|---------|-------------|
| `max-tokens` | 2000000 | Hard stop threshold |
| `warn-tokens` | 500000 | Warning threshold |
| `alert-tokens` | 1000000 | Pause threshold |

### Preferences

| Key | Default | Description |
|-----|---------|-------------|
| `preferred-model` | sonnet | Default model (haiku/sonnet/opus) |
| `auto-approve` | false | Skip approval prompts |
| `verbose-output` | false | Detailed logging |
| `compact-status` | false | Minimal status display |

---

## Behavior

### No Arguments - Show Config

```bash
/autopilot:config
```

Output:

```markdown
# Autopilot Configuration

**Location:** ~/.claude/autopilot/ (macOS/Linux)
**Location:** %USERPROFILE%\.claude\autopilot\ (Windows)

## Current Settings

### Cost Thresholds
| Setting | Value |
|---------|-------|
| Warning | $10.00 |
| Alert | $25.00 |
| Maximum | $50.00 |

### Token Thresholds
| Setting | Value |
|---------|-------|
| Warning | 500K |
| Alert | 1M |
| Maximum | 2M |

### Preferences
| Setting | Value |
|---------|-------|
| Preferred Model | sonnet |
| Auto Approve | false |
| Verbose Output | false |
| Compact Status | false |

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Projects Built | 12 |
| Total Spent | $45.23 |
| Avg per Project | $3.77 |
| Estimate Accuracy | 94% |

---

## Commands

```bash
# Modify settings
/autopilot:config --set max-cost=100

# View history
/autopilot:config --history

# View learnings
/autopilot:config --learnings
```
```

### --set key=value

Set a configuration value:

```bash
/autopilot:config --set max-cost=100
```

Output:

```markdown
## Config Updated

**Changed:** `max-cost`
**From:** $50.00
**To:** $100.00

Current thresholds:
- Warning: $10.00
- Alert: $25.00
- Maximum: **$100.00** (updated)
```

Multiple values:

```bash
/autopilot:config --set max-cost=100 --set warn-cost=20 --set alert-cost=50
```

### --history

Show project history:

```markdown
# Project History

**Total Projects:** 12 | **Success Rate:** 92%

## Recent Projects

| # | Project | Status | Phases | Cost | Variance | Date |
|---|---------|--------|--------|------|----------|------|
| 1 | user-auth | ✅ Done | 8/8 | $4.85 | -7% 🟢 | Jan 25 |
| 2 | api-gateway | ✅ Done | 10/10 | $9.12 | +7% ✅ | Jan 22 |
| 3 | cli-tool | 🔄 Paused | 3/6 | $1.45 | - | Jan 20 |
| 4 | web-dashboard | ✅ Done | 12/12 | $11.50 | +15% ✅ | Jan 18 |
| 5 | data-pipeline | ✅ Done | 6/6 | $3.20 | -12% 🟢 | Jan 15 |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Spent | $45.23 |
| Avg per Project | $3.77 |
| Best Estimate | data-pipeline (-12%) |
| Worst Estimate | web-dashboard (+15%) |

---

## Resumable Projects

| Project | Progress | Remaining |
|---------|----------|-----------|
| cli-tool | 50% | ~$1.55 |

**Resume:** `/autopilot:resume --project=cli-tool`
```

### --learnings

Show extracted learnings:

```markdown
# Autopilot Learnings

**Projects Analyzed:** 12 | **Patterns Found:** 5

## Estimation Accuracy by Phase

| Phase Type | Avg Variance | Samples | Confidence |
|------------|--------------|---------|------------|
| Setup | -15% 🟢 | 12 | High |
| Database | +8% ✅ | 10 | High |
| Auth | +12% ✅ | 8 | Medium |
| API | +5% ✅ | 15 | High |
| Frontend | +18% ✅ | 9 | Medium |
| Testing | -5% 🟢 | 11 | High |

**Overall Accuracy:** 94% | **Trend:** Improving (+2.3%)

---

## Tech Stack Insights

### node-typescript-postgres (5 projects)

| Phase | Avg Cost | Typical Duration |
|-------|----------|------------------|
| Setup | $0.12 | 10 min |
| Database | $0.35 | 25 min |
| Auth | $0.38 | 30 min |
| API | $0.85 | 45 min |

**Common Dependencies:** express, prisma, jest
**Tips:**
- Always add input validation early
- Tests save time on later phases

### react-nextjs (3 projects)

| Phase | Avg Cost |
|-------|----------|
| Setup | $0.15 |
| Components | $0.65 |
| Pages | $0.80 |
| API Routes | $0.45 |

---

## Common Patterns

| Pattern | Phases | Avg Cost | Avg Time |
|---------|--------|----------|----------|
| API with Auth | 5 | $3.50 | 4h |
| Full Stack App | 8 | $8.00 | 8h |
| CLI Tool | 4 | $2.00 | 2h |

---

## Error Patterns

| Error | Frequency | Prevention |
|-------|-----------|------------|
| Missing env vars | 15x | Add .env.example in setup |
| Type errors | 12x | Strict TS config early |
| Test failures | 8x | Write tests with implementation |
```

### --stats

Show aggregate statistics:

```markdown
# Autopilot Statistics

**Since:** January 1, 2026 | **Last Project:** January 25, 2026

## Totals

| Metric | Value |
|--------|-------|
| Projects | 12 |
| Successful | 11 (92%) |
| Failed | 1 (8%) |
| Phases | 87 |
| Tasks | 523 |

## Costs

| Metric | Value |
|--------|-------|
| Total Spent | $45.23 |
| Average per Project | $3.77 |
| Average per Phase | $0.52 |
| Highest Project | $11.50 (web-dashboard) |
| Lowest Project | $1.20 (config-tool) |

## Tokens

| Metric | Value |
|--------|-------|
| Total Input | 12.5M |
| Total Output | 4.8M |
| Avg per Project | 1.4M |

## Accuracy

| Metric | Value |
|--------|-------|
| Overall Accuracy | 94% |
| Best Phase Type | Setup (85% accuracy) |
| Worst Phase Type | Frontend (82% accuracy) |
| Improvement Trend | +2.3% per month |

## Visual

```
Projects:  ████████████ 12
Success:   ███████████░ 92%
Accuracy:  █████████░░░ 94%
```
```

### --export

Export all data:

```bash
/autopilot:config --export
```

Creates `~/.claude/autopilot/export-YYYY-MM-DD.json` with all config, history, learnings, and statistics.

### --reset

Reset configuration to defaults:

```bash
/autopilot:config --reset
```

Output:

```markdown
## Config Reset

Configuration reset to defaults.

**Note:** Project history and learnings are preserved.

To also reset history: `/autopilot:config --reset-history`
To reset everything: `/autopilot:config --reset-all`
```

---

## Global State Initialization

If the global directory doesn't exist, it's created automatically:

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.claude/autopilot/` |
| Windows | `%USERPROFILE%\.claude\autopilot\` |

```markdown
## First Time Setup

Creating global Autopilot state...

**Location:** {platform-specific-path}

**Created:**
- ✅ config.json (default settings)
- ✅ history.json (empty)
- ✅ learnings.json (empty)
- ✅ statistics.json (empty)

Your settings and project history will now persist across sessions.

**View config:** `/autopilot:config`
**Start building:** `/autopilot:build [description]`
```

---

## Error Handling

### Permission Error

```markdown
## Error: Cannot Access Global State

**Error:** Permission denied

**Fix (macOS/Linux):**
```bash
mkdir -p ~/.claude/autopilot
chmod 755 ~/.claude/autopilot
```

**Fix (Windows PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\autopilot"
```

Then retry: `/autopilot:config`
```

### Corrupted File

```markdown
## Warning: Corrupted Config File

**File:** ~/.claude/autopilot/config.json
**Issue:** Invalid JSON

**Action:**
- Backed up to: config.json.backup.2026-01-25
- Created fresh default config

Your settings have been reset. History and learnings are unaffected.
```

---

## Tips

```markdown
## Pro Tips

1. **Set your budget once:**
   ```bash
   /autopilot:config --set max-cost=100
   ```
   All future builds will use this limit.

2. **Check before big projects:**
   ```bash
   /autopilot:config --history --tech=react
   ```
   See what similar projects cost.

3. **Learn from history:**
   ```bash
   /autopilot:config --learnings
   ```
   Use historical data to improve estimates.

4. **Export periodically:**
   ```bash
   /autopilot:config --export
   ```
   Backup your learnings and history.
```

$ARGUMENTS
