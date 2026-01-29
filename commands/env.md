---
description: Environment configuration management with validation, syncing, and secure handling
argument-hint: "[--list] [--validate] [--sync] [--encrypt] [--diff] [--generate]"
model: haiku
---

# Autopilot: ENV Mode
# Project Autopilot - Environment configuration management
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Manage environment variables with validation, syncing, and secure handling.

## Required Skills

**Read before managing:**
1. `/autopilot/skills/environment-management/SKILL.md` - Config patterns

## Required Agents

- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--list` | List all environment variables |
| `--validate` | Validate environment configuration |
| `--sync` | Sync environment across files |
| `--encrypt` | Encrypt sensitive values |
| `--diff` | Compare environments |
| `--generate` | Generate .env.example |
| `--check=env` | Check specific environment |
| `--required` | List required variables |

---

## Usage

### List Environment Variables

```bash
/autopilot:env --list
```

Output:
```markdown
## Environment Variables

### Application
| Variable | Value | Source |
|----------|-------|--------|
| NODE_ENV | development | .env.local |
| PORT | 3000 | .env |
| API_URL | http://localhost:3000 | .env.local |

### Database
| Variable | Value | Source |
|----------|-------|--------|
| DATABASE_URL | postgres://... | .env.local |
| REDIS_URL | redis://localhost:6379 | .env |

### Authentication
| Variable | Value | Source |
|----------|-------|--------|
| JWT_SECRET | *** (set) | .env.local |
| OAUTH_CLIENT_ID | *** (set) | .env.local |
| OAUTH_CLIENT_SECRET | *** (set) | .env.local |

### Third-Party Services
| Variable | Value | Source |
|----------|-------|--------|
| STRIPE_SECRET_KEY | *** (set) | .env.local |
| STRIPE_WEBHOOK_SECRET | *** (set) | .env.local |
| SENDGRID_API_KEY | *** (set) | .env.local |

### Summary
- **Total Variables:** 12
- **Set:** 12
- **Missing:** 0
- **Sources:** .env, .env.local
```

### Validate Environment

```bash
/autopilot:env --validate
```

Output:
```markdown
## Environment Validation

### Configuration Check

| Variable | Required | Set | Valid |
|----------|----------|-----|-------|
| NODE_ENV | ✅ | ✅ | ✅ |
| DATABASE_URL | ✅ | ✅ | ✅ |
| JWT_SECRET | ✅ | ✅ | ⚠️ Weak (too short) |
| STRIPE_SECRET_KEY | ⚠️ Prod | ✅ | ✅ |
| API_URL | ✅ | ✅ | ❌ Invalid URL |

### Issues Found

#### ⚠️ Warning: Weak JWT Secret
**Variable:** `JWT_SECRET`
**Issue:** Secret is only 16 characters
**Recommendation:** Use at least 32 characters

```bash
# Generate strong secret
openssl rand -base64 32
```

#### ❌ Error: Invalid API_URL
**Variable:** `API_URL`
**Value:** `localhost:3000`
**Issue:** Missing protocol
**Fix:** `http://localhost:3000`

### Validation Summary
- ✅ Passed: 10
- ⚠️ Warnings: 1
- ❌ Errors: 1
```

### Compare Environments

```bash
/autopilot:env --diff
```

Output:
```markdown
## Environment Comparison

### .env.local vs .env.staging

| Variable | Local | Staging | Status |
|----------|-------|---------|--------|
| NODE_ENV | development | staging | Different |
| DATABASE_URL | postgres://local/... | postgres://staging/... | Different |
| API_URL | http://localhost:3000 | https://staging.api.com | Different |
| JWT_SECRET | local-secret-key | *** | Different |
| DEBUG | true | - | Missing in staging |
| SENTRY_DSN | - | https://... | Missing in local |

### Summary
- **Shared:** 8 variables
- **Different values:** 4
- **Only in local:** 1 (DEBUG)
- **Only in staging:** 1 (SENTRY_DSN)
```

### Generate .env.example

```bash
/autopilot:env --generate
```

Output:
```markdown
## Generated .env.example

