---
description: Performance analysis and optimization suggestions for frontend, backend, and database
argument-hint: "[--type=frontend|backend|database|all] [--profile] [--suggest] [--benchmark]"
model: sonnet
---

# Autopilot: PERF Mode
# Project Autopilot - Performance analysis
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive performance analysis with profiling, bottleneck detection, and optimization suggestions.

## Required Skills

**Read before analyzing:**
1. `/autopilot/skills/performance-analysis/SKILL.md` - Optimization patterns
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `reviewer` - Code analysis
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--type=type` | Analysis type: frontend, backend, database, all |
| `--profile` | Run performance profiling |
| `--suggest` | Generate optimization suggestions |
| `--benchmark` | Run benchmarks |
| `--compare` | Compare with baseline |
| `--ci` | CI mode with thresholds |
| `--budget=file` | Performance budget file |

---

## Usage

### Full Performance Analysis

```bash
/autopilot:perf --type=all
```

Output:
```markdown
## Performance Analysis Report

### Overall Score
```
Frontend:  ██████████████████░░░░░░ 72/100
Backend:   ████████████████████░░░░ 85/100
Database:  ███████████████░░░░░░░░░ 62/100

Overall:   ████████████████░░░░░░░░ 73/100
```

---

## Frontend Performance

### Core Web Vitals

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | 2.8s | <2.5s | 🟠 Needs Work |
| FID | 45ms | <100ms | 🟢 Good |
| CLS | 0.05 | <0.1 | 🟢 Good |
| TTFB | 0.4s | <0.8s | 🟢 Good |
| FCP | 1.2s | <1.8s | 🟢 Good |

### Bundle Analysis

| Bundle | Size | Gzipped | Budget | Status |
|--------|------|---------|--------|--------|
| main.js | 245KB | 78KB | 100KB | 🔴 Over |
| vendor.js | 312KB | 98KB | 150KB | 🔴 Over |
| styles.css | 45KB | 12KB | 50KB | 🟢 OK |

### Large Dependencies

| Package | Size | Usage | Recommendation |
|---------|------|-------|----------------|
| moment | 72KB | Date formatting | Use date-fns (7KB) |
| lodash | 71KB | 3 functions | Import specific |
| chart.js | 65KB | 1 chart type | Use lightweight alt |

### Render Performance

| Component | Renders | Time | Issue |
|-----------|---------|------|-------|
| Dashboard | 12 | 340ms | Excessive re-renders |
| UserList | 8 | 180ms | Missing memo |
| DataTable | 15 | 520ms | Large list, no virtualization |

---

## Backend Performance

### API Response Times

| Endpoint | Avg | P95 | P99 | Status |
|----------|-----|-----|-----|--------|
| GET /api/users | 45ms | 120ms | 250ms | 🟢 OK |
| GET /api/orders | 380ms | 890ms | 1.2s | 🔴 Slow |
| POST /api/checkout | 520ms | 1.1s | 2.3s | 🔴 Slow |
| GET /api/products | 85ms | 180ms | 320ms | 🟢 OK |

### Slow Endpoints Analysis

#### GET /api/orders (380ms avg)
```
Timeline:
├── Database query: 280ms (74%) ← Bottleneck
├── Serialization: 45ms (12%)
├── Auth check: 35ms (9%)
└── Other: 20ms (5%)
```

**Root Cause:** N+1 query pattern
```typescript
// ❌ Current (N+1 queries)
const orders = await Order.findAll();
for (const order of orders) {
  order.items = await OrderItem.findAll({ orderId: order.id });
}

// ✅ Optimized (single query)
const orders = await Order.findAll({
  include: [{ model: OrderItem }]
});
```

### Memory Usage

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Heap Used | 245MB | 512MB | 🟢 OK |
| Heap Total | 380MB | 1GB | 🟢 OK |
| RSS | 420MB | 1.5GB | 🟢 OK |
| External | 12MB | 100MB | 🟢 OK |

---

## Database Performance

### Slow Queries

| Query | Avg Time | Calls/min | Impact |
|-------|----------|-----------|--------|
| SELECT orders + items | 180ms | 120 | 🔴 High |
| SELECT user stats | 95ms | 45 | 🟠 Medium |
| UPDATE inventory | 75ms | 30 | 🟡 Low |

