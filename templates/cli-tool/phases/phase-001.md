# Phase 001: Project Setup
# Template: cli-tool
# Project: {{project_name}}
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Status:** ⏳ Pending
**Prerequisites:** None (initial phase)
**Provides:** Project structure, TypeScript config, Commander setup

---

## Budget

### 💰 Estimate
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | 3 | - |
| Input Tokens | ~4K | High |
| Output Tokens | ~6K | High |
| **Est. Cost** | **$0.12** | High |

### 📊 Actual *(Updated during execution)*
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | 4K | - | - |
| Output Tokens | 6K | - | - |
| **Total Cost** | **$0.12** | **-** | - |

---

## Objective

Initialize a Node.js CLI project with TypeScript, Commander, and development tooling.

## Dependencies
- [ ] None (initial phase)

## Quality Gate (Entry)
- [ ] Empty or new directory
- [ ] Node.js 18+ available
- [ ] npm available

---

## Tasks

### Task 001.1: Initialize Node.js Project
**Status:** ⏳ Pending
**Agent:** backend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1K tokens |
| Output | ~2K tokens |
| **Est. Cost** | **$0.03** |

**Prerequisites:** None
**Blocks:** 001.2, 001.3

**Actions:**
- Create package.json with CLI configuration
- Configure bin entry point
- Add essential dependencies (commander, chalk, ora)

**Files:**
- Creates: `package.json`
- Creates: `.gitignore`
- Creates: `README.md`

**Acceptance Criteria:**
- [ ] package.json created with correct structure
- [ ] bin field configured
- [ ] Dependencies listed

---

### Task 001.2: Configure TypeScript
**Status:** ⏳ Pending
**Agent:** backend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2K tokens |
| **Est. Cost** | **$0.04** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Create tsconfig.json for Node.js CLI
- Configure output to dist/
- Set up path aliases

**Files:**
- Creates: `tsconfig.json`
- Creates: `src/index.ts` (entry point)

**Acceptance Criteria:**
- [ ] TypeScript compiles
- [ ] Output goes to dist/
- [ ] Path aliases working

---

### Task 001.3: Create CLI Entry Point
**Status:** ⏳ Pending
**Agent:** backend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2K tokens |
| **Est. Cost** | **$0.05** |

**Prerequisites:** Task 001.2 complete
**Blocked By:** 001.2

**Actions:**
- Create src/cli.ts with Commander setup
- Add shebang for npm link
- Implement version and help commands

**Files:**
- Creates: `src/cli.ts`
- Modifies: `package.json` (scripts)

**Acceptance Criteria:**
- [ ] `{{bin_name}} --version` works
- [ ] `{{bin_name}} --help` works
- [ ] Exit codes correct

---

## Phase Summary

### Cost Breakdown
| Task | Description | Est. | Actual | Status |
|------|-------------|------|--------|--------|
| 001.1 | Initialize project | $0.03 | - | ⏳ |
| 001.2 | TypeScript config | $0.04 | - | ⏳ |
| 001.3 | CLI entry point | $0.05 | - | ⏳ |
| **Total** | | **$0.12** | **-** | |

### Quality Gate (Exit)
- [ ] All tasks complete
- [ ] `npm run build` passes
- [ ] `npm link` works
- [ ] `{{bin_name}} --version` outputs version
- [ ] `{{bin_name}} --help` shows help

## Rollback Plan
```bash
# Remove project directory if initialization fails
rm -rf {{project_name}}
```
