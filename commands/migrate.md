---
description: Migration planning and execution for databases, frameworks, and APIs
argument-hint: "[--type=database|framework|api|language] [--from=X] [--to=Y] [--plan-only]"
model: sonnet
---

# Autopilot: MIGRATE Mode
# Project Autopilot - Migration planning and execution
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Migration planning and safe execution for databases, frameworks, APIs, and languages.

## Required Skills

**Read before migrating:**
1. `/autopilot/skills/migration-patterns/SKILL.md` - Migration strategies
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `migration-assistant` - Migration planning and execution
- `reviewer` - Code review during migration
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--type=type` | Migration type: database, framework, api, language, infra |
| `--from=version` | Source version/system |
| `--to=version` | Target version/system |
| `--plan-only` | Generate plan without executing |
| `--dry-run` | Show what would change |
| `--step=N` | Execute specific step only |
| `--rollback` | Rollback last migration |

---

## Migration Types

| Type | Examples |
|------|----------|
| `database` | PostgreSQL version, schema changes, DB engine switch |
| `framework` | React 17→18, Next.js 13→14, Express 4→5 |
| `api` | REST→GraphQL, v1→v2, breaking changes |
| `language` | JavaScript→TypeScript, Python 2→3 |
| `infra` | Heroku→AWS, monolith→microservices |

---

## Usage

### Framework Migration (React 17 → 18)

```bash
/autopilot:migrate --type=framework --from=react17 --to=react18 --plan-only
```

Output:
```markdown
## Migration Plan: React 17 → React 18

### Impact Assessment

| Category | Files | Impact |
|----------|-------|--------|
| Components | 45 | Low |
| Hooks | 12 | Medium |
| Tests | 23 | Medium |
| Dependencies | 8 | Low |

### Breaking Changes Detected

1. **Automatic Batching** (8 files affected)
   - State updates now batched automatically
   - May change rendering behavior in event handlers
   - Files: `src/components/Form.tsx`, `src/hooks/useAsync.ts`...

2. **Strict Mode Double Render** (3 files affected)
   - Effects run twice in development
   - May expose existing issues
   - Files: `src/components/DataLoader.tsx`...

3. **Concurrent Rendering** (5 files affected)
   - May need `useSyncExternalStore` for external stores
   - Files: `src/stores/globalStore.ts`...

---

### Migration Steps

#### Phase 1: Dependency Updates
**Estimated:** $0.15 | **Risk:** Low

```bash
npm install react@18 react-dom@18
npm install @types/react@18 @types/react-dom@18 --save-dev
```

#### Phase 2: Update Entry Point
**Estimated:** $0.05 | **Risk:** Low

```tsx
// Before
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));

// After
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

#### Phase 3: Update Concurrent Incompatible Code
**Estimated:** $0.25 | **Risk:** Medium

- Update `useEffect` cleanup patterns
- Replace `useMutableSource` with `useSyncExternalStore`
- Update third-party library integrations

#### Phase 4: Fix StrictMode Issues
**Estimated:** $0.20 | **Risk:** Medium

- Ensure effects are idempotent
- Fix race conditions exposed by double render
- Update tests for new behavior

#### Phase 5: Verify and Test
**Estimated:** $0.35 | **Risk:** Low

- Run full test suite
- Manual testing of key flows
- Performance comparison

---

### Total Estimate
| Metric | Value |
|--------|-------|
| Total Cost | $1.00 |
| Risk Level | Medium |
| Estimated Time | 2-3 hours |

### Rollback Plan
```bash
git checkout HEAD~1 -- package.json package-lock.json
npm install
```

**Ready to execute? Run without `--plan-only`**
```

### Database Migration

```bash
/autopilot:migrate --type=database --from=postgres14 --to=postgres16
```

Output:
```markdown
## Migration Plan: PostgreSQL 14 → 16

### Compatibility Check

| Feature | Status | Notes |
|---------|--------|-------|
| Extensions | ✅ OK | All extensions compatible |
| Functions | ⚠️ Review | 2 deprecated functions used |
| Queries | ✅ OK | No incompatible syntax |
| Indexes | ✅ OK | No changes needed |

### Deprecated Features Found

1. **`to_tsvector` behavior change**
   - Location: `src/db/search.sql:45`
   - Issue: Default dictionary changed
   - Fix: Explicitly specify dictionary

2. **`pg_stat_activity` columns renamed**
   - Location: `src/monitoring/healthcheck.ts:23`
   - Issue: `procpid` → `pid`
   - Fix: Update column reference

---

### Migration Steps

#### Step 1: Backup Current Database
```bash
pg_dump -Fc mydb > backup_$(date +%Y%m%d).dump
```

#### Step 2: Test Migration (Staging)
```bash
# Spin up PG16 container
docker run -d --name pg16-test -e POSTGRES_PASSWORD=test postgres:16

