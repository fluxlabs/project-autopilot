"""
Pydantic models for Autopilot Dashboard API
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class ThresholdLevel(str, Enum):
    OK = "ok"
    WARNING = "warning"
    ALERT = "alert"
    STOP = "stop"


# Request Models

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    path: str = Field(..., description="Absolute path to project directory")
    task: str = Field(..., min_length=1, description="Task description")
    max_cost: float = Field(default=50.0, ge=0)
    model: str = Field(default="sonnet")


class ResumeProjectRequest(BaseModel):
    project_id: str


class StopProjectRequest(BaseModel):
    project_id: str
    save_checkpoint: bool = True


class UpdateConfigRequest(BaseModel):
    max_cost: float | None = None
    warn_cost: float | None = None
    alert_cost: float | None = None
    model: str | None = None


# Response Models

class CostSummary(BaseModel):
    total_cost: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    api_calls: int
    threshold_level: ThresholdLevel
    remaining_budget: float
    cost_by_model: dict[str, float] = {}


class ProjectSummary(BaseModel):
    id: str
    name: str
    path: str
    task: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    completed_tasks: int = 0
    cost: CostSummary | None = None


class ProjectDetail(ProjectSummary):
    completed_task_list: list[str] = []
    current_phase: str | None = None
    checkpoint_available: bool = False
    last_checkpoint: datetime | None = None


class ProjectListResponse(BaseModel):
    projects: list[ProjectSummary]
    total: int


class HistoryEntry(BaseModel):
    timestamp: datetime
    action: str
    phase: str | None = None
    tasks_completed: int = 0
    cost: float = 0
    tokens: int = 0


class ProjectHistoryResponse(BaseModel):
    project_id: str
    entries: list[HistoryEntry]


class GlobalStatsResponse(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_cost: float
    total_tokens: int
    avg_cost_per_project: float


# WebSocket Message Models

class WSMessageType(str, Enum):
    # Server -> Client
    OUTPUT = "output"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    STATUS = "status"
    COST_UPDATE = "cost_update"
    CHECKPOINT = "checkpoint"
    ERROR = "error"
    COMPLETE = "complete"
    HELP_REQUESTED = "help_requested"

    # Client -> Server
    START = "start"
    STOP = "stop"
    RESUME = "resume"
    HELP_RESPONSE = "help_response"


class WSMessage(BaseModel):
    type: WSMessageType
    data: dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)


class WSOutputMessage(BaseModel):
    type: WSMessageType = WSMessageType.OUTPUT
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)


class WSToolMessage(BaseModel):
    type: WSMessageType
    tool_name: str
    tool_input: dict[str, Any] | None = None
    result: str | None = None
    is_error: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)


class WSStatusMessage(BaseModel):
    type: WSMessageType = WSMessageType.STATUS
    status: ProjectStatus
    completed_tasks: int
    context_usage: float
    cost: CostSummary
    timestamp: datetime = Field(default_factory=datetime.now)
