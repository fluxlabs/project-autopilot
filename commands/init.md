---
description: Initialize project from template
argument-hint: "<template> [--name=project-name] [--var key=value]"
model: haiku
---

# Autopilot: INIT Mode
# Project Autopilot - Template-based project initialization
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Scaffold new projects from pre-defined templates with variable substitution and pre-configured phases.

## Required Skills

**Read before initializing:**
1. `/autopilot/skills/templates/SKILL.md` - Template system rules

## Required Agents

- `template-manager` - Scaffold projects from templates

---

## Options

| Option | Description |
|--------|-------------|
| `--name=X` | Project name (default: current directory name) |
| `--var key=value` | Set template variable (repeatable) |
| `--list` | List available templates |
| `--info=template` | Show template details |
| `--output=path` | Output directory (default: current) |
| `--no-git` | Skip git initialization |
| `--dry-run` | Show what would be created |

---

## Available Templates

| Template | Stack | Phases | Description |
|----------|-------|--------|-------------|
| `nextjs-supabase` | Next.js 14 + Supabase + Tailwind | 10 | Full-stack web app with auth |
| `fastapi-postgres` | FastAPI + PostgreSQL + SQLAlchemy | 8 | Python REST API |
| `react-native-expo` | Expo + React Native + Firebase | 9 | Cross-platform mobile app |
| `electron-react` | Electron + React + SQLite | 8 | Desktop application |
| `cli-tool` | Node.js + Commander + TypeScript | 5 | Command-line tool |
| `api-only` | Express/Fastify + PostgreSQL | 6 | Backend API service |

---

## Usage

### List Templates

```bash
/autopilot:init --list
```

Output:
```markdown
## Available Templates

| Template | Stack | Phases | Est. Cost |
|----------|-------|--------|-----------|
| nextjs-supabase | Next.js + Supabase | 10 | ~$6.50 |
| fastapi-postgres | FastAPI + PostgreSQL | 8 | ~$4.80 |
| react-native-expo | Expo + React Native | 9 | ~$7.20 |
| electron-react | Electron + React | 8 | ~$5.50 |
| cli-tool | Node.js CLI | 5 | ~$2.50 |
| api-only | Express + PostgreSQL | 6 | ~$3.80 |

**Usage:**
```bash
/autopilot:init <template> --name=my-project
```
```

### Template Info

```bash
/autopilot:init --info=nextjs-supabase
```

Output:
```markdown
## Template: nextjs-supabase

**Description:** Full-stack web application with Next.js 14, Supabase backend, and Tailwind CSS styling.

### Tech Stack
- Next.js 14 (App Router)
- Supabase (Auth, Database, Storage)
- Tailwind CSS
- TypeScript
- Jest + Playwright

### Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `project_name` | Yes | - | Project name |
| `database_name` | No | `{project_name}_db` | Supabase database |
| `auth_provider` | No | `supabase` | Auth: supabase, clerk, auth0 |
| `include_storage` | No | `true` | Include file storage |

### Phases (10 total)

| Phase | Description | Est. Cost |
|-------|-------------|-----------|
| 001 | Project setup & dependencies | $0.15 |
| 002 | Supabase configuration | $0.25 |
| 003 | Authentication system | $0.85 |
| 004 | Database schema & migrations | $0.45 |
| 005 | Core API routes | $0.75 |
| 006 | UI component library | $0.90 |
| 007 | Page templates | $1.20 |
| 008 | Testing setup | $0.65 |
| 009 | Security & validation | $0.55 |
| 010 | Documentation & deployment | $0.75 |

**Total Estimate:** ~$6.50

### Usage
```bash
/autopilot:init nextjs-supabase --name=my-app --var auth_provider=clerk
```
```

### Initialize Project

```bash
/autopilot:init nextjs-supabase --name=my-saas-app
```

Output:
```markdown
## Initializing: my-saas-app

**Template:** nextjs-supabase
**Output:** /Users/user/projects/my-saas-app

### Variables
| Variable | Value |
|----------|-------|
| project_name | my-saas-app |
| database_name | my_saas_app_db |
| auth_provider | supabase |
| include_storage | true |

### Creating Files...
✅ package.json
✅ tsconfig.json
✅ next.config.js
✅ tailwind.config.js
✅ .env.example
✅ .gitignore
✅ README.md
✅ src/app/layout.tsx
✅ src/app/page.tsx
✅ src/lib/supabase.ts
✅ ... (24 more files)

### Creating Autopilot Structure...
✅ .autopilot/clearance.md
✅ .autopilot/flightplan.md
✅ .autopilot/TRANSPONDER.md
✅ .autopilot/phases/001/PHASE.md
✅ .autopilot/phases/002/PHASE.md
✅ ... (8 more phases)

### Git Initialization
✅ Initialized git repository
✅ Created initial commit

---

## Project Ready!

**Next Steps:**
```bash
cd my-saas-app

