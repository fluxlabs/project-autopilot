---
description: Extract and apply learnings across projects for continuous improvement
argument-hint: "[--extract] [--apply] [--list] [--category=cat] [--export]"
model: haiku
---

# Autopilot: LEARN Mode
# Project Autopilot - Cross-project learning extraction and application
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Extract patterns, best practices, and lessons learned from projects. Apply learnings to improve future work.

## Required Skills

**Read before using:**
1. `/autopilot/skills/global-state/SKILL.md` - Global learnings storage

## Required Agents

- `history-tracker` - Access project history and learnings

---

## Options

| Option | Description |
|--------|-------------|
| `--extract` | Extract learnings from current project |
| `--apply` | Apply relevant learnings to current project |
| `--list` | List all stored learnings |
| `--category=cat` | Filter by category |
| `--search=query` | Search learnings |
| `--export` | Export learnings to file |
| `--import=file` | Import learnings from file |

---

## Learning Categories

| Category | Description |
|----------|-------------|
| `estimation` | Cost and time estimation accuracy |
| `architecture` | Architectural decisions and patterns |
| `performance` | Performance optimizations |
| `security` | Security best practices |
| `testing` | Testing strategies |
| `tools` | Tool and library recommendations |
| `errors` | Common errors and solutions |
| `process` | Process improvements |

---

## Usage

### Extract Learnings from Current Project

```bash
/autopilot:learn --extract
```

Output:
```markdown
## Learnings Extracted

### Project: my-saas-app
**Tech Stack:** Next.js, Supabase, TypeScript
**Outcome:** Success

### Estimation Learnings

| Phase | Estimated | Actual | Variance | Learning |
|-------|-----------|--------|----------|----------|
| Setup | $0.15 | $0.12 | -20% | Supabase setup faster than expected |
| Auth | $0.55 | $0.72 | +31% | OAuth providers require extra config |
| API | $0.85 | $0.91 | +7% | Good estimate for REST APIs |

**Pattern Detected:** Auth phases typically 25-35% over estimate.
**Recommendation:** Apply 1.3x multiplier to auth phase estimates.

### Architectural Learnings

1. **Supabase Row-Level Security**
   - Challenge: Complex RLS policies for team permissions
   - Solution: Created reusable policy functions
   - Recommendation: Start with simple policies, iterate

2. **Next.js App Router**
   - Challenge: Server component data fetching patterns
   - Solution: Use server actions for mutations
   - Recommendation: Prefer server components by default

### Error Patterns

| Error | Frequency | Solution |
|-------|-----------|----------|
| Hydration mismatch | 3 times | Use `suppressHydrationWarning` or client components |
| Supabase type errors | 5 times | Generate types with `supabase gen types` |
| Missing env vars | 2 times | Add validation on startup |

### Stored to Global Learnings ✅
```

### Apply Learnings to Current Project

```bash
/autopilot:learn --apply
```

Output:
```markdown
## Applicable Learnings

Based on your project (Node.js + TypeScript + PostgreSQL):

### Estimation Adjustments

| Phase | Default | Adjusted | Reason |
|-------|---------|----------|--------|
| Auth | $0.55 | $0.72 | Auth phases typically +30% |
| Database | $0.35 | $0.35 | Good historical accuracy |
| Testing | $0.45 | $0.38 | TypeScript reduces test complexity |

### Recommended Patterns

#### 1. Error Handling (from 5 similar projects)
```typescript
// Recommended pattern
class AppError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string
  ) {
    super(message);
  }
}

// Consistent error response
function handleError(error: unknown): ErrorResponse {
  if (error instanceof AppError) {
    return { code: error.code, message: error.message };
  }
  return { code: 'INTERNAL', message: 'An error occurred' };
}
```

#### 2. Database Connection (from 3 similar projects)
```typescript
// Recommended: Connection pooling with retry
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Add health check
async function checkDb() {
  const client = await pool.connect();
  try {
    await client.query('SELECT 1');
  } finally {
    client.release();
  }
}
```

### Common Pitfalls to Avoid

1. **Missing Input Validation**
   - Seen in: 4/10 similar projects
   - Impact: Security vulnerabilities
   - Prevention: Use Zod for all API inputs

2. **No Rate Limiting**
   - Seen in: 3/10 similar projects
   - Impact: DoS vulnerability
   - Prevention: Add rate limiting middleware early

### Apply These Learnings?
- `y` - Apply all
- `n` - Skip
- `s` - Select specific learnings
```

### List All Learnings

