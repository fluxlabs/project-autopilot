---
description: Deployment orchestration and management for multiple cloud providers
argument-hint: "[--env=staging|production] [--provider=vercel|aws|gcp|railway|fly] [--rollback] [--preview]"
model: sonnet
---

# Autopilot: DEPLOY Mode
# Project Autopilot - Deployment orchestration
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Deployment orchestration for multiple cloud providers with rollback support and preview deployments.

## Required Skills

**Read before deploying:**
1. `/autopilot/skills/deployment/SKILL.md` - Deployment strategies
2. `/autopilot/skills/environment-management/SKILL.md` - Environment handling

## Required Agents

- `monitor` - Health monitoring
- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--env=env` | Target environment: staging, production |
| `--provider=provider` | Cloud provider (auto-detected if not specified) |
| `--rollback` | Rollback to previous deployment |
| `--preview` | Create preview deployment |
| `--dry-run` | Show what would be deployed |
| `--skip-tests` | Skip pre-deploy tests |
| `--promote` | Promote staging to production |

---

## Supported Providers

| Provider | Type | Auto-detect |
|----------|------|-------------|
| Vercel | Serverless/Edge | `vercel.json` |
| AWS | EC2, Lambda, ECS | `aws.yml`, `serverless.yml` |
| GCP | Cloud Run, GKE | `app.yaml`, `cloudbuild.yaml` |
| Railway | Container | `railway.json` |
| Fly.io | Edge | `fly.toml` |
| DigitalOcean | Droplets, App Platform | `do.yaml` |
| Netlify | Static/Serverless | `netlify.toml` |
| Render | Container | `render.yaml` |

---

## Usage

### Deploy to Staging

```bash
/autopilot:deploy --env=staging
```

Output:
```markdown
## Deployment: Staging

### Pre-flight Checks ✅
- [x] All tests passing
- [x] Build successful
- [x] Environment variables configured
- [x] No uncommitted changes

### Deployment Progress
```
[12:34:56] 🔵 Starting deployment to staging
[12:34:58] 📦 Building application...
[12:35:12] ✅ Build complete (14s)
[12:35:13] 🚀 Deploying to Vercel...
[12:35:45] ✅ Deployment complete

URL: https://my-app-staging.vercel.app
```

### Post-deployment Verification
- [x] Health check passed
- [x] API responding (45ms)
- [x] Database connected
- [x] Environment: staging

### Deployment Details
| Metric | Value |
|--------|-------|
| Duration | 49 seconds |
| Build Time | 14 seconds |
| Bundle Size | 245KB |
| Functions | 12 |
| Regions | iad1 |

### Monitoring
View logs: `vercel logs --follow`
Dashboard: https://vercel.com/team/my-app
```

### Deploy to Production

```bash
/autopilot:deploy --env=production
```

Output:
```markdown
## Deployment: Production

### ⚠️ Production Deployment Checklist

| Check | Status |
|-------|--------|
| Staging tested | ✅ Deployed 2h ago |
| All tests passing | ✅ 142/142 passed |
| Change review | ⚠️ 3 files changed |
| Rollback ready | ✅ Previous: v1.2.3 |

### Changes Since Last Deploy
```diff
+ Added rate limiting middleware
+ Updated user authentication flow
- Removed deprecated endpoints
```

### Risk Assessment
| Risk | Level |
|------|-------|
| Breaking changes | 🟢 Low |
| Database migrations | 🟡 Medium (1 migration) |
| Third-party deps | 🟢 Low |

**Proceed with production deployment? (y/n)**

---

### Deploying...
```
[12:45:00] 🔵 Starting production deployment
[12:45:01] 📋 Running database migrations...
[12:45:15] ✅ Migration complete
[12:45:16] 🚀 Deploying (blue-green)...
[12:45:45] ✅ New version deployed
[12:45:46] 🔄 Switching traffic (canary 10%)...
[12:46:00] ✅ Canary healthy
[12:46:01] 🔄 Switching traffic (100%)...
[12:46:10] ✅ Full traffic switch complete
```

