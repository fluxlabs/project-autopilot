---
name: deployment
description: Multi-cloud deployment strategies, rollback procedures, and blue-green deployment patterns. Reference this skill when deploying.
---

# Deployment Skill
# Project Autopilot - Deployment strategies and patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for safe, reliable deployments.

---

## Deployment Strategies

### Blue-Green Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                         LOAD BALANCER                        │
│                              │                               │
│              ┌───────────────┴───────────────┐              │
│              ▼                               ▼              │
│     ┌─────────────────┐           ┌─────────────────┐      │
│     │   BLUE (v1.0)   │           │  GREEN (v1.1)   │      │
│     │   ← Traffic     │    OR     │   ← Traffic     │      │
│     │    Current      │           │     New         │      │
│     └─────────────────┘           └─────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Process:**
1. Deploy new version to Green
2. Run smoke tests on Green
3. Switch traffic to Green
4. Keep Blue for quick rollback
5. Eventually retire Blue

**Pros:** Zero downtime, instant rollback
**Cons:** Requires double infrastructure

### Canary Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                         LOAD BALANCER                        │
│                              │                               │
│              ┌───────┬───────┴───────┬───────┐              │
│              ▼       ▼               ▼       ▼              │
│         ┌────────────────┐    ┌────────────────┐           │
│         │  STABLE (v1.0) │    │  CANARY (v1.1) │           │
│         │     90%        │    │      10%       │           │
│         └────────────────┘    └────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Process:**
1. Deploy to small subset (1-10%)
2. Monitor error rates and latency
3. Gradually increase traffic (10% → 25% → 50% → 100%)
4. Rollback if metrics degrade

**Pros:** Gradual risk exposure
**Cons:** Requires sophisticated traffic management

### Rolling Deployment

```
Instance 1: v1.0 → v1.1 (upgrading)
Instance 2: v1.0 (serving)
Instance 3: v1.0 (serving)
Instance 4: v1.0 (serving)

Instance 1: v1.1 (serving)
Instance 2: v1.0 → v1.1 (upgrading)
Instance 3: v1.0 (serving)
Instance 4: v1.0 (serving)

... continues until all upgraded
```

**Pros:** No extra infrastructure
**Cons:** Slower, mixed versions during deploy

---

## Pre-Deployment Checklist

### Code Quality

- [ ] All tests passing
- [ ] Code review approved
- [ ] No critical security issues
- [ ] Performance benchmarks met

### Environment

- [ ] Environment variables configured
- [ ] Secrets rotated if needed
- [ ] Database migrations ready
- [ ] External services accessible

### Rollback

- [ ] Previous version available
- [ ] Rollback procedure tested
- [ ] Database rollback scripts ready
- [ ] Feature flags can be toggled

### Monitoring

- [ ] Health checks configured
- [ ] Alerts set up
- [ ] On-call notified
- [ ] Status page ready

---

## Rollback Procedures

### Immediate Rollback Triggers

| Condition | Action |
|-----------|--------|
| Error rate > 5% | Auto-rollback |
| P95 latency > 3x baseline | Auto-rollback |
| Health check failures > 3 | Auto-rollback |
| Critical bug reported | Manual rollback |

### Rollback Steps

```bash
# 1. Notify team
/autopilot:notify --channel=deployment "Rolling back production to v1.2.3"

# 2. Switch traffic to previous version
# Vercel
vercel rollback

# AWS
aws deploy stop-deployment --deployment-id <id>

# Kubernetes
kubectl rollout undo deployment/myapp

# 3. Verify rollback
curl https://myapp.com/health

# 4. Investigate root cause
/autopilot:review --diff=v1.2.3..v1.2.4
```

### Database Rollback

```sql
-- If migration was applied, roll back
-- Keep migration scripts reversible!

-- migrations/002_add_column.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- migrations/002_add_column_down.sql
ALTER TABLE users DROP COLUMN avatar_url;
```

---

## Provider-Specific Deployment

### Vercel

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod

# Rollback
vercel rollback

# Environment variables
vercel env add SECRET_KEY production
```

### AWS (ECS)

```bash
# Update service
aws ecs update-service \
  --cluster production \
  --service my-app \
  --task-definition my-app:latest

# Rollback
aws ecs update-service \
  --cluster production \
  --service my-app \
  --task-definition my-app:previous
```

### Kubernetes

```bash
# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl rollout status deployment/my-app

# Rollback
kubectl rollout undo deployment/my-app

# Rollback to specific version
kubectl rollout undo deployment/my-app --to-revision=2
```

### Railway

```bash
# Deploy
railway up

# View deployments
railway deployments

# Rollback
railway rollback
```

---

## Health Checks

### Endpoint Design

```typescript
// Basic health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Comprehensive health check
app.get('/health/ready', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    external: await checkExternalServices(),
  };

  const healthy = Object.values(checks).every(c => c.healthy);

  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'ok' : 'degraded',
    checks,
    version: process.env.APP_VERSION,
    timestamp: new Date().toISOString(),
  });
});

async function checkDatabase() {
  try {
    await db.query('SELECT 1');
    return { healthy: true, latency: '5ms' };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
}
```

### Load Balancer Configuration

```yaml
# AWS ALB
healthCheck:
  path: /health
  interval: 30
  timeout: 5
  healthyThreshold: 2
  unhealthyThreshold: 3

# Kubernetes
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

## Database Migrations

### Safe Migration Pattern

```typescript
// migrations/003_add_email_verified.ts

export async function up(db: Database) {
  // 1. Add column as nullable first
  await db.schema.alterTable('users', (table) => {
    table.boolean('email_verified').nullable();
  });

  // 2. Backfill data
  await db('users').update({ email_verified: false });

  // 3. Add NOT NULL constraint (in separate deploy)
  // await db.schema.alterTable('users', (table) => {
  //   table.boolean('email_verified').notNullable().alter();
  // });
}

export async function down(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('email_verified');
  });
}
```

### Migration Best Practices

| Do | Don't |
|---|------|
| Add nullable columns | Add NOT NULL without default |
| Create indexes concurrently | Lock tables during deploy |
| Small, incremental changes | Large schema changes |
| Test rollback procedures | Assume rollback works |
| Run migrations before code deploy | Deploy code before migrations |

---

## Feature Flags

```typescript
// Use feature flags for safe rollout
const featureFlags = {
  newCheckoutFlow: {
    enabled: true,
    rolloutPercentage: 10,
    allowedUsers: ['beta-testers'],
  },
};

function isFeatureEnabled(flagName: string, user: User): boolean {
  const flag = featureFlags[flagName];
  if (!flag.enabled) return false;

  // Check user allowlist
  if (flag.allowedUsers?.includes(user.group)) return true;

  // Check percentage rollout
  const hash = hashUserId(user.id);
  return hash % 100 < flag.rolloutPercentage;
}

// Usage
if (isFeatureEnabled('newCheckoutFlow', user)) {
  return <NewCheckout />;
} else {
  return <OldCheckout />;
}
```

---

## Deployment Metrics

### Key Metrics to Track

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Deploy Duration | < 5 min | 5-15 min | > 15 min |
| Rollback Rate | < 5% | 5-10% | > 10% |
| Error Rate Post-Deploy | < 0.1% | 0.1-1% | > 1% |
| Time to Rollback | < 2 min | 2-5 min | > 5 min |
