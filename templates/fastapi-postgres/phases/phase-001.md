# Phase 001: Project Setup
# Template: fastapi-postgres
# Project: {{project_name}}
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Status:** ⏳ Pending
**Prerequisites:** None (initial phase)
**Provides:** Project structure, FastAPI setup, Database configuration

---

## Budget

### 💰 Estimate
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | 4 | - |
| Input Tokens | ~6K | High |
| Output Tokens | ~10K | High |
| **Est. Cost** | **$0.20** | High |

### 📊 Actual *(Updated during execution)*
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | 6K | - | - |
| Output Tokens | 10K | - | - |
| **Total Cost** | **$0.20** | **-** | - |

---

## Objective

Initialize a Python project with FastAPI, PostgreSQL via SQLAlchemy, and development tooling.

## Dependencies
- [ ] None (initial phase)

## Quality Gate (Entry)
- [ ] Empty or new directory
- [ ] Python {{python_version}}+ available
- [ ] PostgreSQL available
- [ ] pip/uv available

---

## Tasks

### Task 001.1: Initialize Python Project
**Status:** ⏳ Pending
**Agent:** backend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2.5K tokens |
| **Est. Cost** | **$0.05** |

**Prerequisites:** None
**Blocks:** 001.2, 001.3, 001.4

**Actions:**
- Create pyproject.toml with project configuration
- Set up virtual environment structure
- Add essential dependencies (fastapi, uvicorn, sqlalchemy, pydantic)

**Files:**
- Creates: `pyproject.toml`
- Creates: `.gitignore`
- Creates: `README.md`
- Creates: `.env.example`

**Acceptance Criteria:**
- [ ] pyproject.toml created with correct structure
- [ ] Dependencies listed correctly
- [ ] Virtual environment can be created

---

### Task 001.2: Configure Database
**Status:** ⏳ Pending
**Agent:** database
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2.5K tokens |
| **Est. Cost** | **$0.05** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Create database configuration module
- Set up SQLAlchemy engine and session
- Create base model class
- Configure Alembic for migrations

**Files:**
- Creates: `src/database/config.py`
- Creates: `src/database/session.py`
- Creates: `src/database/base.py`
- Creates: `alembic.ini`
- Creates: `alembic/env.py`

**Acceptance Criteria:**
- [ ] Database connection works
- [ ] Session factory configured
- [ ] Alembic initialized

---

### Task 001.3: Create FastAPI Application
**Status:** ⏳ Pending
**Agent:** backend
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2.5K tokens |
| **Est. Cost** | **$0.05** |

**Prerequisites:** Task 001.1 complete
**Blocked By:** 001.1

**Actions:**
- Create main FastAPI application
- Configure CORS middleware
- Set up health check endpoint
- Configure OpenAPI documentation

**Files:**
- Creates: `src/main.py`
- Creates: `src/api/__init__.py`
- Creates: `src/api/health.py`
- Creates: `src/core/config.py`

**Acceptance Criteria:**
- [ ] FastAPI app runs
- [ ] Health endpoint responds
- [ ] Swagger UI accessible at /docs

---

### Task 001.4: Set Up Development Environment
**Status:** ⏳ Pending
**Agent:** devops
**Model:** Haiku

#### 💰 Estimate
| Metric | Estimate |
|--------|----------|
| Input | ~1.5K tokens |
| Output | ~2.5K tokens |
| **Est. Cost** | **$0.05** |

**Prerequisites:** Tasks 001.2, 001.3 complete
**Blocked By:** 001.2, 001.3

**Actions:**
- Create Docker Compose for local development
- Configure PostgreSQL container
- Set up development scripts
- Create Makefile for common commands

**Files:**
- Creates: `docker-compose.yml`
- Creates: `Dockerfile`
- Creates: `Makefile`
- Creates: `scripts/start-dev.sh`

**Acceptance Criteria:**
- [ ] `docker-compose up` starts services
- [ ] PostgreSQL accessible
- [ ] FastAPI hot-reload works

---

## Phase Summary

### Cost Breakdown
| Task | Description | Est. | Actual | Status |
|------|-------------|------|--------|--------|
| 001.1 | Initialize project | $0.05 | - | ⏳ |
| 001.2 | Database config | $0.05 | - | ⏳ |
| 001.3 | FastAPI setup | $0.05 | - | ⏳ |
| 001.4 | Dev environment | $0.05 | - | ⏳ |
| **Total** | | **$0.20** | **-** | |

### Quality Gate (Exit)
- [ ] All tasks complete
- [ ] `docker-compose up` succeeds
- [ ] API responds at http://localhost:8000
- [ ] Health check passes: GET /health
- [ ] Swagger docs accessible: GET /docs
- [ ] Database migrations run successfully

## Rollback Plan
```bash
# Remove project directory if initialization fails
rm -rf {{project_name}}

# Stop and remove Docker containers
docker-compose down -v
```
