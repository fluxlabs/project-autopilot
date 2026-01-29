---
description: Legacy alias for /autopilot:takeoff (executes or auto-plans a project)
argument-hint: "[feature description] [--max-cost=N] [--yes]"
model: sonnet
---

# Autopilot: BUILD (Alias)

**Deprecated:** Use `/autopilot:takeoff` going forward. This command is kept for backward compatibility and simply delegates to `takeoff`, which will auto-run `/autopilot:flightplan` if no plan exists.

## Behavior

```
FUNCTION build(args):
    FORWARD to /autopilot:takeoff with same args
```

## Examples

```bash
/autopilot:build "user auth" -y            # executes immediately
/autopilot:build --max-cost=25             # enforces budget limits
```

