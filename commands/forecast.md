---
description: Predictive cost and time estimation using historical data and ML patterns
argument-hint: "[description] [--confidence] [--breakdown] [--scenarios]"
model: sonnet
---

# Autopilot: FORECAST Mode
# Project Autopilot - Predictive estimation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Predictive cost and time estimation using historical data and machine learning patterns.

## Required Skills

**Read before forecasting:**
1. `/autopilot/skills/predictive-analytics/SKILL.md` - ML estimation patterns
2. `/autopilot/skills/global-state/SKILL.md` - Historical data access

## Required Agents

- `history-tracker` - Access project history
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `[description]` | Feature/project to estimate |
| `--confidence` | Show confidence intervals |
| `--breakdown` | Show detailed phase breakdown |
| `--scenarios` | Show best/likely/worst scenarios |
| `--compare` | Compare with similar past projects |
| `--budget=N` | Check against budget |

---

## Usage

### Basic Forecast

```bash
/autopilot:forecast "Add user authentication with OAuth"
```

Output:
```markdown
## Forecast: User Authentication with OAuth

### Estimate Summary
| Metric | Estimate | Confidence |
|--------|----------|------------|
| **Total Cost** | **$1.85** | High (±15%) |
| Phases | 4 | High |
| Tasks | ~18 | Medium |

### Confidence Range
```
    $1.57          $1.85          $2.13
      │              │              │
Low ──┼──────────────┼──────────────┼── High
      │              │              │
   Best Case     Likely     Worst Case
```

### Basis for Estimate
- Similar projects: 8 found
- Historical accuracy: 94%
- Tech stack match: Node + TypeScript (100%)
- Feature complexity: Medium
```

### Detailed Breakdown

```bash
/autopilot:forecast "Add user authentication with OAuth" --breakdown
```

Output:
```markdown
## Forecast: User Authentication with OAuth

### Estimate Summary
| Metric | Estimate | Confidence |
|--------|----------|------------|
| **Total Cost** | **$1.85** | High (±15%) |

---

### Phase Breakdown

#### Phase 1: Database Setup
| Task | Est. Cost | Confidence |
|------|-----------|------------|
| User schema | $0.03 | High |
| Session schema | $0.03 | High |
| Migrations | $0.02 | High |
| **Phase Total** | **$0.08** | High |

#### Phase 2: Authentication Core
| Task | Est. Cost | Confidence |
|------|-----------|------------|
| JWT implementation | $0.15 | High |
| Password hashing | $0.05 | High |
| Session management | $0.12 | Medium |
| Token refresh | $0.10 | Medium |
| **Phase Total** | **$0.42** | High |

#### Phase 3: OAuth Integration
| Task | Est. Cost | Confidence |
|------|-----------|------------|
| OAuth setup | $0.08 | High |
| Google provider | $0.15 | Medium |
| GitHub provider | $0.12 | Medium |
| Callback handling | $0.18 | Medium |
| **Phase Total** | **$0.53** | Medium |

*Historical note: OAuth integration often exceeds estimate by 15-20%*

#### Phase 4: Frontend & Testing
| Task | Est. Cost | Confidence |
|------|-----------|------------|
| Login UI | $0.20 | Medium |
| Protected routes | $0.12 | High |
| Unit tests | $0.25 | High |
| Integration tests | $0.25 | High |
| **Phase Total** | **$0.82** | High |

---

### Estimation Adjustments

| Factor | Adjustment | Reason |
|--------|------------|--------|
| Tech stack match | -5% | Node/TS well documented |
| OAuth complexity | +10% | Historical overruns |
| Team experience | 0% | Average |
| **Net Adjustment** | **+5%** | |

### Risk Factors

| Risk | Probability | Impact |
|------|-------------|--------|
| OAuth provider issues | Low | +20% |
| Schema changes | Medium | +15% |
| Test coverage gaps | Low | +10% |
```

### Scenario Analysis

```bash
/autopilot:forecast "Build e-commerce checkout flow" --scenarios
```

Output:
```markdown
## Forecast: E-commerce Checkout Flow

### Scenario Analysis

#### Best Case ($2.80)
- Clean existing codebase
- All integrations documented
- No unexpected requirements
- High code reuse

#### Likely Case ($3.65)
- Moderate complexity
- Some integration challenges
- Normal scope adjustments
- Standard testing effort

#### Worst Case ($4.90)
- Legacy code complications
- Payment provider issues
- Scope creep
- Extended testing needs

### Probability Distribution
```
        Best      Likely      Worst
         ▼          ▼          ▼
    ─────┼──────────┼──────────┼─────
