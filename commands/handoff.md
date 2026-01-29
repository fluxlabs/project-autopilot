---
description: Generate context document for human developer handoff with full project state
argument-hint: "[--scope=full|phase|feature] [--include-learnings] [--format=md|json]"
model: haiku
---

# Autopilot: HANDOFF Mode
# Project Autopilot - Developer handoff documentation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Generate comprehensive context documents for handoff to human developers or new team members.

## Required Skills

**Read before generating handoff:**
1. `/autopilot/skills/documentation-generation/SKILL.md` - Documentation patterns
2. `/autopilot/skills/global-state/SKILL.md` - Project history access

## Required Agents

- `history-tracker` - Access project history

---

## Options

| Option | Description |
|--------|-------------|
| `--scope=scope` | Handoff scope: full, phase, feature |
| `--include-learnings` | Include lessons learned |
| `--include-decisions` | Include decision log |
| `--format=fmt` | Output format: md, json, html |
| `--output=path` | Output file path |
| `--onboarding` | Include setup instructions |

---

## Usage

### Full Project Handoff

```bash
/autopilot:handoff --scope=full
```

Output:
```markdown
# Project Handoff Document

**Project:** my-saas-app
**Generated:** 2026-01-29 14:30:00
**Status:** Phase 5/10 (50% complete)

---

## Executive Summary

SaaS application for team collaboration. Currently in feature development
phase with core infrastructure complete. Ready for frontend integration work.

### Quick Stats
| Metric | Value |
|--------|-------|
| Progress | 50% (5/10 phases) |
| Cost So Far | $4.23 |
| Remaining Est. | $3.50 |
| Tech Stack | Next.js, Supabase, TypeScript |

---

## Current State

### What's Complete ✅
- [x] Project setup and configuration
- [x] Database schema and migrations
- [x] Authentication system (JWT + OAuth)
- [x] Core API endpoints (CRUD)
- [x] Real-time subscriptions setup

### What's In Progress 🔄
- [ ] Dashboard UI components (60%)
- [ ] Settings page
- [ ] Team management

### What's Remaining 📋
- [ ] Notifications system
- [ ] Analytics dashboard
- [ ] Admin panel
- [ ] Testing suite
- [ ] Documentation

---

## Architecture Overview

```
src/
├── app/                    # Next.js app router
│   ├── api/               # API routes
│   ├── (auth)/            # Auth pages
│   └── (dashboard)/       # Dashboard pages
├── components/            # React components
│   ├── ui/               # Base UI components
│   └── features/         # Feature components
├── lib/                   # Utilities
│   ├── supabase/         # Supabase client
│   └── utils/            # Helper functions
└── types/                 # TypeScript types
```

### Key Files

| File | Purpose |
|------|---------|
| `src/app/api/[...route]/route.ts` | Main API handler |
| `src/lib/supabase/server.ts` | Server-side Supabase |
| `src/components/ui/button.tsx` | Base button component |
| `supabase/migrations/` | Database migrations |

---

## Key Decisions Made

### 1. Authentication Strategy
**Decision:** JWT with Supabase Auth
**Rationale:** Built-in OAuth support, row-level security
**Alternatives Considered:** Auth0, NextAuth
**Tradeoffs:** Vendor lock-in vs. development speed

### 2. Database Design
**Decision:** Normalized schema with soft deletes
**Rationale:** Data integrity, audit trail
**Note:** Consider denormalization if performance issues arise

### 3. API Architecture
**Decision:** Next.js API routes (not separate backend)
**Rationale:** Simplified deployment, single codebase
**Tradeoffs:** Less flexibility vs. faster development

---

## Environment Setup

### Prerequisites
- Node.js 20+
- pnpm 8+
- Supabase CLI

### Quick Start

```bash
# Clone and install
git clone <repo>
cd my-saas-app
pnpm install

# Setup environment
cp .env.example .env.local
# Fill in Supabase credentials

# Start Supabase locally
supabase start

# Run migrations
supabase db push

