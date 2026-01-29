---
name: risk-assessment
description: Risk-fronted planning with identification, mitigation, and contingency management.
---

# Risk Assessment Skill

// Project Autopilot - Risk-Fronted Planning
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Implement risk-fronted planning where risks are identified FIRST, mitigation tasks are generated automatically, and high-impact risks are de-risked early in each phase.

---

## Core Principle: De-Risk Early

Traditional approach:
```
Plan → Build → (Discover risk) → Scramble to fix
```

Risk-fronted approach:
```
Identify Risks → Plan Mitigations → Build with confidence
```

**Key insight:** Address high-impact risks early when you have the most flexibility and lowest cost to change.

---

## Risk Categories

### Technical Risks
- Architecture scalability limitations
- Integration complexity with external systems
- Performance bottlenecks under load
- Technical debt accumulation
- Data migration complexity
- Security vulnerabilities

### Integration Risks
- Third-party API reliability and rate limits
- Breaking changes in dependencies
- Version compatibility issues
- Data format mismatches
- Authentication/authorization handoffs

### Estimation Risks
- Scope underestimation
- Complexity hidden in requirements
- Unknown unknowns
- Dependency delays
- Learning curve underestimation

### External Risks
- Third-party service SLAs
- Vendor reliability
- Regulatory/compliance changes
- Market timing pressures

---

## Risk Register Template

### YAML Structure

```yaml
risks:
  - id: R001
    category: technical           # technical | integration | estimation | external
    description: "Database queries may not scale beyond 10k users"
    probability: 3                # 1-5 scale
    impact: 4                     # 1-5 scale
    score: 12                     # probability × impact
    phase: 2                      # Which phase this risk affects
    identified: "2026-01-29"
    mitigation:
      strategy: mitigate          # mitigate | avoid | transfer | accept
      tasks:
        - "Add database indexes for common queries"
        - "Implement query result caching"
        - "Load test at 10k simulated users"
      owner: backend
      due: "Before phase 3"
      effort: medium              # low | medium | high
    contingency:
      trigger: "Response time > 2s at 5k users"
      plan: "Implement read replicas"
      effort: high
    status: open                  # open | mitigating | closed | accepted
    last_review: "2026-01-29"

  - id: R002
    category: integration
    description: "Supabase rate limits may block auth during traffic spikes"
    probability: 2
    impact: 5
    score: 10
    phase: 1
    identified: "2026-01-29"
    mitigation:
      strategy: mitigate
      tasks:
        - "Implement token caching to reduce auth calls"
        - "Add request queuing with exponential backoff"
        - "Set up rate limit monitoring alerts"
      owner: backend
      due: "End of phase 1"
      effort: medium
    contingency:
      trigger: "Rate limit errors > 5% of requests"
      plan: "Switch to self-hosted auth service"
      effort: high
    status: open
```

### Markdown Table Format

```markdown
## Risk Register: Phase {N}

| ID | Description | P | I | Score | Strategy | Status |
|----|-------------|---|---|-------|----------|--------|
| R001 | Database scalability | 3 | 4 | 12 🟠 | Mitigate | Open |
| R002 | Supabase rate limits | 2 | 5 | 10 🟠 | Mitigate | Open |
| R003 | Complex migrations | 3 | 3 | 9 🟡 | Mitigate | Open |
| R004 | Learning curve | 4 | 2 | 8 🟡 | Accept | Accepted |
```

---

## Risk Score Matrix

```
Risk Score = Probability × Impact

         Impact
         1    2    3    4    5
    1    1    2    3    4    5
P   2    2    4    6    8   10
r   3    3    6    9   12   15
o   4    4    8   12   16   20
b   5    5   10   15   20   25

Score 1-4:   🟢 Low - Monitor, no mitigation needed
Score 5-9:   🟡 Medium - Create mitigation plan
Score 10-15: 🟠 High - Active mitigation required
Score 16-25: 🔴 Critical - Immediate action, block phase start
```

---

## Risk-Fronted Planning Protocol

### Step 1: Identify Risks FIRST

```
FUNCTION identifyRisks(phase):
    """
    Identify risks BEFORE planning tasks.
    """
    risks = []

    # Technical risks from phase requirements
    FOR each requirement IN phase.requirements:
        tech_risks = analyzeForTechnicalRisks(requirement)
        risks.extend(tech_risks)

    # Integration risks from dependencies
    FOR each dependency IN phase.dependencies:
        int_risks = analyzeForIntegrationRisks(dependency)
        risks.extend(int_risks)

    # Estimation risks from complexity
    est_risks = analyzeForEstimationRisks(phase)
    risks.extend(est_risks)

    # External risks from third parties
    FOR each external IN phase.external_dependencies:
        ext_risks = analyzeForExternalRisks(external)
        risks.extend(ext_risks)

    RETURN risks
```

