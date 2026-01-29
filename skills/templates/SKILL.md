---
name: templates
description: Template system for project scaffolding. Variable syntax, template structure, and customization guidelines.
---

# Templates Skill
# Project Autopilot - Template system documentation
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for creating, customizing, and using project templates.

---

## Template Directory Structure

```
templates/
├── nextjs-supabase/
│   ├── template.yaml        # Template metadata and configuration
│   ├── scaffold/            # Files to create in new project
│   │   ├── package.json.tmpl
│   │   ├── tsconfig.json.tmpl
│   │   ├── .env.example.tmpl
│   │   ├── .gitignore
│   │   └── src/
│   │       ├── app/
│   │       │   ├── layout.tsx.tmpl
│   │       │   └── page.tsx.tmpl
│   │       └── lib/
│   │           └── supabase.ts.tmpl
│   └── phases/              # Pre-defined Autopilot phases
│       ├── 001/
│       │   └── PHASE.md
│       ├── 002/
│       │   └── PHASE.md
│       └── ...
├── fastapi-postgres/
│   └── ...
└── cli-tool/
    └── ...
```

---

## Template Configuration (template.yaml)

```yaml
# Template metadata
name: nextjs-supabase
version: "1.0"
description: Full-stack web application with Next.js 14 and Supabase
author: Project Autopilot

# Tech stack (for matching similar projects)
techStack:
  - nextjs
  - supabase
  - typescript
  - tailwind

# Template variables
variables:
  - name: project_name
    description: Project name (used for package.json, directory)
    required: true

  - name: database_name
    description: Supabase database name
    default: "{{project_name}}_db"

  - name: auth_provider
    description: Authentication provider
    options:
      - supabase
      - clerk
      - auth0
    default: supabase

  - name: include_storage
    description: Include Supabase Storage setup
    type: boolean
    default: true

  - name: include_realtime
    description: Include Supabase Realtime setup
    type: boolean
    default: false

# Phases pre-defined by this template
phases:
  - id: "001"
    name: Project Setup
    description: Initialize project with dependencies and configuration
    cost: 0.15
    provides: "Project structure, TypeScript config, Tailwind setup"

  - id: "002"
    name: Supabase Configuration
    description: Set up Supabase client, types, and environment
    cost: 0.25
    prerequisites: ["001"]
    provides: "Supabase client, type generation, env config"

  - id: "003"
    name: Authentication
    description: Implement authentication with {{auth_provider}}
    cost: 0.85
    prerequisites: ["002"]
    provides: "Login, signup, password reset, session management"

  # ... more phases

# Commands for the generated project
commands:
  install: "npm install"
  dev: "npm run dev"
  build: "npm run build"
  test: "npm test"

# Total estimated cost
totalCost: 6.50

# Features included
features:
  - Authentication
  - Database with migrations
  - API routes
  - Tailwind styling
  - TypeScript
  - Testing setup
```

---

## Variable Syntax

### Basic Variables

In template files (`.tmpl`), use double curly braces:

```typescript
// package.json.tmpl
{
  "name": "{{project_name}}",
  "version": "0.1.0",
  "description": "{{description}}"
}
```

### Default Built-in Variables

| Variable | Description |
|----------|-------------|
| `{{project_name}}` | User-provided project name |
| `{{_timestamp}}` | Current ISO timestamp |
| `{{_year}}` | Current year |
| `{{_date}}` | Current date (YYYY-MM-DD) |

### Conditional Blocks

Include content only if variable is truthy:

```typescript
// supabase.ts.tmpl

import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

{{#if include_storage}}
// Storage helpers
export const uploadFile = async (bucket: string, path: string, file: File) => {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file);
  return { data, error };
};
{{/if}}

{{#if include_realtime}}
// Realtime subscription helper
export const subscribeToTable = (table: string, callback: Function) => {
  return supabase
    .channel(`${table}_changes`)
    .on('postgres_changes', { event: '*', schema: 'public', table }, callback)
    .subscribe();
};
{{/if}}
```

### Unless Blocks (Negation)

Include content only if variable is falsy:

```typescript
{{#unless production}}
// Development-only logging
console.log('Debug mode enabled');
{{/unless}}
```

### Each Loops

Iterate over arrays:

```typescript
// features/index.ts.tmpl

{{#each features}}
export { {{this}} } from './{{this}}';
{{/each}}
```

With index:

```typescript
{{#each phases}}
// Phase {{@index}}: {{this.name}}
{{/each}}
```

---

## File Naming

### Template Extension

Files ending in `.tmpl` are processed for variable substitution:
- `package.json.tmpl` → `package.json`
- `src/config.ts.tmpl` → `src/config.ts`

Files without `.tmpl` are copied as-is:
- `.gitignore` → `.gitignore`
- `public/favicon.ico` → `public/favicon.ico`

### Dynamic File Names

Use variables in file names:

```
scaffold/
├── src/
│   └── {{project_name}}.config.ts.tmpl
```

With `project_name=my-app`, creates:
```
src/my-app.config.ts
```

