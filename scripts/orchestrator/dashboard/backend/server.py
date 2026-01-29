"""
FastAPI server for Autopilot Dashboard
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Provides REST API and WebSocket endpoints for the orchestrator.
"""

import asyncio
import json
import os
import sys
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directory to path for orchestrator imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import (
    CreateProjectRequest,
    CostSummary,
    GlobalStatsResponse,
    ProjectDetail,
    ProjectHistoryResponse,
    ProjectListResponse,
    ProjectStatus,
    ProjectSummary,
    ResumeProjectRequest,
    StopProjectRequest,
    ThresholdLevel,
    UpdateConfigRequest,
    WSMessage,
    WSMessageType,
)

# Orchestrator imports
from orchestrator import Orchestrator, OrchestratorConfig
from checkpoint import CheckpointManager
from costs import CostTracker, CostConfig


# In-memory project store (in production, use a database)
projects: dict[str, dict] = {}
active_orchestrators: dict[str, Orchestrator] = {}
active_tasks: dict[str, asyncio.Task] = {}
websocket_connections: dict[str, list[WebSocket]] = {}


def load_config() -> dict:
    """Load default configuration."""
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {
        "model": "sonnet",
        "max_tokens": 8192,
        "max_context_tokens": 150000,
        "costs": {"warn": 10.0, "alert": 25.0, "max": 50.0},
    }


DEFAULT_CONFIG = load_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("Autopilot Dashboard starting...")
    yield
    # Shutdown
    print("Shutting down...")
    # Cancel all running tasks
    for task in active_tasks.values():
        task.cancel()