# Restore backup
pg_restore -d postgres://localhost:5433/mydb backup.dump

# Run application tests
npm test:db
```

#### Step 3: Update Application Code
- Fix deprecated function calls
- Update monitoring queries

#### Step 4: Production Migration
```bash
# Maintenance window required
# Estimated downtime: 15-30 minutes
```

---

### Rollback Plan
```bash
# Restore from backup
pg_restore -d mydb backup_$(date +%Y%m%d).dump
```
```

### Language Migration (JS → TypeScript)

```bash
/autopilot:migrate --type=language --from=javascript --to=typescript
```

Output:
```markdown
## Migration Plan: JavaScript → TypeScript

### Codebase Analysis

| Metric | Value |
|--------|-------|
| Total Files | 78 |
| Lines of Code | 12,450 |
| Complexity | Medium |
| Dependencies | 23 (15 have types) |

### Migration Strategy: Gradual Adoption

#### Phase 1: Setup TypeScript ($0.10)
```bash
npm install typescript @types/node --save-dev
npx tsc --init
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": false,
    "allowJs": true,
    "checkJs": false,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

#### Phase 2: Add Missing Type Packages ($0.15)
```bash
npm install @types/express @types/jest @types/lodash --save-dev
```

8 packages need `@types/*`:
- express, jest, lodash, uuid, bcrypt...

#### Phase 3: Rename Core Files ($0.30)
Priority order:
1. Type definitions (create `src/types/`)
2. Utility functions (low coupling)
3. Services (medium coupling)
4. Routes (high coupling)
5. Entry points (last)

#### Phase 4: Add Types Incrementally ($0.80)
```typescript
// Before
function getUser(id) {
  return db.users.findById(id);
}

// After
interface User {
  id: string;
  email: string;
  name: string;
}

function getUser(id: string): Promise<User | null> {
  return db.users.findById(id);
}
```

#### Phase 5: Enable Strict Mode ($0.40)
Gradual strict mode adoption:
1. `noImplicitAny` first
2. `strictNullChecks` second
3. Full `strict: true` last

---

### Estimated Total: $1.75
### Timeline: 1-2 weeks (incremental)
```

---

## Behavior

```
FUNCTION migrate(options):

    # 1. Detect migration type if not specified
    IF NOT options.type:
        options.type = detectMigrationType(options.from, options.to)

    # 2. Load migration patterns
    patterns = loadMigrationPatterns(options.type, options.from, options.to)

    # 3. Analyze current codebase
    analysis = analyzeCodebase(options.type)

    # 4. Identify breaking changes
    breakingChanges = findBreakingChanges(analysis, patterns)

    # 5. Generate migration plan
    plan = generateMigrationPlan(breakingChanges, patterns)

    # 6. Estimate cost and risk
    estimate = estimateMigration(plan)

    # 7. Plan-only mode
    IF options.planOnly:
        DISPLAY migrationPlan(plan, estimate)
        RETURN

    # 8. Dry-run mode
    IF options.dryRun:
        DISPLAY whatWouldChange(plan)
        RETURN

    # 9. Execute specific step
    IF options.step:
        executeStep(plan.steps[options.step])
        RETURN

    # 10. Handle rollback
    IF options.rollback:
        executeRollback()
        RETURN

    # 11. Execute migration
    confirm("Ready to execute migration?")
    executeMigration(plan)
```

---

## Quick Examples

```bash
# Plan React migration
/autopilot:migrate --type=framework --from=react17 --to=react18 --plan-only

# Execute Next.js migration
/autopilot:migrate --type=framework --from=nextjs13 --to=nextjs14

# Database version upgrade
/autopilot:migrate --type=database --from=postgres14 --to=postgres16

# Convert to TypeScript
/autopilot:migrate --type=language --from=javascript --to=typescript

# API version migration
/autopilot:migrate --type=api --from=v1 --to=v2

# Rollback last migration
/autopilot:migrate --rollback
```

$ARGUMENTS
