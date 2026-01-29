---
description: Prompt template management and optimization for reusable AI interactions
argument-hint: "[--list] [--create name] [--use name] [--optimize] [--export]"
model: haiku
---

# Autopilot: PROMPT Mode
# Project Autopilot - Prompt template management
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Manage and optimize reusable prompt templates for consistent AI interactions.

## Required Skills

**Read before managing:**
1. `/autopilot/skills/context-optimization/SKILL.md` - Token optimization

## Required Agents

- `context-optimizer` - Prompt optimization
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--list` | List available prompt templates |
| `--create name` | Create new prompt template |
| `--use name` | Execute a prompt template |
| `--optimize` | Optimize existing prompt |
| `--export` | Export prompts to file |
| `--import=file` | Import prompts from file |
| `--test name` | Test prompt with sample input |

---

## Usage

### List Prompt Templates

```bash
/autopilot:prompt --list
```

Output:
```markdown
## Prompt Templates

### Built-in Templates

| Name | Purpose | Tokens | Last Used |
|------|---------|--------|-----------|
| `code-review` | Review code for issues | ~450 | 2 days ago |
| `test-generate` | Generate unit tests | ~380 | Today |
| `docs-api` | Generate API documentation | ~320 | 1 week ago |
| `refactor-suggest` | Suggest refactorings | ~400 | 3 days ago |
| `bug-analyze` | Analyze bug reports | ~280 | Today |

### Custom Templates

| Name | Purpose | Tokens | Last Used |
|------|---------|--------|-----------|
| `auth-review` | Review auth code specifically | ~520 | Yesterday |
| `react-component` | Generate React components | ~450 | 3 days ago |
| `sql-optimize` | Optimize SQL queries | ~350 | 1 week ago |

### Statistics
- **Total Templates:** 8
- **Average Tokens:** 394
- **Most Used:** `test-generate` (23 uses)
```

### Create Prompt Template

```bash
/autopilot:prompt --create auth-security
```

Output:
```markdown
## Create Prompt Template: auth-security

### Template Editor

**Name:** auth-security
**Category:** Security
**Description:** Review authentication code for security issues

### Template Content

```markdown
# Authentication Security Review

## Context
You are reviewing authentication-related code for security vulnerabilities.

## Files to Review
{files}

## Focus Areas
1. Password handling (hashing, storage)
2. Session management
3. Token security (JWT claims, expiry)
4. OAuth flow implementation
5. Rate limiting
6. Brute force protection

## Output Format
For each issue found:
- **Severity:** Critical/High/Medium/Low
- **Location:** file:line
- **Issue:** Description
- **Fix:** Recommended solution

## Additional Context
{context}
```

### Variables
| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{files}` | string | ✅ | Files to review |
| `{context}` | string | ❌ | Additional context |

### Estimated Tokens
- Template: ~280 tokens
- With typical files: ~800-1200 tokens

**Save template? (y/n)**
```

### Use Prompt Template

```bash
/autopilot:prompt --use test-generate --input="src/services/auth.ts"
```

Output:
```markdown
## Executing: test-generate

### Input
- **File:** src/services/auth.ts

### Expanded Prompt
```
Generate comprehensive unit tests for the following code.

File: src/services/auth.ts
[file contents]

Requirements:
- Use Jest testing framework
- Cover happy paths and error cases
- Mock external dependencies
- Aim for >90% coverage
- Include edge cases
```

### Output

```typescript
// auth.test.ts
import { AuthService } from './auth';
import { mockDb, mockCache } from '../test-utils';

describe('AuthService', () => {
  let authService: AuthService;

  beforeEach(() => {
    authService = new AuthService(mockDb, mockCache);
  });

  describe('login', () => {
    it('should return token for valid credentials', async () => {
      mockDb.users.findByEmail.mockResolvedValue({
        id: '123',
        email: 'test@example.com',
        passwordHash: 'hashed',
      });

      const result = await authService.login('test@example.com', 'password');

      expect(result.token).toBeDefined();
      expect(result.user.email).toBe('test@example.com');
    });

    it('should throw for invalid email', async () => {
      mockDb.users.findByEmail.mockResolvedValue(null);

      await expect(authService.login('invalid@example.com', 'password'))
        .rejects.toThrow('Invalid credentials');
    });

    // ... more tests
  });
});
```

### Statistics
- **Template Tokens:** 380
- **Input Tokens:** 450
- **Output Tokens:** 680
- **Total Cost:** $0.02
```

### Optimize Prompt

```bash
/autopilot:prompt --optimize test-generate
```

