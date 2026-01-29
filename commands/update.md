---
description: Check for and install plugin updates
---

// Project Autopilot - Update Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

<update-check>

## Instructions

Check for updates by comparing installed vs remote version:

1. **Read local version** from the installed plugin's `.claude-plugin/plugin.json`
2. **Fetch remote version** from `https://raw.githubusercontent.com/fluxlabs/project-autopilot/main/.claude-plugin/plugin.json`
3. **Compare versions** and report

### If Update Available

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Update available: v{local} → v{remote}

   Run: /plugin update autopilot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then ask user if they want to update now. If yes, execute:
```bash
# This triggers Claude Code's plugin manager
```

Tell the user to run `/plugin update autopilot` in their terminal.

### If Up to Date

Display:
```
✅ Autopilot v{version} is up to date
```

### If Check Fails

Display:
```
⚠️ Could not check for updates (network issue)
   Current version: v{local}
```

</update-check>