### Production Deployed! 🎉
| Metric | Value |
|--------|-------|
| URL | https://myapp.com |
| Version | v1.2.4 |
| Duration | 70 seconds |
| Rollback | Available |
```

### Preview Deployment

```bash
/autopilot:deploy --preview
```

Creates a unique preview URL for the current branch/PR.

### Rollback

```bash
/autopilot:deploy --rollback
```

Output:
```markdown
## Rollback: Production

### Available Versions
| Version | Deployed | Status | Duration |
|---------|----------|--------|----------|
| v1.2.4 | 2h ago | Current | - |
| v1.2.3 | 1d ago | Healthy | Previous |
| v1.2.2 | 3d ago | Healthy | Available |

**Select version to rollback to:** v1.2.3

### Rolling back...
```
[12:50:00] 🔄 Initiating rollback to v1.2.3
[12:50:05] 🔄 Switching traffic...
[12:50:15] ✅ Rollback complete
```

### Rollback Complete
- Reverted to: v1.2.3
- Time: 15 seconds
- Health check: ✅ Passing
```

### Promote Staging to Production

```bash
/autopilot:deploy --promote
```

---

## Behavior

```
FUNCTION deploy(options):

    # 1. Detect provider
    IF options.provider:
        provider = options.provider
    ELSE:
        provider = detectProvider()

    # 2. Pre-flight checks
    IF NOT options.skipTests:
        runTests()
    verifyBuild()
    checkEnvironment(options.env)

    # 3. Confirm production deployments
    IF options.env == 'production':
        showChanges()
        showRiskAssessment()
        IF NOT confirm():
            RETURN

    # 4. Handle special modes
    IF options.rollback:
        versions = listVersions(provider, options.env)
        selected = selectVersion(versions)
        rollback(provider, options.env, selected)
        RETURN

    IF options.preview:
        deployPreview(provider)
        RETURN

    IF options.promote:
        promoteStagingToProduction(provider)
        RETURN

    # 5. Run deployment
    IF options.dryRun:
        showDeploymentPlan()
        RETURN

    # Build
    buildOutput = build()

    # Deploy
    deployment = deploy(provider, options.env, buildOutput)

    # 6. Post-deployment
    runHealthChecks(deployment.url)
    SPAWN monitor → watchDeployment(deployment)

    # 7. Report
    DISPLAY deploymentSummary(deployment)
```

---

## Provider-Specific Commands

### Vercel

```bash
# Deploy
vercel --prod

# Preview
vercel

# Rollback
vercel rollback
```

### AWS (Serverless)

```bash
# Deploy
serverless deploy --stage production

# Rollback
serverless rollback --stage production
```

### Railway

```bash
# Deploy
railway up

# View logs
railway logs
```

### Fly.io

```bash
# Deploy
fly deploy

# Rollback
fly releases rollback
```

---

## Deployment Strategies

### Blue-Green (Default for Production)

1. Deploy new version alongside old
2. Run health checks on new version
3. Switch traffic to new version
4. Keep old version for quick rollback

### Canary

1. Deploy new version
2. Route 10% traffic to new version
3. Monitor error rates and latency
4. Gradually increase to 100%

### Rolling

1. Replace instances one at a time
2. No downtime
3. Slower but safer

---

## Quick Examples

```bash
# Deploy to staging
/autopilot:deploy --env=staging

# Deploy to production
/autopilot:deploy --env=production

# Preview deployment
/autopilot:deploy --preview

# Dry run
/autopilot:deploy --env=production --dry-run

# Rollback
/autopilot:deploy --rollback

# Promote staging to production
/autopilot:deploy --promote

# Specific provider
/autopilot:deploy --provider=vercel --env=production
```

$ARGUMENTS
