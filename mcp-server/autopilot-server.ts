#!/usr/bin/env node
// Project Autopilot MCP Server - External tool integration for project management
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

// =============================================================================
// Configuration
// =============================================================================

const AUTOPILOT_DIR = path.join(os.homedir(), ".claude", "autopilot");
const PROJECTS_DIR = path.join(AUTOPILOT_DIR, "projects");
const LEARNINGS_FILE = path.join(AUTOPILOT_DIR, "global-learnings.md");
const HISTORY_FILE = path.join(AUTOPILOT_DIR, "project-history.json");

// =============================================================================
// Types
// =============================================================================

interface ProjectState {
  id: string;
  name: string;
  status: "planning" | "active" | "paused" | "completed";
  currentPhase: number;
  totalPhases: number;
  startDate: string;
  lastUpdated: string;
  estimatedCost: number;
  actualCost: number;
}

interface PhaseData {
  id: number;
  name: string;
  status: "pending" | "in_progress" | "completed" | "blocked";
  tasks: TaskData[];
  startTime?: string;
  endTime?: string;
  tokenUsage?: number;
}

interface TaskData {
  id: string;
  description: string;
  status: "pending" | "in_progress" | "completed" | "failed";
  assignedAgent?: string;
}

interface HistoryEntry {
  projectId: string;
  projectName: string;
  completedDate: string;
  totalCost: number;
  totalTokens: number;
  phases: number;
  tasks: number;
  successRate: number;
}

// =============================================================================
// Utility Functions
// =============================================================================

function ensureDirectories(): void {
  if (!fs.existsSync(AUTOPILOT_DIR)) {
    fs.mkdirSync(AUTOPILOT_DIR, { recursive: true });
  }
  if (!fs.existsSync(PROJECTS_DIR)) {
    fs.mkdirSync(PROJECTS_DIR, { recursive: true });
  }
}

function loadProjectState(projectId: string): ProjectState | null {
  const statePath = path.join(PROJECTS_DIR, projectId, "state.json");
  if (fs.existsSync(statePath)) {
    return JSON.parse(fs.readFileSync(statePath, "utf-8"));
  }
  return null;
}

function saveProjectState(projectId: string, state: ProjectState): void {
  const projectDir = path.join(PROJECTS_DIR, projectId);
  if (!fs.existsSync(projectDir)) {
    fs.mkdirSync(projectDir, { recursive: true });
  }
  fs.writeFileSync(
    path.join(projectDir, "state.json"),
    JSON.stringify(state, null, 2)
  );
}

function loadPhaseData(projectId: string, phaseId: number): PhaseData | null {
  const phasePath = path.join(
    PROJECTS_DIR,
    projectId,
    "phases",
    `phase-${phaseId}.json`
  );
  if (fs.existsSync(phasePath)) {
    return JSON.parse(fs.readFileSync(phasePath, "utf-8"));
  }
  return null;
}

function savePhaseData(
  projectId: string,
  phaseId: number,
  data: PhaseData
): void {
  const phasesDir = path.join(PROJECTS_DIR, projectId, "phases");
  if (!fs.existsSync(phasesDir)) {
    fs.mkdirSync(phasesDir, { recursive: true });
  }
  fs.writeFileSync(
    path.join(phasesDir, `phase-${phaseId}.json`),
    JSON.stringify(data, null, 2)
  );
}

function loadHistory(): HistoryEntry[] {
  if (fs.existsSync(HISTORY_FILE)) {
    return JSON.parse(fs.readFileSync(HISTORY_FILE, "utf-8"));
  }
  return [];
}

