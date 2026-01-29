"""
Core orchestrator for Autopilot API Orchestrator
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Main orchestration loop that coordinates context, tools, checkpointing, and API calls.
"""

import time
from typing import Any, Callable

import anthropic

from context import ContextManager, TokenUsage
from tools import Tools
from checkpoint import CheckpointManager
from costs import (
    CostTracker,
    CostConfig,
    ThresholdLevel,
    load_pricing_from_config,
    resolve_model_name,
    DEFAULT_MODEL,
)


class OrchestratorConfig:
    """Orchestrator configuration."""

    def __init__(self, config_dict: dict):
        # Model: accept short name, resolve to full API model ID
        model_input = config_dict.get("model", DEFAULT_MODEL)
        self.model = resolve_model_name(model_input)
        self.max_tokens = config_dict.get("max_tokens", 8192)
        self.max_context_tokens = config_dict.get("max_context_tokens", 150000)
        self.checkpoint_threshold = config_dict.get("checkpoint_threshold", 0.6)
        self.summary_threshold = config_dict.get("summary_threshold", 0.8)

        # Cost configuration
        costs = config_dict.get("costs", {})
        self.cost_config = CostConfig(
            warn=costs.get("warn", 10.0),
            alert=costs.get("alert", 25.0),
            max=costs.get("max", 50.0),
        )

        # Pricing configuration (loaded from config or defaults)
        self.pricing = load_pricing_from_config(config_dict.get("pricing", {}))

        # Execution settings
        execution = config_dict.get("execution", {})
        self.max_iterations = execution.get("max_iterations", 500)
        self.max_tool_calls_per_turn = execution.get("max_tool_calls_per_turn", 20)
        self.cooldown_on_error = execution.get("cooldown_on_error", 5)

        # Git configuration
        git = config_dict.get("git", {})
        self.git_auto_commit = git.get("auto_commit_on_phase", True)
        self.git_commit_prefix = git.get("commit_prefix", "feat")
        self.git_require_verification = git.get("require_verification", True)

        # Tools configuration (passed to Tools class)
        self.tools_config = config_dict.get("tools", {})


