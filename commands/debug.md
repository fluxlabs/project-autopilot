---
name: debug
description: Manage persistent debug sessions with binary search and pattern matching.
argument-hint: [--new] [--resume] [--bisect] [--pattern] [--result] [--close]
model: sonnet
---

# /autopilot:debug - Persistent Debug Sessions

// Project Autopilot - Debug Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Manage multi-session debugging with state persistence, binary search support, and error pattern matching.

**Visual Identity:** 🟡 Amber - Debugging

---

## Required Skills

- `/autopilot/skills/debug-sessions/SKILL.md` - Session management
- `/autopilot/skills/visual-style/SKILL.md` - Output formatting

## Required Agents

- `debugger` - Expert debugging agent

---

## Usage

```bash
# Start new debug session
/autopilot:debug --new "Login fails intermittently with 401 errors"

# Resume active session
/autopilot:debug --resume

# Binary search between commits
/autopilot:debug --bisect abc123 def456

# Report binary search result
/autopilot:debug --result good
/autopilot:debug --result bad

# Match error against patterns
/autopilot:debug --pattern "Cannot read property 'user' of null"

# View session history
/autopilot:debug --history

# Close session with resolution
/autopilot:debug --close "Fixed race condition in auth refresh"
```

---

## Commands

### --new "description"

Start a new debug session.

```
FUNCTION handleNew(description):
    # Check for existing active session
    IF hasActiveSession():
        LOG "⚠️ Active session exists: {activeSession.session_id}"
        LOG "Close it with: /autopilot:debug --close"
        LOG "Or resume it with: /autopilot:debug --resume"
        RETURN

    # Create new session
    session = startDebugSession(description)

    # Try pattern matching
    pattern = matchErrorPattern(description, "")
    IF pattern:
        LOG ""
        LOG "🔍 Pattern Matched: {pattern.name}"
        LOG "This looks like a {pattern.category} issue."
        LOG ""
        LOG "Common causes:"
        FOR each cause IN pattern.common_causes:
            LOG "  • {cause}"

    # Generate initial hypotheses
    hypotheses = generateInitialHypotheses(description, pattern)
    session.investigation.hypotheses = hypotheses

    saveActiveSession(session)

    LOG ""
    LOG "🐛 Debug Session Started: {session.session_id}"
    LOG ""
    LOG "Initial hypotheses:"
    FOR each h IN hypotheses:
        LOG "  [{h.id}] {h.description} ({h.likelihood})"
    LOG ""
    LOG "Next steps:"
    LOG "  1. Reproduce the issue"
    LOG "  2. Test hypotheses one by one"
    LOG "  3. Record findings with investigation"
```

### --resume

Resume active debug session.

```
FUNCTION handleResume():
    session = loadActiveSession()

    IF NOT session:
        LOG "❌ No active debug session"
        LOG "Start one with: /autopilot:debug --new 'description'"
        RETURN

    LOG "🐛 Resuming: {session.session_id}"
    LOG ""
    LOG "Bug: {session.bug.title}"
    LOG "Status: {session.status}"
    LOG "Phase: {session.investigation.phase}"
    LOG ""

    # Show hypotheses
    LOG "Hypotheses:"
    FOR each h IN session.investigation.hypotheses:
        status_icon = getStatusIcon(h.status)
        LOG "  [{h.id}] {status_icon} {h.description} ({h.likelihood})"

    # Show findings
    IF session.findings.length > 0:
        LOG ""
        LOG "Findings:"
        FOR each f IN session.findings:
            LOG "  [{f.id}] {f.description}"

    # Show binary search status
    IF session.investigation.binary_search?.active:
        bs = session.investigation.binary_search
        LOG ""
        LOG "Binary Search Active:"
        LOG "  Testing: {bs.current_test}"
        LOG "  Range: {bs.range_commits} commits remaining"
        LOG "  Report: /autopilot:debug --result good|bad"

    # Spawn debugger agent
    SPAWN debugger WITH session_context
```

### --bisect good_commit bad_commit

Start binary search debugging.

```
FUNCTION handleBisect(good_commit, bad_commit):
    session = loadActiveSession()

    IF NOT session:
        LOG "❌ No active debug session"
        LOG "Start one with: /autopilot:debug --new 'description'"
        RETURN

    # Validate commits
    IF NOT commitExists(good_commit):
        ERROR "Commit not found: {good_commit}"
    IF NOT commitExists(bad_commit):
        ERROR "Commit not found: {bad_commit}"

    # Start binary search
    LOG "🔍 Starting Binary Search Debug"
    LOG ""
    LOG "Known good: {good_commit}"
    LOG "Known bad:  {bad_commit}"
    LOG ""

    commits = getCommitsBetween(good_commit, bad_commit)
    LOG "Commits to search: {commits.length}"
    LOG "Max iterations: {Math.ceil(log2(commits.length))}"
    LOG ""

    mid = binarySearchDebug(good_commit, bad_commit)

    LOG "Testing commit: {mid.hash}"
    LOG "Date: {mid.date}"
    LOG "Author: {mid.author}"
    LOG "Message: {mid.message}"
    LOG ""
    LOG "Checkout and test:"
    LOG "  git checkout {mid.hash}"
    LOG "  <run your test>"
    LOG "  git checkout -"
    LOG ""
    LOG "Then report: /autopilot:debug --result good|bad"
```

### --result good|bad

Report binary search test result.