function saveHistory(history: HistoryEntry[]): void {
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

function loadLearnings(): string {
  if (fs.existsSync(LEARNINGS_FILE)) {
    return fs.readFileSync(LEARNINGS_FILE, "utf-8");
  }
  return "# Global Learnings\n\nNo learnings recorded yet.";
}

function appendLearning(learning: string): void {
  const current = loadLearnings();
  const timestamp = new Date().toISOString().split("T")[0];
  const updated = `${current}\n\n## ${timestamp}\n${learning}`;
  fs.writeFileSync(LEARNINGS_FILE, updated);
}

function generateProjectId(): string {
  return `proj-${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 7)}`;
}

function listProjects(): ProjectState[] {
  if (!fs.existsSync(PROJECTS_DIR)) {
    return [];
  }
  const projects: ProjectState[] = [];
  const dirs = fs.readdirSync(PROJECTS_DIR);
  for (const dir of dirs) {
    const state = loadProjectState(dir);
    if (state) {
      projects.push(state);
    }
  }
  return projects;
}

// =============================================================================
// MCP Server Setup
// =============================================================================

const server = new Server(
  {
    name: "autopilot-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// =============================================================================
// Tools
// =============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // Project Management Tools
      {
        name: "create_project",
        description: "Create a new autopilot project",
        inputSchema: {
          type: "object",
          properties: {
            name: { type: "string", description: "Project name" },
            description: { type: "string", description: "Project description" },
            totalPhases: {
              type: "number",
              description: "Total number of phases",
            },
            estimatedCost: {
              type: "number",
              description: "Estimated cost in dollars",
            },
          },
          required: ["name"],
        },
      },
      {
        name: "update_project_status",
        description: "Update project status",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            status: {
              type: "string",
              enum: ["planning", "active", "paused", "completed"],
              description: "New status",
            },
            actualCost: {
              type: "number",
              description: "Current actual cost",
            },
          },
          required: ["projectId", "status"],
        },
      },
      {
        name: "list_projects",
        description: "List all autopilot projects",
        inputSchema: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["planning", "active", "paused", "completed", "all"],
              description: "Filter by status",
            },
          },
        },
      },

      // Phase Management Tools
      {
        name: "create_phase",
        description: "Create a new phase for a project",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            phaseId: { type: "number", description: "Phase number" },
            name: { type: "string", description: "Phase name" },
            tasks: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  description: { type: "string" },
                },
              },
              description: "List of tasks for this phase",
            },
          },
          required: ["projectId", "phaseId", "name"],
        },
      },
      {
        name: "update_phase_status",
        description: "Update phase status",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            phaseId: { type: "number", description: "Phase number" },
            status: {
              type: "string",
              enum: ["pending", "in_progress", "completed", "blocked"],
              description: "New status",
            },
            tokenUsage: { type: "number", description: "Token usage for phase" },
          },
          required: ["projectId", "phaseId", "status"],
        },
      },
      {
        name: "get_phase",
        description: "Get phase details",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            phaseId: { type: "number", description: "Phase number" },
          },
          required: ["projectId", "phaseId"],
        },
      },

      // Task Management Tools
      {
        name: "update_task_status",
        description: "Update task status within a phase",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            phaseId: { type: "number", description: "Phase number" },
            taskId: { type: "string", description: "Task ID" },
            status: {
              type: "string",
              enum: ["pending", "in_progress", "completed", "failed"],
              description: "New status",
            },
            assignedAgent: {
              type: "string",
              description: "Agent assigned to task",
            },
          },
          required: ["projectId", "phaseId", "taskId", "status"],
        },
      },

      // Analytics Tools
      {
        name: "query_history",
        description: "Query project history for analytics",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "number",
              description: "Number of recent projects to return",
            },
            minSuccessRate: {
              type: "number",
              description: "Filter by minimum success rate",
            },
          },
        },
      },
      {
        name: "get_analytics",
        description: "Get aggregated analytics across all projects",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },

      // Learning Tools
      {
        name: "add_learning",
        description: "Add a learning to the global learnings file",
        inputSchema: {
          type: "object",
          properties: {
            category: {
              type: "string",
              description: "Learning category (e.g., patterns, issues, tools)",
            },
            content: { type: "string", description: "Learning content" },
            projectId: {
              type: "string",
              description: "Related project ID (optional)",
            },
          },
          required: ["category", "content"],
        },
      },
      {
        name: "search_learnings",
        description: "Search global learnings",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search query" },
          },
          required: ["query"],
        },
      },

      // External Integration Tools (Stubs for future implementation)
      {
        name: "sync_jira",
        description: "Sync project with Jira (requires JIRA_API_TOKEN)",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            jiraProjectKey: { type: "string", description: "Jira project key" },
            action: {
              type: "string",
              enum: ["import", "export", "sync"],
              description: "Sync action",
            },
          },
          required: ["projectId", "jiraProjectKey", "action"],
        },
      },
      {
        name: "sync_linear",
        description: "Sync project with Linear (requires LINEAR_API_KEY)",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            linearTeamId: { type: "string", description: "Linear team ID" },
            action: {
              type: "string",
              enum: ["import", "export", "sync"],
              description: "Sync action",
            },
          },
          required: ["projectId", "linearTeamId", "action"],
        },
      },
      {
        name: "export_notion",
        description: "Export project documentation to Notion",
        inputSchema: {
          type: "object",
          properties: {
            projectId: { type: "string", description: "Project ID" },
            notionPageId: { type: "string", description: "Notion page ID" },
            includePhases: {
              type: "boolean",
              description: "Include phase details",
            },
            includeLearnings: {
              type: "boolean",
              description: "Include learnings",
            },
          },
          required: ["projectId", "notionPageId"],
        },
      },
      {
        name: "notify_slack",
        description: "Send notification to Slack",
        inputSchema: {
          type: "object",
          properties: {
            channel: { type: "string", description: "Slack channel" },
            message: { type: "string", description: "Message to send" },
            projectId: {
              type: "string",
              description: "Related project ID (optional)",
            },
          },
          required: ["channel", "message"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  ensureDirectories();

  switch (name) {
    // Project Management
    case "create_project": {
      const projectId = generateProjectId();
      const state: ProjectState = {
        id: projectId,
        name: args?.name as string,
        status: "planning",
        currentPhase: 0,
        totalPhases: (args?.totalPhases as number) || 1,
        startDate: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
        estimatedCost: (args?.estimatedCost as number) || 0,
        actualCost: 0,
      };
      saveProjectState(projectId, state);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ success: true, projectId, state }, null, 2),
          },
        ],
      };
    }

    case "update_project_status": {
      const projectId = args?.projectId as string;
      const state = loadProjectState(projectId);
      if (!state) {
        return {
          content: [
            { type: "text", text: JSON.stringify({ error: "Project not found" }) },
          ],
        };
      }
      state.status = args?.status as ProjectState["status"];
      if (args?.actualCost !== undefined) {
        state.actualCost = args.actualCost as number;
      }
      state.lastUpdated = new Date().toISOString();
      saveProjectState(projectId, state);
      return {
        content: [
          { type: "text", text: JSON.stringify({ success: true, state }, null, 2) },
        ],
      };
    }

    case "list_projects": {
      const projects = listProjects();
      const status = args?.status as string;
      const filtered =
        status && status !== "all"
          ? projects.filter((p) => p.status === status)
          : projects;
      return {
        content: [
          { type: "text", text: JSON.stringify({ projects: filtered }, null, 2) },
        ],
      };
    }

    // Phase Management
    case "create_phase": {
      const projectId = args?.projectId as string;
      const phaseId = args?.phaseId as number;
      const tasks = ((args?.tasks as Array<{ description: string }>) || []).map(
        (t, i) => ({
          id: `task-${phaseId}-${i + 1}`,
          description: t.description,
          status: "pending" as const,
        })
      );
      const phase: PhaseData = {
        id: phaseId,
        name: args?.name as string,
        status: "pending",
        tasks,
      };
      savePhaseData(projectId, phaseId, phase);
      return {
        content: [
          { type: "text", text: JSON.stringify({ success: true, phase }, null, 2) },
        ],
      };
    }

    case "update_phase_status": {
      const projectId = args?.projectId as string;
      const phaseId = args?.phaseId as number;
      const phase = loadPhaseData(projectId, phaseId);
      if (!phase) {
        return {
          content: [
            { type: "text", text: JSON.stringify({ error: "Phase not found" }) },
          ],
        };
      }
      phase.status = args?.status as PhaseData["status"];
      if (args?.status === "in_progress" && !phase.startTime) {
        phase.startTime = new Date().toISOString();
      }
      if (args?.status === "completed") {
        phase.endTime = new Date().toISOString();
      }
      if (args?.tokenUsage !== undefined) {
        phase.tokenUsage = args.tokenUsage as number;
      }
      savePhaseData(projectId, phaseId, phase);

      // Update project current phase
      const state = loadProjectState(projectId);
      if (state && args?.status === "in_progress") {
        state.currentPhase = phaseId;
        state.lastUpdated = new Date().toISOString();
        saveProjectState(projectId, state);
      }

      return {
        content: [
          { type: "text", text: JSON.stringify({ success: true, phase }, null, 2) },
        ],
      };
    }

    case "get_phase": {
      const projectId = args?.projectId as string;
      const phaseId = args?.phaseId as number;
      const phase = loadPhaseData(projectId, phaseId);
      if (!phase) {
        return {
          content: [
            { type: "text", text: JSON.stringify({ error: "Phase not found" }) },
          ],
        };
      }
      return {
        content: [{ type: "text", text: JSON.stringify({ phase }, null, 2) }],
      };
    }

    // Task Management
    case "update_task_status": {
      const projectId = args?.projectId as string;
      const phaseId = args?.phaseId as number;
      const taskId = args?.taskId as string;
      const phase = loadPhaseData(projectId, phaseId);
      if (!phase) {
        return {
          content: [
            { type: "text", text: JSON.stringify({ error: "Phase not found" }) },
          ],
        };
      }
      const task = phase.tasks.find((t) => t.id === taskId);
      if (!task) {
        return {
          content: [
            { type: "text", text: JSON.stringify({ error: "Task not found" }) },
          ],
        };
      }
      task.status = args?.status as TaskData["status"];
      if (args?.assignedAgent) {
        task.assignedAgent = args.assignedAgent as string;
      }
      savePhaseData(projectId, phaseId, phase);
      return {
        content: [
          { type: "text", text: JSON.stringify({ success: true, task }, null, 2) },
        ],
      };
    }

    // Analytics
    case "query_history": {
      const history = loadHistory();
      let filtered = history;
      if (args?.minSuccessRate !== undefined) {
        filtered = filtered.filter(
          (h) => h.successRate >= (args.minSuccessRate as number)
        );
      }
      const limit = (args?.limit as number) || 10;
      filtered = filtered.slice(-limit);
      return {
        content: [
          { type: "text", text: JSON.stringify({ history: filtered }, null, 2) },
        ],
      };
    }

    case "get_analytics": {
      const history = loadHistory();
      const projects = listProjects();

      const analytics = {
        totalProjects: projects.length,
        completedProjects: history.length,
        activeProjects: projects.filter((p) => p.status === "active").length,
        totalCost: history.reduce((sum, h) => sum + h.totalCost, 0),
        averageCost:
          history.length > 0
            ? history.reduce((sum, h) => sum + h.totalCost, 0) / history.length
            : 0,
        averageSuccessRate:
          history.length > 0
            ? history.reduce((sum, h) => sum + h.successRate, 0) / history.length
            : 0,
        totalTokens: history.reduce((sum, h) => sum + h.totalTokens, 0),
      };

      return {
        content: [{ type: "text", text: JSON.stringify({ analytics }, null, 2) }],
      };
    }

    // Learnings
    case "add_learning": {
      const category = args?.category as string;
      const content = args?.content as string;
      const projectId = args?.projectId as string;

      const learning = `### ${category}${projectId ? ` (${projectId})` : ""}\n${content}`;
      appendLearning(learning);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ success: true, message: "Learning added" }),
          },
        ],
      };
    }

    case "search_learnings": {
      const query = (args?.query as string).toLowerCase();
      const learnings = loadLearnings();
      const lines = learnings.split("\n");
      const matches: string[] = [];
      let currentSection = "";

      for (const line of lines) {
        if (line.startsWith("##")) {
          currentSection = line;
        }
        if (line.toLowerCase().includes(query)) {
          matches.push(`${currentSection}\n${line}`);
        }
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ query, matches: matches.slice(0, 10) }, null, 2),
          },
        ],
      };
    }

    // External Integrations (Stubs)
    case "sync_jira":
    case "sync_linear":
    case "export_notion":
    case "notify_slack": {
      // These are stubs - actual implementation would require API keys and SDKs
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Not implemented",
              message: `${name} requires API credentials. Set the appropriate environment variables and implement the integration.`,
              requiredEnvVars:
                name === "sync_jira"
                  ? ["JIRA_API_TOKEN", "JIRA_BASE_URL"]
                  : name === "sync_linear"
                    ? ["LINEAR_API_KEY"]
                    : name === "export_notion"
                      ? ["NOTION_API_KEY"]
                      : ["SLACK_WEBHOOK_URL"],
            }),
          },
        ],
      };
    }

    default:
      return {
        content: [
          { type: "text", text: JSON.stringify({ error: "Unknown tool" }) },
        ],
      };
  }
});

