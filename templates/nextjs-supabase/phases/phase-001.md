# Phase 001: Project Setup
# Template: nextjs-supabase
# Project: {{project_name}}
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Status:** ⏳ Pending
**Prerequisites:** None (initial phase)
**Provides:** Project structure, TypeScript config, Tailwind setup, ESLint config

---

## Budget

### 💰 Estimate
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | 4 | - |
| Input Tokens | ~5K | High |
| Output Tokens | ~8K | High |
| **Est. Cost** | **$0.15** | High |

### 📊 Actual *(Updated during execution)*
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | 5K | - | - |
| Output Tokens | 8K | - | - |
| **Total Cost** | **$0.15** | **-** | - |

---

## Objective

Initialize a Next.js 14 project with TypeScript, Tailwind CSS, and essential development tooling.

## Dependencies
- [ ] None (initial phase)

## Quality Gate (Entry)
- [ ] Empty or new directory
- [ ] Node.js 18+ available
- [ ] npm/yarn/pnpm available

---

## Tasks

### Task 001.1: Initialize Next.js Project
**Status:** ⏳ Pending
**Agent:** frontend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1K tokens |
| Output | ~2K tokens |
| **Est. Cost** | **$0.02** |

**Prerequisites:** None
**Blocks:** 001.2, 001.3, 001.4

**Actions:**
- Run `npx create-next-app@latest {{project_name}} --typescript --tailwind --eslint --app --src-dir`
- Verify project structure created

**Acceptance Criteria:**
- [ ] Project directory exists
- [ ] package.json created
- [ ] next.config.js present
- [ ] TypeScript configured

---

### Task 001.2: Configure TypeScript
**Status:** ⏳ Pending
**Agent:** frontend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1K tokens |
| Output | ~1.5K tokens |
| **Est. Cost** | **$0.02** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Update tsconfig.json with strict settings
- Add path aliases (@/ for src/)
- Configure module resolution

**Files:**
- Modifies: `tsconfig.json`

**Acceptance Criteria:**
- [ ] Strict mode enabled
- [ ] Path aliases working
- [ ] No TypeScript errors

---

### Task 001.3: Configure Tailwind
**Status:** ⏳ Pending
**Agent:** frontend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2.5K tokens |
| **Est. Cost** | **$0.04** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Update tailwind.config.ts with custom theme
- Add base styles to globals.css
- Configure content paths

**Files:**
- Modifies: `tailwind.config.ts`
- Modifies: `src/app/globals.css`

**Acceptance Criteria:**
- [ ] Custom colors defined
- [ ] Dark mode configured
- [ ] Tailwind classes working

---

### Task 001.4: Configure ESLint & Prettier
**Status:** ⏳ Pending
**Agent:** frontend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2K tokens |
| **Est. Cost** | **$0.07** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Install Prettier and ESLint plugins
- Create .prettierrc configuration
- Update .eslintrc.json

**Files:**
- Creates: `.prettierrc`
- Modifies: `.eslintrc.json`
- Modifies: `package.json` (scripts)

**Acceptance Criteria:**
- [ ] ESLint passes
- [ ] Prettier configured
- [ ] npm run lint works

---

## Phase Summary

### Cost Breakdown
| Task | Description | Est. | Actual | Status |
|------|-------------|------|--------|--------|
| 001.1 | Initialize project | $0.02 | - | ⏳ |
| 001.2 | TypeScript config | $0.02 | - | ⏳ |
| 001.3 | Tailwind config | $0.04 | - | ⏳ |
| 001.4 | ESLint & Prettier | $0.07 | - | ⏳ |
| **Total** | | **$0.15** | **-** | |

### Quality Gate (Exit)
- [ ] All tasks complete
- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] No TypeScript errors
- [ ] Project runs with `npm run dev`

## Rollback Plan
```bash
# Remove project directory if initialization fails
rm -rf {{project_name}}
```