### Step 2: Score and Prioritize

```
FUNCTION scoreRisks(risks):
    """
    Score and prioritize identified risks.
    """
    FOR each risk IN risks:
        risk.score = risk.probability * risk.impact

        # Determine priority tier
        IF risk.score >= 16:
            risk.tier = "critical"
            risk.action = "Block phase until mitigated"
        ELSE IF risk.score >= 10:
            risk.tier = "high"
            risk.action = "Active mitigation required"
        ELSE IF risk.score >= 5:
            risk.tier = "medium"
            risk.action = "Create mitigation plan"
        ELSE:
            risk.tier = "low"
            risk.action = "Monitor only"

    RETURN sortByScore(risks, descending=true)
```

### Step 3: Generate Mitigation Tasks

```
FUNCTION generateMitigationTasks(risks):
    """
    Auto-generate mitigation tasks for high-priority risks.
    These tasks are marked with risk_mitigation: true.
    """
    mitigation_tasks = []

    FOR each risk IN risks WHERE risk.score >= 10:
        # Generate tasks from mitigation plan
        FOR index, action IN enumerate(risk.mitigation.tasks):
            task = {
                id: "MIT-{risk.id}-{index + 1}",
                type: "mitigation",
                risk_mitigation: true,           # Mark as mitigation task
                risk_id: risk.id,
                title: action,
                description: "Mitigate {risk.description}",
                priority: "high",
                owner: risk.mitigation.owner,
                phase: risk.phase,
                effort: estimateEffort(action),
                acceptance_criteria: [
                    "Risk score reduced",
                    "Mitigation verified working"
                ]
            }
            mitigation_tasks.add(task)

    RETURN mitigation_tasks
```

### Step 4: Insert Mitigation Tasks Early

```
FUNCTION planWithRisks(phase):
    """
    Create phase plan with mitigation tasks front-loaded.
    """
    # 1. Identify risks FIRST
    risks = identifyRisks(phase)

    # 2. Score and prioritize
    scored_risks = scoreRisks(risks)

    # 3. Check for blockers
    critical_risks = scored_risks.filter(r => r.tier == "critical")
    IF critical_risks.length > 0:
        LOG "⛔ Critical risks block phase start:"
        FOR each risk IN critical_risks:
            LOG "  - {risk.id}: {risk.description} (Score: {risk.score})"
        LOG ""
        LOG "Resolve critical risks before starting phase."
        RETURN {blocked: true, blocking_risks: critical_risks}

    # 4. Generate mitigation tasks
    mitigation_tasks = generateMitigationTasks(scored_risks)

    # 5. Generate regular tasks
    regular_tasks = generatePhaseTasks(phase)

    # 6. Combine with mitigations FIRST (de-risk early)
    plan = {
        phase: phase.number,
        risks: scored_risks,
        tasks: mitigation_tasks + regular_tasks,  # Mitigations come first
        task_order: "mitigation_first"
    }

    # 7. Define contingencies
    FOR each risk IN scored_risks WHERE risk.score >= 10:
        risk.contingency = defineContingency(risk)

    RETURN plan
```

---

## De-Risk Early Principle

High-impact risks should have mitigation tasks scheduled early:

```
Phase Task Order:
┌─────────────────────────────────────────────────┐
│ Wave 1: Critical Risk Mitigations               │
│   • MIT-R001-1: Add database indexes            │
│   • MIT-R002-1: Implement token caching         │
├─────────────────────────────────────────────────┤
│ Wave 2: High Risk Mitigations                   │
│   • MIT-R003-1: Create migration rollback       │
├─────────────────────────────────────────────────┤
│ Wave 3: Regular Tasks (Now Safer)               │
│   • Task 1: Implement feature A                 │
│   • Task 2: Implement feature B                 │
│   • Task 3: Integration tests                   │
└─────────────────────────────────────────────────┘
```

### Why This Works

1. **Early Discovery** - Find problems when they're cheapest to fix
2. **Flexible Response** - More options before you've committed to approaches
3. **Informed Decisions** - Better task estimates with risks understood
4. **Reduced Surprises** - Fewer late-stage emergencies

---

## Contingency Plan Template

