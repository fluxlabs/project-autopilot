---
description: Sync project state with external project management tools
argument-hint: "[--provider=jira|linear|notion|github] [--import] [--export] [--two-way]"
model: haiku
---

# Autopilot: SYNC Mode
# Project Autopilot - External tool synchronization
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Synchronize project state with external project management tools.

## Required Skills

**Read before syncing:**
1. `/autopilot/skills/global-state/SKILL.md` - Project state

## Required Agents

- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--provider=prov` | Tool: jira, linear, notion, github, trello |
| `--import` | Import from external tool |
| `--export` | Export to external tool |
| `--two-way` | Bidirectional sync |
| `--dry-run` | Preview sync without changes |
| `--project=id` | Specific project/board ID |

---

## Supported Providers

| Provider | Features | Auth |
|----------|----------|------|
| Jira | Issues, sprints, epics | API token |
| Linear | Issues, projects, cycles | API key |
| Notion | Databases, pages | Integration |
| GitHub | Issues, projects, milestones | Token |
| Trello | Cards, boards, lists | API key |

---

## Usage

### Export to Linear

```bash
/autopilot:sync --provider=linear --export
```

Output:
```markdown
## Sync Export: Linear

### Connection
✅ Connected to Linear workspace: My Team
✅ Project found: my-saas-app

### Changes to Export

| Type | Local | Linear | Action |
|------|-------|--------|--------|
| Phase 5 | In Progress | Not found | Create |
| Task 5.1 | Complete | Open | Update |
| Task 5.2 | In Progress | Not found | Create |
| Task 5.3 | Pending | Not found | Create |

### Mapping

**Phases → Linear Cycles**
| Phase | Cycle | Status |
|-------|-------|--------|
| Phase 4 | Sprint 11 | ✅ Synced |
| Phase 5 | Sprint 12 | 🆕 Create |

**Tasks → Linear Issues**
| Task | Issue | Status |
|------|-------|--------|
| 5.1 Dashboard layout | - | 🆕 Create |
| 5.2 API integration | - | 🆕 Create |
| 5.3 User settings | - | 🆕 Create |

### Preview

**Will create:**
- 1 cycle (Phase 5 → Sprint 12)
- 3 issues (Tasks 5.1, 5.2, 5.3)

**Will update:**
- 0 issues

**Execute sync? (y/n)**
```

### Import from Jira

```bash
/autopilot:sync --provider=jira --import
```

Output:
```markdown
## Sync Import: Jira

### Connection
✅ Connected to Jira: mycompany.atlassian.net
✅ Project: SAAS (my-saas-app)

### Changes to Import

| Type | Jira | Local | Action |
|------|------|-------|--------|
| Sprint 12 | Active | Phase 5 | Merge |
| SAAS-145 | Done | Task 5.1 (In Progress) | Update |
| SAAS-146 | In Progress | Not found | Create |
| SAAS-147 | To Do | Not found | Create |

### Conflict Resolution

**Task 5.1 Status Conflict**
- Local: In Progress
- Jira: Done (updated 2h ago)
- **Resolution:** Use Jira (more recent)

### Will Apply

**Updates:**
- Task 5.1: In Progress → Complete

**Creates:**
- Task 5.6: SAAS-146 "Add export feature"
- Task 5.7: SAAS-147 "Fix mobile layout"

**Execute import? (y/n)**
```

### Two-Way Sync

```bash
/autopilot:sync --provider=linear --two-way
```

Output:
```markdown
## Two-Way Sync: Linear

### Sync Status

| Direction | Changes |
|-----------|---------|
| Local → Linear | 3 |
| Linear → Local | 2 |
| Conflicts | 1 |

### Outgoing (Local → Linear)

| Task | Status Change |
|------|---------------|
| 5.1 | Complete (was: In Progress) |
| 5.2 | In Progress (new) |
| 5.3 | Pending (new) |

### Incoming (Linear → Local)