# Start development
pnpm dev
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | ✅ |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | ✅ |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key | ✅ |
| `STRIPE_SECRET_KEY` | Stripe API key | ⚠️ For payments |

---

## Known Issues & Workarounds

### Issue 1: Hydration Mismatch
**Location:** `src/components/ThemeProvider.tsx`
**Workaround:** Use `suppressHydrationWarning` on html element
**Proper Fix:** Wait for Next.js 15 fix or implement custom solution

### Issue 2: Slow Initial Load
**Location:** Dashboard page
**Cause:** Loading all team members on mount
**Workaround:** Implement pagination
**Status:** TODO in Phase 7

---

## Recommended Next Steps

### Immediate (Next Session)
1. Complete `DashboardLayout` component
2. Add loading states to all pages
3. Implement error boundaries

### Short-term (This Week)
1. Finish settings page
2. Add team invitation flow
3. Write unit tests for services

### Medium-term (This Sprint)
1. Implement notification system
2. Add analytics tracking
3. Performance optimization pass

---

## Contacts & Resources

### Documentation
- [Supabase Docs](https://supabase.com/docs)
- [Next.js App Router](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Project Links
- Repository: github.com/user/my-saas-app
- Staging: staging.myapp.com
- Production: myapp.com

---

## Cost & Budget

| Phase | Estimated | Actual | Status |
|-------|-----------|--------|--------|
| 1. Setup | $0.15 | $0.12 | ✅ |
| 2. Database | $0.35 | $0.38 | ✅ |
| 3. Auth | $0.55 | $0.52 | ✅ |
| 4. API | $0.85 | $0.91 | ✅ |
| 5. Frontend | $1.20 | $0.80 | 🔄 60% |
| 6-10 | $3.50 | - | ⏳ |
| **Total** | **$6.60** | **$2.73** | |

**Remaining Budget:** $3.87 estimated

---

*Generated by Autopilot v3.0*
```

### Phase-Specific Handoff

```bash
/autopilot:handoff --scope=phase
```

Generates handoff focused on current phase only.

### Feature-Specific Handoff

```bash
/autopilot:handoff --scope=feature --feature="user-auth"
```

Generates handoff for a specific feature.

---

## Behavior

```
FUNCTION generateHandoff(options):

    # 1. Load project state
    projectState = loadProjectState()
    history = loadHistory()

    # 2. Determine scope
    IF options.scope == 'full':
        content = generateFullHandoff(projectState, history)
    ELIF options.scope == 'phase':
        content = generatePhaseHandoff(projectState.currentPhase)
    ELIF options.scope == 'feature':
        content = generateFeatureHandoff(options.feature)

    # 3. Add optional sections
    IF options.includeLearnings:
        content += generateLearningsSection(history.learnings)

    IF options.includeDecisions:
        content += generateDecisionsSection(projectState.decisions)

    IF options.onboarding:
        content += generateOnboardingSection()

    # 4. Format output
    IF options.format == 'json':
        content = convertToJson(content)
    ELIF options.format == 'html':
        content = convertToHtml(content)

    # 5. Write output
    outputPath = options.output OR ".autopilot/HANDOFF.md"
    writeFile(outputPath, content)

    LOG "Generated handoff document: {outputPath}"
```

---

## Handoff Checklist

### Before Handoff

- [ ] All changes committed
- [ ] Tests passing
- [ ] No critical bugs
- [ ] Environment documented
- [ ] Access credentials shared securely

### Handoff Contents

- [ ] Current state summary
- [ ] Architecture overview
- [ ] Key decisions with rationale
- [ ] Environment setup
- [ ] Known issues
- [ ] Next steps

---

## Quick Examples

```bash
# Full project handoff
/autopilot:handoff --scope=full

# Current phase only
/autopilot:handoff --scope=phase

# With learnings and decisions
/autopilot:handoff --include-learnings --include-decisions

# New team member onboarding
/autopilot:handoff --scope=full --onboarding

# JSON format for tooling
/autopilot:handoff --format=json --output=handoff.json
```

$ARGUMENTS
