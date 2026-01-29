---
name: quality-gates
description: Quality standards and validation criteria with Goal-Backward Verification. Reference for parallel validation, must-haves verification, and gap-closure protocols.
---

# Quality Gates Skill

// Project Autopilot - Quality Gates with Goal-Backward Verification
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill to understand quality requirements at each stage of development, including Goal-Backward Verification for phase completion.

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

### Gate 3: Phase Complete (with Goal-Backward Verification)
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

**PLUS Goal-Backward Verification:**
- All Truths verified (behavioral statements)
- All Artifacts exist with minimum viability
- All Key Links connected (regex verified)

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

## Goal-Backward Verification (NEW)

### Overview

Goal-Backward Verification ensures phases deliver what they promised by checking three categories:

1. **Truths** - Behavioral statements that must be true
2. **Artifacts** - Files that must exist with minimum viability
3. **Key Links** - Connections verified via regex patterns

### Must-Haves Structure

```yaml
must_haves:
  truths:
    - statement: "User can see messages"
      verification: "test"           # test | manual | runtime | integration_test
      test_pattern: "chat.*.test"

  artifacts:
    - path: "src/components/Chat.tsx"
      provides: "Chat component"
      min_lines: 30
      required_exports: ["ChatComponent"]
      required_functions: ["sendMessage"]

  key_links:
    - from: "src/components/Chat.tsx"
      to: "/api/chat"
      pattern: "fetch.*api/chat"
      description: "Component calls API"
```

### Verification Protocol

```
FUNCTION verifyMustHaves(phase):
    gaps = []

    # 1. Verify Truths
    FOR each truth IN must_haves.truths:
        IF truth.verification == "test":
            result = runTests(truth.test_pattern)
        ELSE IF truth.verification == "manual":
            result = requestManualVerification(truth)
        ELSE IF truth.verification == "runtime":
            result = checkRuntimeBehavior(truth)
        ELSE IF truth.verification == "integration_test":
            result = runIntegrationTests(truth.test_pattern)

        IF NOT result.passed:
            gaps.add({type: "truth", item: truth})

    # 2. Verify Artifacts
    FOR each artifact IN must_haves.artifacts:
        IF NOT fileExists(artifact.path):
            gaps.add({type: "artifact_missing", item: artifact})
            CONTINUE

        lines = countLines(artifact.path)
        IF lines < artifact.min_lines:
            gaps.add({type: "artifact_insufficient", item: artifact})

        exports = extractExports(artifact.path)
        FOR each required IN artifact.required_exports:
            IF required NOT IN exports:
                gaps.add({type: "export_missing", item: artifact, missing: required})

        functions = extractFunctions(artifact.path)
        FOR each required IN artifact.required_functions:
            IF required NOT IN functions:
                gaps.add({type: "function_missing", item: artifact, missing: required})

    # 3. Verify Key Links (Regex Matching)
    FOR each link IN must_haves.key_links:
        content = readFile(link.from)
        IF NOT regexMatch(content, link.pattern):
            gaps.add({type: "link_missing", item: link})

    # 4. Generate Gap-Closure Tasks
    IF gaps.length > 0:
        gapPlan = generateGapClosurePlan(gaps)
        gapPlan.gap_closure = true
        RETURN {passed: false, gaps: gaps, closure_plan: gapPlan}

    RETURN {passed: true}
```

### Gap-Closure Protocol

When verification finds gaps:

1. **Generate Gap-Closure Plan** - Tasks with `gap_closure: true`
2. **Execute Gap-Closure Tasks** - Fix identified gaps
3. **Re-verify Must-Haves** - Confirm all gaps closed
4. **Proceed to Standard Gates** - Run build, test, lint, etc.

### Gap-Closure Plan Format

```markdown
## Gap-Closure Plan: Phase {N}

**Generated:** {timestamp}
**Reason:** Must-haves verification found {N} gaps
**Priority:** High (blocks phase completion)

### Gaps Identified
| # | Gap | Type | Severity |
|---|-----|------|----------|
| GC-1 | Missing export: UserService | artifact | High |

### Gap-Closure Tasks
#### Task GC-1: Add UserService export
**Type:** gap_closure
**Target:** src/services/user.ts
**Fix:** Export UserService class
```

---

## Parallel Execution (REQUIRED)

### Why Parallel?

Independent checks have no reason to run sequentially. Running in parallel achieves 60-70% time savings.

| Gate | Sequential | Parallel | Savings |
|------|------------|----------|---------|
| Pre-Commit | 60-90s | 15-25s | 70% |
| Task Complete | 45-60s | 12-18s | 70% |
| Phase Complete | 90-120s | 25-35s | 70% |
| Full Release | 180-240s | 50-70s | 70% |

### Check Independence Matrix

```
Build      ─┬─→ (independent)
Typecheck  ─┼─→ (independent)
Lint       ─┼─→ (independent)
Test       ─┼─→ (independent - unless integration tests need build)
Security   ─┴─→ (independent)

All checks can start simultaneously!
```

### Parallel Test Suites

**IMPORTANT:** Different test types are independent and should run in parallel.

