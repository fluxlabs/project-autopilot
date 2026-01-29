---
description: Dependency analysis, updates, security auditing, and license compliance
argument-hint: "[--audit] [--update] [--major] [--security-only] [--outdated] [--unused]"
model: haiku
---

# Autopilot: DEPS Mode
# Project Autopilot - Dependency analysis and management
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive dependency analysis including security auditing, update management, and license compliance.

## Required Skills

**Read before analyzing:**
1. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--audit` | Full dependency audit |
| `--update` | Update dependencies |
| `--major` | Include major version updates |
| `--security-only` | Only security updates |
| `--outdated` | Show outdated packages |
| `--unused` | Find unused dependencies |
| `--license` | License compliance check |
| `--tree` | Show dependency tree |
| `--why=pkg` | Explain why package is needed |

---

## Usage

### Full Dependency Audit

```bash
/autopilot:deps --audit
```

Output:
```markdown
## Dependency Audit Report

### Summary

| Category | Count | Status |
|----------|-------|--------|
| Total Dependencies | 145 | - |
| Direct | 23 | - |
| Transitive | 122 | - |
| Outdated | 12 | ⚠️ |
| Vulnerable | 3 | 🔴 |
| Unused | 2 | 🟡 |

---

### 🔴 Security Vulnerabilities

#### Critical (1)

**lodash** `4.17.19` → `4.17.21`
- **CVE:** CVE-2021-23337
- **Severity:** Critical
- **Type:** Command Injection
- **Path:** lodash → (direct)
- **Fix:** `npm update lodash`

#### High (1)

**axios** `0.21.1` → `1.6.0`
- **CVE:** CVE-2023-45857
- **Severity:** High
- **Type:** Server-Side Request Forgery
- **Path:** axios → (direct)
- **Fix:** `npm update axios`

#### Moderate (1)

**minimatch** `3.0.4` → `3.1.2`
- **CVE:** CVE-2022-3517
- **Severity:** Moderate
- **Type:** ReDoS
- **Path:** jest → jest-haste-map → minimatch
- **Fix:** `npm update jest`

---

### ⚠️ Outdated Dependencies

| Package | Current | Latest | Type | Age |
|---------|---------|--------|------|-----|
| react | 18.2.0 | 18.3.0 | minor | 2mo |
| typescript | 5.3.2 | 5.4.0 | minor | 1mo |
| next | 14.0.4 | 14.2.0 | minor | 3mo |
| eslint | 8.56.0 | 9.0.0 | **major** | 1mo |
| jest | 29.6.0 | 29.7.0 | minor | 2mo |

---

### 🟡 Potentially Unused

| Package | Last Import | Recommendation |
|---------|-------------|----------------|
| moment | None found | Remove (use date-fns) |
| lodash | 2 files | Keep or replace specific functions |

---

### License Summary

| License | Count | Status |
|---------|-------|--------|
| MIT | 98 | ✅ OK |
| Apache-2.0 | 23 | ✅ OK |
| ISC | 15 | ✅ OK |
| BSD-3-Clause | 6 | ✅ OK |
| GPL-3.0 | 2 | ⚠️ Review |
| Unknown | 1 | 🔴 Investigate |

**GPL Dependencies:**
- `some-cli-tool` (dev dependency only) - OK
- `problematic-lib` (runtime) - ⚠️ May need review

---

### Recommendations

1. **Immediate:** Fix 3 security vulnerabilities
   ```bash
   npm update lodash axios jest
   ```

2. **Soon:** Update minor versions (12 packages)
   ```bash
   npm update
   ```

3. **Evaluate:** Review unused packages
   ```bash
   npm uninstall moment
   ```

4. **Consider:** Major version updates
   - ESLint 9 has breaking changes
   - Review changelog before updating
```

### Security-Only Updates

```bash
/autopilot:deps --security-only --update
```

Output:
```markdown
## Security Updates Applied

### Updated Packages

| Package | From | To | Vulnerability |
|---------|------|----|--------------|
| lodash | 4.17.19 | 4.17.21 | CVE-2021-23337 |
| axios | 0.21.1 | 1.6.0 | CVE-2023-45857 |

### Verification
```bash
npm audit
# 0 vulnerabilities
```

### Tests
- Unit tests: ✅ 142/142 passed
- Integration: ✅ 23/23 passed

### Remaining (Non-Security)
- 10 packages have minor updates available
- Run `/autopilot:deps --update` to apply all
```

### Find Unused Dependencies

```bash
/autopilot:deps --unused
```

Output:
```markdown
## Unused Dependencies Analysis

