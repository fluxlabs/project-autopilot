---
description: Scan project to assess completion status with cost estimates for remaining work.
argument-hint: [--phase=N] [--deep] [--research]
model: sonnet
---

# Autopilot: RADAR Mode

// Project Autopilot - Radar Sweep Command
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Analyze this project and generate a completion status report with cost estimates, enhanced by historical data and deep research.

## Required Skills

**Read for cost estimation:**
- `/autopilot/skills/cost-estimation/SKILL.md` - Token estimation guidelines
- `/autopilot/skills/global-state/SKILL.md` - Historical data access

## Required Agents

- `history-tracker` - Find similar projects for estimation
- `project-researcher` - Deep codebase analysis (when --deep or --research)
- `phase-researcher` - Phase-specific research (when --research with phases)
- `research-synthesizer` - Combine research outputs (when --research)

---

## Your Task

### Step 0: Load Historical Context (FIRST)

```
FUNCTION loadHistoricalContext():

    # 1. Load global state if available
    globalDir = expandPath("~/.claude/autopilot/")
    IF exists(globalDir):
        config = readJSON(globalDir + "config.json")
        history = readJSON(globalDir + "history.json")
        learnings = readJSON(globalDir + "learnings.json")

        # 2. Detect tech stack
        techStack = detectTechStack(currentDir)

        # 3. Find similar projects
        similarProjects = SPAWN history-tracker → getSimilarProjects(techStack)

        IF similarProjects.length > 0:
            LOG "Found {N} similar projects in history"
            estimationData = {
                hasSimilar: true,
                projects: similarProjects,
                avgCost: calculateAvgCost(similarProjects),
                avgPhases: calculateAvgPhases(similarProjects),
                accuracy: learnings.estimationAccuracy.overall
            }
        ELSE:
            estimationData = { hasSimilar: false }

    ELSE:
        estimationData = { hasSimilar: false }
        LOG "No global history found. Using base estimates."
        LOG "Tip: Run /autopilot:config to set up cross-session persistence"

    RETURN estimationData
```

### Step 0.5: Research Phase (NEW - when --deep or --research)

```
FUNCTION runResearchPhase(options):
    """
    Run research agents before cost estimation for more accurate analysis.
    Stores output in .autopilot/research/
    """

    # Ensure research directory exists
    ensureDir(".autopilot/research/")

    # 1. Always run project-researcher for deep scans
    IF options.deep OR options.research:
        LOG "🔍 Running deep codebase analysis..."

        SPAWN project-researcher
        WAIT for PROJECT-RESEARCH.md

        LOG "✅ Project research complete: .autopilot/research/PROJECT-RESEARCH.md"

    # 2. Run phase researchers if phases specified
    IF options.research AND options.phases:
        LOG "🎯 Running phase-specific research..."

        # Spawn phase researchers in parallel
        FOR each phase IN options.phases:
            SPAWN phase-researcher(phase) &

        WAIT all complete

        LOG "✅ Phase research complete"

        # 3. Synthesize all research
        LOG "🔗 Synthesizing research outputs..."

        SPAWN research-synthesizer
        WAIT for LOGBOOK.md

        LOG "✅ Research synthesis complete: .autopilot/research/LOGBOOK.md"

    RETURN {
        project_research: loadIfExists(".autopilot/research/PROJECT-RESEARCH.md"),
        phase_researches: loadPhaseResearches(options.phases),
        summary: loadIfExists(".autopilot/research/LOGBOOK.md")
    }
```

### Step 0.7: GSD Detection (NEW)

