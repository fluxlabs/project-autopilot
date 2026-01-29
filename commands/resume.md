---
description: Legacy alias for /autopilot:cockpit (resume from checkpoint)
argument-hint: "[--task=X.Y] [--phase=N] [--project=NAME]"
model: sonnet
---

# Autopilot: RESUME (Alias)

**Deprecated:** Use `/autopilot:cockpit` instead. This alias keeps older prompts working by forwarding arguments to `cockpit`, which resumes from the last waypoint with validation and cost tracking.

## Behavior

```
FUNCTION resume(args):
    FORWARD to /autopilot:cockpit with same args
```

## Examples

```bash
/autopilot:resume                    # resume current project
/autopilot:resume --project=mobile   # resume named project
/autopilot:resume --task=3.2         # start at specific task
```

