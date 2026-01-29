---
name: test-strategy
description: Coverage analysis, mutation testing, visual regression, and test prioritization algorithms
---

# Test Strategy Skill
# Project Autopilot - Advanced testing strategies
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for comprehensive test planning, coverage analysis, and advanced testing techniques.

---

## Coverage Analysis

### Coverage Types

| Type | Measures | Target |
|------|----------|--------|
| Statement | Lines executed | 80% |
| Branch | Decision paths | 75% |
| Function | Functions called | 85% |
| Line | Code lines hit | 80% |
| Condition | Boolean expressions | 70% |

### Coverage Commands

```bash
# JavaScript/TypeScript (Jest)
npm test -- --coverage --coverageReporters=json-summary

# JavaScript (NYC/Istanbul)
npx nyc npm test

# Python (pytest-cov)
pytest --cov=src --cov-report=json

# Go
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out

# Rust
cargo tarpaulin --out Json
```

### Coverage Analysis Algorithm

```
FUNCTION analyzeCoverage(coverageData):

    analysis = {
        summary: {},
        gaps: [],
        recommendations: []
    }

    # Calculate summary
    analysis.summary = {
        statements: coverageData.total.statements.pct,
        branches: coverageData.total.branches.pct,
        functions: coverageData.total.functions.pct,
        lines: coverageData.total.lines.pct
    }

    # Find gaps
    FOR each file, fileData IN coverageData:
        uncoveredLines = fileData.lines.filter(l => l.hits == 0)
        uncoveredBranches = fileData.branches.filter(b => b.taken == 0)

        IF uncoveredLines.length > 0 OR uncoveredBranches.length > 0:
            analysis.gaps.push({
                file: file,
                uncoveredLines: uncoveredLines.map(l => l.line),
                uncoveredBranches: uncoveredBranches.length,
                priority: calculatePriority(file, uncoveredLines)
            })

    # Sort by priority
    analysis.gaps.sort((a, b) => b.priority - a.priority)

    # Generate recommendations
    FOR each gap IN analysis.gaps.slice(0, 5):
        analysis.recommendations.push({
            file: gap.file,
            action: "Add tests for lines {gap.uncoveredLines.join(', ')}",
            priority: gap.priority
        })

    RETURN analysis
```

### Coverage Gap Priority

```
FUNCTION calculatePriority(file, uncoveredLines):

    priority = 0

    # Business logic files are higher priority
    IF file.includes("service") OR file.includes("controller"):
        priority += 50

    # More uncovered lines = higher priority
    priority += uncoveredLines.length * 2

    # Authentication/security files are critical
    IF file.includes("auth") OR file.includes("security"):
        priority += 100

    # Payment/financial code is critical
    IF file.includes("payment") OR file.includes("billing"):
        priority += 100

    RETURN priority
```

---

## Mutation Testing

### What is Mutation Testing?

Mutation testing evaluates test quality by introducing small changes (mutations) to code and checking if tests detect them.

### Mutation Operators

| Operator | Original | Mutated |
|----------|----------|---------|
| Arithmetic | `a + b` | `a - b` |
| Relational | `a > b` | `a >= b` |
| Logical | `a && b` | `a \|\| b` |
| Negation | `!a` | `a` |
| Return | `return true` | `return false` |
| Constant | `5` | `0` |

### Tools

```bash
# JavaScript (Stryker)
npm install --save-dev @stryker-mutator/core
npx stryker run

# Python (mutmut)
pip install mutmut
mutmut run

# Java (PITest)
mvn org.pitest:pitest-maven:mutationCoverage
```

### Configuration (Stryker)

```json
// stryker.conf.json
{
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "testRunner": "jest",
  "reporters": ["html", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

### Mutation Score

```
Mutation Score = (Killed Mutants / Total Mutants) × 100

> 80% = Excellent test suite
70-80% = Good
60-70% = Acceptable
< 60% = Needs improvement
```

---

## Visual Regression Testing

### Tools

| Tool | Platform | Integration |
|------|----------|-------------|
| Percy | Web | CI/CD |
| Chromatic | Storybook | GitHub |
| BackstopJS | Web | Local/CI |
| Applitools | Cross-platform | CI/CD |

### BackstopJS Configuration

```json
// backstop.json
{
  "id": "my-app",
  "viewports": [
    { "label": "phone", "width": 375, "height": 812 },
    { "label": "tablet", "width": 768, "height": 1024 },
    { "label": "desktop", "width": 1440, "height": 900 }
  ],
  "scenarios": [
    {
      "label": "Homepage",
      "url": "http://localhost:3000",
      "selectors": ["document"],
      "delay": 500
    },
    {
      "label": "Login",
      "url": "http://localhost:3000/login",
      "selectors": ["form.login"]
    }
  ],
  "paths": {
    "bitmaps_reference": "backstop_data/bitmaps_reference",
    "bitmaps_test": "backstop_data/bitmaps_test"
  },
  "engine": "playwright"
}
```

### Commands

```bash
# Create reference images
npx backstop reference

# Run comparison
npx backstop test

# Approve changes
npx backstop approve
```

---

## Test Prioritization

### Risk-Based Prioritization

```
FUNCTION prioritizeTests(tests, changes):

    priorities = []

    FOR each test IN tests:
        score = calculateTestPriority(test, changes)
        priorities.push({ test: test, score: score })

    # Sort by score descending
    priorities.sort((a, b) => b.score - a.score)

    RETURN priorities