// =============================================================================
// Resources
// =============================================================================

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const projects = listProjects();

  const resources = [
    {
      uri: "autopilot://learnings",
      name: "Global Learnings",
      description: "Cross-project learnings and patterns",
      mimeType: "text/markdown",
    },
    {
      uri: "autopilot://history",
      name: "Project History",
      description: "Historical project data for analytics",
      mimeType: "application/json",
    },
    ...projects.map((p) => ({
      uri: `autopilot://project/${p.id}`,
      name: `Project: ${p.name}`,
      description: `Status: ${p.status}, Phase: ${p.currentPhase}/${p.totalPhases}`,
      mimeType: "application/json",
    })),
  ];

  return { resources };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "autopilot://learnings") {
    return {
      contents: [
        {
          uri,
          mimeType: "text/markdown",
          text: loadLearnings(),
        },
      ],
    };
  }

  if (uri === "autopilot://history") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(loadHistory(), null, 2),
        },
      ],
    };
  }

  if (uri.startsWith("autopilot://project/")) {
    const projectId = uri.replace("autopilot://project/", "");
    const state = loadProjectState(projectId);
    if (state) {
      return {
        contents: [
          {
            uri,
            mimeType: "application/json",
            text: JSON.stringify(state, null, 2),
          },
        ],
      };
    }
  }

  throw new Error(`Resource not found: ${uri}`);
});

