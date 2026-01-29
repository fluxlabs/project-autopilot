---
name: code-review
description: Code review patterns, style guides, PR templates, and review checklists. Reference this skill when performing code reviews.
---

# Code Review Skill
# Project Autopilot - Review patterns and standards
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for conducting effective code reviews.

---

## Review Priorities

### Priority Order

1. **Security** (CRITICAL) - Vulnerabilities, data exposure
2. **Correctness** (HIGH) - Logic errors, edge cases
3. **Performance** (HIGH) - Bottlenecks, inefficiencies
4. **Maintainability** (MEDIUM) - Readability, complexity
5. **Style** (LOW) - Formatting, conventions

---

## Security Checklist

### Input Validation

```typescript
// ❌ Never trust user input
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;

// ✅ Always parameterize
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [req.params.id]);
```

### Authentication/Authorization

```typescript
// ❌ Missing authorization check
app.get('/admin/users', async (req, res) => {
  const users = await getUsers();
  res.json(users);
});

// ✅ Proper authorization
app.get('/admin/users', requireAuth, requireRole('admin'), async (req, res) => {
  const users = await getUsers();
  res.json(users);
});
```

### Secrets Management

```typescript
// ❌ Hardcoded secrets
const apiKey = 'sk_live_abc123';

// ✅ Environment variables
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error('API_KEY not configured');
```

### XSS Prevention

```typescript
// ❌ Direct HTML injection
element.innerHTML = userInput;

// ✅ Safe rendering
element.textContent = userInput;
// Or with sanitization
element.innerHTML = DOMPurify.sanitize(userInput);
```

---

## Performance Checklist

### Database Queries

```typescript
// ❌ N+1 queries
const users = await getUsers();
for (const user of users) {
  user.orders = await getOrders(user.id); // N queries!
}

// ✅ Single query with join
const users = await getUsersWithOrders();
```

### Async Operations

```typescript
// ❌ Sequential when parallel possible
const user = await getUser(id);
const orders = await getOrders(id);
const reviews = await getReviews(id);

// ✅ Parallel execution
const [user, orders, reviews] = await Promise.all([
  getUser(id),
  getOrders(id),
  getReviews(id)
]);
```

### Memory Management

```typescript
// ❌ Loading all data into memory
const allRecords = await db.query('SELECT * FROM huge_table');

// ✅ Streaming/pagination
const stream = db.queryStream('SELECT * FROM huge_table');
for await (const batch of stream) {
  processBatch(batch);
}
```

### Bundle Size

```typescript
// ❌ Importing entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Tree-shakeable import
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

---

## Code Quality Patterns

### Error Handling

```typescript
// ❌ Silent failures
try {
  await doSomething();
} catch (e) {
  // ignored
}

// ✅ Proper error handling
try {
  await doSomething();
} catch (error) {
  logger.error('Failed to do something', { error, context });
  throw new ApplicationError('Operation failed', { cause: error });
}
```

### Type Safety

```typescript
// ❌ Using any
function processData(data: any): any {
  return data.items.map((i: any) => i.value);
}

// ✅ Proper typing
interface DataItem {
  value: string;
}

interface Data {
  items: DataItem[];
}

function processData(data: Data): string[] {
  return data.items.map(i => i.value);
}
```

### Early Returns

```typescript
// ❌ Nested conditionals
function process(user) {
  if (user) {
    if (user.active) {
      if (user.verified) {
        return doWork(user);
      }
    }
  }
  return null;
}

// ✅ Guard clauses
function process(user) {
  if (!user) return null;
  if (!user.active) return null;
  if (!user.verified) return null;
  return doWork(user);
}
```

### Single Responsibility

```typescript
// ❌ Function doing too much
async function handleUserRegistration(data) {
  // Validate
  // Create user
  // Send email
  // Update analytics
  // Create audit log
}

