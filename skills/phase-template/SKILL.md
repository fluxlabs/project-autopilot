---
name: phase-template
description: Standard template for phase files with token estimation and tracking. Reference when creating or updating phase files.
---

# Phase Template Skill

Standard structure for phase files including token/cost estimation and actuals.

---

## Phase File Template

```markdown
# Phase [XXX]: [Phase Name]
**Status:** ⏳ Pending | 🔄 In Progress | ✅ Complete | ❌ Blocked
**Prerequisites:** Phase [X], Phase [Y]
**Provides:** [What this phase enables for later phases]

---

## Budget

### Estimate (Pre-Execution)
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | [N] | - |
| Input Tokens | [X]K | High/Med/Low |
| Output Tokens | [Y]K | High/Med/Low |
| **Est. Cost** | **$[Z]** | High/Med/Low |

### Actual (Post-Execution)
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | [X]K | [A]K | +/-[N]% |
| Output Tokens | [Y]K | [B]K | +/-[N]% |
| **Total Cost** | **$[Z]** | **$[C]** | +/-[N]% |

**Completed:** [Timestamp]
**Duration:** [X]h [Y]m

---

## Objective
[One sentence describing what this phase accomplishes]

## Dependencies
- [ ] Phase [X] complete
- [ ] [Specific file/resource] exists
- [ ] [Configuration/env] available

## Quality Gate (Entry)
- [ ] All prerequisites satisfied
- [ ] Required files exist
- [ ] Environment ready
- [ ] Budget available: $[remaining] of $[max]

---

## Must-Haves (Goal-Backward Verification)

Derive requirements from phase goal BACKWARD, verify against code AFTER execution.

### Truths
What must be TRUE when this phase is done:
- [ ] [User can do X]
- [ ] [System supports Y]
- [ ] [Data persists across Z]

### Artifacts
Files that MUST exist with minimum viability:
| Path | Provides | Min Lines | Exports |
|------|----------|-----------|---------|
| `src/path/file.ts` | [What it provides] | [N] | [exported items] |
| `src/path/other.ts` | [What it provides] | [N] | [exported items] |

### Key Links
Connections between artifacts that MUST work:
| From | To | Via | Pattern |
|------|-----|-----|---------|
| `Component.tsx` | `/api/endpoint` | fetch in useEffect | `fetch.*api/endpoint` |
| `Service.ts` | `Repository.ts` | constructor injection | `new.*Repository` |

### Verification Protocol
After all tasks complete:
1. Validator checks each Truth (run tests, manual verification)
2. Validator checks each Artifact exists with min viability
3. Validator checks each Key Link with regex pattern matching
4. IF gaps found → Generate gap-closure plan with `gap_closure: true`
5. Execute gap-closure plans
6. Re-verify until all must_haves pass

---

## Tasks

### Task [XXX].1: [Task Name]
**Status:** ⏳ Pending | 🔄 Active | ✅ Done | ❌ Blocked
**Agent:** [agent-name]
**Model:** Opus / Sonnet

**Token Estimate:**
| Metric | Estimate |
|--------|----------|
| Input | ~[X] tokens |
| Output | ~[Y] tokens |
| Cost | ~$[Z] |

**Token Actual:** *(filled after completion)*
| Metric | Actual |
|--------|--------|
| Input | [A] tokens |
| Output | [B] tokens |
| Cost | $[C] |

**Prerequisites:** None (phase entry point)
**Blocks:** [XXX].2, [XXX].3

**Files:**
- Creates: `path/to/new-file.ts`
- Modifies: `path/to/existing-file.ts`

**Acceptance Criteria:**
- [ ] File created/modified correctly
- [ ] Types compile without errors
- [ ] Tests pass
- [ ] Lint clean

**Completion:** *(filled after done)*
- Commit: `[hash]`
- Time: [timestamp]

---

### Task [XXX].2: [Task Name]
**Status:** ⏳ Pending
**Agent:** [agent-name]
**Model:** Sonnet

**Token Estimate:**
| Metric | Estimate |
|--------|----------|
| Input | ~[X] tokens |
| Output | ~[Y] tokens |
| Cost | ~$[Z] |

**Token Actual:** *(filled after completion)*

**Prerequisites:** Task [XXX].1 complete
**Blocked By:** [XXX].1
**Blocks:** [XXX].4

**Files:**
- Creates: `path/to/file.ts`

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

[Continue for all tasks...]

---

## Phase Summary

### Task Cost Breakdown
| Task | Description | Est. Cost | Actual | Status |
|------|-------------|-----------|--------|--------|
| [XXX].1 | [Name] | $0.05 | $0.04 | ✅ |
| [XXX].2 | [Name] | $0.08 | $0.09 | ✅ |
| [XXX].3 | [Name] | $0.12 | - | 🔄 |
| [XXX].4 | [Name] | $0.06 | - | ⏳ |
| **Total** | | **$0.31** | **$0.13** | |

### Quality Gate (Exit)
- [ ] All tasks complete
- [ ] Build passes
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No lint errors
- [ ] Integration tests pass
- [ ] Budget variance acceptable (<20%)

## Rollback Plan
[Steps to undo this phase if needed]

## Learnings
*(Added during/after execution)*
- [Learning 1]
- [Learning 2]
```

---

## Estimation Guidelines

### By Task Type