$2.50   $2.80     $3.65      $4.90   $5.50
         │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
              80% confidence
```

### Scenario Breakdown

| Phase | Best | Likely | Worst |
|-------|------|--------|-------|
| Cart | $0.35 | $0.45 | $0.65 |
| Checkout | $0.80 | $1.10 | $1.50 |
| Payment | $0.65 | $0.85 | $1.20 |
| Confirmation | $0.40 | $0.50 | $0.70 |
| Testing | $0.60 | $0.75 | $0.85 |
| **Total** | **$2.80** | **$3.65** | **$4.90** |
```

### Compare with Similar Projects

```bash
/autopilot:forecast "Real-time chat feature" --compare
```

Output:
```markdown
## Forecast: Real-time Chat Feature

### Estimate: $2.45 (Medium Confidence)

### Similar Projects Comparison

| Project | Features | Cost | Duration |
|---------|----------|------|----------|
| chat-app-v2 | WebSocket, threads | $2.85 | 6h |
| support-chat | Real-time, typing | $2.20 | 4h |
| team-messenger | Channels, mentions | $3.45 | 8h |

### Feature Comparison

| Feature | This Project | chat-app-v2 | support-chat |
|---------|--------------|-------------|--------------|
| WebSocket | ✅ | ✅ | ✅ |
| Typing indicators | ✅ | ❌ | ✅ |
| File upload | ❌ | ✅ | ❌ |
| Threads | ❌ | ✅ | ❌ |

### Estimate Derivation
```
Base (avg similar): $2.83
- No file upload:   -$0.35
- No threads:       -$0.25
+ Typing indicator: +$0.12
+ Complexity adj:   +$0.10
─────────────────────────────
Estimate:           $2.45
```
```

### Budget Check

```bash
/autopilot:forecast "Full dashboard redesign" --budget=5
```

Output:
```markdown
## Forecast: Full Dashboard Redesign

### Budget Analysis

| Metric | Value |
|--------|-------|
| Estimated Cost | $4.25 |
| Budget | $5.00 |
| Buffer | $0.75 (15%) |

### Budget Status: ✅ Within Budget

```
Budget:   ████████████████████████████████████████ $5.00
Estimate: ████████████████████████████████████░░░░ $4.25
          ├────────────────────────────────────┤
                         85%
```

### Risk to Budget

| Scenario | Cost | Budget Impact |
|----------|------|---------------|
| Best | $3.40 | +$1.60 buffer |
| Likely | $4.25 | +$0.75 buffer |
| Worst | $5.50 | -$0.50 over ⚠️ |

### Recommendation
Budget has adequate buffer for likely case.
Consider adding 10% contingency for worst case.
```

---

## Behavior

```
FUNCTION forecast(description, options):

    # 1. Analyze feature requirements
    requirements = analyzeRequirements(description)

    # 2. Find similar historical projects
    similar = findSimilarProjects(requirements)

    # 3. Calculate base estimate
    baseEstimate = calculateBaseEstimate(similar, requirements)

    # 4. Apply adjustments
    adjustments = calculateAdjustments(requirements, context)
    finalEstimate = applyAdjustments(baseEstimate, adjustments)

    # 5. Calculate confidence
    confidence = calculateConfidence(similar.length, adjustments)

    # 6. Generate scenarios if requested
    IF options.scenarios:
        scenarios = generateScenarios(finalEstimate, confidence)

    # 7. Generate breakdown if requested
    IF options.breakdown:
        breakdown = generatePhaseBreakdown(requirements, similar)

    # 8. Compare with similar if requested
    IF options.compare:
        comparison = generateComparison(similar, requirements)

    # 9. Check budget if provided
    IF options.budget:
        budgetAnalysis = checkBudget(finalEstimate, options.budget)

    # 10. Compile and display forecast
    DISPLAY forecastReport(finalEstimate, confidence, breakdown, scenarios)
```

---

## Quick Examples

```bash
# Basic estimate
/autopilot:forecast "Add user profile page"

# Detailed breakdown
/autopilot:forecast "Payment integration" --breakdown

# With scenarios
/autopilot:forecast "Mobile app API" --scenarios

# Compare with similar
/autopilot:forecast "Search functionality" --compare

# Budget check
/autopilot:forecast "Admin dashboard" --budget=10
```

$ARGUMENTS