# Configure Supabase
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# Install dependencies
npm install

# Start development
npm run dev

# Begin Autopilot execution
/autopilot:takeoff -y
```

**Estimated Cost:** ~$6.50
**Estimated Phases:** 10
```

---

## Behavior

```
FUNCTION init(template, options):

    # 1. Validate template exists
    templatePath = findTemplate(template)
    IF NOT templatePath:
        ERROR "Template '{template}' not found"
        SHOW "Run /autopilot:init --list to see available templates"
        RETURN

    # 2. Load template configuration
    config = readYAML(templatePath + "/template.yaml")

    # 3. Collect variables
    variables = {
        project_name: options.name OR basename(cwd())
    }

    # Process --var arguments
    FOR each var IN options.vars:
        variables[var.key] = var.value

    # Apply defaults
    FOR each varDef IN config.variables:
        IF NOT variables[varDef.name] AND varDef.default:
            variables[varDef.name] = interpolate(varDef.default, variables)

    # Validate required variables
    FOR each varDef IN config.variables:
        IF varDef.required AND NOT variables[varDef.name]:
            ERROR "Required variable missing: {varDef.name}"
            RETURN

    # 4. Determine output directory
    outputDir = options.output OR cwd()
    IF NOT options.output AND options.name:
        outputDir = path.join(cwd(), options.name)

    # 5. Check output directory
    IF exists(outputDir) AND NOT isEmpty(outputDir):
        ERROR "Directory not empty: {outputDir}"
        RETURN

    # 6. Spawn template-manager
    SPAWN template-manager → scaffold({
        template: templatePath,
        variables: variables,
        outputDir: outputDir,
        dryRun: options.dryRun,
        initGit: NOT options.noGit
    })
```

---

## Template Variables

### Variable Syntax

In template files, use `{{variable_name}}`:

```typescript
// src/config.ts
export const config = {
  appName: '{{project_name}}',
  database: '{{database_name}}',
};
```

### Conditional Blocks

```typescript
// {{#if include_storage}}
import { storage } from './storage';
// {{/if}}
```

### Loops

```typescript
// {{#each features}}
import { {{this}} } from './features/{{this}}';
// {{/each}}
```

---

## Custom Variables

Pass custom variables with `--var`:

```bash
/autopilot:init nextjs-supabase \
  --name=my-app \
  --var auth_provider=clerk \
  --var include_storage=false \
  --var features="blog,payments,analytics"
```

---

## Dry Run

Preview what would be created:

```bash
/autopilot:init nextjs-supabase --name=test --dry-run
```

Output:
```markdown
## Dry Run: test

**Would create directory:** /Users/user/projects/test

### Files to be created:
- package.json (2.1 KB)
- tsconfig.json (0.8 KB)
- next.config.js (0.5 KB)
- ... (31 files total)

### Autopilot structure:
- .autopilot/scope.md
- .autopilot/roadmap.md
- .autopilot/phases/ (10 files)

### Git:
- Would initialize repository
- Would create initial commit

**No files were created (dry run)**
```

---

## Integration with Build

After initializing, start building:

```bash
# Initialize
/autopilot:init cli-tool --name=my-cli

# Navigate to project
cd my-cli

# Start building (phases are pre-configured)
/autopilot:takeoff -y
```

The template provides:
- Pre-configured scope.md with feature description
- Complete phase breakdown with estimates
- Scaffold files matching phase expectations

---

## Creating Custom Templates

See `/autopilot/skills/templates/SKILL.md` for creating custom templates.

Basic structure:
```
templates/my-template/
├── template.yaml       # Metadata and variables
├── scaffold/          # File templates
│   ├── package.json.tmpl
│   └── src/
│       └── index.ts.tmpl
└── phases/            # Pre-defined phases
    ├── 001/
    │   └── PHASE.md
    └── 002/
        └── PHASE.md
```

---

## Error Handling

### Template Not Found
```markdown
## Error: Template Not Found

Template 'invalid-template' does not exist.

**Available templates:**
- nextjs-supabase
- fastapi-postgres
- cli-tool

Run `/autopilot:init --list` for details.
```

### Missing Required Variable
```markdown
## Error: Missing Required Variable

Template 'nextjs-supabase' requires variable: project_name

**Usage:**
```bash
/autopilot:init nextjs-supabase --name=my-project
```

Or:
```bash
/autopilot:init nextjs-supabase --var project_name=my-project
```
```

### Directory Not Empty
```markdown
## Error: Directory Not Empty

Cannot initialize in non-empty directory: /Users/user/projects/existing

**Options:**
1. Use a different directory: `--output=/path/to/new-dir`
2. Use a project name: `--name=new-project`
3. Clear the directory first
```

$ARGUMENTS
