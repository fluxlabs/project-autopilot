---
name: checkpoint-protocol
description: Human interaction protocol with automation-first rule. Defines checkpoint types and when to use them.
---

# Checkpoint Protocol

// Project Autopilot - Checkpoint Protocol Skill
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Golden Rule:** If it has CLI/API, Claude does it. Humans only do what requires judgment.

---

## Checkpoint Types

### Distribution

| Type | Frequency | When to Use |
|------|-----------|-------------|
| `checkpoint:human-verify` | 90% | User confirms it works |
| `checkpoint:decision` | 9% | User chooses between options |
| `checkpoint:human-action` | 1% | Truly unavoidable manual step |

---

## Type 1: Human-Verify (90%)

Claude automates everything, human just confirms it works.

### When to Use
- Visual verification (UI looks right)
- Interactive flows (click through app)
- Functional verification (feature works as expected)

### Format

```xml
<task type="auto">
  <name>Start dev server</name>
  <action>Run `npm run dev` in background</action>
  <verify>curl localhost:3000 returns 200</verify>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Dashboard - server at http://localhost:3000</what-built>
  <how-to-verify>
    Visit http://localhost:3000/dashboard and verify:
    1. Desktop (>1024px): sidebar visible, cards display data
    2. Mobile (375px): single column, bottom nav visible
    3. Click "Settings" - modal opens
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### Key Rules

- **Claude starts servers** - User never runs `npm run dev`
- **Claude sets up data** - User never creates test data
- **Claude provides URLs** - User just clicks links
- **User only looks** - Visual/functional confirmation

### Example Output

```markdown
🟢 checkpoint:human-verify

## Built: User Dashboard

**Server running:** http://localhost:3000/dashboard

### Please verify:
1. ✅ Page loads without errors
2. ✅ User data displays correctly
3. ✅ Sidebar navigation works
4. ✅ Mobile view is responsive

**Resume:** Type "approved" or describe issues
```

---

## Type 2: Decision (9%)

Human must make a choice affecting implementation.

### When to Use
- Technology selection (which library)
- Architecture decisions (approach A vs B)
- Design choices (layout, color, UX)
- Business logic (pricing, limits, rules)

### Format

```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Select authentication provider</decision>
  <context>
    Need user auth for the app. Three options with tradeoffs.
  </context>
  <options>
    <option id="supabase">
      <name>Supabase Auth</name>
      <pros>Built-in with DB, free tier generous, email templates</pros>
      <cons>Less customizable UI, vendor lock-in</cons>
    </option>
    <option id="clerk">
      <name>Clerk</name>
      <pros>Best DX, beautiful UI, social logins easy</pros>
      <cons>Paid after 10k MAU, another vendor</cons>
    </option>
    <option id="custom">
      <name>Custom JWT</name>
      <pros>Full control, no external dependencies</pros>
      <cons>More implementation work, security responsibility</cons>
    </option>
  </options>
  <resume-signal>Select: supabase, clerk, or custom</resume-signal>
</task>
```

### Key Rules

- **Present balanced options** - No prescriptive recommendation
- **Include context** - Why this decision matters
- **Show tradeoffs** - Pros AND cons for each
- **No "correct" answer** - All options are valid

### Example Output

```markdown
🟡 checkpoint:decision

## Decision Required: Authentication Provider

**Context:** Need user auth. Three approaches available.

| Option | Pros | Cons |
|--------|------|------|
| **Supabase** | Built-in, free tier | Less customizable |
| **Clerk** | Best DX, beautiful UI | Paid after 10k users |
| **Custom JWT** | Full control | More work |

**Select:** supabase, clerk, or custom
```

---

## Type 3: Human-Action (1% - RARE)

Truly unavoidable manual step. **Exhaust all automation first.**

### When to Use (Only These Cases)
- Email verification clicks (can't automate)
- 3D Secure / MFA in payment flow
- OAuth consent screens in browser
- Physical hardware interaction
- Captcha solving

### When NOT to Use
- ❌ Running CLI commands (Claude runs them)
- ❌ Creating accounts (Claude uses API/CLI)
- ❌ Starting servers (Claude runs them)
- ❌ Creating files (Claude creates them)
- ❌ Configuration (Claude edits files)
- ❌ Database setup (Claude runs migrations)

### Format

```xml
<task type="auto">
  <name>Create SendGrid account</name>
  <action>Use API to create account, request verification email</action>
