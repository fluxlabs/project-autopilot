---
name: documentation-generation
description: Documentation templates, JSDoc/TSDoc patterns, and auto-generation strategies. Reference this skill when generating documentation.
---

# Documentation Generation Skill
# Project Autopilot - Documentation templates and patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for generating high-quality documentation.

---

## Documentation Types

### README Template

```markdown
# Project Name

![Build Status](badge-url)
![Coverage](badge-url)
![License](badge-url)

Brief, compelling description in 1-2 sentences.

## Features

- ✨ Feature 1 - Brief description
- 🚀 Feature 2 - Brief description
- 🔒 Feature 3 - Brief description

## Quick Start

```bash
npm install package-name
```

```typescript
import { Thing } from 'package-name';

const thing = new Thing();
thing.doSomething();
```

## Installation

### Prerequisites
- Node.js 18+
- npm/yarn/pnpm

### Install
```bash
npm install package-name
```

## Usage

### Basic Example
[Code example with explanation]

### Advanced Example
[More complex example]

## API Reference

See [API Documentation](./docs/api.md)

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | string | `'default'` | What it does |
| `option2` | number | `100` | What it does |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT © [Author]
```

---

## API Documentation

### OpenAPI Template

```yaml
openapi: 3.0.3
info:
  title: API Name
  description: Brief API description
  version: 1.0.0
  contact:
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /resource:
    get:
      summary: List resources
      description: Returns a paginated list of resources
      operationId: listResources
      tags:
        - Resources
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    Resource:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        createdAt:
          type: string
          format: date-time

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## Code Documentation

### TypeScript/JSDoc Patterns

```typescript
/**
 * User service for managing user accounts.
 *
 * @example
 * ```typescript
 * const userService = new UserService(db);
 * const user = await userService.findById('123');
 * ```
 */
class UserService {
  /**
   * Creates a new UserService instance.
   *
   * @param db - Database connection
   * @param cache - Optional cache client
   */
  constructor(
    private readonly db: Database,
    private readonly cache?: CacheClient
  ) {}

  /**
   * Finds a user by their unique identifier.
   *
   * @param id - The user's unique identifier
   * @returns The user if found, null otherwise
   * @throws {DatabaseError} If database connection fails
   *
   * @example
   * ```typescript
   * const user = await service.findById('user-123');
   * if (user) {
   *   console.log(user.email);
   * }
   * ```
   */
  async findById(id: string): Promise<User | null> {
    // Implementation
  }

  /**
   * Creates a new user account.
   *
   * @param data - User creation data
   * @param data.email - User's email address
   * @param data.name - User's display name
   * @param data.password - User's password (will be hashed)
   * @returns The created user
   * @throws {ValidationError} If email is invalid
   * @throws {ConflictError} If email already exists
   */
  async create(data: CreateUserInput): Promise<User> {
    // Implementation
  }
}
```

### Python Docstrings

```python
"""User service for managing user accounts.

This module provides the UserService class for CRUD operations
on user accounts.

Example:
    >>> service = UserService(db)
    >>> user = await service.find_by_id("123")
    >>> print(user.email)
"""

from typing import Optional


class UserService:
    """Service class for user account management.

    Attributes:
        db: Database connection instance
        cache: Optional cache client for performance

    Example:
        >>> service = UserService(db, cache=redis_client)
        >>> users = await service.list_all(page=1, limit=10)
    """

    def __init__(self, db: Database, cache: Optional[CacheClient] = None):
        """Initialize UserService.

        Args:
            db: Database connection
            cache: Optional cache client
        """
        self.db = db
        self.cache = cache

    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by their unique identifier.

        Args:
            user_id: The user's unique identifier

        Returns:
            The user if found, None otherwise

        Raises:
            DatabaseError: If database connection fails

        Example:
            >>> user = await service.find_by_id("user-123")
            >>> if user:
            ...     print(user.email)
        """
        pass
```

---

## Architecture Documentation

### C4 Model Template

```markdown
# Architecture Documentation

## Level 1: System Context

```
┌─────────────────────────────────────────────────────────────┐
│                         [Users]                              │
│                     Web/Mobile Users                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    [Our System]                              │
│              Main Application System                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    [Email API]  [Payment]   [Analytics]
```

## Level 2: Container Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Our System                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web App   │  │   Mobile    │  │    Admin    │        │
│  │   (React)   │  │   (RN)      │  │   (React)   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         └────────────────┼────────────────┘                │
│                          ▼                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    API Gateway                         │ │
│  │                    (Kong/AWS)                          │ │
│  └───────────────────────┬───────────────────────────────┘ │
│                          │                                  │
│         ┌────────────────┼────────────────┐                │
│         ▼                ▼                ▼                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Auth     │  │   Orders    │  │   Users     │        │
│  │  Service    │  │  Service    │  │  Service    │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         └────────────────┼────────────────┘                │
│                          ▼                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    PostgreSQL                          │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Level 3: Component Diagram

[Detailed component breakdown for each service]

## Data Flow

### User Authentication Flow

```
User → Web App → API Gateway → Auth Service → Database
                     ↓
              JWT Token ← ← ← ← ← ← ← ← ←
```

## Decision Records

### ADR-001: Database Selection

**Status:** Accepted
**Context:** Need persistent storage for user data
**Decision:** PostgreSQL
**Consequences:** Strong consistency, mature ecosystem
```

---

## Changelog Format

### Keep a Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature in development

## [1.2.0] - 2026-01-29

### Added
- User authentication with OAuth
- Rate limiting middleware (#48)

### Changed
- Updated to Express 5.0 (#50)
- Improved error messages

### Deprecated
- Old configuration format (use new format)

### Removed
- Legacy API endpoints

### Fixed
- Memory leak in connection pool (#47)

### Security
- Updated dependencies with known vulnerabilities

## [1.1.0] - 2026-01-15

### Added
- Initial release

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

---

## Detection Strategies

### Route Detection

| Framework | Pattern |
|-----------|---------|
| Express | `app.METHOD(path, handler)` |
| Fastify | `fastify.METHOD(path, opts, handler)` |
| Next.js | File-based routing in `app/api` |
| NestJS | `@Controller`, `@Get`, `@Post` decorators |
| FastAPI | `@app.get()`, `@app.post()` decorators |
| Flask | `@app.route()` decorator |

### Type Extraction

| Source | Method |
|--------|--------|
| TypeScript | Parse interfaces, types, generics |
| JSDoc | Parse @param, @returns, @typedef |
| Python | Parse type hints, dataclasses |
| Pydantic | Parse model fields |
| Zod | Parse schema definitions |

### Example Detection

```typescript
// From code comments
// Example: const user = await getUser('123')

// From test files
describe('getUser', () => {
  it('returns user by id', async () => {
    const user = await getUser('123');
    expect(user.id).toBe('123');
  });
});

// From JSDoc
/**
 * @example
 * const user = await getUser('123');
 */
```

---

## Quality Checklist

### README Quality

- [ ] Clear project description
- [ ] Installation instructions
- [ ] Quick start example
- [ ] API reference link
- [ ] Contributing guidelines
- [ ] License information
- [ ] Badge accuracy

### API Documentation Quality

- [ ] All endpoints documented
- [ ] Request/response schemas
- [ ] Authentication explained
- [ ] Error codes listed
- [ ] Examples provided
- [ ] Versioning documented

### Code Documentation Quality

- [ ] All public APIs documented
- [ ] Parameters described
- [ ] Return values specified
- [ ] Exceptions documented
- [ ] Examples included
- [ ] No outdated comments
