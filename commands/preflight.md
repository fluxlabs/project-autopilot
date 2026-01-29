---
name: preflight
description: Gather phase context through structured gray-area identification, 4-question decision loops, and scope creep detection.
argument: phase_number
---

<!--
CAPABILITY NOTE FOR CLAUDE:
All pseudocode in this file (SPAWN, parallel_spawn, etc.) maps to Claude Code tools:
- SPAWN agent → Task tool with subagent_type="autopilot:{agent}"
- parallel_spawn([...]) → Multiple Task tool calls in single message
- Read/Write files → Read, Write, Edit tools
- Bash commands → Bash tool

You CAN and SHOULD execute this workflow. See /CLAUDE.md for full mapping.
-->

# /autopilot:preflight - Pre-Flight Briefing

// Project Autopilot - Pre-Flight Briefing Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Identify gray areas, capture decisions, and prevent scope creep BEFORE planning, so execution requires zero questions.

**Visual Identity:** 🟣 Purple - Discussion/Discovery

---

## Required Skills

- `/autopilot/skills/preflight-protocol/SKILL.md` - Core preflight protocol
- `/autopilot/skills/decision-logging/SKILL.md` - Decision capture (when available)

---

## Why This Matters

Without PREFLIGHT:
- Questions pop up during execution
- Context switches break flow
- Decisions scattered across sessions

With PREFLIGHT:
- All decisions captured upfront in BRIEFING.md
- Downstream agents read decisions autonomously
- "Claude's Discretion" sections eliminate micro-questions

---

## Input Required

```
/autopilot:preflight <phase_number>
/autopilot:preflight <phase_number> --skip      # Minimal BRIEFING.md
/autopilot:preflight <phase_number> --resume    # Continue previous session
```

**Prerequisites:**
- `.autopilot/flightplan.md` exists with phase defined
- Phase has clear goal/objective

---

## Gray Area Identification

### What Are Gray Areas?

Implementation decisions where multiple valid approaches exist:

**GOOD gray areas (phase-specific, actionable):**
- "Layout style — Cards vs list vs timeline?"
- "Loading behavior — Infinite scroll or pagination?"
- "Data format — JSON, CSV, or both?"
- "Auth method — JWT vs session cookies?"
- "Error handling — Toast notifications or inline errors?"

**BAD gray areas (generic, not actionable):**
- "UI" (too vague)
- "UX" (not actionable)
- "Behavior" (what behavior?)
- "Design" (be specific)

### Identification Process

```
1. Read phase goal from flightplan.md
2. Analyze phase scope for decision points
3. Generate 4-8 phase-specific gray areas
4. Present as multi-select checkboxes
5. User picks which to discuss (can skip all)
```

### Multi-Select UI Pattern

```
📋 Phase 3: User Dashboard

Goal: "Create user dashboard with activity feed and settings"

I've identified these gray areas. Which should we discuss?

☑️ Layout style — Sidebar navigation vs top tabs?
☑️ Activity feed — Real-time updates or manual refresh?
☐ Settings organization — Single page or categorized sections?
☐ Data density — Compact view or spacious cards?
☑️ Mobile behavior — Responsive or separate mobile view?

Options:
[ ] Select all
[ ] Clear all

[Continue with selected]  [Skip all - Claude decides everything]
```

---

## 4-Question Decision Loop

For each selected gray area, run a focused 4-question loop.

### Loop Protocol

```
FOR each selected gray area:
    question_count = 0

    WHILE question_count < 4:
        question_count += 1

        # Present question with concrete options
        PRESENT {
            question: "How should [area] work?",
            options: [
                {id: "A", label: "[Option A]", description: "[What this means]"},
                {id: "B", label: "[Option B]", description: "[What this means]"},
                {id: "C", label: "[Option C]", description: "[What this means]"},
                {id: "claude", label: "Claude decides", description: "Delegate to Claude's judgment"}
            ]
        }

        # Handle response
        IF user_selects("claude"):
            markAsAutonomous(area, "User said 'you decide'")
            BREAK  # Move to next area

        captureDecision(area, user_selection)

        # Check if area is resolved
        IF isAreaResolved(area, decisions):
            BREAK

        # After 4 questions, offer continuation
        IF question_count == 4:
            PRESENT "More about this area, or move on?"
            IF "move on":
                BREAK
            ELSE:
                question_count = 0  # Allow more questions
```

