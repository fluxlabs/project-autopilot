---
name: discuss
description: Gather phase context through gray-area identification before planning. Eliminates questions during execution.
argument: phase_number
---

# /autopilot:discuss - Phase Context Gathering

// Project Autopilot - Phase Discussion Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Identify gray areas and capture decisions BEFORE planning, so execution requires zero questions.

**Visual Identity:** 🟣 Purple - Discussion/Discovery

---

## Why This Matters

Without DISCUSS:
- Questions pop up during execution
- Context switches break flow
- Decisions scattered across sessions

With DISCUSS:
- All decisions captured upfront in CONTEXT.md
- Downstream agents read decisions autonomously
- "Claude's Discretion" sections eliminate micro-questions

---

## Input Required

```
/autopilot:discuss <phase_number>
```

**Prerequisites:**
- `.autopilot/roadmap.md` exists with phase defined
- Phase has clear goal/objective

---

## Gray Area Identification

### What Are Gray Areas?

Implementation decisions where multiple valid approaches exist:

**GOOD gray areas (phase-specific):**
- "Layout style — Cards vs list vs timeline?"
- "Loading behavior — Infinite scroll or pagination?"
- "Data format — JSON, CSV, or both?"
- "Auth method — JWT vs session cookies?"

**BAD gray areas (generic categories):**
- "UI" (too vague)
- "UX" (not actionable)
- "Behavior" (what behavior?)

### Identification Process

```
1. Read phase goal from roadmap.md
2. Read any existing codebase patterns
3. Identify 4-8 phase-specific gray areas
4. Present as multiselect checkboxes
5. User picks which to discuss (can skip all)
```

---

## Discussion Protocol

### The 4-Question Loop

For each selected gray area:

```
LOOP (max 4 questions per area):
    1. Ask concrete decision question
    2. Present 2-4 specific options + "Claude decides"
    3. User selects option(s)
    4. IF user selects "Claude decides":
         Mark as autonomous area
         BREAK
    5. IF 4 questions asked:
         Ask: "More about this area, or move on?"
         IF "move on": BREAK
```

### Question Rules

**DO:**
- Ask about HOW user imagines it working
- Ask about WHAT it should feel/look like
- Ask about WHAT'S essential vs nice-to-have
- Offer "Claude decides" for every question

**DON'T:**
- Ask about codebase patterns (read the code)
- Ask about technical implementation details
- Ask about success metrics (infer from work)
- Ask generic "what do you want" questions

### Scope Creep Prevention

If user mentions something outside phase:

```
"[Feature X] sounds like a new capability — that belongs in its own phase.
I'll note it as a deferred idea.

Back to [current area]: [return to current question]"
```

---

## Output: CONTEXT.md

Generate `.autopilot/phases/{phase}/CONTEXT.md`:

```markdown
# Phase {N}: {Name} - Context

**Generated:** {timestamp}
**Phase Goal:** {from roadmap}

---

## Phase Boundary

{What this phase delivers - scope anchor from roadmap}

---

## Implementation Decisions

### {Category 1 - discussed}
- {Decision captured}
- {Specific choice made}

### {Category 2 - discussed}
- {Decision captured}

---

## Claude's Discretion

These areas are delegated to Claude's judgment:

- {Area 1} - User said "you decide"
- {Area 2} - Not discussed, Claude chooses
- Exact spacing/padding values
- Animation timing and easing
- Error message wording
- Code organization within patterns

---

## Specific Ideas

{References, examples, "I want it like X" from discussion}

- {Specific idea mentioned}
- {Reference to existing product}

---

## Deferred Ideas

{Features mentioned but belong in other phases}

- {Deferred feature} → Phase {N+X}
- {Out of scope item} → Future consideration

---

## Technical Context

{Auto-captured from codebase analysis}

### Existing Patterns
- {Pattern detected in code}
- {Convention to follow}

### Dependencies
- {What this phase depends on}
- {What depends on this phase}
```

---

## Execution Flow

```
/autopilot:discuss {phase}

# 1. Load context
Read .autopilot/roadmap.md
Read .autopilot/STATE.md (if exists)
Read existing codebase patterns

# 2. Identify gray areas
Analyze phase goal
Generate 4-8 phase-specific gray areas
Present as multiselect: "Which areas should we discuss?"

# 3. Discussion loops
FOR each selected area:
    Run 4-question loop
    Capture decisions
    Mark "Claude decides" areas

# 4. Capture deferred ideas
Any out-of-scope mentions → Deferred Ideas section

# 5. Generate CONTEXT.md
Write to .autopilot/phases/{phase}/CONTEXT.md

# 6. Update STATE.md
Status: "Ready to plan"
Last activity: "Discussed phase {N}"

# 7. Present next action
"Phase {N} context captured. Ready to plan."
"Next: /autopilot:build {phase} --plan-only"
```

---

## Example Session

```
User: /autopilot:discuss 3

Claude: 📋 Phase 3: User Dashboard

Goal: "Create user dashboard with activity feed and settings"

I've identified these gray areas. Which should we discuss?

☑️ Layout style — Sidebar navigation vs top tabs?
☑️ Activity feed — Real-time updates or manual refresh?
☐ Settings organization — Single page or categorized sections?
☐ Data density — Compact view or spacious cards?
☑️ Mobile behavior — Responsive or separate mobile view?

[User selects 3 areas]

Claude: Let's start with Layout style.

How do you envision the dashboard navigation?

1. **Sidebar** - Always visible, vertical menu (like Notion)
2. **Top tabs** - Horizontal tabs below header (like GitHub)
3. **Hybrid** - Collapsible sidebar on desktop, bottom nav on mobile
4. **Claude decides** - I'll choose based on content structure

[User selects "Hybrid"]

Claude: Hybrid it is. For the sidebar behavior:

When should the sidebar collapse?

1. **User toggle** - Manual expand/collapse button
2. **Breakpoint** - Auto-collapse below 1024px
3. **Hover expand** - Collapsed by default, expands on hover
4. **Claude decides**

[... continues for 2 more questions ...]

Claude: Moving to Activity feed...

[... 4 questions about activity feed ...]

Claude: Finally, Mobile behavior...

[... 4 questions about mobile ...]

Claude: ✅ Phase 3 context captured!

Created: .autopilot/phases/03-user-dashboard/CONTEXT.md

## Summary
- Layout: Hybrid sidebar (collapsible at 1024px)
- Activity: Real-time with WebSocket
- Mobile: Responsive with bottom nav

## Claude's Discretion
- Settings organization
- Data density
- Animation details
- Exact breakpoints

Next: /autopilot:build 3 --plan-only
```

---

## Integration with Pipeline

```
DISCUSS → CONTEXT.md
    ↓
PLAN (reads CONTEXT.md) → PLAN.md
    ↓
EXECUTE (reads CONTEXT.md for edge cases) → SUMMARY.md
```

**Key:** Downstream agents read CONTEXT.md and decide autonomously within captured decisions. No questions during execution.

---

## Skip Discussion

If user wants to skip:

```
/autopilot:discuss 3 --skip
```

Generates minimal CONTEXT.md:
- Phase boundary from roadmap
- All areas marked "Claude's Discretion"
- No specific decisions captured

**Warning:** More questions may arise during execution.
