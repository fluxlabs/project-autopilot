---
description: Revert to a previous phase checkpoint
argument-hint: "<phase> [--hard] [--dry-run] [--list]"
model: sonnet
---

# Autopilot: ROLLBACK Mode
# Project Autopilot - Phase checkpoint recovery
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Revert project state to a previous phase checkpoint while preserving learnings and history.

## Required Skills

**Read before rolling back:**
1. `/autopilot/skills/rollback-protocol/SKILL.md` - Checkpoint and recovery procedures
2. `/autopilot/skills/git-workflow/SKILL.md` - Git operations

## Required Agents

- `validator` - Verify state before and after rollback

---

## Options

| Option | Description |
|--------|-------------|
| `<phase>` | Target phase number to rollback to |
| `--hard` | Force rollback (skip confirmation) |
| `--dry-run` | Show what would change without executing |
| `--list` | List available checkpoints |
| `--preserve-learnings` | Keep learnings.md (default: true) |
| `--preserve-branch` | Create backup branch before rollback |

---

## Behavior

### List Checkpoints (--list)

```bash
/autopilot:rollback --list
```

Output:
```markdown
## Available Checkpoints

| Phase | Tag | Date | Description | Files Changed |
|-------|-----|------|-------------|---------------|
| 004 | autopilot/phase-004-complete | 2h ago | API Layer complete | 12 files |
| 003 | autopilot/phase-003-complete | 5h ago | Auth complete | 8 files |
| 002 | autopilot/phase-002-complete | 8h ago | Database complete | 5 files |
| 001 | autopilot/phase-001-complete | 12h ago | Setup complete | 15 files |

**Current position:** Phase 005, Task 005.3

**Usage:**
```bash
# Rollback to end of phase 003
/autopilot:rollback 003

# Preview changes first
/autopilot:rollback 003 --dry-run
```
```

### Dry Run (--dry-run)

```bash
/autopilot:rollback 003 --dry-run
```

Output:
```markdown
## Rollback Preview: Phase 003

**Current position:** Phase 005, Task 005.3
**Target:** Phase 003 complete
**Tag:** autopilot/phase-003-complete

### Changes to Revert

**Files modified since Phase 003:**
| File | Action | Lines Changed |
|------|--------|---------------|
| src/services/order.ts | Created | +245 |
| src/services/payment.ts | Created | +312 |
| src/routes/api/orders.ts | Created | +89 |
| src/routes/api/payments.ts | Created | +76 |
| src/models/order.ts | Created | +45 |
| tests/orders.test.ts | Created | +156 |
| src/lib/db.ts | Modified | +23, -5 |

**Commits to revert:** 8 commits

### State Changes

| Item | Current | After Rollback |
|------|---------|----------------|
| Phase | 005 | 003 |
| Task | 005.3 | 003.8 |
| Cost spent | $4.85 | $2.15 |

### Preserved
- ✅ learnings.md (insights kept)
- ✅ Global history (record maintained)
- ✅ Estimation accuracy data

**No changes made (dry run)**

To execute: `/autopilot:rollback 003`
```

### Execute Rollback

```bash
/autopilot:rollback 003
```

Flow:
```markdown
## Rollback: Phase 003

**Target:** autopilot/phase-003-complete
**Method:** Git checkout + state reset

### Confirmation Required

This will:
1. Create backup branch: `autopilot-backup-20260129-1430`
2. Revert 8 commits (changes in phases 004-005)
3. Reset STATE.md to phase 003 position
4. Clear phase files for 004, 005
5. Preserve learnings.md

**Files to be reverted:** 7
**Commits to undo:** 8
**Cost data:** $2.70 will be marked as "rolled back"

Type 'confirm' to proceed, or 'cancel' to abort:
```

After confirmation:
```markdown
## Rollback Complete

✅ Backup created: autopilot-backup-20260129-1430
✅ Reverted to: autopilot/phase-003-complete
✅ STATE.md updated
✅ Phase files cleaned
✅ Learnings preserved

### New State
| Item | Value |
|------|-------|
| Phase | 003 (complete) |
| Next task | 004.1 |
| Budget spent | $2.15 |
| Budget remaining | $47.85 |

### Resume
```bash
/autopilot:cockpit  # Continue from phase 004
```

### Recover if needed
```bash
# View backup branch
git log autopilot-backup-20260129-1430

# Restore backup (if rollback was wrong)
git checkout autopilot-backup-20260129-1430
```
```

---

## Rollback Protocol

