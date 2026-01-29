---
description: Auto-generate documentation from code including API docs, README, guides, and changelogs
argument-hint: "[--type=api|readme|guide|changelog|arch] [--output=path] [--format=md|html]"
model: haiku
---

# Autopilot: DOCS Mode
# Project Autopilot - Documentation generation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Auto-generate documentation from code analysis, comments, and project structure.

## Required Skills

**Read before generating docs:**
1. `/autopilot/skills/documentation-generation/SKILL.md` - Doc templates and patterns
2. `/autopilot/skills/token-optimization/SKILL.md` - Minimize token usage

## Required Agents

- `model-selector` - Choose optimal model per task

---

## Options

| Option | Description |
|--------|-------------|
| `--type=type` | Documentation type (see below) |
| `--output=path` | Output file path |
| `--format=fmt` | Output format: md, html, json |
| `--include=glob` | Files to analyze |
| `--exclude=glob` | Files to exclude |
| `--update` | Update existing docs |
| `--badges` | Include status badges (README) |

---

## Documentation Types

| Type | Description | Output |
|------|-------------|--------|
| `api` | OpenAPI/Swagger from routes | `docs/api.yaml` |
| `readme` | Project README | `README.md` |
| `guide` | User/developer guide | `docs/guide.md` |
| `changelog` | Git-based changelog | `CHANGELOG.md` |
| `arch` | Architecture documentation | `docs/architecture.md` |
| `components` | React component docs | `docs/components.md` |

---

## Usage

### Generate API Documentation

```bash
/autopilot:docs --type=api
```

Output:
```yaml
# docs/api.yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: Auto-generated API documentation

paths:
  /api/users:
    get:
      summary: List all users
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
        '404':
          description: User not found

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
```

### Generate README

```bash
/autopilot:docs --type=readme --badges
```

Output:
```markdown
# My Project

![Build Status](https://img.shields.io/github/workflow/status/user/repo/CI)
![Coverage](https://img.shields.io/codecov/c/github/user/repo)
![License](https://img.shields.io/github/license/user/repo)

Brief description extracted from package.json

## Features

- Feature 1 (detected from code)
- Feature 2
- Feature 3

## Installation

```bash
npm install my-project
```

## Quick Start

```typescript
import { MyProject } from 'my-project';

const app = new MyProject();
app.start();
```

## API Reference

See [API Documentation](./docs/api.md)

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3000 |
| `DATABASE_URL` | Database connection | - |

## Contributing

See [Contributing Guide](./CONTRIBUTING.md)

## License

MIT
```

### Generate Changelog

```bash
/autopilot:docs --type=changelog
```

Output:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-01-29

### Added
- User authentication system (#45)
- Rate limiting middleware (#48)

### Changed
- Updated to Express 5.0 (#50)
- Improved error handling (#51)

### Fixed
- Memory leak in connection pool (#47)
- Race condition in cache (#49)

## [1.1.0] - 2026-01-15

### Added
- Initial API endpoints
- Database migrations

[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

### Generate Architecture Documentation

```bash
/autopilot:docs --type=arch
```

Output:
```markdown
# Architecture Documentation

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                      Client Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Web App   │  │ Mobile App  │  │   CLI Tool  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────┐
│                      API Layer                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │               Express Server                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │   │
│  │  │ Routes  │─▶│ Services│─▶│  Repositories   │  │   │
│  │  └─────────┘  └─────────┘  └────────┬────────┘  │   │
│  └─────────────────────────────────────┼───────────┘   │
└────────────────────────────────────────┼────────────────┘
                                         │
┌────────────────────────────────────────┼────────────────┐
│                    Data Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  PostgreSQL │  │    Redis    │  │     S3      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Components

### Routes (`src/routes/`)
Entry points for HTTP requests. Handle request parsing, validation,
and response formatting.

### Services (`src/services/`)
Business logic layer. Orchestrates operations and enforces rules.

### Repositories (`src/repositories/`)
Data access layer. Abstracts database operations.

## Data Flow

1. Request enters through route
2. Route validates and forwards to service
3. Service applies business logic
4. Repository handles data operations
5. Response returns through same path

## Security

- JWT authentication
- Role-based authorization
- Input validation on all endpoints
- Rate limiting: 100 req/min

## Scalability

- Stateless API servers (horizontal scaling)
- Redis for session caching
- PostgreSQL read replicas
- S3 for file storage
```

---

## Behavior

```
FUNCTION generateDocs(options):

    # 1. Detect project type
    projectType = detectProjectType()

    # 2. Analyze source files
    IF options.type == 'api':
        analysis = analyzeRoutes(options.include)
        template = loadTemplate('openapi')

    ELIF options.type == 'readme':
        analysis = analyzeProject()
        template = loadTemplate('readme')

    ELIF options.type == 'changelog':
        analysis = analyzeGitHistory()
        template = loadTemplate('changelog')

    ELIF options.type == 'arch':
        analysis = analyzeArchitecture()
        template = loadTemplate('architecture')

    ELIF options.type == 'guide':
        analysis = analyzeUsage()
        template = loadTemplate('guide')

    # 3. Generate documentation
    docs = renderTemplate(template, analysis)

    # 4. Format output
    IF options.format == 'html':
        docs = convertToHtml(docs)
    ELIF options.format == 'json':
        docs = convertToJson(docs)

    # 5. Add badges if requested
    IF options.badges:
        docs = addBadges(docs, detectCI())

    # 6. Write output
    outputPath = options.output OR defaultPath(options.type)

    IF options.update AND exists(outputPath):
        docs = mergeWithExisting(docs, readFile(outputPath))

    writeFile(outputPath, docs)

    LOG "Generated {options.type} documentation: {outputPath}"
```

---

## Detection Capabilities

### API Route Detection

| Framework | Detection Method |
|-----------|------------------|
| Express | `app.get/post/put/delete` patterns |
| Fastify | Route handlers and schemas |
| Next.js | `pages/api` and `app/api` directories |
| NestJS | Decorators and modules |
| FastAPI | Route decorators and Pydantic models |
| Flask | Route decorators |

### Type Extraction

| Source | Extraction |
|--------|------------|
| TypeScript | Interface/type definitions |
| JSDoc | @param, @returns annotations |
| OpenAPI | Existing schema definitions |
| Pydantic | Model definitions |
| Zod | Schema definitions |

---

## Quick Examples

```bash
# Generate API docs
/autopilot:docs --type=api

# Generate README with badges
/autopilot:docs --type=readme --badges

# Generate changelog from git
/autopilot:docs --type=changelog

# Generate architecture docs
/autopilot:docs --type=arch

# Update existing docs
/autopilot:docs --type=readme --update

# Generate as HTML
/autopilot:docs --type=guide --format=html --output=docs/guide.html
```

$ARGUMENTS
