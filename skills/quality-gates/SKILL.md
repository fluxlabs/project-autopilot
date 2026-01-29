---
name: quality-gates
description: Quality standards and validation criteria for all phases. Reference this skill to understand what must pass before proceeding.
---

# Quality Gates Skill

Reference this skill to understand quality requirements at each stage of development.

---

## Gate Definitions

### Gate 0: Pre-Work
**Before starting any task:**
- Git status clean (no uncommitted changes)
- On correct branch
- Dependencies installed
- Environment variables set

### Gate 1: Pre-Commit
**Before every commit:**

**PARALLEL EXECUTION (all independent):**
```bash
# Run ALL checks in parallel - they don't depend on each other
npm run build &
npm run lint &
npm run typecheck &
npm test -- --related &
wait  # Collect all results

# Exit if any failed
if [ $? -ne 0 ]; then exit 1; fi
```

**Time comparison:**
- Sequential: ~60-90s
- Parallel: ~15-25s (60-70% faster)

### Gate 2: Task Complete
**After completing a task:**
- Deliverable files exist
- Unit tests written and passing
- No new lint warnings
- Code matches project style

### Gate 3: Phase Complete
**Before marking phase done:**

**PARALLEL EXECUTION (all independent):**
```bash
# Run ALL quality checks in parallel
npm run build &
BUILD_PID=$!

npm run lint &
LINT_PID=$!

npm test -- --coverage &
TEST_PID=$!

npm audit &
AUDIT_PID=$!

# Wait for all and collect exit codes
wait $BUILD_PID || BUILD_FAIL=1
wait $LINT_PID || LINT_FAIL=1
wait $TEST_PID || TEST_FAIL=1
wait $AUDIT_PID || AUDIT_FAIL=1

# Report results
echo "Build: ${BUILD_FAIL:-✓}"
echo "Lint: ${LINT_FAIL:-✓}"
echo "Test: ${TEST_FAIL:-✓}"
echo "Audit: ${AUDIT_FAIL:-✓}"
```

Coverage must be ≥80%

**Time comparison:**
- Sequential: ~90-120s
- Parallel: ~25-35s (70% faster)

### Gate 4: Security Scan
**Before phase completion (if enabled):**
- No critical vulnerabilities
- No high severity issues (or acknowledged)
- Dependencies scanned
- Secrets detection passed

**PARALLEL EXECUTION (all independent):**
```bash
# Run ALL security checks in parallel
npm audit --audit-level=moderate &
bandit -r src/ -ll &  # Python
semgrep --config=auto src/ &
gitleaks detect &
wait
```

### Gate 5: Release Ready
**Before deployment:**
- All phases complete
- E2E tests pass
- Security audit passed
- Documentation complete
- Changelog updated

---

## Validation Commands

### JavaScript/TypeScript
```bash
# Build
npm run build

# Type check
npx tsc --noEmit

# Lint
npx eslint . --ext .ts,.tsx

# Format
npx prettier --check .

# Test with coverage
npm test -- --coverage --coverageThreshold='{"global":{"branches":80}}'

# Security
npm audit --audit-level=moderate
```

### Python
```bash
# Type check
mypy src/

# Lint
ruff check src/
pylint src/

# Format
black --check src/

# Test
pytest --cov=src --cov-fail-under=80

# Security
bandit -r src/
safety check
```

---

## Coverage Requirements

| Type | Minimum | Target |
|------|---------|--------|
| Statements | 75% | 85% |
| Branches | 70% | 80% |
| Functions | 80% | 90% |
| Lines | 75% | 85% |

---

## Blocking Conditions

### Cannot Commit If:
- Build fails
- Lint errors exist
- Type errors exist
- Tests fail

### Cannot Complete Task If:
- Acceptance criteria not met
- No unit tests
- Coverage dropped

### Cannot Complete Phase If:
- Any task incomplete
- Integration tests fail
- Coverage below threshold
- Security vulnerabilities (high/critical)

### Cannot Deploy If:
- Any phase incomplete
- E2E tests fail
- Security audit failed
- Documentation missing

---

## Quick Reference

```
Task Flow:
  Start → Implement → Test → Lint → Commit → Verify

Phase Flow:
  All Tasks → Integration Test → Coverage Check → Security → Complete

Release Flow:
  All Phases → E2E → Security Audit → Docs → Deploy
```
