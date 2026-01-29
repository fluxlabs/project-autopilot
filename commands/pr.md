---
description: Create pull request with phase context
argument-hint: "[--phase=N] [--title=text] [--draft] [--link-issues]"
model: sonnet
---

# Autopilot: PR Mode
# Project Autopilot - Pull request creation with context
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Create pull requests with automatic context from Autopilot phases, cost tracking, and issue linking.

## Required Skills

**Read before creating PR:**
1. `/autopilot/skills/git-integration/SKILL.md` - PR templates and conventions
2. `/autopilot/skills/git-workflow/SKILL.md` - Branch management

---

## Options

| Option | Description |
|--------|-------------|
| `--phase=N` | Include context from specific phase(s) |
| `--title=text` | Custom PR title (default: auto-generated) |
| `--draft` | Create as draft PR |
| `--link-issues` | Auto-link related issues |
| `--base=branch` | Target branch (default: main) |
| `--no-costs` | Exclude cost tracking from description |
| `--template=name` | Use specific PR template |

---

## Behavior

### Basic PR Creation

```bash
/autopilot:pr
```

Flow:
```
FUNCTION createPR(options):

    # 1. Detect current state
    branch = git.currentBranch()
    state = readFile(".autopilot/STATE.md")
    phases = getCompletedPhases()

    # 2. Generate title if not provided
    IF NOT options.title:
        title = generateTitle(phases, branch)

    # 3. Generate description
    description = generateDescription({
        phases: phases,
        state: state,
        includeCosts: NOT options.noCosts,
        linkIssues: options.linkIssues
    })

    # 4. Ensure branch is pushed
    IF NOT git.hasRemote(branch):
        git.push("-u", "origin", branch)

    # 5. Create PR
    pr = gh.createPR({
        title: title,
        body: description,
        base: options.base OR "main",
        draft: options.draft
    })

    # 6. Link issues if requested
    IF options.linkIssues:
        issues = extractIssueReferences(phases)
        FOR each issue IN issues:
            gh.linkIssue(pr, issue)

    DISPLAY prSummary(pr)
```

---

## PR Template

### Auto-Generated Description

```markdown
## Summary

[Phase-based summary of changes]

- **Phase 003:** Authentication system with JWT
- **Phase 004:** REST API endpoints for users and orders
- **Phase 005:** Input validation and error handling

## Changes

### Files Modified
- `src/services/auth.ts` - JWT authentication service
- `src/routes/api/users.ts` - User CRUD endpoints
- `src/routes/api/orders.ts` - Order management endpoints
- `src/middleware/validation.ts` - Request validation

### Features Added
- User authentication (login, signup, password reset)
- User profile management
- Order creation and tracking
- Input validation with Zod

## Cost Tracking

| Metric | Estimate | Actual | Variance |
|--------|----------|--------|----------|
| Phases | 3 | 3 | 0% |
| Tasks | 24 | 26 | +8% |
| Cost | $2.85 | $3.12 | +9% |

*Tracked by Autopilot*

## Testing

- [x] Unit tests passing (coverage: 87%)
- [x] Integration tests passing
- [ ] E2E tests (pending Phase 006)

## Related Issues

Closes #123
Related to #124, #125

---

🤖 Generated with [Autopilot](https://github.com/project-autopilot)
```

---

## Phase-Specific PR

Create PR for specific phase:

```bash
/autopilot:pr --phase=003
```

Output:
```markdown
## Creating PR for Phase 003

**Title:** feat(auth): Add authentication system with JWT

### Commits included (Phase 003 only)
- `abc1234` feat(auth): Add JWT service
- `def5678` feat(auth): Add login/signup routes
- `ghi9012` feat(auth): Add auth middleware
- `jkl3456` test(auth): Add authentication tests

### Description preview

## Summary

Phase 003: Authentication System

Implements complete authentication flow with JWT tokens:
- Login and signup endpoints
- Password reset flow
- Session management
- Protected route middleware

## Changes
[... phase-specific changes ...]

## Cost Tracking
| Phase | Est. | Actual | Variance |
|-------|------|--------|----------|
| 003 | $0.85 | $0.92 | +8% |

---

Create this PR? (y/n)
```

---

## Multi-Phase PR

Include multiple phases:

```bash
/autopilot:pr --phase=003,004,005
```

Or use range:

```bash
/autopilot:pr --phase=003-005
```

---

## Draft PR

Create as draft for early review:

```bash
/autopilot:pr --draft --title="WIP: User dashboard"
```

Output:
```markdown
## Draft PR Created

**Title:** WIP: User dashboard
**Status:** Draft (not ready for merge)
**URL:** https://github.com/user/repo/pull/42

### Next Steps
1. Complete remaining tasks
2. Run `/autopilot:pr --update` to convert to ready
3. Or use GitHub UI to mark ready for review
```

---

## Issue Linking

Auto-link issues mentioned in phase files:

```bash
/autopilot:pr --link-issues
```

Scans for:
- `Closes #123`
- `Fixes #456`
- `Related to #789`
- Issue URLs

---

## Platform Support

### GitHub (Default)

```bash
/autopilot:pr
# Uses: gh pr create
```

### GitLab

```bash
/autopilot:pr --platform=gitlab
# Uses: glab mr create
```

### Bitbucket

```bash
/autopilot:pr --platform=bitbucket
# Uses: Bitbucket API
```

---

## Output Examples

### Successful Creation

```markdown
## PR Created Successfully

**Title:** feat(auth,api): Add authentication and API layer
**Number:** #42
**URL:** https://github.com/user/repo/pull/42
**Status:** Open (ready for review)

### Linked
- Closes #123 (User authentication)
- Closes #124 (API endpoints)

### Reviewers
- @team-lead (auto-assigned)

### Labels
- `feature`
- `autopilot`

### Next Steps
```bash
# Check PR status
gh pr view 42

# Request specific reviewers
gh pr edit 42 --add-reviewer @username

# Merge when ready
gh pr merge 42
```
```

### Already Exists

```markdown
## PR Already Exists

A pull request already exists for branch `feature/auth`:

**#41:** feat(auth): Add authentication system
**URL:** https://github.com/user/repo/pull/41
**Status:** Open

### Options
1. Update existing PR: `/autopilot:pr --update`
2. Create new PR: `/autopilot:pr --force`
3. View PR: `gh pr view 41`
```

---

## Error Handling

### Not on Feature Branch

```markdown
## Error: Cannot Create PR from Main

You're currently on the `main` branch.

**Fix:** Create or switch to a feature branch:
```bash
git checkout -b feature/your-feature
```
```

### No Commits to PR

```markdown
## Error: No New Commits

No new commits compared to `main`.

**Current branch:** feature/auth
**Base branch:** main
**Ahead/Behind:** 0/0

Make some changes and commit before creating a PR.
```

### Remote Not Configured

```markdown
## Error: No Remote Repository

No remote repository configured.

**Fix:**
```bash
git remote add origin https://github.com/user/repo.git
git push -u origin feature/auth
```

Then try again:
```bash
/autopilot:pr
```
```

---

## Quick Start Examples

```bash
# Basic PR from current branch
/autopilot:pr

# PR with custom title
/autopilot:pr --title="Add user authentication"

# Draft PR for early feedback
/autopilot:pr --draft

# PR for specific phases
/autopilot:pr --phase=003

# PR without cost tracking
/autopilot:pr --no-costs

# PR to different base branch
/autopilot:pr --base=develop

# PR with issue linking
/autopilot:pr --link-issues
```

$ARGUMENTS