```yaml
contingency:
  id: CONT-R001
  risk_id: R001
  trigger:
    condition: "Response time > 2s at 5k concurrent users"
    detection: "Load test results or production monitoring"
    threshold: "Must trigger before production launch"
  response:
    immediate_actions:
      - "Alert team lead"
      - "Stop current sprint work"
      - "Assess actual impact"
    short_term:
      plan: "Implement read replicas"
      effort: "3-5 days"
      owner: "backend team"
    long_term:
      plan: "Migrate to horizontally scalable solution"
      effort: "2-3 weeks"
      decision_point: "Review after short-term fix"
  success_criteria:
    - "Response time < 500ms at 10k users"
    - "No data consistency issues"
  rollback:
    trigger: "Contingency makes things worse"
    plan: "Revert read replica changes"
```

---

## Risk Review Protocol

### Phase Start Review

```
FUNCTION reviewRisksAtPhaseStart(phase):
    """
    Review and update risks before starting a phase.
    """
    risks = loadRisksForPhase(phase)

    LOG "⚠️ Risk Review: Phase {phase.number}"
    LOG ""

    # Check for blockers
    FOR each risk IN risks WHERE risk.tier == "critical":
        LOG "🔴 BLOCKER: {risk.id} - {risk.description}"
        LOG "   Score: {risk.score}, Status: {risk.status}"
        IF risk.status != "mitigating":
            RETURN {proceed: false, reason: "Unaddressed critical risk"}

    # Review high risks
    FOR each risk IN risks WHERE risk.tier == "high":
        LOG "🟠 HIGH: {risk.id} - {risk.description}"
        LOG "   Mitigation: {risk.mitigation.strategy}"
        LOG "   Tasks: {risk.mitigation.tasks.length}"

    # Summary
    LOG ""
    LOG "Risk Summary:"
    LOG "  Critical: {count critical} (must be mitigating)"
    LOG "  High: {count high} (mitigation required)"
    LOG "  Medium: {count medium} (plans needed)"
    LOG "  Low: {count low} (monitoring)"

    RETURN {proceed: true, risks: risks}
```

### Ongoing Monitoring

```
FUNCTION monitorRisks(activeRisks):
    """
    Continuous risk monitoring during execution.
    """
    FOR each risk IN activeRisks:
        # Check if trigger conditions met
        IF risk.contingency AND checkTrigger(risk.contingency.trigger):
            LOG "⚠️ Risk {risk.id} TRIGGERED: {risk.description}"
            activateContingency(risk)
            CONTINUE

        # Check for score changes
        new_score = reassessRisk(risk)
        IF new_score != risk.score:
            LOG "📊 Risk {risk.id} score changed: {risk.score} → {new_score}"
            risk.score = new_score
            IF new_score >= 16:
                escalateToCritical(risk)
```

---

## Integration Points

### With /autopilot:plan

```
plan.md integrates:
    - Identify risks during phase planning
    - Generate mitigation tasks automatically
    - Insert mitigations early in task order
    - Track risk_mitigation: true tasks
```

### With /autopilot:takeoff

```
build.md integrates:
    - Review risks at phase start
    - Execute mitigation tasks first
    - Monitor risks during execution
    - Activate contingencies if triggered
```

### With /autopilot:discuss

```
discuss.md integrates:
    - Surface potential risks during discussion
    - Capture risk-related decisions
    - Link decisions to risk mitigations
```

---

## Output Formats

### Risk Summary (Compact)

```
⚠️ Risk Assessment: Phase 3

🔴 Critical: 0 (clear to proceed)
🟠 High: 2 (mitigations scheduled)
🟡 Medium: 3 (plans created)
🟢 Low: 4 (monitoring)

Top Risks:
• R001: Database scalability (12) - Mitigating
• R002: Rate limit issues (10) - Open
```

### Risk Details

```markdown
## Risk R001: Database Scalability

**Category:** Technical
**Score:** 12 (P:3 × I:4) - 🟠 High
**Status:** Mitigating

### Description
Database queries may not scale beyond 10k concurrent users.

### Mitigation (In Progress)
- [x] Add indexes for common queries
- [ ] Implement query result caching
- [ ] Load test at 10k users

### Contingency
**Trigger:** Response time > 2s at 5k users
**Plan:** Implement read replicas
**Effort:** High (3-5 days)
```

---

## Best Practices

### DO:
- Identify risks BEFORE planning tasks
- Score risks objectively with probability × impact
- Generate mitigation tasks for high risks
- Schedule mitigations early in phases
- Define contingencies for all high risks
- Review risks at phase boundaries

### DON'T:
- Ignore risks hoping they won't happen
- Over-engineer mitigations for low risks
- Start phases with unaddressed critical risks
- Skip contingency planning for high risks
- Forget to reassess risks as context changes
