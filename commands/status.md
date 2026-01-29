---
description: Legacy alias for /autopilot:altitude (progress/status check)
argument-hint: "[--project=NAME]"
model: sonnet
---

# Autopilot: STATUS (Alias)

**Deprecated:** Use `/autopilot:altitude` for status checks. This alias forwards arguments to `altitude`, which reports progress, cost, and checkpoints.

## Behavior

```
FUNCTION status(args):
    FORWARD to /autopilot:altitude with same args
```

## Examples

```bash
/autopilot:status
/autopilot:status --project=my-api
```

