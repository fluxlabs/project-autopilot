---
description: Test coverage analysis with gap detection and actionable suggestions
argument-hint: "[--threshold=N] [--report] [--suggest] [--by-file] [--critical]"
model: haiku
---

# Autopilot: COVERAGE Mode
# Project Autopilot - Test coverage analysis
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Analyze test coverage, identify gaps, and suggest priority areas for testing.

## Required Skills

**Read before analyzing:**
1. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `model-selector` - Choose optimal model per task

---

## Options

| Option | Description |
|--------|-------------|
| `--threshold=N` | Minimum coverage target (default: 80) |
| `--report` | Generate detailed coverage report |
| `--suggest` | Suggest tests for uncovered code |
| `--by-file` | Show per-file coverage |
| `--critical` | Focus on critical paths only |
| `--diff` | Only analyze changed files |
| `--type=unit\|integration\|e2e` | Filter by test type |

---

## Usage

### Basic Coverage Analysis

```bash
/autopilot:coverage
```

Output:
```markdown
## Coverage Analysis

### Summary
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Statements | 78% | 80% | ⚠️ -2% |
| Branches | 65% | 75% | ❌ -10% |
| Functions | 82% | 80% | ✅ +2% |
| Lines | 79% | 80% | ⚠️ -1% |

### Coverage Trend
```
Jan 20: ████████████████████░░░░ 78%
Jan 22: █████████████████████░░░ 80%
Jan 25: ██████████████████████░░ 82%
Jan 28: ████████████████████░░░░ 78% ← Current
```

### Critical Gaps (Priority Order)

| File | Coverage | Priority | Impact |
|------|----------|----------|--------|
| src/services/auth.ts | 45% | 🔴 High | Auth logic untested |
| src/api/payments.ts | 52% | 🔴 High | Payment flow gaps |
| src/utils/validation.ts | 68% | 🟠 Medium | Edge cases missing |
| src/components/Form.tsx | 71% | 🟡 Low | UI interactions |

### Uncovered Critical Paths

1. **Authentication Flow** (`src/services/auth.ts:45-78`)
   - `refreshToken()` - 0% coverage
   - `validateSession()` - 0% coverage
   - Error handling paths - 0% coverage

2. **Payment Processing** (`src/api/payments.ts:23-67`)
   - Failed payment retry - 0% coverage
   - Webhook verification - 0% coverage
   - Refund logic - 0% coverage

### Recommendations
1. Add tests for auth token refresh (Critical)
2. Add payment error path tests (Critical)
3. Add validation edge case tests (Medium)
```

### Coverage with Suggestions

```bash
/autopilot:coverage --suggest
```

Output:
```markdown
## Coverage Analysis with Suggestions

### Gaps Identified: 12

#### 1. `src/services/auth.ts` (45% → target 80%)

**Missing Tests:**

```typescript
// test/services/auth.test.ts

describe('AuthService', () => {
  describe('refreshToken', () => {
    it('should refresh valid token', async () => {
      const oldToken = createValidToken({ exp: Date.now() - 1000 });
      const newToken = await authService.refreshToken(oldToken);
      expect(newToken).toBeDefined();
      expect(newToken).not.toBe(oldToken);
    });

    it('should reject expired refresh token', async () => {
      const expiredToken = createExpiredToken();
      await expect(authService.refreshToken(expiredToken))
        .rejects.toThrow('Token expired');
    });

    it('should reject invalid token', async () => {
      await expect(authService.refreshToken('invalid'))
        .rejects.toThrow('Invalid token');
    });
  });

  describe('validateSession', () => {
    it('should validate active session', async () => {
      const session = await createSession();
      const result = await authService.validateSession(session.id);
      expect(result.valid).toBe(true);
    });

    it('should reject expired session', async () => {
      const session = await createExpiredSession();
      const result = await authService.validateSession(session.id);
      expect(result.valid).toBe(false);
      expect(result.reason).toBe('expired');
    });
  });
});
```

**Impact:** +35% coverage for auth.ts

#### 2. `src/api/payments.ts` (52% → target 80%)

**Missing Tests:**

```typescript
// test/api/payments.test.ts