```
FUNCTION handleResult(result):
    session = loadActiveSession()

    IF NOT session:
        ERROR "No active debug session"

    IF NOT session.investigation.binary_search?.active:
        ERROR "No binary search in progress"

    IF result NOT IN ["good", "bad"]:
        ERROR "Result must be 'good' or 'bad'"

    # Process result
    breaking_commit = reportBinarySearchResult(result)

    IF breaking_commit:
        # Found it!
        LOG "🎯 Found Breaking Commit!"
        LOG ""
        LOG "Commit: {breaking_commit.hash}"
        LOG "Author: {breaking_commit.author}"
        LOG "Date:   {breaking_commit.date}"
        LOG "Message: {breaking_commit.message}"
        LOG ""
        LOG "Files changed:"
        FOR each file IN breaking_commit.files:
            LOG "  {file.status} {file.path}"
        LOG ""
        LOG "View changes: git show {breaking_commit.hash}"
    ELSE:
        # Continue search
        LOG "Result recorded. Continuing binary search..."
```

### --pattern "error message"

Match error against known patterns.

```
FUNCTION handlePattern(error_message):
    match = matchErrorPattern(error_message, "")

    IF match:
        LOG "🔍 Pattern Matched: {match.pattern.name}"
        LOG "Category: {match.pattern.category}"
        LOG "Confidence: {match.confidence}%"
        LOG ""
        LOG "Common causes:"
        FOR each cause IN match.pattern.common_causes:
            LOG "  • {cause}"
        LOG ""
        LOG "Debug steps:"
        FOR each step IN match.pattern.debug_steps:
            LOG "  {step}"
        LOG ""
        LOG "Example fix:"
        LOG "  {match.pattern.example_fix}"
    ELSE:
        LOG "❓ No matching pattern found"
        LOG ""
        LOG "Try providing more context or the full stack trace."
```

### --history

View debug session history.

```
FUNCTION handleHistory():
    sessions = loadAllSessions()

    LOG "📜 Debug Session History"
    LOG ""

    IF sessions.length == 0:
        LOG "No debug sessions found."
        RETURN

    LOG "| ID | Date | Bug | Status | Resolution |"
    LOG "|-----|------|-----|--------|------------|"

    FOR each session IN sessions:
        date = formatDate(session.created)
        bug = truncate(session.bug.title, 30)
        status = session.status
        resolution = session.resolution?.description OR "-"

        LOG "| {session.session_id} | {date} | {bug} | {status} | {resolution} |"

    LOG ""
    LOG "View details: /autopilot:debug --show <session_id>"
```

### --close "resolution"

Close active session with resolution.

```
FUNCTION handleClose(resolution_text):
    session = loadActiveSession()

    IF NOT session:
        ERROR "No active debug session"

    # Gather resolution details
    resolution = {
        description: resolution_text,
        commit: getCurrentCommit(),
        root_cause: session.findings[0]?.description OR "Not documented",
        prevention: inferPrevention(session)
    }

    closeDebugSession(resolution)

    LOG "✅ Debug Session Closed"
    LOG ""
    LOG "Session: {session.session_id}"
    LOG "Bug: {session.bug.title}"
    LOG "Resolution: {resolution.description}"
    LOG ""
    LOG "Session archived to: .autopilot/debug/sessions/{session.session_id}.json"
```

---

## Execution Flow

```
/autopilot:debug [options]

# Parse arguments
IF --new:
    handleNew(description)
ELSE IF --resume:
    handleResume()
ELSE IF --bisect:
    handleBisect(good_commit, bad_commit)
ELSE IF --result:
    handleResult(result)
ELSE IF --pattern:
    handlePattern(error_message)
ELSE IF --history:
    handleHistory()
ELSE IF --close:
    handleClose(resolution)
ELSE:
    # Default: resume or show help
    IF hasActiveSession():
        handleResume()
    ELSE:
        showHelp()
```

---

## Example Sessions

### Basic Debug Session

```
User: /autopilot:debug --new "TypeError: Cannot read property 'email' of null"

Claude: 🔍 Pattern Matched: Null Reference
This looks like a null_reference issue.

Common causes:
  • Missing null check before property access
  • Async timing issue - accessing before data loaded
  • Incorrect data shape from API response
  • State not initialized before render

🐛 Debug Session Started: debug-001

Initial hypotheses:
  [H1] Missing null check on user object (HIGH)
  [H2] User not loaded before render (MEDIUM)
  [H3] API returning unexpected shape (LOW)

Next steps:
  1. Reproduce the issue
  2. Test hypotheses one by one
  3. Record findings with investigation
```

### Binary Search Session

```
User: /autopilot:debug --bisect abc123 def456

Claude: 🔍 Starting Binary Search Debug

Known good: abc123 (2026-01-15)
Known bad:  def456 (2026-01-29)

Commits to search: 47
Max iterations: 6

Testing commit: ghi789
Date: 2026-01-22
Author: developer@example.com
Message: Refactor auth service

Checkout and test:
  git checkout ghi789
  <run your test>
  git checkout -

Then report: /autopilot:debug --result good|bad

---

User: /autopilot:debug --result bad

Claude: Result recorded. Continuing binary search...

Testing commit: jkl012
Date: 2026-01-18
...

---

User: /autopilot:debug --result good

Claude: 🎯 Found Breaking Commit!

Commit: mno345
Author: developer@example.com
Date:   2026-01-19
Message: Update token refresh logic

Files changed:
  M src/services/auth.ts
  M src/hooks/useAuth.ts

View changes: git show mno345
```

---

## State Persistence

Debug sessions persist across Claude restarts:
- Session state saved to `.autopilot/debug/active-session.json`
- Binary search progress preserved
- Hypotheses and findings retained
- Resume exactly where you left off

---

## Integration with debugger Agent

When resuming a session, the debugger agent receives:
- Full session context
- Pattern match results
- Current hypotheses and their status
- Previous test results
- Binary search state if active

This enables continuation without re-explaining the problem.
