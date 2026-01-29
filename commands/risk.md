---
description: Risk assessment and mitigation planning for projects
argument-hint: "[--assess] [--monitor] [--mitigate=risk-id] [--report]"
model: sonnet
---

# Autopilot: RISK Mode
# Project Autopilot - Risk assessment and mitigation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Project risk assessment, monitoring, and mitigation planning.

## Required Skills

**Read before assessing:**
1. `/autopilot/skills/risk-management/SKILL.md` - Risk patterns

## Required Agents

- `risk-assessor` - Risk analysis
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--assess` | Full risk assessment |
| `--monitor` | Monitor active risks |
| `--mitigate=id` | Plan mitigation for specific risk |
| `--report` | Generate risk report |
| `--category=cat` | Filter by category |
| `--severity=level` | Filter by severity |

---

## Usage

### Risk Assessment

```bash
/autopilot:risk --assess
```

Output:
```markdown
## Risk Assessment: my-saas-app

**Assessment Date:** Jan 29, 2026
**Project Phase:** 5/10 (50%)

---

### Risk Matrix

```
              Impact
         Low    Med    High
      ┌──────┬──────┬──────┐
 High │  R4  │  R2  │  R1  │
Prob. ├──────┼──────┼──────┤
 Med  │  R6  │  R3  │  R5  │
      ├──────┼──────┼──────┤
 Low  │  R8  │  R7  │      │
      └──────┴──────┴──────┘
```

---

### High Priority Risks

#### R1: Third-Party API Dependency 🔴
**Category:** Technical
**Probability:** High | **Impact:** High | **Score:** 9

**Description:**
Critical dependency on Stripe API for payment processing. Any
outage or breaking changes would directly impact core functionality.

**Current Status:** Active - Monitoring
**Indicators:**
- Stripe status page: ✅ Operational
- Last incident: 14 days ago
- API version: Current

**Mitigation Plan:**
1. Implement circuit breaker pattern
2. Add fallback payment provider
3. Cache payment intents
4. Create offline queue

**Contingency:**
- Enable maintenance mode for checkout
- Queue orders for later processing
- Notify users of delay

---

#### R2: Scope Creep 🟠
**Category:** Project
**Probability:** High | **Impact:** Medium | **Score:** 6

**Description:**
New feature requests arriving during development. Current backlog
has grown 30% since project start.

**Current Status:** Active - Mitigating
**Indicators:**
- Backlog growth: +12 items (30%)
- Unplanned work: 15% of sprint

**Mitigation Plan:**
1. Strict change control process
2. All new requests → backlog
3. Weekly scope review
4. Clear MVP definition

**Progress:**
- [x] Change control documented
- [x] Backlog triage scheduled
- [ ] MVP re-confirmed

---

### Medium Priority Risks

#### R3: Team Knowledge Gaps 🟡
**Category:** Resource
**Probability:** Medium | **Impact:** Medium | **Score:** 4

**Description:**
Limited experience with WebSocket implementation. May impact
real-time features timeline.

**Mitigation:**
- Technical spike scheduled (Sprint 6)
- Documentation review complete
- Fallback to polling if needed

---

#### R5: Performance at Scale 🟠
**Category:** Technical
**Probability:** Medium | **Impact:** High | **Score:** 6

**Description:**
Untested performance with 1000+ concurrent users.
Production traffic patterns unknown.

**Mitigation:**
- Load testing scheduled (Phase 8)
- Horizontal scaling configured
- CDN caching implemented

---

### Low Priority Risks

| ID | Risk | Category | Score | Status |
|----|------|----------|-------|--------|
| R4 | Browser compatibility | Technical | 3 | Monitoring |
| R6 | Documentation debt | Quality | 2 | Accepted |
| R7 | Dependency vulnerabilities | Security | 3 | Monitoring |
| R8 | Team availability | Resource | 2 | Accepted |

---

### Risk Summary

| Category | High | Medium | Low | Total |
|----------|------|--------|-----|-------|
| Technical | 2 | 1 | 1 | 4 |
| Project | 1 | 0 | 0 | 1 |
| Resource | 0 | 1 | 1 | 2 |
| Security | 0 | 0 | 1 | 1 |
| **Total** | **3** | **2** | **3** | **8** |

### Overall Risk Level: 🟠 Medium

**Recommendation:** Address R1 and R2 before Phase 6
```

### Monitor Risks

```bash
/autopilot:risk --monitor
```

Output:
```markdown
## Risk Monitor

**Last Updated:** Jan 29, 2026 14:30

### Active Risk Status

| Risk | Status | Trend | Last Check |
|------|--------|-------|------------|
| R1: API Dependency | 🟢 Stable | → | 5 min ago |
| R2: Scope Creep | 🟡 Warning | ↑ | 1 day ago |
| R3: Knowledge Gaps | 🟢 Improving | ↓ | 2 days ago |
| R5: Performance | 🟢 Stable | → | 1 week ago |