```
FUNCTION detectGSDProject():
    """
    Detect existing GSD project and offer import.
    """

    IF exists(".planning/"):
        LOG "🔍 Detected GSD project structure"

        gsd_artifacts = {
            project: readIfExists(".planning/PROJECT.md"),
            roadmap: readIfExists(".planning/ROADMAP.md"),
            phases: glob(".planning/phases/*.md"),
            discussions: glob(".planning/discussions/*.md"),
            contexts: glob(".planning/phases/*/CONTEXT.md"),
            plans: glob(".planning/phases/*/PLAN.md")
        }

        # Count what exists
        artifact_count = countNonNull(gsd_artifacts)

        IF artifact_count > 0:
            LOG ""
            LOG "Found GSD artifacts:"
            IF gsd_artifacts.project:
                LOG "  📄 PROJECT.md"
            IF gsd_artifacts.roadmap:
                LOG "  📄 ROADMAP.md"
            IF gsd_artifacts.phases.length > 0:
                LOG "  📁 {gsd_artifacts.phases.length} phase files"
            IF gsd_artifacts.discussions.length > 0:
                LOG "  📁 {gsd_artifacts.discussions.length} discussions"
            IF gsd_artifacts.contexts.length > 0:
                LOG "  📁 {gsd_artifacts.contexts.length} context files"
            IF gsd_artifacts.plans.length > 0:
                LOG "  📁 {gsd_artifacts.plans.length} plan files"

            LOG ""
            LOG "Would you like to import GSD artifacts into Autopilot format?"
            LOG "This preserves original files and creates .autopilot/ structure."
            LOG ""
            LOG "Type 'import' to import, or 'skip' to scan without import."

            response = waitForUserResponse()

            IF response == "import":
                importedResult = importGSDToAutopilot(gsd_artifacts)
                LOG ""
                LOG "✅ Imported {importedResult.phases} phases from GSD"
                LOG "   Original files preserved in .planning/"
                LOG ""
                RETURN {imported: true, result: importedResult}

        RETURN {imported: false, gsd_detected: true}

    RETURN {imported: false, gsd_detected: false}
```

### GSD Import Function

```
FUNCTION importGSDToAutopilot(gsd_artifacts):
    """
    Import GSD project structure into Autopilot format.
    Preserves original GSD files.
    """

    # Ensure .autopilot/ exists
    ensureDir(".autopilot/")
    ensureDir(".autopilot/phases/")

    imported = {
        phases: 0,
        decisions: 0,
        contexts: 0
    }

    # 1. Import PROJECT.md → clearance.md
    IF gsd_artifacts.project:
        LOG "  Importing PROJECT.md..."
        project = parseGSDProject(gsd_artifacts.project)
        writeAutopilotScope(project)
        LOG "    ✓ Created .autopilot/clearance.md"

    # 2. Import ROADMAP.md → flightplan.md
    IF gsd_artifacts.roadmap:
        LOG "  Importing ROADMAP.md..."
        roadmap = parseGSDRoadmap(gsd_artifacts.roadmap)
        writeAutopilotRoadmap(roadmap)
        LOG "    ✓ Created .autopilot/flightplan.md"

    # 3. Import phases
    FOR each phase_file IN gsd_artifacts.phases:
        LOG "  Importing {basename(phase_file)}..."
        phase = parseGSDPhase(phase_file)
        phase_dir = ".autopilot/phases/{pad(phase.number, 3)}/"
        ensureDir(phase_dir)

        # Convert to Autopilot phase format
        writeAutopilotPhase(phase_dir, phase)
        imported.phases += 1
        LOG "    ✓ Created {phase_dir}PHASE.md"

    # 4. Import discussions as BRIEFING.md
    FOR each discussion IN gsd_artifacts.discussions:
        LOG "  Importing discussion..."
        context = parseGSDDiscussion(discussion)
        phase_dir = ".autopilot/phases/{pad(context.phase, 3)}/"

        IF exists(phase_dir):
            writeAutopilotContext(phase_dir, context)
            imported.contexts += 1
            LOG "    ✓ Created {phase_dir}BRIEFING.md"

    # 5. Import existing CONTEXT.md files as BRIEFING.md
    FOR each context_file IN gsd_artifacts.contexts:
        phase_num = extractPhaseNumber(context_file)
        LOG "  Importing context for phase {phase_num}..."
        context = parseGSDContext(context_file)
        phase_dir = ".autopilot/phases/{pad(phase_num, 3)}/"

        IF exists(phase_dir) AND NOT exists(phase_dir + "BRIEFING.md"):
            copyFile(context_file, phase_dir + "BRIEFING.md")
            imported.contexts += 1
            LOG "    ✓ Copied BRIEFING.md"

    # 6. Import PLAN.md files as ROUTE.md
    FOR each plan_file IN gsd_artifacts.plans:
        phase_num = extractPhaseNumber(plan_file)
        LOG "  Importing plan for phase {phase_num}..."
        phase_dir = ".autopilot/phases/{pad(phase_num, 3)}/"

        IF exists(phase_dir) AND NOT exists(phase_dir + "ROUTE.md"):
            plan = parseGSDPlan(plan_file)
            writeAutopilotPlan(phase_dir, plan)
            LOG "    ✓ Created {phase_dir}ROUTE.md"

    # 7. Create initial TRANSPONDER.md
    createInitialState(imported.phases)

    LOG ""
    LOG "Import complete:"
    LOG "  Phases: {imported.phases}"
    LOG "  Briefings: {imported.contexts}"
    LOG ""
    LOG "Original GSD files preserved in .planning/"

    RETURN imported

FUNCTION parseGSDProject(content):
    """
    Parse GSD PROJECT.md into Autopilot clearance structure.
    """
    project = {
        name: extractSection(content, "Project Name"),
        description: extractSection(content, "Description"),
        requirements: extractSection(content, "Requirements"),
        tech_stack: extractSection(content, "Tech Stack"),
        mvp_scope: extractSection(content, "MVP Scope")
    }
    RETURN project

FUNCTION parseGSDRoadmap(content):
    """
    Parse GSD ROADMAP.md into Autopilot flightplan structure.
    """
    roadmap = {
        phases: [],
        milestones: []
    }

    # Extract phase definitions
    phase_matches = regexFindAll(content, r"## Phase (\d+): (.+)\n([\s\S]*?)(?=## Phase|\z)")

    FOR each match IN phase_matches:
        phase = {
            number: parseInt(match[1]),
            name: match[2].trim(),
            description: extractFirstParagraph(match[3]),
            goal: extractSection(match[3], "Goal"),
            tasks: extractTasks(match[3])
        }
        roadmap.phases.add(phase)

    RETURN roadmap

FUNCTION parseGSDPhase(content):
    """
    Parse GSD phase file into Autopilot phase structure.
    """
    phase = {
        number: extractPhaseNumber(content),
        name: extractSection(content, "name"),
        goal: extractSection(content, "Goal"),
        must_haves: extractMustHaves(content),
        assumptions: extractAssumptions(content),
        tasks: extractTasks(content)
    }
    RETURN phase

FUNCTION parseGSDDiscussion(content):
    """
    Parse GSD discussion into Autopilot BRIEFING.md format.
    """
    context = {
        phase: extractPhaseNumber(content),
        decisions: extractDecisions(content),
        claude_discretion: extractSection(content, "Claude's Discretion"),
        deferred_ideas: extractSection(content, "Deferred Ideas"),
        specific_ideas: extractSection(content, "Specific Ideas")
    }
    RETURN context
```

