---
description: Intelligent refactoring suggestions and safe execution with preview
argument-hint: "[--target=file|dir] [--pattern=extract|inline|rename|move] [--dry-run] [--preview]"
model: sonnet
---

# Autopilot: REFACTOR Mode
# Project Autopilot - Intelligent code refactoring
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Intelligent refactoring with suggestions, safe execution, and rollback support.

## Required Skills

**Read before refactoring:**
1. `/autopilot/skills/refactoring-patterns/SKILL.md` - Safe refactoring techniques
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `reviewer` - Code analysis
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--target=path` | File or directory to refactor |
| `--pattern=type` | Refactoring pattern (see below) |
| `--dry-run` | Show changes without applying |
| `--preview` | Interactive preview mode |
| `--suggest` | Only suggest refactorings |
| `--all` | Apply all suggested refactorings |
| `--backup` | Create backup before changes |

---

## Refactoring Patterns

| Pattern | Description | Auto-safe |
|---------|-------------|-----------|
| `extract` | Extract method/function | ✅ |
| `inline` | Inline variable/function | ✅ |
| `rename` | Rename with all references | ✅ |
| `move` | Move to separate file | ✅ |
| `convert-ts` | Convert JavaScript to TypeScript | ⚠️ |
| `dead-code` | Remove unused code | ⚠️ |
| `simplify` | Simplify complex expressions | ✅ |
| `modernize` | Update to modern syntax | ✅ |

---

## Usage

### Suggest Refactorings

```bash
# Get suggestions for a file
/autopilot:refactor --target=src/utils.ts --suggest
```

Output:
```markdown
## Refactoring Suggestions: src/utils.ts

### 🔵 Extract Method (High Impact)
**Lines 45-78** - Complex logic could be extracted
```typescript
// Before (34 lines of nested logic)
function processUser(user) {
  // ... complex validation ...
  // ... complex transformation ...
  // ... complex saving ...
}

// After (3 clear functions)
function processUser(user) {
  const validated = validateUser(user);
  const transformed = transformUser(validated);
  return saveUser(transformed);
}
```
**Command:** `/autopilot:refactor --pattern=extract --target=src/utils.ts:45-78`

### 🟡 Inline Variable (Low Impact)
**Line 23** - Single-use variable
```typescript
// Before
const result = calculateTotal(items);
return result;

// After
return calculateTotal(items);
```
**Command:** `/autopilot:refactor --pattern=inline --target=src/utils.ts:23`

### 🟢 Modernize Syntax
**Lines 12, 34, 56** - Can use modern JavaScript
- Line 12: `var` → `const`
- Line 34: Function → Arrow function
- Line 56: Callback → async/await

**Command:** `/autopilot:refactor --pattern=modernize --target=src/utils.ts`
```

### Apply Specific Pattern

```bash
# Extract function
/autopilot:refactor --pattern=extract --target=src/utils.ts:45-78

# Rename with all references
/autopilot:refactor --pattern=rename --target=src/utils.ts --from=oldName --to=newName

# Move function to new file
/autopilot:refactor --pattern=move --target=src/utils.ts:calculateTotal --to=src/calculations.ts
```

### Preview Mode

```bash
/autopilot:refactor --pattern=extract --target=src/utils.ts:45-78 --preview
```

Output:
```markdown
## Refactoring Preview

### Extract Method: processValidation

**From:** `src/utils.ts:45-78`
**Creates:** `src/utils.ts:validateUser` (new function)

### Changes
```diff
- function processUser(user) {
-   // 34 lines of validation logic
-   if (!user.email) throw new Error('Invalid email');
-   if (!user.name) throw new Error('Invalid name');
-   // ... more validation
-   return transformedUser;
- }

+ function validateUser(user) {
+   if (!user.email) throw new Error('Invalid email');
+   if (!user.name) throw new Error('Invalid name');
+   // ... extracted validation
+   return user;
+ }
+
+ function processUser(user) {
+   const validated = validateUser(user);
+   return transformUser(validated);
+ }
```

### Impact Analysis
| Metric | Before | After |
|--------|--------|-------|
| Lines | 34 | 12 + 15 |
| Complexity | 8 | 3 + 4 |
| Testability | Low | High |