### Alerts

#### ⚠️ R2: Scope Creep
**Trigger:** Backlog items > threshold
**Current:** 45 items (threshold: 40)
**Action Required:** Review and prioritize backlog

### Monitoring Dashboard

```
R1 (API)     [████████████████████] 100% uptime
R2 (Scope)   [████████████░░░░░░░░]  60% controlled
R3 (Skills)  [██████████████████░░]  90% confidence
R5 (Perf)    [████████████████░░░░]  80% ready
```

### Upcoming Reviews

| Risk | Next Review | Owner |
|------|-------------|-------|
| R1 | Daily auto | System |
| R2 | Tomorrow | PM |
| R5 | Feb 5 | Tech Lead |
```

### Mitigate Specific Risk

```bash
/autopilot:risk --mitigate=R1
```

Output:
```markdown
## Mitigation Plan: R1 - Third-Party API Dependency

### Current Risk Status
- **Score:** 9 (High × High)
- **Status:** Active
- **Time in State:** 14 days

---

### Mitigation Strategy

#### Phase 1: Detection (Day 1-2)
**Goal:** Know immediately when API issues occur

| Action | Status | Owner |
|--------|--------|-------|
| Add health check endpoint | ⏳ | Backend |
| Configure alerting (PagerDuty) | ⏳ | DevOps |
| Add status page monitoring | ⏳ | DevOps |

**Estimated Cost:** $0.15

#### Phase 2: Resilience (Day 3-5)
**Goal:** Survive temporary outages

| Action | Status | Owner |
|--------|--------|-------|
| Implement circuit breaker | ⏳ | Backend |
| Add retry with exponential backoff | ⏳ | Backend |
| Cache successful responses | ⏳ | Backend |
| Queue failed operations | ⏳ | Backend |

**Estimated Cost:** $0.35

#### Phase 3: Redundancy (Day 6-10)
**Goal:** Full fallback capability

| Action | Status | Owner |
|--------|--------|-------|
| Evaluate backup provider | ⏳ | Architect |
| Implement provider abstraction | ⏳ | Backend |
| Add provider switching logic | ⏳ | Backend |
| Test failover procedure | ⏳ | QA |

**Estimated Cost:** $0.55

---

### Success Criteria

| Criteria | Target | Current |
|----------|--------|---------|
| Detection time | < 1 min | N/A |
| Recovery time | < 5 min | N/A |
| Data loss | 0 | N/A |
| User impact | Minimal | N/A |

---

### Post-Mitigation Risk Score

| Factor | Before | After |
|--------|--------|-------|
| Probability | High | Medium |
| Impact | High | Low |
| **Score** | **9** | **2** |

**Implement this mitigation plan? (y/n)**
```

---

## Behavior

```
FUNCTION assessRisk(options):

    # 1. Gather project context
    project = loadProjectState()
    history = loadProjectHistory()
    dependencies = analyzeDependencies()

    IF options.assess:
        # Full assessment
        risks = identifyRisks(project, dependencies)
        scored = scoreRisks(risks)
        matrix = buildRiskMatrix(scored)

        DISPLAY riskAssessment(matrix, scored)

    ELIF options.monitor:
        # Monitor active risks
        active = getActiveRisks()
        status = checkRiskStatus(active)
        alerts = getAlerts(status)

        DISPLAY riskMonitor(status, alerts)

    ELIF options.mitigate:
        # Plan mitigation
        risk = getRisk(options.mitigate)
        plan = generateMitigationPlan(risk)
        estimate = estimateMitigation(plan)

        DISPLAY mitigationPlan(plan, estimate)

        IF confirm():
            executeMitigation(plan)

    ELIF options.report:
        # Generate report
        all = getAllRisks()
        report = generateRiskReport(all)

        writeFile(".autopilot/risk-report.md", report)
        DISPLAY "Report generated: .autopilot/risk-report.md"
```

---

## Risk Categories

| Category | Examples |
|----------|----------|
| Technical | API dependencies, scalability, security |
| Project | Scope, timeline, budget |
| Resource | Skills, availability, turnover |
| External | Market, regulatory, competition |
| Quality | Bugs, technical debt, testing |

---

## Quick Examples

```bash
# Full assessment
/autopilot:risk --assess

# Monitor active risks
/autopilot:risk --monitor

# Mitigate specific risk
/autopilot:risk --mitigate=R1

# Generate report
/autopilot:risk --report

# Filter by category
/autopilot:risk --assess --category=technical

# Filter by severity
/autopilot:risk --assess --severity=high
```

$ARGUMENTS
