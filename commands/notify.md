---
description: Configure notification webhooks
argument-hint: "[--add provider=url] [--remove provider] [--test] [--list] [--events]"
model: haiku
---

# Autopilot: NOTIFY Mode
# Project Autopilot - Notification webhook configuration
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Configure webhook notifications for project events like phase completion, budget alerts, and build status.

## Required Skills

**Read before configuring:**
1. `/autopilot/skills/notifications/SKILL.md` - Webhook schemas and providers
2. `/autopilot/skills/global-state/SKILL.md` - Configuration storage

## Required Agents

- `notifier` - Dispatch notifications

---

## Options

| Option | Description |
|--------|-------------|
| `--add provider=url` | Add webhook for provider |
| `--remove provider` | Remove webhook |
| `--test [provider]` | Send test notification |
| `--list` | List configured webhooks |
| `--events` | List available events |
| `--enable event` | Enable event notifications |
| `--disable event` | Disable event notifications |

---

## Supported Providers

| Provider | Format | Features |
|----------|--------|----------|
| `slack` | Slack Incoming Webhook | Rich formatting, attachments |
| `discord` | Discord Webhook | Embeds, mentions |
| `teams` | Microsoft Teams | Adaptive cards |
| `webhook` | Generic HTTP POST | Custom payload |
| `email` | SendGrid/Mailgun API | Email notifications |

---

## Usage

### Add Webhook

```bash
# Slack
/autopilot:notify --add slack=https://hooks.slack.com/services/T00/B00/xxx

# Discord
/autopilot:notify --add discord=https://discord.com/api/webhooks/xxx/yyy

# Microsoft Teams
/autopilot:notify --add teams=https://outlook.office.com/webhook/xxx

# Generic webhook
/autopilot:notify --add webhook=https://example.com/webhook
```

Output:
```markdown
## Webhook Added

**Provider:** Slack
**URL:** https://hooks.slack.com/services/T00/B00/xxx (masked)
**Status:** ✅ Verified

### Enabled Events
- ✅ phase_complete
- ✅ build_complete
- ✅ budget_alert
- ✅ build_failed

Send a test notification?
```bash
/autopilot:notify --test slack
```
```

### List Webhooks

```bash
/autopilot:notify --list
```

Output:
```markdown
## Configured Webhooks

| Provider | URL | Events | Status |
|----------|-----|--------|--------|
| slack | ...xxx | 4 | ✅ Active |
| discord | ...yyy | 3 | ✅ Active |

### Event Configuration

| Event | Slack | Discord |
|-------|-------|---------|
| phase_complete | ✅ | ✅ |
| build_complete | ✅ | ✅ |
| budget_alert | ✅ | ❌ |
| build_failed | ✅ | ✅ |
| checkpoint_created | ❌ | ❌ |

### Manage
```bash
# Test a provider
/autopilot:notify --test slack

# Remove a provider
/autopilot:notify --remove discord

# Enable event for provider
/autopilot:notify --enable budget_alert --provider=discord
```
```

### Test Notification

```bash
/autopilot:notify --test slack
```

Output:
```markdown
## Test Notification Sent

**Provider:** Slack
**Status:** ✅ Delivered

### Payload Sent
```json
{
  "text": "🧪 Autopilot Test Notification",
  "attachments": [{
    "color": "#36a64f",
    "text": "This is a test from Autopilot",
    "footer": "Project: my-project",
    "ts": 1706540400
  }]
}
```

Check your Slack channel for the message.
```

### List Events

```bash
/autopilot:notify --events
```

Output:
```markdown
## Available Notification Events

| Event | Trigger | Default |
|-------|---------|---------|
| `phase_start` | Phase execution begins | Off |
| `phase_complete` | Phase passes quality gate | **On** |
| `build_complete` | All phases finish | **On** |
| `build_failed` | Build or test failure | **On** |
| `budget_warning` | Cost reaches warn threshold | **On** |
| `budget_alert` | Cost reaches alert threshold | **On** |
| `budget_exceeded` | Cost exceeds max | **On** |
| `checkpoint_created` | Checkpoint saved | Off |
| `rollback` | Rollback executed | **On** |

### Enable/Disable Events

```bash
# Enable an event
/autopilot:notify --enable checkpoint_created

# Disable an event
/autopilot:notify --disable phase_start

# For specific provider
/autopilot:notify --enable budget_warning --provider=slack
```
```

### Remove Webhook

```bash
/autopilot:notify --remove discord
```