class Orchestrator:
    """
    Main orchestration loop.

    Handles:
    - API communication
    - Tool execution
    - Context management
    - Checkpointing
    - Cost tracking
    """

    def __init__(
        self,
        project_dir: str,
        config: OrchestratorConfig,
        on_output: Callable[[str], None] = None,
        on_tool_start: Callable[[str, dict], None] = None,
        on_tool_end: Callable[[str, str, bool], None] = None,
        on_checkpoint: Callable[[], None] = None,
        on_cost_warning: Callable[[float], None] = None,
        on_cost_alert: Callable[[float], None] = None,
        on_help_requested: Callable[[str], str] = None,
        on_confirm_request: Callable[[str], bool] = None,
    ):
        self.project_dir = project_dir
        self.config = config

        # Callbacks
        self.on_output = on_output or print
        self.on_tool_start = on_tool_start
        self.on_tool_end = on_tool_end
        self.on_checkpoint = on_checkpoint
        self.on_help_requested = on_help_requested

        # Initialize components
        self.client = anthropic.Anthropic()
        self.tools = Tools(project_dir, config.tools_config, config)
        self.tools.on_confirm_request = on_confirm_request
        self.checkpoint_mgr = CheckpointManager(project_dir)
        self.cost_tracker = CostTracker(
            config=config.cost_config,
            pricing=config.pricing,
            on_warning=on_cost_warning,
            on_alert=on_cost_alert,
        )

        # State
        self.context: ContextManager = None
        self.token_usage = TokenUsage()
        self.task_description: str = ""
        self.completed_tasks: list[str] = []
        self.is_complete: bool = False
        self.needs_human_input: bool = False
        self.human_input_request: str = ""

    def _build_system_prompt(self) -> str:
        """Build the system prompt."""
        learnings = self.checkpoint_mgr.load_learnings()

        prompt = f"""You are an expert software engineer working on a project.

PROJECT DIRECTORY: {self.project_dir}

TASK: {self.task_description}

INSTRUCTIONS:
1. Break down the task into phases (logical units of work)
2. For each phase:
   a. Implement the changes
   b. Verify it works (run tests, check syntax, manual verification)
   c. Call phase_complete with summary and verification details
   d. This will automatically commit the changes
3. If stuck or need clarification, use request_help tool
4. When ALL phases are done, use task_complete tool

CONSTRAINTS:
- Only modify files within the project directory
- Follow existing code style and patterns
- Write tests for new functionality
- Keep changes minimal and focused

"""
        if learnings:
            prompt += f"""
PROJECT LEARNINGS (from previous sessions):
{learnings}

"""

        if self.completed_tasks:
            prompt += f"""
COMPLETED SO FAR:
{chr(10).join(f'- {t}' for t in self.completed_tasks)}

Continue from where you left off.
"""

        return prompt

    def initialize(self, task_description: str) -> None:
        """Initialize a new session."""
        self.task_description = task_description
        self.context = ContextManager(
            system_prompt=self._build_system_prompt(),
            max_context_tokens=self.config.max_context_tokens,
            checkpoint_threshold=self.config.checkpoint_threshold,
            summary_threshold=self.config.summary_threshold,
        )
        self.completed_tasks = []
        self.is_complete = False

    def resume(self) -> bool:
        """
        Resume from checkpoint.

        Returns True if checkpoint was loaded, False otherwise.
        """
        result = self.checkpoint_mgr.restore_context(self.config.max_context_tokens)

        if not result:
            return False

        context, token_usage, total_cost, checkpoint_data = result

        self.context = context
        self.token_usage = token_usage
        self.cost_tracker.set_initial_cost(total_cost)
        self.task_description = checkpoint_data.get("task_description", "")
        self.completed_tasks = checkpoint_data.get("completed_tasks", [])

        # Rebuild system prompt with current state
        self.context.system_prompt = self._build_system_prompt()

        self.on_output(f"Resumed from checkpoint")
        self.on_output(f"  Task: {self.task_description}")
        self.on_output(f"  Completed: {len(self.completed_tasks)} tasks")
        self.on_output(f"  Cost so far: ${total_cost:.2f}")

        return True

    def save_checkpoint(self, reason: str = "periodic") -> None:
        """Save current state to checkpoint."""
        self.checkpoint_mgr.save(
            context=self.context,
            token_usage=self.token_usage,
            total_cost=self.cost_tracker.total_cost,
            task_description=self.task_description,
            completed_tasks=self.completed_tasks,
        )

        if self.on_checkpoint:
            self.on_checkpoint()

        self.on_output(f"[Checkpoint saved: {reason}]")

    def _call_api(self) -> anthropic.types.Message:
        """Make an API call."""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=self.context.system_prompt,
            messages=self.context.get_messages(),
            tools=self.tools.get_tool_definitions(),
        )

        # Track usage
        usage = response.usage
        self.token_usage.add({
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
        })
        self.cost_tracker.add_usage(
            self.config.model,
            usage.input_tokens,
            usage.output_tokens,
        )

        return response

    def _execute_tools(self, tool_uses: list[dict]) -> list[dict]:
        """Execute tool calls and return results."""
        results = []

        # Enforce max tool calls per turn
        max_tools = self.config.max_tool_calls_per_turn
        if len(tool_uses) > max_tools:
            self.on_output(
                f"⚠️  Limiting tool calls from {len(tool_uses)} to {max_tools} per turn"
            )
            tool_uses = tool_uses[:max_tools]

        for tool_use in tool_uses:
            tool_name = tool_use.name
            tool_input = tool_use.input
            tool_id = tool_use.id

            if self.on_tool_start:
                self.on_tool_start(tool_name, tool_input)

            # Execute
            result, is_error = self.tools.execute(tool_name, tool_input)

            if self.on_tool_end:
                self.on_tool_end(tool_name, result[:200], is_error)

            # Handle special tools
            if tool_name == "task_complete":
                self.is_complete = True
                self.completed_tasks.append(tool_input.get("summary", "Task completed"))

            elif tool_name == "request_help":
                self.needs_human_input = True
                self.human_input_request = result
                if self.on_help_requested:
                    human_response = self.on_help_requested(result)
                    if human_response:
                        result = f"Human response: {human_response}"
                        self.needs_human_input = False

            results.append({
                "tool_use_id": tool_id,
                "content": result,
                "is_error": is_error,
            })

        return results

    def _handle_context_pressure(self) -> None:
        """Handle context window pressure."""
        if self.context.should_checkpoint:
            self.save_checkpoint("context_threshold")

        if self.context.should_summarize:
            self.on_output("[Context pressure - requesting summary]")
            # Ask Claude to summarize older context
            self.context.add_user_message(
                "Please provide a brief summary of what has been accomplished so far, "
                "including key decisions and current state. This will be used to compress context."
            )

            response = self._call_api()

            # Extract summary from response
            summary = ""
            for block in response.content:
                if block.type == "text":
                    summary = block.text
                    break

            if summary:
                self.context.summarize_old_context(summary, keep_recent=6)
                self.on_output("[Context summarized]")

    def run(self) -> bool:
        """
        Run the orchestration loop.

        Returns True if task completed, False if stopped early.
        """
        if not self.context:
            raise RuntimeError("Call initialize() or resume() first")

        iterations = 0

        # Initial prompt to start work
        self.context.add_user_message(
            "Please begin working on the task. Start by exploring the project structure "
            "and understanding what needs to be done, then proceed with implementation."
        )

        while iterations < self.config.max_iterations:
            iterations += 1

            # Check cost threshold
            if self.cost_tracker.should_stop:
                self.on_output(f"\n🛑 Cost limit reached: ${self.cost_tracker.total_cost:.2f}")
                self.save_checkpoint("cost_limit")
                return False

            # Check context pressure
            self._handle_context_pressure()

            # Make API call
            try:
                response = self._call_api()
            except anthropic.APIError as e:
                self.on_output(f"\n⚠️ API error: {e}")
                time.sleep(self.config.cooldown_on_error)
                continue

            # Process response
            assistant_content = response.content
            self.context.add_assistant_message(assistant_content)

            # Extract text and tool uses
            text_blocks = []
            tool_uses = []

            for block in assistant_content:
                if block.type == "text":
                    text_blocks.append(block.text)
                elif block.type == "tool_use":
                    tool_uses.append(block)

            # Output text
            for text in text_blocks:
                self.on_output(text)

            # Check stop reason
            if response.stop_reason == "end_turn" and not tool_uses:
                # Model finished without tools - might be done or stuck
                if self.is_complete:
                    self.on_output("\n✓ Task completed!")
                    self.checkpoint_mgr.clear()
                    return True
                else:
                    # Prompt to continue or confirm completion
                    self.context.add_user_message(
                        "Are you finished with the task? If so, use the task_complete tool. "
                        "If not, continue working."
                    )
                    continue

            # Execute tools
            if tool_uses:
                results = self._execute_tools(tool_uses)
                self.context.add_tool_results(results)

                # Check if task completed
                if self.is_complete:
                    self.on_output("\n✓ Task completed!")
                    self.checkpoint_mgr.clear()
                    return True

                # Check if human input needed
                if self.needs_human_input:
                    self.save_checkpoint("human_input_needed")
                    return False

        # Max iterations reached
        self.on_output(f"\n⚠️ Max iterations ({self.config.max_iterations}) reached")
        self.save_checkpoint("max_iterations")
        return False

    def get_status(self) -> dict:
        """Get current orchestrator status."""
        return {
            "task": self.task_description,
            "completed_tasks": len(self.completed_tasks),
            "is_complete": self.is_complete,
            "cost": self.cost_tracker.get_summary(),
            "context_usage": self.context.context_usage if self.context else 0,
        }