### Step 1: Read project configuration

- Check for `.autopilot/` folder (existing autopilot state)
- **Check for `.planning/` folder (GSD project - offer import)**
- Read CLAUDE.md, package.json, configs
- Understand the tech stack
- **Use PROJECT-RESEARCH.md if available** (from --deep scan)

### Step 2: Analyze codebase

- Scan all source files
- Identify implemented features
- Find TODOs, FIXMEs, incomplete code
- Check test coverage
- **Use research findings for deeper analysis**

### Step 3: Estimate remaining work (with historical adjustment)

- Calculate tasks needed per feature
- Apply cost estimation guidelines
- **Apply research-based insights if available**
- **Apply historical accuracy adjustment if available**
- Sum to project total

### Step 4: Generate scan report (with historical comparison)

Create `.autopilot/scan-report.md` with:

```markdown
# Radar Sweep Report: [Project Name]

// Project Autopilot - Radar Sweep Report
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Scanned:** [Date/Time]
**Scan Mode:** [Standard | Deep | Research]

---

## Project Overview
- **Type:** [Web app, API, CLI, etc.]
- **Stack:** [Technologies detected]
- **Size:** [File count, LOC estimate]

---

## 🔍 Research Findings (if --deep or --research)

### Codebase Analysis
*From PROJECT-RESEARCH.md*

| Aspect | Finding |
|--------|---------|
| Architecture | {pattern detected} |
| Test Coverage | {percentage} |
| Code Quality | {assessment} |
| Technical Debt | {level} |

### Key Patterns Detected
- {Pattern 1 with location}
- {Pattern 2 with location}

### Recommendations from Research
1. {Research-based recommendation}
2. {Research-based recommendation}

---

## 📊 Historical Context

*If similar projects found:*

### Similar Projects in History
| Project | Stack Match | Cost | Phases | Variance |
|---------|-------------|------|--------|----------|
| my-api | 90% | $4.85 | 8 | -7% |
| auth-service | 85% | $3.20 | 6 | +5% |
| user-mgmt | 80% | $5.10 | 9 | +12% |

**Historical Average:** $4.38 for similar projects
**Your Estimation Accuracy:** 94% (based on 12 projects)

### Adjusted Estimates
Estimates below are adjusted by your historical accuracy (+6% buffer)

*If no similar projects:*

### No Historical Data
This appears to be a new tech stack combination.
Run `/autopilot:config` to enable cross-session learning.

---

## 💰 Cost Estimate Summary

### Remaining Work Estimate
| Category | Tasks | Est. Tokens | Base Est. | Adjusted | Confidence |
|----------|-------|-------------|-----------|----------|------------|
| New Features | [N] | [X]K | $[Y] | $[Y*adj] | Medium |
| Bug Fixes | [N] | [X]K | $[Y] | $[Y*adj] | High |
| Tests | [N] | [X]K | $[Y] | $[Y*adj] | Medium |
| Documentation | [N] | [X]K | $[Y] | $[Y*adj] | High |
| Tech Debt | [N] | [X]K | $[Y] | $[Y*adj] | Low |
| **Total** | **[N]** | **[X]K** | **$[Y]** | **$[Y*adj]** | |

*Adjusted estimates include historical accuracy factor*

### Recommended Budget
| Type | Amount | Reasoning |
|------|--------|-----------|
| Adjusted Estimate | $[X] | Base + accuracy adjustment |
| Buffer (1.25x) | $[Y] | For unknowns |
| **Recommended** | **$[Z]** | Set --max-cost |
| Historical Avg | $[H] | Similar projects averaged |

---

## ✅ Completed Work

### [Feature Area]
| Feature | Status | Files | Evidence |
|---------|--------|-------|----------|
| [Feature] | ✅ Done | `file.ts` | Has tests, documented |

---

## 🟡 Partial Work

### [Feature Area]
| Feature | Status | Files | What's Missing | Est. Cost |
|---------|--------|-------|----------------|-----------|
| [Feature] | 🟡 ~60% | `file.ts` | No validation | $0.05 |

---

## ⏳ Remaining Work

### [Feature Area]
| Feature | Priority | Complexity | Tasks | Est. Cost |
|---------|----------|------------|-------|-----------|
| [Feature] | High | Medium | 4 | $0.15 |
| [Feature] | Medium | Simple | 2 | $0.05 |

### Estimated Phase Breakdown
| Phase | Description | Tasks | Est. Cost |
|-------|-------------|-------|-----------|
| Database | Schema changes | 3 | $0.12 |
| API | New endpoints | 5 | $0.25 |
| Frontend | UI components | 8 | $0.45 |
| Testing | Coverage | 6 | $0.20 |
| **Total** | | **22** | **$1.02** |

---

## Technical Debt
| Issue | Location | Severity | Est. Fix Cost |
|-------|----------|----------|---------------|
| [Issue] | `file:line` | High | $0.03 |
| [Issue] | `file:line` | Medium | $0.02 |

---

## Recommendations

### Do First
1. [Critical item] - Est: $[X]

### Short Term
1. [Important item] - Est: $[X]

---

## Next Steps

```bash
# Create flight plan from scan results (dry run first)
/autopilot:flightplan --from-scan --dry-run