```bash
# Run ALL test types in parallel
run_parallel_tests() {
    echo "🧪 Running test suites in parallel..."

    # Unit tests (fastest, most numerous)
    npm test -- --testPathPattern='\.unit\.' &
    UNIT_PID=$!

    # Integration tests (medium speed)
    npm test -- --testPathPattern='\.integration\.' &
    INT_PID=$!

    # E2E tests (slowest, but independent)
    npm test -- --testPathPattern='\.e2e\.' &
    E2E_PID=$!

    # API contract tests
    npm test -- --testPathPattern='\.contract\.' &
    CONTRACT_PID=$!

    # Wait for all
    wait $UNIT_PID && UNIT_OK=1
    wait $INT_PID && INT_OK=1
    wait $E2E_PID && E2E_OK=1
    wait $CONTRACT_PID && CONTRACT_OK=1

    # Report and return
    echo "Unit: ${UNIT_OK:-FAIL} | Integration: ${INT_OK:-FAIL} | E2E: ${E2E_OK:-FAIL} | Contract: ${CONTRACT_OK:-FAIL}"
    [ -n "$UNIT_OK" ] && [ -n "$INT_OK" ]  # Only unit + integration are critical
}
```

### Test Suite Criticality

| Suite | Critical | Notes |
|-------|----------|-------|
| Unit | Yes | Must pass to proceed |
| Integration | Yes | Must pass to proceed |
| E2E | No | Warning only (may have flaky tests) |
| Contract | No | Warning only |
| Performance | No | Informational |

### Parallel Validation Function

```bash
# PARALLEL validation function with proper result tracking
validate_parallel() {
    local scope="${1:-all}"
    local start=$(date +%s)
    declare -A results
    declare -A pids

    echo "🔄 Starting parallel validation (scope: $scope)..."

    # Launch all checks in parallel
    npm run build 2>&1 &
    pids[build]=$!

    npm run typecheck 2>&1 &
    pids[typecheck]=$!

    npm run lint 2>&1 &
    pids[lint]=$!

    npm test -- --coverage 2>&1 &
    pids[test]=$!

    if [[ "$scope" == "all" || "$scope" == "phase" ]]; then
        npm audit 2>&1 &
        pids[security]=$!
    fi

    # Wait for each and capture exit codes
    for name in "${!pids[@]}"; do
        wait ${pids[$name]}
        results[$name]=$?
    done

    local end=$(date +%s)
    local duration=$((end - start))

    # Report
    echo ""
    echo "╔══════════════════════════════════════╗"
    echo "║     Parallel Validation Results      ║"
    echo "╠══════════════════════════════════════╣"
    for name in build typecheck lint test security; do
        if [[ -n "${results[$name]}" ]]; then
            if [[ ${results[$name]} -eq 0 ]]; then
                echo "║  ✓ $name"
            else
                echo "║  ✗ $name (exit: ${results[$name]})"
            fi
        fi
    done
    echo "╠══════════════════════════════════════╣"
    echo "║  Duration: ${duration}s (parallel)         ║"
    echo "╚══════════════════════════════════════╝"

    # Check for critical failures (build, typecheck, test)
    if [[ ${results[build]} -ne 0 ]] || [[ ${results[typecheck]} -ne 0 ]] || [[ ${results[test]} -ne 0 ]]; then
        echo "❌ Critical checks failed"
        return 1
    fi

    # Warn about non-critical failures
    if [[ ${results[lint]} -ne 0 ]]; then
        echo "⚠️  Lint issues (non-blocking)"
    fi
    if [[ -n "${results[security]}" ]] && [[ ${results[security]} -ne 0 ]]; then
        echo "⚠️  Security issues found (review recommended)"
    fi

    echo "✅ All critical checks passed"
    return 0
}
```

### Wave-Based Execution

For checks with dependencies, use wave-based parallel execution:

```bash
# Wave 1: All static analysis (parallel)
validate_wave1() {
    npm run build &
    npm run typecheck &
    npm run lint &
    wait
}

# Wave 2: Tests (parallel, requires build)
validate_wave2() {
    npm test -- --testPathPattern=unit &
    npm test -- --testPathPattern=integration &
    npm test -- --testPathPattern=e2e &
    wait
}

# Wave 3: Security and coverage (parallel, requires tests)
validate_wave3() {
    npm audit &
    npx nyc report --check-coverage --lines 80 &
    wait
}

# Full wave validation
validate_all_waves() {
    validate_wave1 || return 1
    validate_wave2 || return 1
    validate_wave3 || return 1
    echo "✅ All waves passed"
}
```

### CI/CD Parallel Configuration

**GitHub Actions:**
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        check: [build, typecheck, lint, test, security]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run ${{ matrix.check }}
```

**Parallel Test Sharding:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

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
- **Must-haves verification fails**
- **Gap-closure not complete**

### Cannot Deploy If:
- Any phase incomplete
- E2E tests fail
- Security audit failed
- Documentation missing

---

## Verification Output Format

### Pass
```
✅ Phase 3 Quality Gate: PASSED
   ✓ Build (2.3s)
   ✓ Tests 45/45 (12.1s)
   ✓ Coverage 87% (>80%)
   ✓ Lint (3.2s)
   ✓ Security (4.5s)
   ✓ Truths 3/3
   ✓ Artifacts 4/4
   ✓ Key Links 3/3
```

### Fail with Gaps
```
❌ Phase 3 Quality Gate: BLOCKED
   ✓ Build (2.3s)
   ✓ Tests 45/45 (12.1s)
   ✓ Coverage 87% (>80%)
   ✓ Lint (3.2s)
   ✓ Security (4.5s)
   ✓ Truths 3/3
   ✗ Artifacts 3/4 - Missing export
   ✓ Key Links 3/3

   Gap-Closure Required:
   • GC-1: Add UserService export
```

---

## Quick Reference

```
Task Flow:
  Start → Implement → Test → Lint → Commit → Verify

Phase Flow:
  All Tasks → Must-Haves Verification → Gap-Closure (if needed)
           → Integration Test → Coverage → Security → Complete

Release Flow:
  All Phases → E2E → Security Audit → Docs → Deploy
```