// =============================================================================
// Prompts
// =============================================================================

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "planning-template",
        description: "Template for project planning phase",
        arguments: [
          {
            name: "projectName",
            description: "Name of the project",
            required: true,
          },
          {
            name: "description",
            description: "Project description",
            required: true,
          },
        ],
      },
      {
        name: "review-template",
        description: "Template for code review",
        arguments: [
          {
            name: "files",
            description: "Files to review",
            required: true,
          },
          {
            name: "focusAreas",
            description: "Areas to focus on (security, performance, etc.)",
            required: false,
          },
        ],
      },
      {
        name: "standup-template",
        description: "Template for daily standup summary",
        arguments: [
          {
            name: "projectId",
            description: "Project ID",
            required: true,
          },
        ],
      },
      {
        name: "handoff-template",
        description: "Template for developer handoff documentation",
        arguments: [
          {
            name: "projectId",
            description: "Project ID",
            required: true,
          },
          {
            name: "scope",
            description: "Scope of handoff (full, phase, feature)",
            required: false,
          },
        ],
      },
    ],
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "planning-template":
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `# Project Planning: ${args?.projectName}

## Description
${args?.description}

## Planning Checklist
1. Define project scope and boundaries
2. Identify key requirements and constraints
3. Break down into phases (aim for 3-8 phases)
4. Estimate effort and cost per phase
5. Identify risks and mitigation strategies
6. Define success criteria

## Output Format
Please provide:
1. Phase breakdown with clear deliverables
2. Task list per phase
3. Resource requirements
4. Timeline estimate
5. Risk assessment
6. Quality gates`,
            },
          },
        ],
      };

    case "review-template":
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `# Code Review Request

## Files to Review
${args?.files}

## Focus Areas
${args?.focusAreas || "General code quality, security, performance"}

## Review Checklist
- [ ] Code correctness and logic
- [ ] Error handling
- [ ] Security vulnerabilities
- [ ] Performance considerations
- [ ] Code style and readability
- [ ] Test coverage
- [ ] Documentation

## Output Format
For each issue found:
- **Severity:** Critical/High/Medium/Low
- **Location:** file:line
- **Issue:** Description
- **Suggestion:** Recommended fix`,
            },
          },
        ],
      };

    case "standup-template": {
      const projectId = args?.projectId as string;
      const state = loadProjectState(projectId);
      const phase = state ? loadPhaseData(projectId, state.currentPhase) : null;

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `# Daily Standup Summary

## Project: ${state?.name || "Unknown"}
## Current Phase: ${phase?.name || "None"} (${state?.currentPhase}/${state?.totalPhases})

Generate a standup summary including:

### Yesterday
- Completed tasks
- Progress made

### Today
- Planned tasks
- Focus areas

### Blockers
- Any impediments
- Risks identified

### Metrics
- Phase progress: ${phase?.tasks.filter((t) => t.status === "completed").length}/${phase?.tasks.length || 0} tasks
- Budget status: $${state?.actualCost || 0} / $${state?.estimatedCost || 0}`,
            },
          },
        ],
      };
    }

    case "handoff-template": {
      const projectId = args?.projectId as string;
      const state = loadProjectState(projectId);
      const scope = args?.scope || "full";

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `# Developer Handoff Document

## Project: ${state?.name || "Unknown"}
## Scope: ${scope}

Generate a comprehensive handoff document including:

### 1. Project Overview
- Purpose and goals
- Current status: ${state?.status}
- Phase: ${state?.currentPhase}/${state?.totalPhases}

### 2. Architecture
- System design
- Key components
- Data flow

### 3. Environment Setup
- Prerequisites
- Configuration
- Build/run instructions

### 4. Current State
- What's completed
- What's in progress
- Known issues

### 5. Next Steps
- Remaining work
- Priority items
- Recommendations

### 6. Key Decisions
- Technical choices made
- Rationale
- Alternatives considered

### 7. Learnings
- Patterns discovered
- Gotchas/pitfalls
- Tips for continuation`,
            },
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
});

// =============================================================================
// Server Start
// =============================================================================

async function main() {
  ensureDirectories();

  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error("Autopilot MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