# Create flight plan from scan with budget
/autopilot:flightplan --from-scan --max-cost=[recommended]

# Create the flight plan, then execute
/autopilot:flightplan --from-scan
/autopilot:takeoff

# Execute immediately without approval
/autopilot:takeoff -y

# Run with deep research first
/autopilot:radar --deep
/autopilot:flightplan --from-scan
```

**Recommended budget:** `--max-cost=$[Z]` based on estimates
```

### Step 5: Present findings

- Show the scan report with cost estimates
- Compare with historical data if available
- **Include research findings if available**
- Recommend appropriate budget
- Offer to generate phase files for remaining work

---

## Scan Options

### --deep
Run deep codebase analysis before scanning:
```bash
/autopilot:radar --deep
```

This spawns `project-researcher` to:
- Map complete codebase structure
- Identify tech stack and patterns
- Detect conventions
- Analyze test coverage

Output stored in `.autopilot/research/PROJECT-RESEARCH.md`

### --research
Run full research phase with phase-specific analysis:
```bash
/autopilot:radar --research
/autopilot:radar --research --phases=1,2,3
```

This spawns:
1. `project-researcher` → PROJECT-RESEARCH.md
2. `phase-researcher` (per phase) → RESEARCH.md
3. `research-synthesizer` → LOGBOOK.md