Output:
```markdown
## Webhook Removed

**Provider:** Discord
**URL:** https://discord.com/api/webhooks/... (removed)

Remaining providers: 1 (slack)
```

---

## Notification Payloads

### Phase Complete (Slack)

```json
{
  "text": "✅ Phase Complete",
  "attachments": [{
    "color": "#36a64f",
    "title": "Phase 003: Authentication",
    "fields": [
      { "title": "Status", "value": "Complete", "short": true },
      { "title": "Cost", "value": "$0.85", "short": true },
      { "title": "Tasks", "value": "8/8", "short": true },
      { "title": "Variance", "value": "+5%", "short": true }
    ],
    "footer": "Project: my-project | Phase 3 of 10",
    "ts": 1706540400
  }]
}
```

### Budget Alert (Slack)

```json
{
  "text": "⚠️ Budget Alert",
  "attachments": [{
    "color": "#ff9900",
    "title": "Budget threshold reached",
    "fields": [
      { "title": "Current Cost", "value": "$25.50", "short": true },
      { "title": "Alert Threshold", "value": "$25.00", "short": true },
      { "title": "Max Budget", "value": "$50.00", "short": true },
      { "title": "Progress", "value": "Phase 5/10", "short": true }
    ],
    "footer": "Project: my-project",
    "ts": 1706540400
  }]
}
```

### Build Failed (Discord)

```json
{
  "embeds": [{
    "title": "❌ Build Failed",
    "color": 15158332,
    "fields": [
      { "name": "Phase", "value": "004: API Layer", "inline": true },
      { "name": "Task", "value": "004.5: Validation", "inline": true },
      { "name": "Error", "value": "Test failure in user.test.ts" }
    ],
    "footer": { "text": "Project: my-project" },
    "timestamp": "2026-01-29T12:00:00Z"
  }]
}
```

---

## Configuration Storage

Notifications are stored in global config:

```json
// ~/.claude/autopilot/config.json
{
  "notifications": {
    "webhooks": {
      "slack": {
        "url": "https://hooks.slack.com/services/...",
        "enabled": true,
        "addedAt": "2026-01-29T00:00:00Z"
      },
      "discord": {
        "url": "https://discord.com/api/webhooks/...",
        "enabled": true,
        "addedAt": "2026-01-29T00:00:00Z"
      }
    },
    "events": {
      "phase_complete": ["slack", "discord"],
      "build_complete": ["slack", "discord"],
      "budget_alert": ["slack"],
      "build_failed": ["slack", "discord"]
    },
    "defaults": {
      "enabled": true,
      "retryOnFailure": true,
      "maxRetries": 3
    }
  }
}
```

---

## Notification Triggers

### Automatic Triggers

Notifications are sent automatically during execution:

```
DURING /autopilot:takeoff OR /autopilot:cockpit:

    ON phase_complete:
        SPAWN notifier → send("phase_complete", phaseData)

    ON budget_threshold_reached:
        SPAWN notifier → send("budget_alert", budgetData)

    ON build_failed:
        SPAWN notifier → send("build_failed", errorData)

    ON all_phases_complete:
        SPAWN notifier → send("build_complete", summaryData)
```

### Manual Triggers

```bash
# Send custom notification
/autopilot:notify --send "Custom message" --provider=slack
```

---

## Error Handling

### Webhook Verification Failed

```markdown
## Error: Webhook Verification Failed

Could not verify webhook URL for Slack.

**Attempted URL:** https://hooks.slack.com/services/...
**Error:** Connection refused

**Troubleshooting:**
1. Verify the URL is correct
2. Check if the webhook is still active in Slack
3. Ensure network connectivity

The webhook was **not** added. Fix the issue and try again.
```

### Delivery Failed

```markdown
## Warning: Notification Delivery Failed

Failed to deliver notification to Discord.

**Event:** phase_complete
**Error:** HTTP 429 (Rate Limited)
**Retry:** Will retry in 60 seconds

Notifications will continue for other providers.
```

---

## Quick Start Examples

```bash
# Add Slack webhook
/autopilot:notify --add slack=https://hooks.slack.com/services/xxx

# Test the webhook
/autopilot:notify --test slack

# See all configured webhooks
/autopilot:notify --list

# Enable budget warnings for Discord
/autopilot:notify --enable budget_warning --provider=discord

# Remove a webhook
/autopilot:notify --remove teams

# List available events
/autopilot:notify --events
```

$ARGUMENTS
