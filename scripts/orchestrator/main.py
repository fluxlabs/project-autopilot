#!/usr/bin/env python3
"""
Autopilot API Orchestrator - Main Entry Point
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Direct API-based orchestrator for continuous autonomous coding.

Usage:
    python main.py --project /path/to/project --task "Build a REST API"
    python main.py --project /path/to/project --resume
    python main.py --project /path/to/project --status
"""

import argparse
import os
import sys
from pathlib import Path

import yaml

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from orchestrator import Orchestrator, OrchestratorConfig
from checkpoint import CheckpointManager
from costs import ThresholdLevel


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file."""
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


def create_callbacks(console):
    """Create callback functions for orchestrator events."""

    def on_output(text: str):
        console.print(text)

    def on_tool_start(tool_name: str, tool_input: dict):
        # Truncate input for display
        input_str = str(tool_input)
        if len(input_str) > 100:
            input_str = input_str[:100] + "..."
        console.print(f"  [dim]→ {tool_name}[/dim]", highlight=False)

    def on_tool_end(tool_name: str, result: str, is_error: bool):
        if is_error:
            console.print(f"  [red]✗ {tool_name} failed[/red]")
        else:
            console.print(f"  [green]✓ {tool_name}[/green]")

    def on_checkpoint():
        console.print("[yellow]📌 Checkpoint saved[/yellow]")

    def on_cost_warning(cost: float):
        console.print(f"[yellow]⚠️  Cost warning: ${cost:.2f}[/yellow]")

    def on_cost_alert(cost: float):
        console.print(f"[bold yellow]🟠 Cost alert: ${cost:.2f}[/bold yellow]")
        if RICH_AVAILABLE:
            if not Confirm.ask("Continue execution?"):
                raise KeyboardInterrupt("User stopped at cost alert")

    def on_help_requested(request: str) -> str:
        console.print(Panel(request, title="Help Requested", border_style="yellow"))
        if RICH_AVAILABLE:
            return Prompt.ask("Your response")
        else:
            return input("Your response: ")

    def on_confirm_request(message: str) -> bool:
        console.print(Panel(message, title="⚠️  Confirmation Required", border_style="yellow"))
        if RICH_AVAILABLE:
            return Confirm.ask("Allow this command?")
        else:
            response = input("Allow this command? [y/N]: ")
            return response.lower() in ("y", "yes")

    return {
        "on_output": on_output,
        "on_tool_start": on_tool_start,
        "on_tool_end": on_tool_end,
        "on_checkpoint": on_checkpoint,
        "on_cost_warning": on_cost_warning,
        "on_cost_alert": on_cost_alert,
        "on_help_requested": on_help_requested,
        "on_confirm_request": on_confirm_request,
    }


def show_status(project_dir: str, console):
    """Show current project status."""
    checkpoint_mgr = CheckpointManager(project_dir)
    checkpoint = checkpoint_mgr.load()

    if not checkpoint:
        console.print("[yellow]No checkpoint found[/yellow]")
        return

    console.print(Panel.fit(
        f"""[bold]Task:[/bold] {checkpoint.get('task_description', 'Unknown')}

[bold]Progress:[/bold]
  Completed tasks: {len(checkpoint.get('completed_tasks', []))}
  Current phase: {checkpoint.get('current_phase', 'Unknown')}

[bold]Cost:[/bold]
  Total: ${checkpoint.get('total_cost', 0):.2f}
  Tokens: {checkpoint.get('token_usage', {}).get('total', 0):,}

