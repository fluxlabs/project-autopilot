"""
Checkpoint manager for Autopilot API Orchestrator
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Handles state persistence and recovery.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from context import ContextManager, TokenUsage


class CheckpointManager:
    """Manages checkpointing and state recovery."""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.checkpoint_dir = self.project_dir / ".autopilot"
        self.checkpoint_dir.mkdir(exist_ok=True)

    @property
    def checkpoint_file(self) -> Path:
        return self.checkpoint_dir / "checkpoint.json"

    @property
    def history_file(self) -> Path:
        return self.checkpoint_dir / "history.jsonl"

    @property
    def learnings_file(self) -> Path:
        return self.checkpoint_dir / "learnings.json"

    def save(
        self,
        context: ContextManager,
        token_usage: TokenUsage,
        total_cost: float,
        task_description: str,
        current_phase: str = None,
        completed_tasks: list[str] = None,
        extra_state: dict = None,
    ) -> None:
        """Save checkpoint to disk."""
        checkpoint = {
            "version": 1,
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "current_phase": current_phase,
            "completed_tasks": completed_tasks or [],
            "token_usage": token_usage.to_dict(),
            "total_cost": total_cost,
            "context": context.to_dict(),
            "extra_state": extra_state or {},
        }

        # Atomic write
        temp_file = self.checkpoint_file.with_suffix(".tmp")
        temp_file.write_text(json.dumps(checkpoint, indent=2))
        temp_file.rename(self.checkpoint_file)

        # Append to history
        history_entry = {
            "timestamp": checkpoint["timestamp"],
            "action": "checkpoint",
            "phase": current_phase,
            "tasks_completed": len(completed_tasks or []),
            "cost": total_cost,
            "tokens": token_usage.total,
        }
        with open(self.history_file, "a") as f:
            f.write(json.dumps(history_entry) + "\n")

    def load(self) -> dict | None:
        """Load checkpoint from disk."""
        if not self.checkpoint_file.exists():
            return None

        try:
            data = json.loads(self.checkpoint_file.read_text())
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load checkpoint: {e}")
            return None

    def restore_context(self, max_context_tokens: int = 150000) -> tuple[ContextManager, TokenUsage, float, dict] | None:
        """
        Restore full state from checkpoint.

        Returns: (context, token_usage, total_cost, checkpoint_data) or None
        """
        checkpoint = self.load()
        if not checkpoint:
            return None

        # Restore context
        context = ContextManager.from_dict(
            checkpoint.get("context", {}),
            max_context_tokens=max_context_tokens
        )

        # Restore token usage
        usage_data = checkpoint.get("token_usage", {})
        token_usage = TokenUsage(
            input_tokens=usage_data.get("input_tokens", 0),
            output_tokens=usage_data.get("output_tokens", 0),
            cache_read_tokens=usage_data.get("cache_read_tokens", 0),
            cache_creation_tokens=usage_data.get("cache_creation_tokens", 0),
        )

        total_cost = checkpoint.get("total_cost", 0.0)

        return context, token_usage, total_cost, checkpoint

    def clear(self) -> None:
        """Clear checkpoint (project complete)."""
        if self.checkpoint_file.exists():
            # Move to completed
            completed_file = self.checkpoint_dir / f"completed-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
            self.checkpoint_file.rename(completed_file)

    def save_learnings(self, learnings: dict) -> None:
        """Save project learnings for future reference."""
        existing = {}
        if self.learnings_file.exists():
            try:
                existing = json.loads(self.learnings_file.read_text())
            except Exception:
                pass

        # Merge learnings
        existing.update(learnings)
        existing["last_updated"] = datetime.now().isoformat()

        self.learnings_file.write_text(json.dumps(existing, indent=2))

    def load_learnings(self) -> dict:
        """Load project learnings."""
        if not self.learnings_file.exists():
            return {}

        try:
            return json.loads(self.learnings_file.read_text())
        except Exception:
            return {}

    def get_history(self, limit: int = 50) -> list[dict]:
        """Get recent history entries."""
        if not self.history_file.exists():
            return []

        entries = []
        try:
            with open(self.history_file) as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
        except Exception:
            pass

        return entries[-limit:]