### Query Analysis

#### Slow Query #1
```sql
SELECT o.*, oi.*
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = $1
ORDER BY o.created_at DESC
-- Time: 180ms avg
-- Rows scanned: 50,000
-- Rows returned: 150
```

**Missing Index:**
```sql
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at DESC);
-- Expected improvement: 180ms → 15ms
```

### Index Analysis

| Table | Recommended Index | Reason |
|-------|-------------------|--------|
| orders | (user_id, created_at) | Sort optimization |
| products | (category_id, price) | Filter + sort |
| sessions | (expires_at) | Cleanup queries |

### Connection Pool

| Metric | Value | Recommended |
|--------|-------|-------------|
| Pool Size | 10 | 20 (for 4 cores) |
| Idle Timeout | 30s | 10s |
| Max Lifetime | ∞ | 1h |
| Wait Queue | 0 | < 10 |

---

## Recommendations Summary

### High Priority
1. 🔴 Add database index for orders query (-90% time)
2. 🔴 Fix N+1 queries in order loading (-75% API time)
3. 🔴 Split vendor bundle (tree shaking) (-40% bundle)

### Medium Priority
4. 🟠 Replace moment.js with date-fns (-65KB bundle)
5. 🟠 Add React.memo to UserList component
6. 🟠 Implement query result caching

### Low Priority
7. 🟡 Virtualize DataTable for large lists
8. 🟡 Lazy load chart.js
9. 🟡 Optimize images with next/image
```

### Frontend-Only Analysis

```bash
/autopilot:perf --type=frontend --profile
```

### Database Profiling

```bash
/autopilot:perf --type=database --suggest
```

---

## Behavior

```
FUNCTION analyzePerformance(options):

    # 1. Determine analysis scope
    types = options.type == 'all'
        ? ['frontend', 'backend', 'database']
        : [options.type]

    results = {}

    # 2. Frontend analysis
    IF 'frontend' IN types:
        IF options.profile:
            results.frontend = runLighthouse()
        ELSE:
            results.frontend = analyzeBundle() + analyzeComponents()

    # 3. Backend analysis
    IF 'backend' IN types:
        IF options.profile:
            results.backend = runAPIProfiling()
        ELSE:
            results.backend = analyzeEndpoints() + analyzeMemory()

    # 4. Database analysis
    IF 'database' IN types:
        IF options.profile:
            results.database = runQueryProfiling()
        ELSE:
            results.database = analyzeQueries() + analyzeIndexes()

    # 5. Generate suggestions
    IF options.suggest:
        suggestions = generateOptimizations(results)
        results.suggestions = prioritize(suggestions)

    # 6. Compare with baseline
    IF options.compare:
        baseline = loadBaseline()
        results.comparison = compareWithBaseline(results, baseline)

    # 7. Check performance budget
    IF options.budget:
        budget = loadBudget(options.budget)
        results.budgetStatus = checkBudget(results, budget)

    # 8. CI mode
    IF options.ci:
        IF results.budgetStatus.failed:
            EXIT 1

    DISPLAY performanceReport(results)
```

---

## Performance Budgets

### Budget File Format

```json
{
  "frontend": {
    "bundleSize": "200KB",
    "lcp": "2.5s",
    "fid": "100ms",
    "cls": 0.1
  },
  "backend": {
    "p95ResponseTime": "500ms",
    "p99ResponseTime": "1s",
    "memoryUsage": "512MB"
  },
  "database": {
    "maxQueryTime": "100ms",
    "connectionPoolWait": "50ms"
  }
}
```

---

## Quick Examples

```bash
# Full analysis
/autopilot:perf --type=all

# Frontend with profiling
/autopilot:perf --type=frontend --profile

# Backend optimization suggestions
/autopilot:perf --type=backend --suggest

# Database index analysis
/autopilot:perf --type=database

# CI with budget
/autopilot:perf --ci --budget=perf-budget.json

# Compare with baseline
/autopilot:perf --benchmark --compare
```

$ARGUMENTS
