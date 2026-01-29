# Installation Guide

## Requirements

- Claude Code v2.0.12 or higher
- Run `claude --version` to check

---

## Quick Install

### Option 1: npx (Fastest)

```bash
npx claude-plugins install @fluxlabs/project-autopilot/autopilot
```

Done! ✅

### Option 2: Claude Code Commands

```bash
# Add marketplace
/plugin marketplace add fluxlabs/project-autopilot

# Install plugin
/plugin install autopilot
```

Done! ✅

### Option 3: Interactive Menu

```bash
/plugin
```

Use `Tab` to navigate:
1. **Marketplaces** → Add → `fluxlabs/project-autopilot`
2. **Discover** → Select **autopilot** → Install

---

## Verify Installation

```bash
/autopilot:help
```

You should see the help menu with all available commands.

---

## First Use

```bash
# 1. Initialize global settings (optional but recommended)
/autopilot:config

# 2. Scan your project
/autopilot:scan

# 3. Build with budget
/autopilot:build user auth --max-cost=20

# 4. Check progress
/autopilot:status

# 5. Resume if needed
/autopilot:resume
```

---

## Global State Setup

Autopilot stores settings and history for cross-session persistence.

### Storage Location

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.claude/autopilot/` |
| Windows | `%USERPROFILE%\.claude\autopilot\` |

### Automatic Setup

The global directory is created automatically on first use of:
- `/autopilot:build`
- `/autopilot:config`

### Manual Setup (Optional)

**macOS/Linux:**
```bash
mkdir -p ~/.claude/autopilot
/autopilot:config
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\autopilot"
```

**Windows (Command Prompt):**
```cmd
mkdir "%USERPROFILE%\.claude\autopilot"
```

Then run `/autopilot:config` to initialize.

### What Gets Stored

```
{autopilot-dir}/
├── config.json        # Your default thresholds and preferences
├── history.json       # All projects built (for resume from anywhere)
├── learnings.json     # Patterns for better estimates
└── statistics.json    # Aggregate stats across projects
```

### Set Your Defaults

Configure once, apply to all projects:

```bash
# Set default budget
/autopilot:config --set max-cost=100

# Set warning threshold
/autopilot:config --set warn-cost=20

# View current config
/autopilot:config
```

---

## Managing the Plugin

### Update

```bash
/plugin update autopilot
```

### Disable / Enable

```bash
/plugin disable autopilot
/plugin enable autopilot
```

### Uninstall

```bash
/plugin uninstall autopilot
```

### View Errors

```bash
/plugin errors
```

---

## Scope Options

| Scope | Description | Flag |
|-------|-------------|------|
| `user` | All projects (default) | `--scope user` |
| `project` | Current project only | `--scope project` |

### Project-Only Install

```bash
/plugin install autopilot --scope project
```

---

## Troubleshooting

### "Plugin not found"

Add the marketplace first:

```bash
/plugin marketplace add fluxlabs/project-autopilot
```

### Commands not working after install

1. Restart Claude Code
2. Run `/plugin errors`
3. Run `/help` to see available commands

### Global state permission error

**macOS/Linux:**
```bash
mkdir -p ~/.claude/autopilot
chmod 755 ~/.claude/autopilot
ls -la ~/.claude/autopilot
```

**Windows (PowerShell as Admin):**
```powershell
$dir = "$env:USERPROFILE\.claude\autopilot"
New-Item -ItemType Directory -Force -Path $dir
Get-Acl $dir
```

### Reset global state

If global state is corrupted:

**macOS/Linux:**
```bash
mv ~/.claude/autopilot ~/.claude/autopilot.backup
/autopilot:config
```

**Windows (PowerShell):**
```powershell
Rename-Item "$env:USERPROFILE\.claude\autopilot" "autopilot.backup"
```

Or reset specific files via command:

```bash
/autopilot:config --reset           # Reset config only
/autopilot:config --reset-history   # Reset history only
/autopilot:config --reset-all       # Reset everything
```

### Update marketplace catalog

```bash
/plugin
```

→ **Marketplaces** → **fluxlabs/project-autopilot** → **Update**

---

## Alternative: Full GitHub URL

```bash
/plugin marketplace add https://github.com/fluxlabs/project-autopilot
/plugin install autopilot
```

---

## Support

- **GitHub:** https://github.com/fluxlabs/project-autopilot
- **Issues:** https://github.com/fluxlabs/project-autopilot/issues
- **Help:** `/autopilot:help`