```bash
/autopilot:learn --list
```

Output:
```markdown
## Global Learnings Library

### By Category

#### 📊 Estimation (23 learnings)
- Auth phases: +30% buffer recommended
- TypeScript projects: -15% variance on average
- Database setup: Highly accurate estimates
- Frontend features: High variance (+/-40%)

#### 🏗️ Architecture (18 learnings)
- Supabase RLS patterns (5 projects)
- Next.js App Router patterns (8 projects)
- API error handling (12 projects)
- Database indexing strategies (6 projects)

#### ⚡ Performance (12 learnings)
- N+1 query detection patterns
- Bundle size optimization
- Database connection pooling
- Caching strategies

#### 🔒 Security (15 learnings)
- Input validation patterns
- Authentication best practices
- Rate limiting configurations
- Secret management

#### 🧪 Testing (10 learnings)
- Test coverage targets by project type
- Integration test patterns
- Mock strategies

#### 🛠️ Tools (8 learnings)
- Recommended libraries by use case
- Tool configurations
- Development workflow optimizations

### Statistics
| Metric | Value |
|--------|-------|
| Total Learnings | 86 |
| Projects Contributing | 25 |
| Most Common Category | Estimation |
| Last Updated | 2026-01-29 |
```

### Search Learnings

```bash
/autopilot:learn --search="authentication"
```

Output:
```markdown
## Search Results: "authentication"

### Found 7 learnings

1. **Auth Phase Estimation**
   - Category: Estimation
   - Source: 8 projects
   - Learning: Auth phases typically 25-35% over estimate

2. **JWT vs Session Authentication**
   - Category: Architecture
   - Source: 5 projects
   - Learning: JWT for stateless APIs, sessions for server-rendered

3. **OAuth Provider Configuration**
   - Category: Errors
   - Source: 4 projects
   - Learning: Each OAuth provider needs specific callback handling

4. **Password Hashing**
   - Category: Security
   - Source: 6 projects
   - Learning: Use bcrypt with cost factor 12 minimum

[...]
```

---

## Behavior

```
FUNCTION learn(options):

    # 1. Load global learnings
    learnings = loadGlobalLearnings()

    IF options.extract:
        # Extract from current project
        projectState = loadProjectState()
        history = loadHistory()

        newLearnings = extractLearnings(projectState, history)
        mergedLearnings = mergeLearnings(learnings, newLearnings)

        saveGlobalLearnings(mergedLearnings)
        DISPLAY extractionReport(newLearnings)

    ELIF options.apply:
        # Find applicable learnings
        projectType = detectProjectType()
        techStack = detectTechStack()

        applicable = findApplicableLearnings(learnings, projectType, techStack)
        DISPLAY applicableLearnings(applicable)

        IF user.confirms():
            applyLearnings(applicable)

    ELIF options.list:
        IF options.category:
            filtered = learnings.filter(l => l.category == options.category)
        ELSE:
            filtered = learnings

        DISPLAY learningsList(filtered)

    ELIF options.search:
        results = searchLearnings(learnings, options.search)
        DISPLAY searchResults(results)

    ELIF options.export:
        exportLearnings(learnings, options.export)

    ELIF options.import:
        imported = importLearnings(options.import)
        merged = mergeLearnings(learnings, imported)
        saveGlobalLearnings(merged)
```

---

## Learning Storage

### Global Location

```
~/.claude/autopilot/learnings.json
```

### Learning Format

```json
{
  "id": "uuid",
  "category": "estimation",
  "title": "Auth Phase Estimation",
  "description": "Auth phases typically 25-35% over estimate",
  "techStacks": ["node", "typescript"],
  "projectCount": 8,
  "confidence": 0.85,
  "examples": [
    {
      "project": "my-saas-app",
      "estimated": 0.55,
      "actual": 0.72,
      "variance": 0.31
    }
  ],
  "recommendations": [
    "Apply 1.3x multiplier to auth phase estimates",
    "Break down OAuth providers separately"
  ],
  "created": "2026-01-15",
  "updated": "2026-01-29"
}
```

---

## Quick Examples

```bash
# Extract learnings from current project
/autopilot:learn --extract

# Apply learnings to current project
/autopilot:learn --apply

# List all learnings
/autopilot:learn --list

# Filter by category
/autopilot:learn --list --category=security

# Search learnings
/autopilot:learn --search="database connection"

# Export learnings
/autopilot:learn --export --output=learnings-backup.json

# Import learnings
/autopilot:learn --import=shared-learnings.json
```

$ARGUMENTS