Output:
```markdown
## Prompt Optimization: test-generate

### Current Template Analysis

**Token Count:** 380
**Redundancy Score:** 23%
**Clarity Score:** 85%

### Optimization Suggestions

#### 1. Remove Redundant Instructions
**Before:**
```
Generate comprehensive unit tests for the following code.
Make sure to cover all edge cases and error scenarios.
The tests should be comprehensive and thorough.
```

**After:**
```
Generate unit tests covering happy paths, errors, and edge cases.
```

**Savings:** 45 tokens (12%)

#### 2. Use Structured Format
**Before:**
```
Use Jest. Mock dependencies. Cover edge cases. High coverage.
```

**After:**
```
Requirements:
- Framework: Jest
- Coverage: >90%
- Mock: External deps
- Include: Edge cases
```

**Savings:** 12 tokens (better clarity, similar cost)

#### 3. Specify Output Format
**Add:**
```
Output: TypeScript test file with describe/it blocks
```

**Result:** More consistent outputs

### Optimized Template

```markdown
Generate unit tests for:
{file}

Requirements:
- Framework: Jest
- Coverage: >90%
- Mock external deps
- Cover: Happy paths, errors, edge cases

Output: TypeScript test file
```

### Comparison
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Tokens | 380 | 285 | -25% |
| Clarity | 85% | 92% | +7% |
| Output Quality | Good | Good | → |

**Apply optimization? (y/n)**
```

### Test Prompt

```bash
/autopilot:prompt --test code-review --sample=true
```

Output:
```markdown
## Prompt Test: code-review

### Using Sample Input
```typescript
function processUser(user) {
  const data = eval(user.input);
  const query = `SELECT * FROM users WHERE id = ${user.id}`;
  console.log('Password:', user.password);
  return data;
}
```

### Expected Output Categories
- [ ] Security issues detected
- [ ] SQL injection flagged
- [ ] eval() usage flagged
- [ ] Sensitive data logging flagged

### Actual Output
```markdown
## Code Review

### 🔴 Critical Issues

1. **SQL Injection**
   - Line 3: String concatenation in SQL
   - Fix: Use parameterized queries

2. **Code Injection (eval)**
   - Line 2: Dangerous eval() with user input
   - Fix: Remove eval, parse safely

3. **Sensitive Data Exposure**
   - Line 4: Logging password
   - Fix: Never log sensitive data
```

### Test Result: ✅ PASS
- All expected categories detected
- No false positives
- Clear recommendations provided
```

---

## Behavior

```
FUNCTION managePrompts(options):

    IF options.list:
        prompts = loadAllPrompts()
        DISPLAY promptList(prompts)

    ELIF options.create:
        template = interactiveCreate(options.create)
        validateTemplate(template)
        savePrompt(options.create, template)
        DISPLAY "Template saved: {options.create}"

    ELIF options.use:
        template = loadPrompt(options.use)
        expanded = expandTemplate(template, options.input)
        result = executePrompt(expanded)
        DISPLAY result

    ELIF options.optimize:
        template = loadPrompt(options.optimize)
        analysis = analyzePrompt(template)
        optimized = optimizePrompt(template, analysis)
        DISPLAY optimizationReport(template, optimized)

        IF confirm():
            savePrompt(options.optimize, optimized)

    ELIF options.test:
        template = loadPrompt(options.test)
        sample = options.sample ? getSampleInput(options.test) : options.input
        result = testPrompt(template, sample)
        DISPLAY testResults(result)

    ELIF options.export:
        prompts = loadAllPrompts()
        exportPrompts(prompts, options.export)

    ELIF options.import:
        imported = importPrompts(options.import)
        mergePrompts(imported)
```

---

## Template Format

### Structure

```yaml
name: template-name
description: Brief description
category: review|generate|analyze|optimize
model: haiku|sonnet|opus
tokens_estimate: 350

variables:
  - name: file
    type: file
    required: true
  - name: context
    type: string
    required: false

template: |
  Your prompt content here.

  Include variables like {file} and {context}.

output_format: markdown|code|json

examples:
  - input:
      file: src/auth.ts
    expected_output: |
      Expected output example
```

---

## Quick Examples

```bash
# List all prompts
/autopilot:prompt --list

# Create new prompt
/autopilot:prompt --create my-review

# Use a prompt
/autopilot:prompt --use test-generate --input="src/service.ts"

# Optimize prompt
/autopilot:prompt --optimize code-review

# Test prompt
/autopilot:prompt --test code-review --sample=true

# Export prompts
/autopilot:prompt --export --output=prompts.yaml

# Import prompts
/autopilot:prompt --import=shared-prompts.yaml
```

$ARGUMENTS