</task>

<task type="checkpoint:human-action">
  <action>Complete email verification</action>
  <why-manual>Email verification requires clicking link in your inbox</why-manual>
  <instructions>
    1. Check your inbox for email from SendGrid
    2. Click the verification link
    3. Return here when done
  </instructions>
  <resume-signal>Type "done" when verified</resume-signal>
</task>
```

### Key Rules

- **Try automation FIRST** - Only ask for help when blocked
- **Explain why manual** - User should know why this can't be automated
- **Minimize steps** - Do everything possible before/after the manual step
- **Golden rule:** If it has CLI/API, Claude MUST do it

### Example Output

```markdown
🔴 checkpoint:human-action

## Manual Step Required: Email Verification

**Why manual:** Email verification links can't be automated

### Instructions:
1. Check your inbox for email from SendGrid
2. Click "Verify Email" button
3. Return here when done

**Resume:** Type "done" when verified
```

---

## Automation-First Checklist

Before using ANY checkpoint, ask:

```
□ Can I do this with a CLI command?
□ Can I do this with an API call?
□ Can I do this by editing a file?
□ Can I start/stop a server myself?
□ Can I create test data myself?
□ Can I run a script for this?
```

If ANY answer is YES → Don't ask user to do it.

---

## Common Anti-Patterns

### ❌ Wrong: Asking User to Run Commands

```markdown
Please run: npm run dev
```

### ✅ Right: Claude Runs Commands

```bash
# Claude executes
npm run dev &
# Then presents checkpoint
Visit http://localhost:3000 to verify
```

---

### ❌ Wrong: Asking User to Create Files

```markdown
Please create a file at src/config.ts with:
[content]
```

### ✅ Right: Claude Creates Files

```bash
# Claude creates the file
Write src/config.ts
# Done - no checkpoint needed
```

---

### ❌ Wrong: Asking User to Set Up Database

```markdown
Please create a PostgreSQL database called "myapp"
```

### ✅ Right: Claude Uses CLI

```bash
# Claude executes
createdb myapp
psql myapp < schema.sql
# Done - no checkpoint needed
```

---

### ❌ Wrong: Decision as Human-Action

```markdown
Should I use React or Vue?
Please choose and let me know.
```

### ✅ Right: Use Decision Checkpoint

```xml
<task type="checkpoint:decision">
  <decision>Frontend framework</decision>
  <options>
    <option id="react">React - Larger ecosystem</option>
    <option id="vue">Vue - Simpler learning curve</option>
  </options>
</task>
```

---

## Checkpoint Flow in Execution

```
FOR each plan:
    IF plan.autonomous == true:
        Execute all tasks automatically
        Generate SUMMARY.md

    ELSE IF plan has checkpoint:
        Execute tasks up to checkpoint

        SWITCH checkpoint.type:
            CASE human-verify:
                Present what was built
                Show verification steps
                WAIT for "approved" or issues

            CASE decision:
                Present options with tradeoffs
                WAIT for selection
                Continue with selected option

            CASE human-action:
                Present instructions
                WAIT for "done"

        Continue remaining tasks
        Generate SUMMARY.md
```

---

## Integration with Wave Execution

```yaml
# Plan with checkpoint (runs sequentially, not parallel)
---
phase: 3
plan: 06
wave: 3
autonomous: false
checkpoint:
  type: human-verify
  after_task: 4
  what: "Integration tests pass, dashboard functional"
depends_on: ["04", "05"]
---
```

- Plans with checkpoints are NOT spawned in parallel
- They run sequentially after parallel wave completes
- Checkpoint pauses execution until user responds
