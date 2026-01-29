---
description: CI/CD pipeline generation and management for multiple providers
argument-hint: "[--provider=github|gitlab|bitbucket] [--template=basic|full|custom] [--update]"
model: sonnet
---

# Autopilot: CI Mode
# Project Autopilot - CI/CD pipeline generation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Generate and manage CI/CD pipelines for multiple providers with best practices built in.

## Required Skills

**Read before generating:**
1. `/autopilot/skills/ci-cd-patterns/SKILL.md` - Pipeline patterns
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `model-selector` - Choose optimal model

---

## Options

| Option | Description |
|--------|-------------|
| `--provider=prov` | CI provider: github, gitlab, bitbucket, circleci |
| `--template=tpl` | Template: basic, full, custom |
| `--update` | Update existing pipeline |
| `--add=job` | Add specific job to pipeline |
| `--optimize` | Optimize existing pipeline |
| `--validate` | Validate pipeline configuration |
| `--matrix` | Enable matrix builds |

---

## Supported Providers

| Provider | Config File | Features |
|----------|-------------|----------|
| GitHub Actions | `.github/workflows/*.yml` | Matrix, caching, artifacts |
| GitLab CI | `.gitlab-ci.yml` | Stages, environments, SAST |
| Bitbucket | `bitbucket-pipelines.yml` | Pipes, deployments |
| CircleCI | `.circleci/config.yml` | Orbs, workflows |

---

## Usage

### Generate Basic Pipeline

```bash
/autopilot:ci --provider=github --template=basic
```

Output:
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
```

### Generate Full Pipeline

```bash
/autopilot:ci --provider=github --template=full
```

Output:
```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Lint and type check
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  # Unit and integration tests
  test:
    runs-on: ubuntu-latest
    needs: lint

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci

      - name: Run tests
        run: npm test -- --coverage
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  # E2E tests
  e2e:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  # Security scanning
  security:
    runs-on: ubuntu-latest
    needs: lint
    permissions:
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2

  # Build and push Docker image
  build:
    runs-on: ubuntu-latest
    needs: [test, e2e]
    if: github.event_name != 'pull_request'
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Deploy to staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          # Your staging deployment script
          echo "Deploying to staging..."

  # Deploy to production
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'release'
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          # Your production deployment script
          echo "Deploying to production..."
```

### Add Specific Job

```bash
/autopilot:ci --add=security
```

### Matrix Builds

```bash
/autopilot:ci --provider=github --matrix
```

Output:
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

### Validate Pipeline

```bash
/autopilot:ci --validate
```

Output:
```markdown
## Pipeline Validation

### Syntax Check ✅
No syntax errors found.

### Best Practices

| Check | Status | Note |
|-------|--------|------|
| Caching enabled | ✅ | npm cache configured |
| Secrets not hardcoded | ✅ | Using secrets context |
| Pinned action versions | ⚠️ | Use @v4 instead of @latest |
| Timeout configured | ❌ | Add timeout-minutes |
| Concurrency control | ❌ | Add concurrency group |

### Recommendations

1. **Add timeout to jobs**
```yaml
jobs:
  test:
    timeout-minutes: 15
```

2. **Add concurrency control**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

3. **Pin action versions**
```yaml
# Instead of
uses: actions/checkout@latest

# Use
uses: actions/checkout@v4
```
```

### Optimize Pipeline

```bash
/autopilot:ci --optimize
```

---

## Behavior

```
FUNCTION generateCI(options):

    # 1. Detect or use specified provider
    IF options.provider:
        provider = options.provider
    ELSE:
        provider = detectCIProvider()

    # 2. Detect project type
    projectType = detectProjectType()
    techStack = detectTechStack()

    # 3. Load template
    IF options.template == 'custom':
        template = loadCustomTemplate()
    ELSE:
        template = loadTemplate(provider, options.template)

    # 4. Generate pipeline
    pipeline = generatePipeline(template, {
        projectType,
        techStack,
        matrix: options.matrix,
    })

    # 5. Handle modes
    IF options.validate:
        results = validatePipeline(readExistingPipeline())
        DISPLAY validationResults(results)
        RETURN

    IF options.optimize:
        optimizations = findOptimizations(readExistingPipeline())
        DISPLAY optimizationSuggestions(optimizations)
        RETURN

    IF options.add:
        pipeline = addJob(readExistingPipeline(), options.add)

    IF options.update:
        pipeline = mergePipeline(readExistingPipeline(), pipeline)

    # 6. Write pipeline
    configPath = getConfigPath(provider)
    writeFile(configPath, pipeline)

    DISPLAY pipelineSummary(pipeline)
```

---

## Provider Templates

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

lint:
  stage: lint
  image: node:${NODE_VERSION}
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint

test:
  stage: test
  image: node:${NODE_VERSION}
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test
    POSTGRES_PASSWORD: postgres
  script:
    - npm ci
    - npm test

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
  environment:
    name: production
  only:
    - main
  when: manual
```

---

## Quick Examples

```bash
# Generate basic GitHub Actions
/autopilot:ci --provider=github --template=basic

# Generate full pipeline with all jobs
/autopilot:ci --provider=github --template=full

# Add security scanning job
/autopilot:ci --add=security

# Enable matrix testing
/autopilot:ci --matrix

# Validate existing pipeline
/autopilot:ci --validate

# Optimize pipeline
/autopilot:ci --optimize

# Update existing with new best practices
/autopilot:ci --update
```

$ARGUMENTS