```bash
# Application
NODE_ENV=development
PORT=3000
API_URL=http://localhost:3000

# Database
DATABASE_URL=postgres://user:password@localhost:5432/myapp

# Authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret

# Third-Party Services
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....

# Optional
DEBUG=false
LOG_LEVEL=info
```

**File written:** `.env.example`

### Documentation Generated

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| NODE_ENV | enum | ✅ | development, staging, production |
| PORT | number | ❌ | Server port (default: 3000) |
| DATABASE_URL | url | ✅ | PostgreSQL connection string |
| JWT_SECRET | string | ✅ | Secret for JWT signing |
```

### Sync Environments

```bash
/autopilot:env --sync
```

Ensures all .env files have consistent structure.

### List Required Variables

```bash
/autopilot:env --required
```

Output:
```markdown
## Required Environment Variables

### Production Requirements

| Variable | Description | Validation |
|----------|-------------|------------|
| DATABASE_URL | Database connection | Valid URL |
| JWT_SECRET | Auth secret | Min 32 chars |
| STRIPE_SECRET_KEY | Payment processing | Starts with sk_ |

### Currently Missing for Production

1. **SENTRY_DSN** - Error tracking
2. **REDIS_URL** - Session caching

### Setup Command

```bash
# Copy required variables
cp .env.example .env.production

# Generate secrets
echo "JWT_SECRET=$(openssl rand -base64 32)" >> .env.production
```
```

---

## Behavior

```
FUNCTION manageEnv(options):

    # 1. Load all env files
    envFiles = findEnvFiles()
    variables = parseEnvFiles(envFiles)

    IF options.list:
        DISPLAY variableList(variables)

    ELIF options.validate:
        schema = loadEnvSchema()
        results = validateEnv(variables, schema)
        DISPLAY validationResults(results)

    ELIF options.diff:
        comparison = compareEnvs(variables)
        DISPLAY envComparison(comparison)

    ELIF options.generate:
        example = generateExample(variables)
        writeFile('.env.example', example)
        DISPLAY exampleGenerated(example)

    ELIF options.sync:
        syncEnvFiles(envFiles)
        DISPLAY syncResults()

    ELIF options.encrypt:
        encrypted = encryptSensitive(variables)
        writeEncrypted(encrypted)

    ELIF options.required:
        required = getRequiredVars()
        missing = checkMissing(variables, required)
        DISPLAY requiredVars(required, missing)

    ELIF options.check:
        env = loadEnv(options.check)
        results = validateEnv(env)
        DISPLAY validationResults(results)
```

---

## Environment Files

### Priority Order

```
1. .env.local           (highest - never committed)
2. .env.{environment}   (staging, production)
3. .env                 (lowest - default values)
```

### Best Practices

```bash
# .env (committed - defaults only)
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# .env.example (committed - template)
DATABASE_URL=postgres://user:pass@localhost:5432/app
JWT_SECRET=your-secret-here
STRIPE_SECRET_KEY=sk_test_...

# .env.local (NOT committed - actual secrets)
DATABASE_URL=postgres://real:connection@server/prod
JWT_SECRET=actual-secret-key-32-chars-min
STRIPE_SECRET_KEY=sk_live_actual_key

# .gitignore
.env.local
.env.*.local
```

---

## Validation Schema

```typescript
// env.schema.ts
export const envSchema = {
  NODE_ENV: {
    type: 'enum',
    values: ['development', 'staging', 'production'],
    required: true,
  },
  DATABASE_URL: {
    type: 'url',
    protocol: ['postgres', 'postgresql'],
    required: true,
  },
  JWT_SECRET: {
    type: 'string',
    minLength: 32,
    required: true,
  },
  PORT: {
    type: 'number',
    min: 1,
    max: 65535,
    default: 3000,
  },
  STRIPE_SECRET_KEY: {
    type: 'string',
    pattern: /^sk_(test|live)_/,
    requiredIn: ['production'],
  },
};
```

---

## Quick Examples

```bash
# List all variables
/autopilot:env --list

# Validate configuration
/autopilot:env --validate

# Compare local vs staging
/autopilot:env --diff

# Generate .env.example
/autopilot:env --generate

# Check production readiness
/autopilot:env --check=production

# List required variables
/autopilot:env --required

# Sync all env files
/autopilot:env --sync
```

$ARGUMENTS