app = FastAPI(
    title="Autopilot Dashboard API",
    description="API for managing autonomous coding projects",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper functions

async def broadcast_to_project(project_id: str, message: dict):
    """Send message to all WebSocket connections for a project."""
    if project_id in websocket_connections:
        dead_connections = []
        for ws in websocket_connections[project_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead_connections.append(ws)
        # Clean up dead connections
        for ws in dead_connections:
            websocket_connections[project_id].remove(ws)


def get_project_or_404(project_id: str) -> dict:
    """Get project or raise 404."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


def project_to_summary(project: dict) -> ProjectSummary:
    """Convert internal project dict to summary model."""
    cost = None
    if "cost_tracker" in project:
        ct = project["cost_tracker"]
        cost = CostSummary(
            total_cost=ct.get("total_cost", 0),
            input_tokens=ct.get("input_tokens", 0),
            output_tokens=ct.get("output_tokens", 0),
            total_tokens=ct.get("input_tokens", 0) + ct.get("output_tokens", 0),
            api_calls=ct.get("api_calls", 0),
            threshold_level=ThresholdLevel(ct.get("threshold_level", "ok")),
            remaining_budget=ct.get("remaining_budget", 50.0),
            cost_by_model=ct.get("cost_by_model", {}),
        )

    return ProjectSummary(
        id=project["id"],
        name=project["name"],
        path=project["path"],
        task=project["task"],
        status=ProjectStatus(project["status"]),
        created_at=project["created_at"],
        updated_at=project["updated_at"],
        completed_tasks=len(project.get("completed_tasks", [])),
        cost=cost,
    )


# REST Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/projects", response_model=ProjectListResponse)
async def list_projects():
    """List all projects."""
    summaries = [project_to_summary(p) for p in projects.values()]
    return ProjectListResponse(projects=summaries, total=len(summaries))


@app.post("/api/projects", response_model=ProjectSummary)
async def create_project(request: CreateProjectRequest):
    """Create a new project."""
    # Validate path
    project_path = Path(request.path)
    if not project_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Directory not found: {request.path}")

    project_id = str(uuid.uuid4())[:8]

    project = {
        "id": project_id,
        "name": request.name,
        "path": request.path,
        "task": request.task,
        "status": "idle",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "completed_tasks": [],
        "max_cost": request.max_cost,
        "model": request.model,
        "cost_tracker": {
            "total_cost": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "api_calls": 0,
            "threshold_level": "ok",
            "remaining_budget": request.max_cost,
            "cost_by_model": {},
        },
    }

    projects[project_id] = project
    return project_to_summary(project)


@app.get("/api/projects/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: str):
    """Get project details."""
    project = get_project_or_404(project_id)

    # Check for checkpoint
    checkpoint_mgr = CheckpointManager(project["path"])
    checkpoint = checkpoint_mgr.load()

    cost = None
    if "cost_tracker" in project:
        ct = project["cost_tracker"]
        cost = CostSummary(
            total_cost=ct.get("total_cost", 0),
            input_tokens=ct.get("input_tokens", 0),
            output_tokens=ct.get("output_tokens", 0),
            total_tokens=ct.get("input_tokens", 0) + ct.get("output_tokens", 0),
            api_calls=ct.get("api_calls", 0),
            threshold_level=ThresholdLevel(ct.get("threshold_level", "ok")),
            remaining_budget=ct.get("remaining_budget", 50.0),
            cost_by_model=ct.get("cost_by_model", {}),
        )

    return ProjectDetail(
        id=project["id"],
        name=project["name"],
        path=project["path"],
        task=project["task"],
        status=ProjectStatus(project["status"]),
        created_at=project["created_at"],
        updated_at=project["updated_at"],
        completed_tasks=len(project.get("completed_tasks", [])),
        completed_task_list=project.get("completed_tasks", []),
        current_phase=checkpoint.get("current_phase") if checkpoint else None,
        checkpoint_available=checkpoint is not None,
        last_checkpoint=datetime.fromisoformat(checkpoint["timestamp"]) if checkpoint else None,
        cost=cost,
    )


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project."""
    project = get_project_or_404(project_id)

    # Stop if running
    if project_id in active_tasks:
        active_tasks[project_id].cancel()
        del active_tasks[project_id]

    if project_id in active_orchestrators:
        del active_orchestrators[project_id]

    del projects[project_id]
    return {"status": "deleted"}


@app.post("/api/projects/{project_id}/start")
async def start_project(project_id: str):
    """Start or resume a project."""
    project = get_project_or_404(project_id)

    if project["status"] == "running":
        raise HTTPException(status_code=400, detail="Project already running")

    # Create orchestrator config
    config_dict = DEFAULT_CONFIG.copy()
    config_dict["model"] = project.get("model", config_dict["model"])
    config_dict["costs"] = {"max": project.get("max_cost", 50.0), "warn": 10.0, "alert": 25.0}
    config = OrchestratorConfig(config_dict)

    # Create callbacks that broadcast to WebSocket
    async def on_output(text: str):
        await broadcast_to_project(project_id, {
            "type": "output",
            "text": text,
            "timestamp": datetime.now().isoformat(),
        })

    async def on_tool_start(tool_name: str, tool_input: dict):
        await broadcast_to_project(project_id, {
            "type": "tool_start",
            "tool_name": tool_name,
            "tool_input": tool_input,
            "timestamp": datetime.now().isoformat(),
        })

    async def on_tool_end(tool_name: str, result: str, is_error: bool):
        await broadcast_to_project(project_id, {
            "type": "tool_end",
            "tool_name": tool_name,
            "result": result[:500],
            "is_error": is_error,
            "timestamp": datetime.now().isoformat(),
        })

    async def on_checkpoint():
        project["updated_at"] = datetime.now()
        await broadcast_to_project(project_id, {
            "type": "checkpoint",
            "timestamp": datetime.now().isoformat(),
        })

    async def on_cost_warning(cost: float):
        await broadcast_to_project(project_id, {
            "type": "cost_update",
            "level": "warning",
            "cost": cost,
            "timestamp": datetime.now().isoformat(),
        })

    async def on_cost_alert(cost: float):
        await broadcast_to_project(project_id, {
            "type": "cost_update",
            "level": "alert",
            "cost": cost,
            "timestamp": datetime.now().isoformat(),
        })

    # Create orchestrator with sync wrappers for async callbacks
    def sync_output(text):
        asyncio.create_task(on_output(text))

    def sync_tool_start(name, inp):
        asyncio.create_task(on_tool_start(name, inp))

    def sync_tool_end(name, result, err):
        asyncio.create_task(on_tool_end(name, result, err))

    def sync_checkpoint():
        asyncio.create_task(on_checkpoint())

    def sync_cost_warning(cost):
        asyncio.create_task(on_cost_warning(cost))

    def sync_cost_alert(cost):
        asyncio.create_task(on_cost_alert(cost))

    orchestrator = Orchestrator(
        project_dir=project["path"],
        config=config,
        on_output=sync_output,
        on_tool_start=sync_tool_start,
        on_tool_end=sync_tool_end,
        on_checkpoint=sync_checkpoint,
        on_cost_warning=sync_cost_warning,
        on_cost_alert=sync_cost_alert,
    )

    # Try to resume, otherwise initialize
    checkpoint_mgr = CheckpointManager(project["path"])
    if checkpoint_mgr.load():
        orchestrator.resume()
    else:
        orchestrator.initialize(project["task"])

    active_orchestrators[project_id] = orchestrator

    # Run in background task
    async def run_orchestrator():
        try:
            project["status"] = "running"
            await broadcast_to_project(project_id, {
                "type": "status",
                "status": "running",
                "timestamp": datetime.now().isoformat(),
            })

            # Run synchronously in thread pool
            loop = asyncio.get_event_loop()
            completed = await loop.run_in_executor(None, orchestrator.run)

            if completed:
                project["status"] = "completed"
                await broadcast_to_project(project_id, {
                    "type": "complete",
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                project["status"] = "paused"

        except asyncio.CancelledError:
            project["status"] = "paused"
            orchestrator.save_checkpoint("cancelled")
        except Exception as e:
            project["status"] = "error"
            await broadcast_to_project(project_id, {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            })
        finally:
            # Update cost tracker
            if orchestrator.cost_tracker:
                project["cost_tracker"] = orchestrator.cost_tracker.get_summary()
            project["completed_tasks"] = orchestrator.completed_tasks
            project["updated_at"] = datetime.now()

            if project_id in active_tasks:
                del active_tasks[project_id]
            if project_id in active_orchestrators:
                del active_orchestrators[project_id]

    task = asyncio.create_task(run_orchestrator())
    active_tasks[project_id] = task

    return {"status": "started", "project_id": project_id}


@app.post("/api/projects/{project_id}/stop")
async def stop_project(project_id: str, request: StopProjectRequest = None):
    """Stop a running project."""
    project = get_project_or_404(project_id)

    if project_id not in active_tasks:
        raise HTTPException(status_code=400, detail="Project not running")

    # Cancel the task
    active_tasks[project_id].cancel()

    project["status"] = "paused"
    project["updated_at"] = datetime.now()

    return {"status": "stopped"}


@app.get("/api/projects/{project_id}/history", response_model=ProjectHistoryResponse)
async def get_project_history(project_id: str):
    """Get project execution history."""
    project = get_project_or_404(project_id)

    checkpoint_mgr = CheckpointManager(project["path"])
    history = checkpoint_mgr.get_history()

    entries = []
    for entry in history:
        entries.append({
            "timestamp": datetime.fromisoformat(entry["timestamp"]),
            "action": entry.get("action", "unknown"),
            "phase": entry.get("phase"),
            "tasks_completed": entry.get("tasks_completed", 0),
            "cost": entry.get("cost", 0),
            "tokens": entry.get("tokens", 0),
        })

    return ProjectHistoryResponse(project_id=project_id, entries=entries)


@app.get("/api/stats", response_model=GlobalStatsResponse)
async def get_global_stats():
    """Get global statistics."""
    total = len(projects)
    active = sum(1 for p in projects.values() if p["status"] == "running")
    completed = sum(1 for p in projects.values() if p["status"] == "completed")

    total_cost = sum(
        p.get("cost_tracker", {}).get("total_cost", 0)
        for p in projects.values()
    )
    total_tokens = sum(
        p.get("cost_tracker", {}).get("input_tokens", 0) +
        p.get("cost_tracker", {}).get("output_tokens", 0)
        for p in projects.values()
    )

    return GlobalStatsResponse(
        total_projects=total,
        active_projects=active,
        completed_projects=completed,
        total_cost=total_cost,
        total_tokens=total_tokens,
        avg_cost_per_project=total_cost / total if total > 0 else 0,
    )


@app.get("/api/config")
async def get_config():
    """Get current configuration."""
    return DEFAULT_CONFIG


@app.put("/api/config")
async def update_config(request: UpdateConfigRequest):
    """Update configuration."""
    if request.max_cost is not None:
        DEFAULT_CONFIG["costs"]["max"] = request.max_cost
    if request.warn_cost is not None:
        DEFAULT_CONFIG["costs"]["warn"] = request.warn_cost
    if request.alert_cost is not None:
        DEFAULT_CONFIG["costs"]["alert"] = request.alert_cost
    if request.model is not None:
        DEFAULT_CONFIG["model"] = request.model

    return DEFAULT_CONFIG


# WebSocket endpoint

@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()

    # Register connection
    if project_id not in websocket_connections:
        websocket_connections[project_id] = []
    websocket_connections[project_id].append(websocket)

    try:
        # Send initial status
        if project_id in projects:
            project = projects[project_id]
            await websocket.send_json({
                "type": "status",
                "status": project["status"],
                "completed_tasks": len(project.get("completed_tasks", [])),
                "cost": project.get("cost_tracker", {}),
                "timestamp": datetime.now().isoformat(),
            })

        # Listen for messages
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "start":
                # Start project via WebSocket
                await start_project(project_id)

            elif msg_type == "stop":
                # Stop project via WebSocket
                await stop_project(project_id)

            elif msg_type == "help_response":
                # Handle help response
                if project_id in active_orchestrators:
                    orchestrator = active_orchestrators[project_id]
                    # Would need to implement this in orchestrator
                    pass

    except WebSocketDisconnect:
        pass
    finally:
        # Unregister connection
        if project_id in websocket_connections:
            websocket_connections[project_id].remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
