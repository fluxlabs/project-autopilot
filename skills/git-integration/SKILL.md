---
name: git-integration
description: PR templates, issue linking, release notes generation, and platform-specific Git integrations
---

# Git Integration Skill
# Project Autopilot - Pull request and issue management
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for PR creation, issue linking, release notes, and Git platform integrations.

---

## PR Templates

### Default Autopilot PR Template

```markdown
## Summary

[Brief description of changes - auto-generated from phase descriptions]

## Changes

### Phases Included
{{#each phases}}
- **Phase {{this.id}}:** {{this.name}} - {{this.description}}
{{/each}}

### Files Modified
{{#each files}}
- `{{this.path}}` - {{this.description}}
{{/each}}

## Cost Tracking

| Metric | Estimate | Actual | Variance |
|--------|----------|--------|----------|
| Phases | {{phases.estimated}} | {{phases.actual}} | {{phases.variance}} |
| Tasks | {{tasks.estimated}} | {{tasks.actual}} | {{tasks.variance}} |
| Cost | ${{cost.estimated}} | ${{cost.actual}} | {{cost.variance}} |

*Tracked by Autopilot*

## Testing

{{#each testResults}}
- [{{#if this.passed}}x{{else}} {{/if}}] {{this.name}} {{#if this.coverage}}(coverage: {{this.coverage}}%){{/if}}
{{/each}}

## Related Issues

{{#each issues}}
{{this.action}} #{{this.number}}
{{/each}}

---

🤖 Generated with [Autopilot](https://github.com/project-autopilot)
```

### Minimal PR Template

For quick PRs:

```markdown
## Summary

{{summary}}

## Changes

{{changes}}

## Testing

- [ ] Tests passing
- [ ] Manual verification

---

🤖 Autopilot
```

### Feature PR Template

```markdown
## Feature: {{featureName}}

### Description

{{description}}

### Implementation

#### Architecture
{{architecture}}

#### Key Components
{{#each components}}
- **{{this.name}}:** {{this.purpose}}
{{/each}}

### Screenshots/Demo

[Add screenshots if applicable]

### Testing Plan

| Test Type | Coverage | Status |
|-----------|----------|--------|
| Unit | {{unitCoverage}}% | {{unitStatus}} |
| Integration | {{integrationCoverage}}% | {{integrationStatus}} |
| E2E | {{e2eCoverage}}% | {{e2eStatus}} |

### Rollout Plan

- [ ] Feature flag configured
- [ ] Monitoring alerts set
- [ ] Documentation updated

### Cost Summary

| Phase | Est. | Actual |
|-------|------|--------|
{{#each phases}}
| {{this.name}} | ${{this.estimated}} | ${{this.actual}} |
{{/each}}

---

🤖 Generated with Autopilot
```

---

## Issue Linking

### Supported Patterns

| Pattern | Action | Example |
|---------|--------|---------|
| `Closes #N` | Closes issue on merge | `Closes #123` |
| `Fixes #N` | Closes issue on merge | `Fixes #456` |
| `Resolves #N` | Closes issue on merge | `Resolves #789` |
| `Related to #N` | Links without closing | `Related to #101` |
| `Part of #N` | Links to parent issue | `Part of #102` |
| `Depends on #N` | Links as dependency | `Depends on #103` |

### Auto-Detection

Scan phase files for issue references:

```
FUNCTION extractIssueReferences(phases):

    issues = []
    patterns = [
        /Closes? #(\d+)/gi,
        /Fixes? #(\d+)/gi,
        /Resolves? #(\d+)/gi,
        /Related to #(\d+)/gi,
        /Part of #(\d+)/gi,
        /Depends on #(\d+)/gi,
        /https:\/\/github\.com\/[^\/]+\/[^\/]+\/issues\/(\d+)/gi
    ]

    FOR each phase IN phases:
        content = readFile(phase.file)
        FOR each pattern IN patterns:
            matches = content.match(pattern)
            FOR each match IN matches:
                issues.push({
                    number: extractNumber(match),
                    action: extractAction(match),
                    source: phase.id
                })

    RETURN deduplicate(issues)
```

### Issue Linking in PR

```markdown
## Related Issues

Closes #123 (User authentication)
Closes #124 (API endpoints)
Related to #125 (Documentation)
Part of #100 (Q1 Feature Epic)
```

---

## Platform Support

### GitHub

```bash
# Create PR
gh pr create --title "..." --body "..."

# Create draft
gh pr create --draft --title "..."

# Link issues
gh pr edit N --add-label "feature"

# Request reviewers
gh pr edit N --add-reviewer @username

# View PR
gh pr view N
```

### GitLab

```bash
# Create MR
glab mr create --title "..." --description "..."

# Create draft
glab mr create --draft --title "..."

# Set labels
glab mr update N --label "feature"

# Assign reviewers
glab mr update N --reviewer @username
```