---

## Phase Template Files

### Phase File Structure

```markdown
# Phase [XXX]: [Phase Name]
# Template: {{_template_name}}
# Project: {{project_name}}

**Status:** ⏳ Pending
**Prerequisites:** {{prerequisites}}
**Provides:** {{provides}}

---

## Budget

### 💰 Estimate
| Metric | Estimate | Confidence |
|--------|----------|------------|
| Tasks | [N] | - |
| Input Tokens | ~[X]K | Medium |
| Output Tokens | ~[Y]K | Medium |
| **Est. Cost** | **$[Z]** | Medium |

### 📊 Actual *(Updated during execution)*
| Metric | Estimated | Actual | Variance |
|--------|-----------|--------|----------|
| Input Tokens | [X]K | - | - |
| Output Tokens | [Y]K | - | - |
| **Total Cost** | **$[Z]** | **-** | - |

---

## Objective

[Template-specific objective]

## Tasks

### Task [XXX].1: [Task Name]
**Status:** ⏳ Pending
**Agent:** [agent-name]
**Model:** Sonnet

[Task details...]

---

## Quality Gate (Exit)
- [ ] All tasks complete
- [ ] Build passes
- [ ] Tests pass
```

---

## Creating Custom Templates

### Step 1: Create Directory Structure

```bash
mkdir -p templates/my-template/{scaffold,phases}
```

### Step 2: Create template.yaml

```yaml
name: my-template
version: "1.0"
description: My custom project template

techStack:
  - node
  - typescript

variables:
  - name: project_name
    required: true
  - name: author
    default: "Unknown"

phases:
  - id: "001"
    name: Setup
    cost: 0.15

totalCost: 2.00
```

### Step 3: Create Scaffold Files

```bash
# Create template files
touch templates/my-template/scaffold/package.json.tmpl
touch templates/my-template/scaffold/src/index.ts.tmpl
```

### Step 4: Create Phase Files

```bash
mkdir -p templates/my-template/phases/001
touch templates/my-template/phases/001/PHASE.md
```

### Step 5: Test Template

```bash
/autopilot:init my-template --name=test-project --dry-run
```

---

## Template Best Practices

### Variables

1. **Use descriptive names** - `database_name` not `db`
2. **Provide sensible defaults** - Minimize required inputs
3. **Validate with options** - Use `options` for constrained values
4. **Document clearly** - Include description for each variable

### Scaffold Files

1. **Include essentials** - package.json, tsconfig, .gitignore
2. **Provide .env.example** - Never commit actual secrets
3. **Include README** - Setup instructions for the template
4. **Test the output** - Ensure scaffolded project runs

### Phases

1. **Match scaffold to phases** - Phases should build on scaffold
2. **Include accurate estimates** - Based on similar projects
3. **Define clear dependencies** - Prevent execution order issues
4. **Set realistic totals** - Sum of phases ≤ totalCost

---

## Built-in Templates

### nextjs-supabase

Full-stack web app with:
- Next.js 14 App Router
- Supabase (Auth, DB, Storage)
- Tailwind CSS
- TypeScript
- Testing with Jest + Playwright

### fastapi-postgres

Python REST API with:
- FastAPI
- PostgreSQL + SQLAlchemy
- Alembic migrations
- Pydantic schemas
- Pytest

### cli-tool

Node.js CLI application with:
- Commander for CLI parsing
- TypeScript
- Jest testing
- npm packaging setup

---

## Template Variables Reference

### Variable Definition

```yaml
variables:
  - name: variable_name          # Required: unique identifier
    description: "Help text"     # Optional: shown in --info
    required: true               # Optional: default false
    type: string                 # Optional: string, boolean, number
    default: "value"             # Optional: default value
    options:                     # Optional: constrain to list
      - option1
      - option2
```

### Type Handling

| Type | Input | Template Value |
|------|-------|----------------|
| string | `"hello"` | `hello` |
| boolean | `true`/`false` | `true`/`false` |
| number | `42` | `42` |
| array | `"a,b,c"` | `["a","b","c"]` |

---

## Error Handling

### Missing Required Variable

```
Error: Required variable 'project_name' not provided.

Usage: /autopilot:init template-name --name=my-project
```

### Invalid Option Value

```
Error: Invalid value 'invalid' for variable 'auth_provider'.
Valid options: supabase, clerk, auth0
```

### Template Syntax Error

```
Error: Template syntax error in scaffold/config.ts.tmpl:12
  Unclosed conditional block: {{#if feature
```

---

## Integration Points

### With /autopilot:takeoff

After initialization:
```bash
cd my-project
/autopilot:takeoff -y  # Phases are pre-configured
```

### With /autopilot:estimate

Preview costs before initializing:
```bash
/autopilot:init --info=nextjs-supabase
# Shows estimated cost for all phases
```

### With Global History

Template usage is tracked:
```json
// ~/.claude/autopilot/history.json
{
  "projects": [{
    "template": "nextjs-supabase",
    "variables": { "auth_provider": "clerk" }
  }]
}
```