| Task Type | Typical Input | Typical Output | Est. Cost (Sonnet) |
|-----------|---------------|----------------|-------------------|
| Read config/setup | 500-1,000 | 200-500 | $0.003-0.006 |
| Create simple file | 1,000-2,000 | 1,000-3,000 | $0.01-0.03 |
| Create complex file | 2,000-5,000 | 3,000-8,000 | $0.03-0.08 |
| Modify existing file | 1,500-3,000 | 500-2,000 | $0.01-0.04 |
| Write unit tests | 2,000-4,000 | 2,000-5,000 | $0.02-0.05 |
| Write integration tests | 3,000-6,000 | 3,000-7,000 | $0.04-0.08 |
| Code review | 3,000-8,000 | 1,000-3,000 | $0.02-0.05 |
| Documentation | 1,000-3,000 | 2,000-5,000 | $0.02-0.04 |
| Debug/fix | 2,000-10,000 | 1,000-5,000 | $0.02-0.10 |

### By Phase Type

| Phase | Typical Tasks | Est. Tokens | Est. Cost (Sonnet) |
|-------|---------------|-------------|-------------------|
| Setup | 3-5 | 15K-25K | $0.08-0.15 |
| Database | 4-6 | 25K-40K | $0.15-0.25 |
| Infrastructure | 4-6 | 20K-35K | $0.12-0.20 |
| Auth | 5-8 | 40K-60K | $0.25-0.40 |
| API | 6-10 | 50K-80K | $0.30-0.50 |
| Business Logic | 8-12 | 60K-100K | $0.40-0.65 |
| Frontend | 8-15 | 80K-150K | $0.50-1.00 |
| Features | 10-20 | 100K-200K | $0.65-1.30 |
| Testing | 6-10 | 50K-80K | $0.30-0.50 |
| Security | 4-8 | 40K-70K | $0.25-0.45 |
| Documentation | 4-8 | 30K-60K | $0.20-0.40 |
| DevOps | 5-10 | 40K-80K | $0.25-0.50 |

### Confidence Levels

| Confidence | When to Use | Variance Expected |
|------------|-------------|-------------------|
| **High** | Well-defined task, similar past work | ±10-15% |
| **Medium** | Clear requirements, some unknowns | ±20-30% |
| **Low** | Vague scope, complex integration, new tech | ±40-60% |

---

## Tracking Protocol

### Before Phase Starts

1. Calculate estimates for each task
2. Sum for phase total
3. Check against remaining budget
4. If over budget, alert user before starting

### During Phase Execution

After each task:
1. Record actual tokens from response
2. Calculate actual cost
3. Update task section with actuals
4. Update phase running total
5. Check variance from estimate
6. Alert if significantly over (>30%)

### After Phase Completes

1. Fill in all actual values
2. Calculate total variance
3. Update phase summary table
4. Add learnings for future estimation
5. Update `.autopilot/token-usage.md` with phase totals

---

## Variance Alerts

| Variance | Action |
|----------|--------|
| <10% | ✅ Normal, no action |
| 10-20% | 📝 Note in learnings |
| 20-30% | ⚠️ Review estimation approach |
| 30-50% | 🟠 Alert user, adjust future estimates |
| >50% | 🛑 Pause, investigate cause |

---

## Example Phase File

```markdown
# Phase 004: Authentication
**Status:** ✅ Complete
**Prerequisites:** Phase 002 (Database), Phase 003 (Infrastructure)
**Provides:** Auth middleware, JWT tokens, user sessions

---

## Budget

### Estimate (Pre-Execution)
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | 6 | - |
| Input Tokens | 45K | Medium |
| Output Tokens | 25K | Medium |
| **Est. Cost** | **$0.32** | Medium |

### Actual (Post-Execution)
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | 45K | 52K | +16% |
| Output Tokens | 25K | 28K | +12% |
| **Total Cost** | **$0.32** | **$0.38** | **+19%** |

**Completed:** 2024-01-15 14:32:00
**Duration:** 1h 45m

---

## Tasks

### Task 004.1: Create User Entity
**Status:** ✅ Done
**Agent:** database
**Model:** Sonnet

**Token Estimate:**
| Metric | Estimate |
|--------|----------|
| Input | ~5,000 |
| Output | ~3,000 |
| Cost | ~$0.04 |

**Token Actual:**
| Metric | Actual |
|--------|--------|
| Input | 4,821 |
| Output | 3,245 |
| Cost | $0.04 |

**Completion:**
- Commit: `a1b2c3d`
- Time: 2024-01-15 12:45:00

### Task 004.2: Auth Service
**Status:** ✅ Done
**Agent:** backend
**Model:** Sonnet

**Token Estimate:**
| Metric | Estimate |
|--------|----------|
| Input | ~8,000 |
| Output | ~5,000 |
| Cost | ~$0.06 |

**Token Actual:**
| Metric | Actual |
|--------|--------|
| Input | 9,234 |
| Output | 5,891 |
| Cost | $0.07 |

[... more tasks ...]

---

## Phase Summary

### Task Cost Breakdown
| Task | Description | Est. Cost | Actual | Status |
|------|-------------|-----------|--------|--------|
| 004.1 | User Entity | $0.04 | $0.04 | ✅ |
| 004.2 | Auth Service | $0.06 | $0.07 | ✅ |
| 004.3 | JWT Middleware | $0.05 | $0.06 | ✅ |
| 004.4 | Login Endpoint | $0.06 | $0.08 | ✅ |
| 004.5 | Password Reset | $0.05 | $0.06 | ✅ |
| 004.6 | Unit Tests | $0.06 | $0.07 | ✅ |
| **Total** | | **$0.32** | **$0.38** | ✅ |

**Variance:** +19% (within acceptable range)

## Learnings
- Auth service took longer due to edge case handling
- Password reset required additional validation logic
- Future auth phases: add 20% buffer to estimates
```