### Question Progression

| Round | Focus | Example Question |
|-------|-------|------------------|
| 1 | Core approach | "Sidebar or top tabs?" |
| 2 | Key variation | "Always visible or collapsible?" |
| 3 | Edge behavior | "What happens when empty?" |
| 4 | Polish details | "Animation on expand?" |

### Question Rules

**DO:**
- Ask about HOW user imagines it working
- Ask about WHAT it should feel/look like
- Ask about WHAT'S essential vs nice-to-have
- Offer "Claude decides" for EVERY question
- Use concrete options, not open-ended questions

**DON'T:**
- Ask about codebase patterns (read the code)
- Ask about technical implementation details
- Ask about success metrics (infer from work)
- Ask generic "what do you want" questions
- Exceed 4 questions without user consent

---

## Claude's Discretion

### Default Autonomous Areas

These are ALWAYS in Claude's discretion unless user explicitly overrides:

```yaml
always_autonomous:
  styling:
    - Exact spacing/padding values
    - Animation timing and easing
    - Border radius values
    - Shadow depths

  code:
    - Code organization within patterns
    - Variable naming within conventions
    - Internal function structure

  content:
    - Error message wording
    - Placeholder text content
    - Loading indicator text
```

### Marking Protocol

When user selects "Claude decides":
1. Log the area as autonomous
2. Record reason: "User said 'you decide'"
3. Add to "Claude's Discretion" section in BRIEFING.md

When area is not discussed:
1. Mark as "Not discussed"
2. Add to Claude's Discretion with reason: "Not discussed, Claude chooses"

---

## Scope Creep Detection

### Detection Triggers

Watch for user input containing:
- "We could also..."
- "It would be nice to..."
- "Later we should..."
- "What about adding..."
- "Can we also..."

### Response Pattern

When scope creep detected:

```
"[Feature X] sounds like a new capability — that belongs in its own phase.
I'll note it as a deferred idea.

Back to [current area]: [return to current question]"
```

### Deferred Ideas Capture

```
FUNCTION handleScopeCreep(feature, context):
    # Add to deferred ideas list
    deferred_ideas.add({
        feature: feature,
        mentioned_during: current_gray_area,
        suggested_phase: inferPhase(feature),
        timestamp: now()
    })

    # Log to user
    LOG "Noted: {feature} → Deferred Ideas"

    # Return to discussion flow
    returnToCurrentQuestion()
```

---

## Output: BRIEFING.md

Generate `.autopilot/phases/{phase}/BRIEFING.md`:

```markdown
# Phase {N}: {Name} - Pre-Flight Briefing

// Project Autopilot - Phase Briefing
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Generated:** {timestamp}
**Phase Goal:** {from flightplan}

---

## Phase Boundary

{What this phase delivers - scope anchor from flightplan}

**In Scope:**
- {Deliverable 1}
- {Deliverable 2}

**Out of Scope:**
- {Explicitly excluded}

---

## Implementation Decisions

### {Category 1 - discussed}
**Gray Area:** {original question}
**Decision:** {selected option}

- {Specific detail captured}
- {Additional context from follow-up}

### {Category 2 - discussed}
**Gray Area:** {original question}
**Decision:** {selected option}

- {Decision captured}

---

## Claude's Discretion

These areas are delegated to Claude's judgment:

### User Delegated
- {Area 1} - User said "you decide"
- {Area 2} - User selected "Claude decides"

### Not Discussed
- {Area 3} - Not selected for discussion
- {Area 4} - Skipped

### Default Autonomous
- Exact spacing/padding values
- Animation timing and easing
- Error message wording
- Code organization within patterns

---

## Specific Ideas

{References, examples, "I want it like X" from discussion}

- "{Exact quote from user}"
- "{Reference to existing product}"

---

## Deferred Ideas

{Features mentioned but belong in other phases}

| Feature | Mentioned During | Suggested Phase |
|---------|------------------|-----------------|
| {Deferred feature 1} | Layout discussion | Phase {N+X} |
| {Out of scope item 2} | Behavior discussion | Future consideration |

---

## Technical Context

{Auto-captured from codebase analysis}

### Existing Patterns
- {Pattern detected in code}
- {Convention to follow}

### Dependencies
**Requires from earlier phases:**
- {What this phase depends on}

**Provides for later phases:**
- {What depends on this phase}

### Integration Points
| From | To | Via |
|------|-----|-----|
| {Component} | {Service} | {Method} |
```