### Definitely Unused (No imports found)

| Package | Size | Recommendation |
|---------|------|----------------|
| moment | 290KB | Remove |
| request | 175KB | Remove (deprecated) |

### Potentially Unused (Low usage)

| Package | Imports | Files | Recommendation |
|---------|---------|-------|----------------|
| lodash | 3 | 2 | Replace with specific imports |
| underscore | 1 | 1 | Migrate to native methods |

### Usage Details

**lodash** (2 files):
- `src/utils/helpers.ts:5` - `_.debounce`
- `src/utils/helpers.ts:8` - `_.throttle`
- `src/components/Search.tsx:3` - `_.debounce`

**Recommendation:** Replace with:
```bash
npm install lodash.debounce lodash.throttle
```
Saves: ~65KB in bundle

---

### Removal Commands

```bash
# Remove definitely unused
npm uninstall moment request

# Replace lodash
npm uninstall lodash
npm install lodash.debounce lodash.throttle
```
```

### Dependency Tree

```bash
/autopilot:deps --tree
```

Output:
```markdown
## Dependency Tree

```
my-app@1.0.0
├── react@18.2.0
├── react-dom@18.2.0
│   └── react@18.2.0 (peer)
├── next@14.1.0
│   ├── react@18.2.0 (peer)
│   ├── @next/env@14.1.0
│   └── postcss@8.4.31
│       ├── nanoid@3.3.7
│       ├── picocolors@1.0.0
│       └── source-map-js@1.0.2
├── typescript@5.3.2
└── @types/node@20.10.0
```

### Duplicate Dependencies

| Package | Versions | Deduplication Possible |
|---------|----------|------------------------|
| nanoid | 3.3.6, 3.3.7 | ✅ Yes |
| debug | 4.3.4, 4.3.5 | ✅ Yes |

Run `npm dedupe` to optimize.
```

### Explain Why Package Needed

```bash
/autopilot:deps --why=nanoid
```

Output:
```markdown
## Why: nanoid

**Package:** nanoid@3.3.7
**Size:** 4.5KB
**Purpose:** Secure unique ID generation

### Dependency Chain

```
my-app@1.0.0
└── next@14.1.0
    └── postcss@8.4.31
        └── nanoid@3.3.7
```

### Used By
- postcss (source map IDs)
- next.js build process

### Direct Alternative
If you need unique IDs in your code:
```typescript
import { nanoid } from 'nanoid';
const id = nanoid(); // "V1StGXR8_Z5jdHi6B-myT"
```

Or use native crypto:
```typescript
const id = crypto.randomUUID();
```
```

---

## Behavior

```
FUNCTION analyzeDeps(options):

    # 1. Load package manifest
    manifest = loadPackageJson()

    IF options.audit:
        # Run full audit
        vulnerabilities = runSecurityAudit()
        outdated = checkOutdated()
        unused = findUnused()
        licenses = checkLicenses()

        DISPLAY auditReport(vulnerabilities, outdated, unused, licenses)

    ELIF options.update:
        # Determine update scope
        IF options.securityOnly:
            packages = getSecurityUpdates()
        ELIF options.major:
            packages = getAllUpdates(includeMajor: true)
        ELSE:
            packages = getAllUpdates(includeMajor: false)

        # Apply updates
        applyUpdates(packages)
        runTests()
        DISPLAY updateReport(packages)

    ELIF options.outdated:
        outdated = checkOutdated()
        DISPLAY outdatedReport(outdated)

    ELIF options.unused:
        unused = findUnusedDeps()
        DISPLAY unusedReport(unused)

    ELIF options.license:
        licenses = checkLicenses()
        DISPLAY licenseReport(licenses)

    ELIF options.tree:
        tree = buildDepTree()
        DISPLAY treeReport(tree)

    ELIF options.why:
        chain = explainDependency(options.why)
        DISPLAY whyReport(chain)
```

---

## Quick Examples

```bash
# Full audit
/autopilot:deps --audit

# Update all (minor/patch only)
/autopilot:deps --update

# Security updates only
/autopilot:deps --security-only --update

# Include major versions
/autopilot:deps --update --major

# Check for outdated
/autopilot:deps --outdated

# Find unused packages
/autopilot:deps --unused

# License compliance
/autopilot:deps --license

# Dependency tree
/autopilot:deps --tree

# Why is package included
/autopilot:deps --why=lodash
```

$ARGUMENTS