```

### Priority Calculation

```
FUNCTION calculateTestPriority(test, changes):

    score = 0

    # Recent failures (higher priority)
    IF test.lastFailed:
        daysSinceFailure = daysBetween(test.lastFailed, now())
        IF daysSinceFailure < 7:
            score += 100
        ELIF daysSinceFailure < 30:
            score += 50

    # Tests covering changed files
    FOR each file IN changes.modifiedFiles:
        IF test.coverages(file):
            score += 80

    # Execution time (prefer faster tests first)
    IF test.avgDuration < 100:  # ms
        score += 30
    ELIF test.avgDuration < 1000:
        score += 10

    # Test type priority
    SWITCH test.type:
        CASE "unit": score += 40
        CASE "integration": score += 30
        CASE "e2e": score += 20

    # Historical flakiness (lower priority)
    IF test.flakyRate > 0.1:
        score -= 20

    RETURN score
```

---

## Performance Baseline Testing

### Metrics to Track

| Metric | Unit | Threshold |
|--------|------|-----------|
| Response Time | ms | p95 < 500ms |
| Throughput | req/s | > 1000 |
| Error Rate | % | < 0.1% |
| Memory Usage | MB | < 512MB |
| CPU Usage | % | < 80% |

### Configuration

```yaml
# performance.config.yaml
baseline:
  api:
    responseTime:
      p50: 50
      p95: 200
      p99: 500
    throughput: 1000
    errorRate: 0.1

  web:
    lcp: 2500      # Largest Contentful Paint
    fid: 100       # First Input Delay
    cls: 0.1       # Cumulative Layout Shift
    ttfb: 600      # Time to First Byte

thresholds:
  degradation: 10%  # Alert if > 10% worse than baseline
  improvement: 5%   # Celebrate if > 5% better
```

### Lighthouse CI

```bash
# Install
npm install -g @lhci/cli

# Run
lhci autorun

# Configuration
# lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/'],
      numberOfRuns: 3
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'interactive': ['error', { maxNumericValue: 5000 }]
      }
    }
  }
};
```

---

## Test Organization

### File Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── services/
│   │   ├── user.test.ts
│   │   └── auth.test.ts
│   └── utils/
│       └── helpers.test.ts
├── integration/             # API and DB tests
│   ├── api/
│   │   ├── users.test.ts
│   │   └── orders.test.ts
│   └── db/
│       └── queries.test.ts
├── e2e/                     # End-to-end flows
│   ├── auth.spec.ts
│   └── checkout.spec.ts
├── visual/                  # Visual regression
│   └── backstop.json
├── performance/             # Load/stress tests
│   └── k6/
│       └── load.js
└── fixtures/                # Shared test data
    ├── users.json
    └── orders.json
```

### Naming Conventions

```typescript
// Unit tests: [file].test.ts
user.service.test.ts
auth.utils.test.ts

// Integration tests: [feature].integration.test.ts
users-api.integration.test.ts

// E2E tests: [flow].spec.ts or [flow].e2e.ts
login.spec.ts
checkout.e2e.ts

// Test descriptions
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', () => {});
    it('should throw ValidationError for invalid email', () => {});
    it('should hash password before storing', () => {});
  });
});
```

---

## Test Execution Strategy

### Parallel Execution

```javascript
// jest.config.js
module.exports = {
  maxWorkers: '50%',  // Use half of available CPU
  testSequencer: './customSequencer.js'  // Optional custom ordering
};
```

### Test Sharding

```bash
# Split tests across CI nodes
# Node 1
npx jest --shard=1/3

# Node 2
npx jest --shard=2/3

# Node 3
npx jest --shard=3/3
```

### Watch Mode Strategy

```bash
# Only affected tests
npm test -- --watch --onlyChanged

# Related tests for changed files
npm test -- --watch --findRelatedTests
```

---

## Quality Metrics

### Test Health Dashboard

```markdown
## Test Suite Health

### Coverage
| Type | Current | Target | Status |
|------|---------|--------|--------|
| Statements | 85% | 80% | ✅ |
| Branches | 72% | 75% | ⚠️ |
| Functions | 90% | 85% | ✅ |

### Mutation Score
| Module | Score | Target | Status |
|--------|-------|--------|--------|
| auth | 82% | 80% | ✅ |
| api | 75% | 80% | ⚠️ |
| utils | 88% | 80% | ✅ |

### Performance
| Metric | Baseline | Current | Trend |
|--------|----------|---------|-------|
| p95 Response | 180ms | 175ms | ↓ 3% |
| Throughput | 1200/s | 1250/s | ↑ 4% |
| Error Rate | 0.05% | 0.04% | ↓ 20% |

### Flaky Tests
| Test | Flake Rate | Last Failure |
|------|------------|--------------|
| checkout.spec.ts | 5% | 2 days ago |
| auth.e2e.ts | 2% | 5 days ago |
```

---

## Integration with Autopilot

### Phase Testing Requirements

```yaml
# In phase template
testing:
  required:
    - unit: 80% coverage
    - integration: key paths
  optional:
    - mutation: 70% score
    - visual: baseline updated
    - performance: no degradation
```

### Test Gate in Quality Gates

```
Gate 3: Testing
- Unit tests: 80% coverage, all passing
- Integration tests: key paths covered
- No flaky tests in critical paths
- Mutation score > 70% (if enabled)
- Visual regression: no unexpected changes
```