// ✅ Separated concerns
async function handleUserRegistration(data) {
  const validated = validateRegistration(data);
  const user = await createUser(validated);
  await Promise.all([
    sendWelcomeEmail(user),
    trackRegistration(user),
    auditLog('user.created', user)
  ]);
  return user;
}
```

---

## Style Guides

### TypeScript Style

```typescript
// Naming
const CONSTANT_VALUE = 42;        // Constants: UPPER_SNAKE
const myVariable = 'value';        // Variables: camelCase
function doSomething() {}          // Functions: camelCase
class MyClass {}                   // Classes: PascalCase
interface IMyInterface {}          // Interfaces: PascalCase (I prefix optional)
type MyType = string;              // Types: PascalCase

// Imports
import { Component } from 'react';           // External first
import { MyService } from '@/services';       // Internal second
import { helper } from './utils';             // Relative last

// Functions
// Prefer arrow functions for callbacks
const items = data.map(item => item.value);

// Named functions for declarations
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Python Style

```python
# Naming
CONSTANT_VALUE = 42              # Constants: UPPER_SNAKE
my_variable = 'value'            # Variables: snake_case
def do_something():              # Functions: snake_case
class MyClass:                   # Classes: PascalCase

# Type hints
def calculate_total(items: list[Item]) -> float:
    return sum(item.price for item in items)

# Docstrings
def process_user(user: User) -> ProcessedUser:
    """Process a user record.

    Args:
        user: The user to process.

    Returns:
        The processed user with additional fields.

    Raises:
        ValidationError: If user data is invalid.
    """
    pass
```

---

## PR Review Template

```markdown
## PR Review: #{number}

### Summary
Brief description of the changes.

### Review Status
- [ ] Code correctness
- [ ] Security review
- [ ] Performance check
- [ ] Test coverage
- [ ] Documentation

### Findings

#### 🔴 Must Fix
- Issue 1 with location and fix

#### 🟡 Should Fix
- Issue 2 with location and fix

#### 🟢 Suggestions
- Optional improvement 1
- Optional improvement 2

### Questions
- Clarification needed on X

### Approval
- [ ] Approved
- [ ] Approved with comments
- [ ] Changes requested
```

---

## Review Comments Best Practices

### Be Specific

```markdown
❌ "This could be better"
✅ "Consider extracting lines 45-60 into a separate `validateUser()`
   function to improve readability and testability"
```

### Be Constructive

```markdown
❌ "This is wrong"
✅ "This approach might cause issues when `user` is null.
   Consider adding a null check: `if (!user) return null;`"
```

### Explain Why

```markdown
❌ "Use const instead of let"
✅ "Use const here since `result` is never reassigned.
   This helps communicate intent and prevents accidental mutations."
```

### Offer Alternatives

```markdown
Instead of:
```typescript
for (let i = 0; i < items.length; i++) {
  process(items[i]);
}
```

Consider:
```typescript
items.forEach(item => process(item));
// or
for (const item of items) {
  process(item);
}
```

This is more readable and less error-prone.
```

---

## Common Patterns to Flag

### Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `any` type | Type safety loss | Define proper types |
| `// TODO` without issue | Lost context | Create issue, reference it |
| Commented code | Clutter | Remove (git has history) |
| Magic numbers | Unclear meaning | Extract to named constant |
| Deep nesting | Hard to read | Early returns, extraction |
| Long functions | Hard to test | Split into smaller functions |

### Good Patterns to Encourage

| Pattern | Why |
|---------|-----|
| Early returns | Reduces nesting |
| Const by default | Prevents mutations |
| Explicit types | Documents intent |
| Small functions | Easy to test |
| Descriptive names | Self-documenting |
| Error boundaries | Graceful failures |

---

## Automated Checks

### Pre-Review Automation

Run before manual review:
1. Linting (ESLint, Pylint)
2. Type checking (tsc, mypy)
3. Unit tests
4. Coverage report
5. Security scan (Snyk, npm audit)

### Review Automation

Can be automated:
- Import ordering
- Formatting
- Naming convention checks
- Unused code detection
- Complexity metrics

Cannot be automated:
- Business logic correctness
- Architecture decisions
- Performance implications
- Security context
- Code clarity

---

## Review Metrics

### Healthy Review Process

| Metric | Target |
|--------|--------|
| Review time | < 24 hours |
| PR size | < 400 lines |
| Review rounds | ≤ 2 |
| Comment resolution | 100% |
| Test coverage | ≥ 80% |
