---
name: context-optimization
description: Advanced token reduction strategies, smart summarization, and context management. Reference this skill for maximum token efficiency.
---

# Context Optimization Skill
# Project Autopilot - Advanced token efficiency patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Advanced patterns for minimizing token usage while maintaining effectiveness.

---

## Context Management Principles

### The Context Pyramid

```
              ┌─────────┐
             ╱  Active   ╲
            ╱    Task     ╲         10% - Current work
           ├───────────────┤
          ╱   References    ╲       20% - Types, interfaces
         ╱                   ╲
        ├─────────────────────┤
       ╱      Cached Info      ╲    30% - Structure, conventions
      ╱                         ╲
     ├───────────────────────────┤
    ╱         Available           ╲  40% - Buffer for reasoning
   ╱                               ╲
  └─────────────────────────────────┘
```

### Context Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Load    │ →  │   Use    │ →  │  Clear   │
│ Minimal  │    │  Smart   │    │  Early   │
└──────────┘    └──────────┘    └──────────┘
     │               │               │
     │               │               │
     ▼               ▼               ▼
  Summaries      Reference       Checkpoint
  Not full       Not re-read     Before limit
```

---

## Smart File Reading

### Decision Tree

```
Need file content?
│
├── File already in context?
│   └── YES → Use existing (0 tokens)
│
├── File in learnings cache?
│   └── YES → Use cached summary (50-100 tokens)
│
├── Need full file?
│   ├── YES → Read full (500-5000 tokens)
│   └── NO ─┬── Need types only?
│           │   └── YES → Read interface/type sections (100-300 tokens)
│           │
│           ├── Need specific function?
│           │   └── YES → Read function + imports (200-500 tokens)
│           │
│           └── Need structure only?
│               └── YES → Read outline (50-100 tokens)
```

### File Reading Patterns

#### Types and Interfaces Only

```typescript
// Instead of reading entire file...

// Read just the types
interface User {
  id: string;
  email: string;
  role: Role;
}

type Role = 'admin' | 'user';

// Skip implementation details
```

#### Function-Level Reading

```typescript
// Target: Modify validateEmail function

// Read: Imports it depends on
import { isValidFormat } from './utils';

// Read: The function itself
function validateEmail(email: string): boolean {
  // function body
}

// Skip: Everything else in file
```

#### Outline Reading

```typescript
// File: src/services/user.service.ts
//
// Structure (not full content):
// - Imports: 5 (db, types, utils, errors, logger)
// - Class: UserService
//   - constructor(db, cache)
//   - findById(id): Promise<User>
//   - findByEmail(email): Promise<User>
//   - create(data): Promise<User>
//   - update(id, data): Promise<User>
//   - delete(id): Promise<void>
// - Private methods: 3
// - Lines: 245
```

---

## Summarization Techniques

### Code Summarization

```typescript
// Original: 150 lines
class OrderService {
  constructor(private db: Database, private payment: PaymentService) {}

  async create(data: CreateOrderInput): Promise<Order> {
    // 30 lines of validation
    // 40 lines of order creation
    // 20 lines of payment processing
    // 15 lines of notification
  }

  async update(id: string, data: UpdateOrderInput): Promise<Order> {
    // 25 lines
  }

  // ... more methods
}

// Summary: 15 lines
// OrderService: Order management with payment integration
// Dependencies: Database, PaymentService
// Methods:
//   - create(CreateOrderInput): Creates order, processes payment, notifies
//   - update(id, UpdateOrderInput): Updates order status/details
//   - cancel(id): Cancels order, refunds payment
//   - getByUser(userId): Lists user's orders
// Note: Uses transaction for create
```

### Documentation Summarization

```markdown
# Original README: 500 lines

# Summary: 30 lines
## Project: e-commerce-api
## Stack: Node.js, TypeScript, PostgreSQL, Redis
## Key Commands:
- `npm run dev` - Start development
- `npm test` - Run tests
- `npm run migrate` - Database migrations

## Architecture:
- src/routes/ - API endpoints
- src/services/ - Business logic
- src/models/ - Database entities

## Environment: See .env.example for required vars
```

### Conversation Summarization

```markdown
# Previous conversation summary (for context continuity)

## What was discussed:
- User wants to add authentication to the app
- Decided on JWT-based auth with refresh tokens
- Database schema designed for users table

## What was built:
- User model (src/models/user.ts)
- Auth service (src/services/auth.ts) - 80% complete

## What remains:
- Token refresh endpoint
- Password reset flow
- Email verification

## Key decisions:
- bcrypt for password hashing (cost factor 12)
- 15-minute access token expiry
- 7-day refresh token expiry
```

---

## Caching Strategies

### What to Cache

| Content | Cache? | Reason |
|---------|--------|--------|
| Project structure | ✅ | Changes rarely |
| Key type definitions | ✅ | Referenced often |
| Conventions/patterns | ✅ | Need consistency |
| Config files | ✅ | Small, important |
| Implementation details | ❌ | Read when needed |
| Test files | ❌ | Context-specific |
| Generated files | ❌ | Don't read at all |

### Cache Format

```markdown
# .autopilot/learnings.md - Keep under 500 lines