Output stored in `.autopilot/research/`

### --phase=N
Scan specific phase only:
```bash
/autopilot:radar --phase=3
```

---

## Research Integration

### Directory Structure

```
.autopilot/
├── research/
│   ├── PROJECT-RESEARCH.md    # From project-researcher
│   ├── LOGBOOK.md             # From research-synthesizer
│   └── phases/
│       ├── 01-RESEARCH.md     # From phase-researcher
│       ├── 02-RESEARCH.md
│       └── 03-RESEARCH.md
├── scan-report.md             # Scan output
└── ...
```

### Research Flow

```
/autopilot:radar --research

┌─────────────────────────────────────────────────────────┐
│  STEP 1: Project Research (parallel-ready)              │
│  ┌──────────────────────┐                               │
│  │  project-researcher  │ → PROJECT-RESEARCH.md         │
│  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Phase Research (parallel execution)            │
│  ┌──────────────────────┐                               │
│  │  phase-researcher(1) │ → 01-RESEARCH.md              │
│  └──────────────────────┘                               │
│  ┌──────────────────────┐                               │
│  │  phase-researcher(2) │ → 02-RESEARCH.md              │
│  └──────────────────────┘                               │
│  ┌──────────────────────┐                               │
│  │  phase-researcher(3) │ → 03-RESEARCH.md              │
│  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: Synthesis                                      │
│  ┌──────────────────────┐                               │
│  │  research-synthesizer│ → LOGBOOK.md                  │
│  └──────────────────────┘                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: Enhanced Scan Report                           │
│  Uses research findings for:                            │
│  - More accurate estimates                              │
│  - Better pattern detection                             │
│  - Informed recommendations                             │
└─────────────────────────────────────────────────────────┘
```

---

## Tips Based on History

*If historical data available:*

```markdown
## 💡 Tips from Similar Projects

Based on your history with [tech stack]:

1. **Setup Phase** - Usually 15% under estimate (you're efficient here)
2. **Frontend Phase** - Often 18% over estimate (add buffer)
3. **Common Issues:**
   - Missing env vars (happened 5x) - Add .env.example early
   - Type errors (happened 3x) - Use strict TS config

**Recommended approach:** Based on auth-service project pattern
```

---

## Historical Learning Integration

After scan completes, learnings are automatically applied:

| Phase Type | Your Avg Variance | Adjustment Applied |
|------------|-------------------|-------------------|
| Setup | -15% | Use base estimate |
| Database | +8% | +8% buffer |
| Auth | +12% | +12% buffer |
| API | +5% | +5% buffer |
| Frontend | +18% | +18% buffer |
| Testing | -5% | Use base estimate |

This improves estimate accuracy from ~85% to ~95% over time.

---

## GSD Project Detection

### Automatic Detection

When scanning, automatically detect GSD project structure:

```
.planning/                     # GSD project marker
├── PROJECT.md                 # Project definition
├── ROADMAP.md                 # Phase roadmap
├── phases/
│   ├── 1-setup.md             # Phase definition files
│   ├── 2-database.md
│   └── 3-api.md
└── discussions/               # Discussion captures
    └── phase-1-discussion.md
```

### Detection Protocol

```
FUNCTION scanWithGSDDetection():
    """
    Enhanced scan that detects and handles GSD projects.
    """

    # Check for GSD structure
    IF exists(".planning/"):
        LOG "🔍 Detected GSD project structure"

        # Also check for Autopilot structure
        IF exists(".autopilot/"):
            LOG "📁 Both .planning/ and .autopilot/ exist"
            LOG "   Using .autopilot/ as primary"
            # Continue with standard scan
        ELSE:
            # GSD-only project
            gsd_result = detectGSDProject()

            IF gsd_result.imported:
                LOG "✅ GSD project imported to Autopilot format"
                # Continue scan with newly imported structure
            ELSE IF gsd_result.gsd_detected:
                LOG "📋 GSD project detected but not imported"
                LOG "   Use --import-gsd to convert to Autopilot format"
                # Scan GSD structure directly
                RETURN scanGSDProject()

    # Standard Autopilot scan
    RETURN scanAutopilotProject()
```

### GSD Parser Functions