---

## Execution Flow

```
/autopilot:preflight {phase}

# 1. Load context
Read .autopilot/flightplan.md
Read .autopilot/TRANSPONDER.md (if exists)
Read existing codebase patterns

# 2. Generate and present gray areas
Analyze phase goal and scope
Generate 4-8 phase-specific gray areas
PRESENT multi-select: "Which areas should we discuss?"

# 3. Discussion loops
FOR each selected area:
    Run 4-question loop
    ON each user input: Check for scope creep
    Capture decisions
    Mark "Claude decides" areas

# 4. Capture deferred ideas
Any out-of-scope mentions → Deferred Ideas section

# 5. Generate BRIEFING.md
Write to .autopilot/phases/{phase}/BRIEFING.md

# 6. Update TRANSPONDER.md
Status: "Ready to plan"
Last activity: "Preflight complete for phase {N}"

# 7. Present next action
"Phase {N} briefing complete. Ready to file flight plan."
"Next: /autopilot:takeoff {phase} --plan-only"
```

---

## Example Session

```
User: /autopilot:preflight 3

Claude: 📋 Phase 3: User Dashboard

Goal: "Create user dashboard with activity feed and settings"

I've identified these gray areas. Which should we discuss?

☑️ Layout style — Sidebar navigation vs top tabs?
☑️ Activity feed — Real-time updates or manual refresh?
☐ Settings organization — Single page or categorized sections?
☐ Data density — Compact view or spacious cards?
☑️ Mobile behavior — Responsive or separate mobile view?

[User selects 3 areas: Layout, Activity feed, Mobile]

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

[User selects "Breakpoint"]

Claude: Got it - auto-collapse at 1024px. One more question:

For collapsed state, what should be visible?

1. **Icons only** - Show icon strip
2. **Nothing** - Fully hidden until expanded
3. **Mini labels** - Icons with truncated labels
4. **Claude decides**

[User selects "Claude decides"]

Claude: Noted - I'll decide the collapsed state details.

Moving to Activity feed...

User: "Oh, we should also add dark mode"

Claude: "Dark mode" sounds like a new capability — that belongs in its own phase.
I'll note it as a deferred idea.

Back to Activity feed: Should updates appear in real-time?

1. **Real-time** - WebSocket push, instant updates
2. **Polling** - Check every 30s for updates
3. **Manual refresh** - User pulls to refresh
4. **Claude decides**

[... continues for remaining questions ...]

Claude: ✅ Phase 3 pre-flight briefing complete!

Created: .autopilot/phases/03-user-dashboard/BRIEFING.md

## Summary
- Layout: Hybrid sidebar (collapses at 1024px)
- Activity: Real-time with WebSocket
- Mobile: Responsive with bottom nav

## Claude's Discretion
- Collapsed state appearance
- Settings organization
- Data density
- Animation details

## Deferred Ideas
- Dark mode → Phase 5

Next: /autopilot:takeoff 3 --plan-only
```

---

## Integration with Pipeline

```
PREFLIGHT → BRIEFING.md
    ↓
FLIGHTPLAN (reads BRIEFING.md) → ROUTE.md
    ↓
TAKEOFF (reads BRIEFING.md for edge cases) → LOGBOOK.md
```

**Key:** Downstream agents read BRIEFING.md and decide autonomously within captured decisions. No questions during execution.

---

## Options

### --skip
Skip preflight briefing, generate minimal BRIEFING.md:
- Phase boundary from flightplan
- All areas marked "Claude's Discretion"
- No specific decisions captured

```
/autopilot:preflight 3 --skip
```

**Warning:** More questions may arise during execution.

### --resume
Resume a previous incomplete preflight session:

```
/autopilot:preflight 3 --resume
```

Loads discussion state from `.autopilot/phases/{phase}/preflight-state.json`

---

## Backward Compatibility

This enhanced preflight command is fully backward compatible with existing Autopilot projects:
- Existing BRIEFING.md files are respected
- Old format CONTEXT.md files are readable by new planners (will be migrated)
- New features (scope creep detection, decision logging) are additive

$ARGUMENTS
