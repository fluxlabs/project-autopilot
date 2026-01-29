---
description: Automated code review with best practices checking, style enforcement, and security scanning
argument-hint: "[--files=glob] [--strict] [--auto-fix] [--style=guide] [--security] [--perf]"
model: sonnet
---

# Autopilot: REVIEW Mode
# Project Autopilot - Automated code review
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Automated code review with best practices checking, security vulnerability detection, and auto-fix capabilities.

## Required Skills

**Read before reviewing:**
1. `/autopilot/skills/code-review/SKILL.md` - Review patterns and style guides
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `reviewer` - Code analysis and review
- `model-selector` - Choose optimal model per file

---

## Options

| Option | Description |
|--------|-------------|
| `--files=glob` | Files to review (default: staged files) |
| `--strict` | Enforce all rules, fail on warnings |
| `--auto-fix` | Automatically fix auto-fixable issues |
| `--style=guide` | Style guide: airbnb, google, standard |
| `--security` | Focus on security vulnerabilities |
| `--perf` | Focus on performance anti-patterns |
| `--diff-only` | Only review changed lines |
| `--report` | Generate detailed report file |

---

## Usage

### Basic Review

```bash
# Review staged files
/autopilot:review

# Review specific files
/autopilot:review --files="src/**/*.ts"

# Review with auto-fix
/autopilot:review --files="src/services/*.ts" --auto-fix
```

### Security-Focused Review

```bash
/autopilot:review --security --files="src/**/*.ts"
```

### Strict Mode (CI/CD)

```bash
/autopilot:review --strict --files="src/**/*.ts"
# Exit code 1 if any issues found
```

---

## Output Format

```markdown
## Code Review Report

### Summary
| Category | Issues | Auto-fixable | Severity |
|----------|--------|--------------|----------|
| Style | 12 | 10 | 🟡 Low |
| Performance | 3 | 1 | 🟠 Medium |
| Security | 1 | 0 | 🔴 High |
| Best Practices | 5 | 3 | 🟡 Low |

### Critical Issues

#### 🔴 [SECURITY] SQL Injection Risk
**File:** `src/db/queries.ts:45`
**Rule:** no-sql-injection
```typescript
// ❌ Current
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Suggested
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);
```

#### 🟠 [PERFORMANCE] N+1 Query Pattern
**File:** `src/services/userService.ts:78`
**Rule:** no-n-plus-one
```typescript
// ❌ Current - N+1 queries
for (const user of users) {
  const orders = await getOrders(user.id);
}

// ✅ Suggested - Single query with join
const usersWithOrders = await getUsersWithOrders(userIds);
```

### Style Issues

| File | Line | Issue | Auto-fix |
|------|------|-------|----------|
| src/utils.ts | 15 | Missing semicolon | ✅ |
| src/utils.ts | 23 | Prefer const | ✅ |
| src/api.ts | 45 | Line too long (120) | ✅ |

### Auto-Fix Summary
Applied 10 auto-fixes. Run `git diff` to review changes.
```

---

## Review Categories

### Security Rules

| Rule | Severity | Auto-fix |
|------|----------|----------|
| no-sql-injection | 🔴 Critical | ❌ |
| no-xss | 🔴 Critical | ❌ |
| no-hardcoded-secrets | 🔴 Critical | ❌ |
| no-eval | 🔴 Critical | ❌ |
| no-unsafe-regex | 🟠 High | ❌ |
| no-path-traversal | 🟠 High | ❌ |
| validate-input | 🟠 High | ❌ |
| use-parameterized-queries | 🟠 High | ❌ |

### Performance Rules

| Rule | Severity | Auto-fix |
|------|----------|----------|
| no-n-plus-one | 🟠 High | ❌ |
| no-sync-in-async | 🟠 High | ❌ |
| no-memory-leak | 🟠 High | ❌ |
| prefer-lazy-load | 🟡 Medium | ❌ |
| no-unnecessary-await | 🟡 Medium | ✅ |
| prefer-batch-operations | 🟡 Medium | ❌ |

### Style Rules

| Rule | Severity | Auto-fix |
|------|----------|----------|
| consistent-naming | 🟡 Low | ❌ |
| max-line-length | 🟡 Low | ✅ |
| prefer-const | 🟡 Low | ✅ |
| no-unused-vars | 🟡 Low | ✅ |
| consistent-quotes | 🟡 Low | ✅ |
| trailing-comma | 🟡 Low | ✅ |

### Best Practices

| Rule | Severity | Auto-fix |
|------|----------|----------|
| no-magic-numbers | 🟡 Medium | ❌ |
| prefer-early-return | 🟡 Medium | ❌ |
| no-nested-ternary | 🟡 Medium | ❌ |
| prefer-nullish-coalescing | 🟡 Low | ✅ |
| prefer-optional-chaining | 🟡 Low | ✅ |
| explicit-return-type | 🟡 Low | ❌ |

---

## Behavior

```
FUNCTION review(options):

    # 1. Determine files to review
    IF options.files:
        files = glob(options.files)
    ELSE:
        files = getStagedFiles()

    IF files.length == 0:
        LOG "No files to review"
        RETURN

    # 2. Load style guide
    styleGuide = loadStyleGuide(options.style OR detectProjectStyle())

    # 3. Review each file
    issues = []
    FOR each file IN files:

        # Select model based on file size
        model = SPAWN model-selector → selectModel(file.size, "review")

        # Run review
        fileIssues = SPAWN reviewer → reviewFile(file, {
            styleGuide: styleGuide,
            security: options.security,
            performance: options.perf,
            diffOnly: options.diffOnly
        })

        issues.concat(fileIssues)

    # 4. Categorize and prioritize
    categorized = categorizeIssues(issues)
    sorted = sortBySeverity(categorized)

    # 5. Auto-fix if requested
    IF options.autoFix:
        fixable = issues.filter(i => i.autoFixable)
        FOR each issue IN fixable:
            applyFix(issue)
        LOG "Applied {fixable.length} auto-fixes"

    # 6. Generate report
    IF options.report:
        writeReport(sorted, ".autopilot/review-report.md")

    # 7. Display summary
    DISPLAY reviewSummary(sorted)

    # 8. Exit with appropriate code
    IF options.strict AND sorted.critical.length > 0:
        EXIT 1

    RETURN sorted
```

---

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Code Review
  run: |
    /autopilot:review --strict --files="src/**/*.ts" --report

- name: Upload Review Report
  uses: actions/upload-artifact@v3
  with:
    name: review-report
    path: .autopilot/review-report.md
```

---

## Style Guide Detection

Automatically detects project style from:

1. `.eslintrc.*` - ESLint configuration
2. `.prettierrc.*` - Prettier configuration
3. `package.json` - eslintConfig or prettier fields
4. `tsconfig.json` - TypeScript settings

Falls back to sensible defaults if none found.

---

## Quick Examples

```bash
# Quick review of staged changes
/autopilot:review

# Full security audit
/autopilot:review --security --strict --files="**/*.ts"

# Auto-fix style issues
/autopilot:review --auto-fix --files="src/**/*.ts"

# Review with detailed report
/autopilot:review --report --files="src/**/*.ts"

# CI mode - fail on any issues
/autopilot:review --strict --files="src/**/*.ts"
```

$ARGUMENTS