```
FUNCTION parseGSDProjectFile(path):
    """
    Parse GSD PROJECT.md format.
    """
    content = readFile(path)

    project = {
        name: extractMarkdownHeader(content, 1),
        milestone: extractSection(content, "Current Milestone"),
        vision: extractSection(content, "Vision"),
        requirements: extractSection(content, "Core Requirements"),
        tech_stack: extractSection(content, "Tech Stack"),
        constraints: extractSection(content, "Constraints"),
        success_criteria: extractSection(content, "Success Criteria")
    }

    RETURN project

FUNCTION parseGSDRoadmapFile(path):
    """
    Parse GSD ROADMAP.md format.
    """
    content = readFile(path)

    roadmap = {
        phases: [],
        dependencies: [],
        critical_path: []
    }

    # Extract phases
    phase_pattern = r"## Phase (\d+): ([^\n]+)\n([\s\S]*?)(?=## Phase|\Z)"
    matches = regexFindAll(content, phase_pattern)

    FOR each match IN matches:
        phase = {
            number: parseInt(match[1]),
            name: match[2].trim(),
            description: extractFirstParagraph(match[3]),
            goal: extractBulletPoint(match[3], "Goal"),
            delivers: extractBulletList(match[3], "Delivers"),
            depends_on: extractBulletList(match[3], "Depends on"),
            tasks: extractTaskList(match[3])
        }
        roadmap.phases.add(phase)

    RETURN roadmap

FUNCTION parseGSDPhaseFile(path):
    """
    Parse individual GSD phase file.
    """
    content = readFile(path)

    phase = {
        number: extractFromFilename(path) OR extractFrontmatter(content, "phase"),
        name: extractFrontmatter(content, "name") OR extractMarkdownHeader(content, 1),
        status: extractFrontmatter(content, "status") OR "pending",
        goal: extractSection(content, "Goal") OR extractSection(content, "Objective"),
        must_haves: extractGSDMustHaves(content),
        tasks: extractGSDTasks(content),
        assumptions: extractSection(content, "Assumptions")
    }

    RETURN phase

FUNCTION extractGSDMustHaves(content):
    """
    Extract GSD must-haves structure and convert to Autopilot format.
    """
    must_haves = {
        truths: [],
        artifacts: [],
        key_links: []
    }

    # Check for truths section
    truths_section = extractSection(content, "Truths")
    IF truths_section:
        truth_lines = extractBulletList(truths_section)
        FOR each line IN truth_lines:
            must_haves.truths.add({
                statement: line,
                verification: "manual"  # Default, can be overridden
            })

    # Check for artifacts section
    artifacts_section = extractSection(content, "Artifacts")
    IF artifacts_section:
        artifact_lines = extractBulletList(artifacts_section)
        FOR each line IN artifact_lines:
            path = extractPath(line)
            IF path:
                must_haves.artifacts.add({
                    path: path,
                    provides: line,
                    min_lines: 10  # Default
                })

    # Check for key links / connections
    links_section = extractSection(content, "Key Links") OR extractSection(content, "Connections")
    IF links_section:
        link_lines = extractBulletList(links_section)
        FOR each line IN link_lines:
            # Try to parse "A -> B" or "A connects to B" format
            parts = parseConnectionLine(line)
            IF parts:
                must_haves.key_links.add({
                    from: parts.from,
                    to: parts.to,
                    pattern: generatePatternFromConnection(parts),
                    description: line
                })

    RETURN must_haves
```

### Scan Report with GSD Info

When GSD project detected, scan report includes:

```markdown
## 📁 Project Structure

**Detected:** GSD project (.planning/)

| Format | Status | Files |
|--------|--------|-------|
| GSD (.planning/) | ✅ Present | 12 files |
| Autopilot (.autopilot/) | ❌ Missing | - |

### GSD Artifacts Found

| Artifact | Status |
|----------|--------|
| PROJECT.md | ✅ Found |
| ROADMAP.md | ✅ Found |
| Phase files | 6 phases |
| Plans | 3 ready |
| Contexts | 2 captured |

### Recommendation

```bash
# Import GSD to Autopilot for full feature access
/autopilot:radar --import-gsd

# Or build directly with GSD compatibility
/autopilot:takeoff
```
```

---

## Scan Options Summary

| Option | Description |
|--------|-------------|
| `--deep` | Run deep codebase analysis |
| `--research` | Full research with synthesis |
| `--phase=N` | Scan specific phase |
| `--import-gsd` | Import GSD project to Autopilot |
| `--gsd-only` | Scan GSD without import |

$ARGUMENTS
