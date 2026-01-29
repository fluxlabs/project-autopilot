---
name: git-workflow
description: Git best practices for commits, branches, and collaboration. Reference this skill for proper version control workflow.
---

// Project Autopilot - Git Best Practices
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Git Workflow Skill

Reference this skill for proper Git practices during development.

---

## Branching Strategy

### Branch Types

```
main (production)
  └── develop (integration)
       ├── feature/[ticket]-description
       ├── bugfix/[ticket]-description
       ├── hotfix/[ticket]-description
       └── release/v1.2.0
```

### Branch Naming

```bash
# Features
feature/AUTH-123-user-login
feature/API-456-payment-endpoint

# Bug fixes
bugfix/BUG-789-null-pointer
bugfix/UI-012-button-alignment

# Hotfixes (production)
hotfix/SEC-999-xss-vulnerability

# Releases
release/v1.2.0
```

---

## Commit Message Format

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting (no code change) |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance |
| `perf` | Performance |
| `ci` | CI/CD changes |
| `build` | Build system |

### Examples

```bash
# Feature
feat(auth): add JWT token refresh endpoint

# Bug fix
fix(api): handle null user in profile endpoint

Fixes #123

# Breaking change
feat(api)!: change response format for users endpoint

BREAKING CHANGE: Response now wraps data in { data: ... }

# Multiple scopes
feat(auth,api): implement OAuth2 flow

# With body
refactor(database): optimize user queries

- Add index on email column
- Use prepared statements
- Remove N+1 query in getUserOrders
```

---

## Commit Rules

### Do
- ✅ One logical change per commit
- ✅ Write in imperative mood ("add" not "added")
- ✅ Keep subject line under 72 characters
- ✅ Reference issue numbers
- ✅ Commit working code only

### Don't
- ❌ Mix unrelated changes
- ❌ Commit broken code
- ❌ Include "WIP" commits in main
- ❌ Commit secrets or credentials
- ❌ Commit generated files

---

## Workflow Commands

### Starting Work

```bash
# Ensure main is current
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/AUTH-123-user-login

# Or from develop
git checkout develop
git pull origin develop
git checkout -b feature/AUTH-123-user-login
```

### During Work

```bash
# Check status
git status

# Stage specific files
git add src/auth/login.ts src/auth/login.test.ts

# Commit
git commit -m "feat(auth): add login endpoint"

# Push to remote
git push -u origin feature/AUTH-123-user-login
```

### Finishing Work

```bash
# Ensure branch is up to date
git fetch origin
git rebase origin/main

# Or merge (if team prefers)
git merge origin/main

# Push final changes
git push origin feature/AUTH-123-user-login

# Create PR via GitHub/GitLab
```

---

## Phase Commits

### Commit Pattern for Phases

```bash
# Phase start (optional)
git commit --allow-empty -m "chore: begin phase 003 - API endpoints"

# Task commits
git commit -m "feat(api): add user CRUD endpoints [003.1]"
git commit -m "feat(api): add order endpoints [003.2]"
git commit -m "test(api): add user endpoint tests [003.3]"

# Phase complete (optional)
git commit --allow-empty -m "chore: complete phase 003 - API endpoints"
```

### Tagging Releases

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0 - User authentication"

# Push tags
git push origin v1.2.0
```

---

## Autopilot Checkpoint Tagging

### Automatic Phase Checkpoints

Autopilot creates checkpoint tags at phase boundaries:

```bash
# Tag format for phase completion
autopilot/phase-001-complete
autopilot/phase-002-complete
autopilot/phase-003-complete

# Tag format for build completion
autopilot/build-complete-v1.0.0

# Manual checkpoint tag
autopilot/checkpoint-20260129-1430
```

### Creating Phase Checkpoints

```bash
# Automatic (done by Autopilot)
git tag -a "autopilot/phase-003-complete" -m "Phase 003: Auth complete

Tasks: 8 completed
Cost: $0.85
Time: 2h 15m
"

# Push checkpoint
git push origin "autopilot/phase-003-complete"
```

### Listing Checkpoints

```bash
# List all Autopilot checkpoints
git tag -l "autopilot/*"

# Show checkpoint details
git show autopilot/phase-003-complete
```

### Rollback Using Checkpoints

```bash
# View files at checkpoint
git show autopilot/phase-002-complete:src/

# Checkout to checkpoint (detached HEAD)
git checkout autopilot/phase-002-complete

# Create branch from checkpoint
git checkout -b rollback-branch autopilot/phase-002-complete
```

### Checkpoint Best Practices

1. **Don't delete checkpoint tags** - They're recovery points
2. **Push checkpoints to remote** - Backup and collaboration
3. **Use annotated tags** - Include metadata (cost, tasks, time)
4. **Create manual checkpoints** before risky operations

---

## Handling Issues

### Fixing a Bad Commit

```bash
# Amend last commit (before push)
git commit --amend -m "fix(auth): correct typo in login function"

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3
```

### Undoing Changes

```bash
# Unstage file
git reset HEAD file.ts

# Discard changes
git checkout -- file.ts

# Revert a commit (creates new commit)
git revert <commit-hash>
```

### Resolving Conflicts

```bash
# During rebase
git status                    # See conflicts
# Edit files to resolve
git add resolved-file.ts
git rebase --continue

# Abort if needed
git rebase --abort
```

---

## PR/MR Guidelines

### PR Title
```
[TICKET-123] feat(auth): implement user login

OR

feat(auth): implement user login (#123)
```

### PR Description Template
```markdown
## Summary
Brief description of changes

## Changes
- Added login endpoint
- Added JWT token generation
- Added refresh token flow

## Testing
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Manual testing done

## Related Issues
Fixes #123
Related to #456

## Screenshots (if UI)
[Add screenshots]
```

---

## Quick Reference

```bash
# Common workflow
git checkout main && git pull
git checkout -b feature/TASK-description
# ... make changes ...
git add .
git commit -m "feat(scope): description"
git push -u origin feature/TASK-description
# Create PR

# Sync with main
git fetch origin
git rebase origin/main

# Clean up after merge
git checkout main
git pull
git branch -d feature/TASK-description
```