### Bitbucket

```bash
# Using API
curl -X POST \
  https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pullrequests \
  -H "Content-Type: application/json" \
  -d '{
    "title": "...",
    "source": { "branch": { "name": "feature/..." } },
    "destination": { "branch": { "name": "main" } }
  }'
```

---

## Release Notes Generation

### From Phases

```
FUNCTION generateReleaseNotes(version, phases):

    notes = """
# Release {{version}}

**Date:** {{date}}

## What's New

{{#each phases}}
### {{this.name}}

{{this.description}}

**Changes:**
{{#each this.tasks}}
- {{this.description}}
{{/each}}

{{/each}}

## Cost Summary

| Metric | Value |
|--------|-------|
| Total Cost | ${{totalCost}} |
| Phases | {{phaseCount}} |
| Tasks | {{taskCount}} |

## Contributors

- Autopilot AI
- [Your Name]

---

*Generated by Autopilot*
"""

    RETURN interpolate(notes, data)
```

### From Git Log

```bash
# Conventional commits to changelog
git log v1.0.0..HEAD --pretty=format:"%s" | \
  grep -E "^(feat|fix|docs|chore|refactor|test):" | \
  sort | uniq
```

### Release Notes Template

```markdown
# Release v{{version}}

## Highlights

{{highlights}}

## Features

{{#each features}}
- {{this.description}} (#{{this.pr}})
{{/each}}

## Bug Fixes

{{#each fixes}}
- {{this.description}} (#{{this.pr}})
{{/each}}

## Breaking Changes

{{#if breakingChanges}}
{{#each breakingChanges}}
- **{{this.area}}:** {{this.description}}
  - Migration: {{this.migration}}
{{/each}}
{{else}}
None
{{/if}}

## Upgrade Guide

{{upgradeGuide}}

## Full Changelog

https://github.com/{{owner}}/{{repo}}/compare/v{{previousVersion}}...v{{version}}
```

---

## Branch Naming Conventions

### Standard Format

```
<type>/<ticket>-<description>
```

### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New features | `feature/AUTH-123-user-login` |
| `bugfix/` | Bug fixes | `bugfix/BUG-456-null-check` |
| `hotfix/` | Production fixes | `hotfix/SEC-789-xss-fix` |
| `release/` | Release preparation | `release/v1.2.0` |
| `autopilot/` | Autopilot-managed | `autopilot/phase-003-auth` |

### Autopilot Branch Naming

```
FUNCTION generateBranchName(phase, description):

    # Sanitize description
    slug = description
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .slice(0, 30)

    RETURN "autopilot/phase-{phase}-{slug}"

# Example: autopilot/phase-003-user-authentication
```

---

## Commit Message Integration

### Phase-Tagged Commits

```
<type>(<scope>): <description> [phase.task]

[optional body]

[optional footer]
```

Examples:
```
feat(auth): Add JWT refresh endpoint [003.2]

fix(api): Handle null user in profile endpoint [004.5]

test(auth): Add integration tests for login flow [003.8]
```

### Auto-Generated Commit Messages

```
FUNCTION generateCommitMessage(task, changes):

    type = inferCommitType(task)
    scope = inferScope(changes)
    description = task.description.slice(0, 50)
    taskId = "{task.phase}.{task.number}"

    RETURN "{type}({scope}): {description} [{taskId}]"

# Examples:
# feat(auth): Add login endpoint [003.1]
# test(api): Add user endpoint tests [004.8]
```

---

## PR Review Integration

### Auto-Assign Reviewers

```json
// .github/CODEOWNERS
# Autopilot-generated code
.autopilot/ @team-lead
src/services/ @backend-team
src/components/ @frontend-team
```

### PR Labels

| Label | When Applied |
|-------|--------------|
| `autopilot` | All Autopilot PRs |
| `phase-XXX` | Specific phase |
| `feature` | New functionality |
| `bugfix` | Bug fixes |
| `cost-tracking` | Includes cost data |
| `draft` | Work in progress |

### Status Checks

```yaml
# .github/workflows/autopilot-pr.yml
name: Autopilot PR Check

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate PR description
        run: |
          # Check for cost tracking section
          grep -q "## Cost Tracking" pr_body.txt || exit 1

      - name: Check for related issues
        run: |
          # Check for issue references
          grep -qE "(Closes|Fixes|Related to) #[0-9]+" pr_body.txt
```

---

## Error Handling

### PR Creation Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `No remote` | Branch not pushed | `git push -u origin branch` |
| `Branch up to date` | No new commits | Make commits first |
| `PR exists` | PR already open | Use `--force` or update existing |
| `Auth failed` | Token expired | `gh auth login` |

### Issue Linking Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `Issue not found` | Wrong repo or number | Verify issue exists |
| `Permission denied` | No write access | Request access |
| `Rate limited` | Too many API calls | Wait and retry |