[bold]Last checkpoint:[/bold] {checkpoint.get('timestamp', 'Unknown')}
""",
        title="Autopilot Status",
    ))

    # Show completed tasks
    completed = checkpoint.get("completed_tasks", [])
    if completed:
        console.print("\n[bold]Completed tasks:[/bold]")
        for task in completed[-10:]:
            console.print(f"  ✓ {task}")
        if len(completed) > 10:
            console.print(f"  ... and {len(completed) - 10} more")


def run_loop(orchestrator: Orchestrator, console):
    """
    Run the orchestrator in a loop, handling context resets.

    This is the "continuous" mode that restarts when context fills.
    """
    iteration = 0
    max_restarts = 100

    while iteration < max_restarts:
        iteration += 1
        console.print(f"\n[bold blue]━━━ Session {iteration} ━━━[/bold blue]")

        try:
            completed = orchestrator.run()

            if completed:
                console.print("\n[bold green]✓ Project completed![/bold green]")
                console.print(orchestrator.cost_tracker.format_status())
                return True

            # Check why we stopped
            status = orchestrator.get_status()

            if orchestrator.needs_human_input:
                console.print("\n[yellow]Paused for human input[/yellow]")
                return False

            if orchestrator.cost_tracker.should_stop:
                console.print("\n[red]Cost limit reached[/red]")
                return False

            # Context filled - restart
            console.print("\n[blue]Context limit reached - restarting session[/blue]")

            # Resume from checkpoint
            if not orchestrator.resume():
                console.print("[red]Failed to resume from checkpoint[/red]")
                return False

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            orchestrator.save_checkpoint("user_interrupt")
            return False

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            orchestrator.save_checkpoint("error")
            raise

    console.print(f"\n[yellow]Max restarts ({max_restarts}) reached[/yellow]")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Autopilot API Orchestrator - Continuous autonomous coding"
    )
    parser.add_argument(
        "--project", "-p",
        required=True,
        help="Project directory"
    )
    parser.add_argument(
        "--task", "-t",
        help="Task description (for new projects)"
    )
    parser.add_argument(
        "--resume", "-r",
        action="store_true",
        help="Resume from checkpoint"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show project status"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to config file (default: config.yaml in orchestrator dir)"
    )
    parser.add_argument(
        "--max-cost",
        type=float,
        help="Maximum cost limit (overrides config)"
    )
    parser.add_argument(
        "--model",
        help="Model to use (overrides config)"
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run in continuous mode (auto-restart on context fill)"
    )

    args = parser.parse_args()

    # Validate project directory
    project_dir = Path(args.project).resolve()
    if not project_dir.is_dir():
        print(f"Error: Project directory not found: {project_dir}")
        sys.exit(1)

    # Load config
    if args.config:
        config_path = Path(args.config)
    else:
        config_path = Path(__file__).parent / "config.yaml"

    config_dict = load_config(config_path)

    # Apply CLI overrides
    if args.max_cost:
        config_dict.setdefault("costs", {})["max"] = args.max_cost
    if args.model:
        config_dict["model"] = args.model

    config = OrchestratorConfig(config_dict)

    # Setup console
    if RICH_AVAILABLE:
        console = Console()
    else:
        class SimpleConsole:
            def print(self, *args, **kwargs):
                # Strip rich formatting
                text = str(args[0]) if args else ""
                import re
                text = re.sub(r'\[/?[^\]]+\]', '', text)
                print(text)
        console = SimpleConsole()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY environment variable not set[/red]")
        sys.exit(1)

    # Status mode
    if args.status:
        show_status(str(project_dir), console)
        return

    # Create orchestrator
    callbacks = create_callbacks(console) if RICH_AVAILABLE else {}
    orchestrator = Orchestrator(
        project_dir=str(project_dir),
        config=config,
        **callbacks
    )

    # Resume or new task
    if args.resume:
        if not orchestrator.resume():
            console.print("[yellow]No checkpoint found. Use --task to start a new project.[/yellow]")
            sys.exit(1)
    elif args.task:
        orchestrator.initialize(args.task)
        console.print(Panel.fit(
            f"[bold]Task:[/bold] {args.task}\n"
            f"[bold]Project:[/bold] {project_dir}\n"
            f"[bold]Model:[/bold] {config.model}\n"
            f"[bold]Budget:[/bold] ${config.cost_config.max:.2f}",
            title="Starting Autopilot",
        ))
    else:
        console.print("[red]Error: Provide --task or --resume[/red]")
        sys.exit(1)

    # Run
    if args.continuous:
        success = run_loop(orchestrator, console)
    else:
        try:
            success = orchestrator.run()
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted - saving checkpoint[/yellow]")
            orchestrator.save_checkpoint("user_interrupt")
            success = False

    # Final status
    console.print("\n" + orchestrator.cost_tracker.format_status())

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
