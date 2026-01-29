---
description: Run security scanning and fixes
argument-hint: "[--deep] [--fix] [--report]"
model: sonnet
---

# Autopilot: SECURITY-SCAN Mode

Security scanning powered by the `security-scanner` agent. Use for static checks, dependency audit, and optional auto-fixes.

## Required Agents
- `security-scanner` - Perform scans and generate reports
- `tester` (optional) - Run security-focused tests when `--fix` is used

## Usage

```bash
/autopilot:security-scan              # default scan
/autopilot:security-scan --deep       # deeper scan (slower)
/autopilot:security-scan --fix        # attempt automated fixes
/autopilot:security-scan --report     # output markdown report
```

## Behavior

```
FUNCTION securityScan(options):
    ensureDir('.autopilot/security/')
    SPAWN security-scanner → scan({
        depth: options.deep ? "deep" : "standard",
        fix: options.fix,
        report: options.report
    })
    IF options.fix:
        SPAWN tester → runSecurityTests()
```