```
FUNCTION rollback(targetPhase, options):

    # 1. Validate target checkpoint exists
    checkpointTag = "autopilot/phase-{targetPhase}-complete"
    IF NOT git.tagExists(checkpointTag):
        ERROR "Checkpoint not found: {checkpointTag}"
        SHOW "Run /autopilot:rollback --list to see available checkpoints"
        RETURN

    # 2. Dry run preview
    IF options.dryRun:
        preview = generatePreview(checkpointTag)
        DISPLAY preview
        RETURN

    # 3. Show confirmation (unless --hard)
    IF NOT options.hard:
        changes = calculateChanges(checkpointTag)
        DISPLAY confirmationPrompt(changes)
        response = WAIT for user input
        IF response != "confirm":
            LOG "Rollback cancelled"
            RETURN

    # 4. Create backup branch
    IF options.preserveBranch OR true:  # Default on
        backupBranch = "autopilot-backup-{timestamp}"
        git.branch(backupBranch)
        LOG "✅ Backup created: {backupBranch}"

    # 5. Preserve learnings (unless disabled)
    IF options.preserveLearnings OR true:  # Default on
        learnings = readFile(".autopilot/learnings.md")

    # 6. Execute git rollback
    git.checkout(checkpointTag)
    LOG "✅ Reverted to: {checkpointTag}"

    # 7. Restore learnings
    IF learnings:
        writeFile(".autopilot/learnings.md", learnings)

    # 8. Update STATE.md
    updateState({
        currentPhase: targetPhase,
        status: "complete",
        rollbackFrom: previousPhase,
        rollbackTime: now()
    })
    LOG "✅ STATE.md updated"

    # 9. Clean up phase files beyond target
    cleanPhaseFiles(targetPhase + 1, maxPhase)
    LOG "✅ Phase files cleaned"

    # 10. Update global history
    SPAWN history-tracker → recordRollback({
        projectId: projectId,
        fromPhase: previousPhase,
        toPhase: targetPhase,
        reason: "user_initiated"
    })

    # 11. Display summary
    DISPLAY rollbackSummary()
```

---

## Checkpoint Tags

Checkpoints are created automatically at phase boundaries:

| Event | Tag Format | Example |
|-------|------------|---------|
| Phase complete | `autopilot/phase-XXX-complete` | `autopilot/phase-003-complete` |
| Manual checkpoint | `autopilot/checkpoint-YYYYMMDD-HHMM` | `autopilot/checkpoint-20260129-1430` |

### Creating Manual Checkpoints

```bash
# Create checkpoint at current state
git tag -a "autopilot/checkpoint-$(date +%Y%m%d-%H%M)" -m "Manual checkpoint"
```

---

## Error Handling

### Checkpoint Not Found

```markdown
## Error: Checkpoint Not Found

No checkpoint found for phase 007.

**Available checkpoints:**
- Phase 001: autopilot/phase-001-complete
- Phase 002: autopilot/phase-002-complete
- Phase 003: autopilot/phase-003-complete

**Tip:** Checkpoints are created when phases complete successfully.
If a phase is in progress, it won't have a checkpoint yet.
```

### Uncommitted Changes

```markdown
## Error: Uncommitted Changes

Cannot rollback with uncommitted changes.

**Uncommitted files:**
- src/services/user.ts (modified)
- src/routes/api/users.ts (modified)

**Options:**
1. Commit changes: `git commit -am "WIP before rollback"`
2. Stash changes: `git stash`
3. Discard changes: `git checkout -- .` (⚠️ destructive)
```

### Merge Conflicts

```markdown
## Error: Merge Conflicts

Rollback resulted in merge conflicts.

**Conflicted files:**
- src/lib/config.ts

**Options:**
1. Resolve conflicts manually, then:
   ```bash
   git add .
   git commit -m "Resolved rollback conflicts"
   ```

2. Abort rollback:
   ```bash
   git checkout autopilot-backup-20260129-1430
   ```
```

---

## Integration with Resume

After rollback, resume continues from the new position:

```bash
# Rollback to phase 003
/autopilot:rollback 003

# Resume from phase 004
/autopilot:cockpit
```

STATE.md is automatically updated to reflect the new starting position.

---

## Quick Start Examples

```bash
# List available checkpoints
/autopilot:rollback --list

# Preview rollback to phase 002
/autopilot:rollback 002 --dry-run

# Execute rollback to phase 002
/autopilot:rollback 002

# Force rollback (skip confirmation)
/autopilot:rollback 002 --hard

# Rollback but don't preserve learnings
/autopilot:rollback 002 --preserve-learnings=false
```

$ARGUMENTS