describe('PaymentAPI', () => {
  describe('processPayment', () => {
    it('should handle card declined', async () => {
      mockStripe.charges.create.mockRejectedValue({
        code: 'card_declined'
      });

      const result = await processPayment(declinedCard);
      expect(result.status).toBe('failed');
      expect(result.error).toBe('card_declined');
    });

    it('should retry on network error', async () => {
      mockStripe.charges.create
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValue({ id: 'ch_123' });

      const result = await processPayment(validCard);
      expect(result.status).toBe('success');
      expect(mockStripe.charges.create).toHaveBeenCalledTimes(2);
    });
  });
});
```

**Impact:** +28% coverage for payments.ts
```

### Per-File Coverage

```bash
/autopilot:coverage --by-file
```

Output:
```markdown
## Per-File Coverage Report

### Below Threshold (80%)

| File | Stmts | Branch | Funcs | Lines | Δ |
|------|-------|--------|-------|-------|---|
| src/services/auth.ts | 45% | 38% | 50% | 45% | -35% |
| src/api/payments.ts | 52% | 45% | 60% | 52% | -28% |
| src/utils/validation.ts | 68% | 55% | 75% | 70% | -10% |
| src/components/Form.tsx | 71% | 62% | 78% | 72% | -8% |

### Meeting Threshold

| File | Stmts | Branch | Funcs | Lines |
|------|-------|--------|-------|-------|
| src/services/user.ts | 92% | 88% | 95% | 92% |
| src/api/users.ts | 88% | 82% | 90% | 87% |
| src/utils/format.ts | 95% | 92% | 100% | 95% |
| src/components/Button.tsx | 100% | 100% | 100% | 100% |

### Uncovered Files (0%)

- src/workers/email.ts (new)
- src/cron/cleanup.ts (new)
- src/scripts/migrate.ts (intentionally uncovered?)
```

---

## Behavior

```
FUNCTION analyzeCoverage(options):

    # 1. Run coverage tool
    coverage = runCoverageTool()

    # 2. Parse coverage data
    parsed = parseCoverageReport(coverage)

    # 3. Calculate metrics
    metrics = {
        statements: calculateMetric(parsed, 'statements'),
        branches: calculateMetric(parsed, 'branches'),
        functions: calculateMetric(parsed, 'functions'),
        lines: calculateMetric(parsed, 'lines')
    }

    # 4. Identify gaps
    gaps = findCoverageGaps(parsed, options.threshold)

    # 5. Prioritize by criticality
    IF options.critical:
        gaps = filterCriticalPaths(gaps)

    prioritized = prioritizeGaps(gaps)

    # 6. Generate suggestions if requested
    IF options.suggest:
        FOR each gap IN prioritized:
            suggestion = generateTestSuggestion(gap)
            gap.suggestion = suggestion

    # 7. Generate report
    IF options.report:
        writeReport(prioritized, ".autopilot/coverage-report.md")

    # 8. Display results
    DISPLAY coverageSummary(metrics, prioritized)

    # 9. Return status
    IF metrics.overall < options.threshold:
        RETURN 'below_threshold'
    ELSE:
        RETURN 'passing'
```

---

## Coverage Tool Detection

| Tool | Detection | Command |
|------|-----------|---------|
| Jest | `package.json` has jest | `npm test -- --coverage` |
| Vitest | `vitest.config.*` exists | `npx vitest run --coverage` |
| NYC/Istanbul | `nyc` in package.json | `npx nyc npm test` |
| c8 | `c8` in package.json | `npx c8 npm test` |
| pytest-cov | `pytest.ini` or `setup.cfg` | `pytest --cov` |
| go test | `go.mod` exists | `go test -cover` |

---

## Critical Path Detection

Paths considered critical:
1. Authentication/authorization
2. Payment processing
3. Data mutations (create, update, delete)
4. Security-sensitive operations
5. Error handling paths
6. External API integrations

---

## Quick Examples

```bash
# Basic coverage check
/autopilot:coverage

# Check with 90% threshold
/autopilot:coverage --threshold=90

# Get test suggestions
/autopilot:coverage --suggest

# Focus on critical paths
/autopilot:coverage --critical

# Only changed files
/autopilot:coverage --diff

# Generate full report
/autopilot:coverage --report --by-file
```

$ARGUMENTS