**Apply this change?**
- `y` - Apply
- `n` - Cancel
- `e` - Edit suggestion
```

---

## Behavior

```
FUNCTION refactor(options):

    # 1. Load target file(s)
    IF options.target:
        files = resolveTarget(options.target)
    ELSE:
        files = getAllSourceFiles()

    # 2. Analyze for refactoring opportunities
    IF options.suggest OR NOT options.pattern:
        opportunities = []
        FOR each file IN files:
            analysis = SPAWN reviewer → analyzeRefactoring(file)
            opportunities.concat(analysis.suggestions)

        DISPLAY refactoringSuggestions(opportunities)

        IF NOT options.pattern:
            RETURN opportunities

    # 3. Validate pattern
    pattern = validatePattern(options.pattern)

    # 4. Create backup if requested
    IF options.backup:
        createBackup(files)

    # 5. Preview changes
    IF options.dryRun OR options.preview:
        changes = calculateChanges(files, pattern, options)
        DISPLAY previewChanges(changes)

        IF options.dryRun:
            RETURN changes

        IF options.preview:
            confirmation = PROMPT "Apply changes? (y/n/e)"
            IF confirmation != 'y':
                RETURN

    # 6. Apply refactoring
    results = []
    FOR each file IN files:
        result = applyRefactoring(file, pattern, options)
        results.push(result)

    # 7. Verify changes
    verifyBuild()
    verifyTests()

    # 8. Report results
    DISPLAY refactoringResults(results)

    RETURN results
```

---

## Pattern Details

### Extract Method

Extracts a block of code into a new function.

```bash
/autopilot:refactor --pattern=extract --target=src/file.ts:20-45
```

**Automatically handles:**
- Parameter detection
- Return value inference
- Variable scope analysis
- TypeScript types

### Inline Variable/Function

Replaces a variable or function with its definition.

```bash
/autopilot:refactor --pattern=inline --target=src/file.ts:myVariable
```

**Safety checks:**
- Single use verification
- Side effect detection
- Scope validation

### Rename Symbol

Renames a symbol across all references.

```bash
/autopilot:refactor --pattern=rename --from=oldName --to=newName --target=src/
```

**Scope:**
- Same file references
- Import/export references
- Type references
- JSDoc references

### Move to File

Moves a function/class to a new or existing file.

```bash
/autopilot:refactor --pattern=move --target=src/utils.ts:myFunction --to=src/helpers.ts
```

**Automatically handles:**
- Import updates
- Export additions
- Dependency resolution

### Dead Code Removal

Removes unused code.

```bash
/autopilot:refactor --pattern=dead-code --target=src/
```

**Detects:**
- Unused functions
- Unused variables
- Unused imports
- Unreachable code

### Modernize Syntax

Updates to modern JavaScript/TypeScript.

```bash
/autopilot:refactor --pattern=modernize --target=src/
```

**Transformations:**
- `var` → `const`/`let`
- Function → Arrow function
- Callback → async/await
- `require` → `import`
- String concat → Template literal

---

## Safety Features

### Pre-flight Checks

Before any refactoring:
1. ✅ Verify file is version controlled
2. ✅ Check for uncommitted changes
3. ✅ Run existing tests
4. ✅ Create restoration point

### Post-flight Validation

After refactoring:
1. ✅ Verify build passes
2. ✅ Run affected tests
3. ✅ Check for type errors
4. ✅ Validate no functionality change

### Rollback

If validation fails:
```bash
/autopilot:refactor --rollback
```

Restores from the most recent backup point.

---

## Quick Examples

```bash
# Get suggestions
/autopilot:refactor --suggest --target=src/

# Extract method with preview
/autopilot:refactor --pattern=extract --target=src/utils.ts:45-78 --preview

# Rename across project
/autopilot:refactor --pattern=rename --from=getUserById --to=findUserById --target=src/

# Remove dead code (dry run)
/autopilot:refactor --pattern=dead-code --target=src/ --dry-run

# Modernize syntax
/autopilot:refactor --pattern=modernize --target=src/**/*.js
```

$ARGUMENTS