## Structure (Last updated: 2026-01-29)
[Directory tree - 20 lines]

## Types (Last updated: 2026-01-29)
[Key interfaces - 50 lines]

## Conventions (Last updated: 2026-01-28)
[Patterns and rules - 30 lines]

## API Endpoints (Last updated: 2026-01-29)
[Route summary - 40 lines]

## Known Issues (Last updated: 2026-01-29)
[Current bugs/workarounds - 20 lines]
```

### Cache Freshness

```
FUNCTION checkCacheFreshness(cache):

    # Check last modified times
    FOR each cachedItem IN cache:
        sourceFile = getSourceFile(cachedItem)

        IF sourceFile.modifiedTime > cachedItem.cachedTime:
            # Cache is stale
            invalidate(cachedItem)
            LOG "Cache invalidated: {cachedItem.name}"

    RETURN cache
```

---

## Token Budget Management

### Budget Tracking

```typescript
interface TokenBudget {
  total: 200000;
  allocated: {
    system: 10000;      // Fixed
    cached: 20000;      // Learnings, structure
    task: 40000;        // Current work
    working: 80000;     // Reasoning space
    buffer: 50000;      // Unexpected needs
  };
  current: {
    used: 45000;
    remaining: 155000;
    percentUsed: 22.5;
  };
  thresholds: {
    warn: 40;           // Start considering checkpoint
    checkpoint: 60;     // Strongly recommend checkpoint
    critical: 80;       // Must checkpoint
  };
}
```

### Budget Alerts

```
Context Usage: ████████░░░░░░░░░░░░ 40%

WARN: Approaching checkpoint threshold
Actions:
1. Clear completed task context
2. Save state to learnings
3. Prepare checkpoint if needed
```

---

## Redundancy Patterns

### Common Redundancies

| Pattern | Problem | Solution |
|---------|---------|----------|
| Type in multiple files | Repeated definitions | Reference shared types |
| Similar code blocks | Duplicate content | Extract and reference |
| Same explanation | Verbose responses | Concise output rules |
| Re-reading files | Token waste | Check cache first |

### Deduplication

```typescript
// ❌ Redundant - Same type defined multiple times
// file1.ts
interface User { id: string; name: string; email: string }

// file2.ts
interface User { id: string; name: string; email: string }

// ✅ Deduplicated - Single source of truth
// types.ts
interface User { id: string; name: string; email: string }

// file1.ts & file2.ts
import { User } from './types';
```

---

## Prompt Compression

### Before (Verbose)

```markdown
I would like you to please create a new service for handling
user authentication. This service should be able to handle
login functionality, logout functionality, and also the ability
to refresh authentication tokens. The service needs to follow
the existing patterns that we have established in our codebase.
Please make sure to add appropriate error handling and also
include TypeScript types for all the function parameters and
return values. The service should be placed in the services
directory.
```

### After (Compressed)

```markdown
Create AuthService in src/services/:
- Methods: login, logout, refreshToken
- Match existing service patterns
- Full TypeScript types
- Error handling included
```

### Token Savings

| Version | Tokens | Savings |
|---------|--------|---------|
| Verbose | ~120 | - |
| Compressed | ~35 | 71% |

---

## Checkpoint Protocol

### When to Checkpoint

1. **Context at 40%** - Optional, prepare
2. **Context at 60%** - Recommended
3. **Context at 80%** - Required
4. **Task complete** - Always save learnings
5. **Error occurs** - Save state for recovery

### Checkpoint Content

```markdown
# Checkpoint: Phase 5, Task 3

## Completed
- [x] Dashboard layout
- [x] Navigation component
- [x] API service setup

## In Progress
- [ ] User settings page (60%)
  - Route created
  - Component scaffolded
  - Need: Form implementation

## Next Steps
1. Complete settings form
2. Add validation
3. Connect to API

## Key Learnings
- Use FormProvider for complex forms
- Settings API expects nested objects

## Resume Command
/autopilot:resume
```

---

## Quick Reference

### Token Costs (Approximate)

| Content | Tokens |
|---------|--------|
| 100 lines of code | 400-600 |
| Interface (10 properties) | 50-80 |
| Function (20 lines) | 80-120 |
| Directory listing | 50-100 |
| Summary paragraph | 30-50 |

### Optimization Checklist

- [ ] Using cache before reading files?
- [ ] Reading only necessary parts?
- [ ] Summarizing instead of full content?
- [ ] Avoiding redundant information?
- [ ] Keeping output concise?
- [ ] Monitoring context usage?
- [ ] Checkpointing appropriately?