| Issue | Change |
|-------|--------|
| PRJ-45 | Priority: High → Critical |
| PRJ-46 | New issue: "Bug fix needed" |

### Conflict

**Task 5.4 / PRJ-47**
| Field | Local | Linear |
|-------|-------|--------|
| Status | Complete | In Review |
| Updated | Jan 29 14:00 | Jan 29 14:30 |

**Resolution Options:**
1. Use Linear (more recent)
2. Use Local
3. Manual merge

**Select resolution (1/2/3):** 1

---

### Summary

| Action | Count |
|--------|-------|
| Create (Linear) | 2 |
| Update (Linear) | 1 |
| Create (Local) | 1 |
| Update (Local) | 1 |

**Execute two-way sync? (y/n)**
```

### Dry Run

```bash
/autopilot:sync --provider=github --export --dry-run
```

Output:
```markdown
## Sync Preview (Dry Run): GitHub

### Would Create

**Milestone: Phase 5 - Frontend Integration**
```yaml
title: "Phase 5: Frontend Integration"
due_on: "2026-02-05"
description: "Frontend components and API integration"
```

**Issues:**
| Title | Labels | Assignees |
|-------|--------|-----------|
| Dashboard layout component | frontend, phase-5 | - |
| API service integration | frontend, api | - |
| User settings page | frontend, phase-5 | - |

### Would Update

| Issue | Field | From | To |
|-------|-------|------|-----|
| #45 | state | open | closed |
| #46 | labels | - | +completed |

### No changes made (dry run)
```

---

## Behavior

```
FUNCTION sync(options):

    # 1. Connect to provider
    provider = connectProvider(options.provider)

    IF NOT provider.connected:
        ERROR "Failed to connect to {options.provider}"
        RETURN

    # 2. Load local state
    localState = loadProjectState()

    # 3. Load remote state
    remoteState = provider.getState(options.autopilot)

    # 4. Calculate diff
    IF options.export:
        changes = diffLocalToRemote(localState, remoteState)
    ELIF options.import:
        changes = diffRemoteToLocal(remoteState, localState)
    ELIF options.twoWay:
        changes = diffBidirectional(localState, remoteState)

    # 5. Resolve conflicts
    IF changes.conflicts.length > 0:
        resolved = resolveConflicts(changes.conflicts)
        changes = applyResolutions(changes, resolved)

    # 6. Preview changes
    DISPLAY syncPreview(changes)

    # 7. Dry run check
    IF options.dryRun:
        LOG "Dry run complete - no changes made"
        RETURN

    # 8. Execute sync
    IF confirm():
        IF options.export OR options.twoWay:
            provider.applyChanges(changes.outgoing)

        IF options.import OR options.twoWay:
            applyLocalChanges(changes.incoming)

        DISPLAY syncComplete(changes)
```

---

## Provider Configuration

### Setup

```bash
# Configure provider credentials
/autopilot:config --set linear.apiKey=lin_api_xxx
/autopilot:config --set jira.baseUrl=mycompany.atlassian.net
/autopilot:config --set jira.email=user@example.com
/autopilot:config --set jira.apiToken=xxx
```

### Mapping Configuration

```json
{
  "sync": {
    "linear": {
      "projectId": "PRJ-xxx",
      "mapping": {
        "phases": "cycles",
        "tasks": "issues",
        "status": {
          "pending": "Todo",
          "in_progress": "In Progress",
          "complete": "Done"
        }
      }
    }
  }
}
```

---

## Quick Examples

```bash
# Export to Linear
/autopilot:sync --provider=linear --export

# Import from Jira
/autopilot:sync --provider=jira --import

# Two-way sync with GitHub
/autopilot:sync --provider=github --two-way

# Preview without changes
/autopilot:sync --provider=notion --export --dry-run

# Specific project
/autopilot:sync --provider=linear --project=PRJ-123 --export
```

$ARGUMENTS
