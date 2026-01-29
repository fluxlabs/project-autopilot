"""
Cost tracking for Autopilot API Orchestrator
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Tracks token usage and costs with threshold alerts.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class ThresholdLevel(Enum):
    OK = "ok"
    WARNING = "warning"
    ALERT = "alert"
    STOP = "stop"


@dataclass
class CostConfig:
    """Cost threshold configuration."""
    warn: float = 10.0
    alert: float = 25.0
    max: float = 50.0


@dataclass
class Pricing:
    """Per-million token pricing."""
    input: float
    output: float


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODEL CONFIGURATION - Single source of truth
# Update these when new model versions are released
# Reference: https://docs.anthropic.com/en/docs/about-claude/models/overview
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Map short names to actual API model IDs (Claude 4.5 generation)
# Using aliases for automatic updates to latest snapshots
MODEL_MAP = {
    "haiku": "claude-haiku-4-5-20251001",    # Fastest, near-frontier intelligence
    "sonnet": "claude-sonnet-4-5-20250929",  # Best balance of speed/intelligence
    "opus": "claude-opus-4-5-20251101",      # Maximum intelligence
}

# Aliases (auto-update to latest snapshots - use for experimentation)
MODEL_ALIASES = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-4-5",
    "opus": "claude-opus-4-5",
}

# Default model (short name)
DEFAULT_MODEL = "sonnet"

# Pricing per million tokens (Claude 4.5 generation)
# Reference: https://docs.anthropic.com/en/docs/about-claude/pricing
DEFAULT_PRICING = {
    "haiku": Pricing(input=1.0, output=5.0),     # Fast, affordable
    "sonnet": Pricing(input=3.0, output=15.0),   # Balanced
    "opus": Pricing(input=5.0, output=25.0),     # Premium
}


def resolve_model_name(model: str) -> str:
    """
    Resolve a model name to its full API model ID.

    Accepts:
      - Short names: "sonnet", "haiku", "opus"
      - Full names: "claude-sonnet-4-20250514" (passed through)

    Returns the full API model ID.
    """
    # If it's a short name, map it
    if model.lower() in MODEL_MAP:
        return MODEL_MAP[model.lower()]

    # If it already looks like a full model name, pass through
    if model.startswith("claude-"):
        return model

    # Try to extract family from unknown format
    model_lower = model.lower()
    if "haiku" in model_lower:
        return MODEL_MAP["haiku"]
    elif "opus" in model_lower:
        return MODEL_MAP["opus"]
    else:
        # Default to sonnet
        return MODEL_MAP["sonnet"]


def get_model_short_name(model: str) -> str:
    """
    Get the short name for a model.

    "claude-sonnet-4-20250514" -> "sonnet"
    "sonnet" -> "sonnet"
    """
    model_lower = model.lower()

    # Already a short name
    if model_lower in MODEL_MAP:
        return model_lower

    # Extract from full name
    if "haiku" in model_lower:
        return "haiku"
    elif "opus" in model_lower:
        return "opus"
    else:
        return "sonnet"


def load_pricing_from_config(pricing_config: dict) -> dict[str, Pricing]:
    """
    Load pricing from config dict, merging with defaults.

    Config format (use short names):
        pricing:
          sonnet:
            input: 3.0
            output: 15.0
          haiku:
            input: 0.25
            output: 1.25
    """
    if not pricing_config:
        return DEFAULT_PRICING.copy()

    pricing = DEFAULT_PRICING.copy()

    for model, rates in pricing_config.items():
        if isinstance(rates, dict) and "input" in rates and "output" in rates:
            # Normalize to short name
            short_name = get_model_short_name(model)
            pricing[short_name] = Pricing(
                input=float(rates["input"]),
                output=float(rates["output"])
            )

    return pricing


class CostTracker:
    """
    Tracks costs and enforces thresholds.

    Usage:
        tracker = CostTracker(config)
        tracker.add_usage(model, input_tokens, output_tokens)
        if tracker.should_stop:
            # halt execution
    """

    def __init__(
        self,
        config: CostConfig = None,
        pricing: dict[str, Pricing] = None,
        on_warning: Callable[[float], None] = None,
        on_alert: Callable[[float], None] = None,
    ):
        self.config = config or CostConfig()
        self.pricing = pricing or DEFAULT_PRICING

        self.on_warning = on_warning
        self.on_alert = on_alert

        # Tracking state
        self.total_cost: float = 0.0
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.api_calls: int = 0

        # Per-model breakdown
        self.cost_by_model: dict[str, float] = {}
        self.tokens_by_model: dict[str, dict] = {}

        # Threshold state
        self.warning_acknowledged: bool = False
        self.alert_acknowledged: bool = False

    def get_pricing(self, model: str) -> Pricing:
        """Get pricing for a model (accepts short or full names)."""
        short_name = get_model_short_name(model)
        return self.pricing.get(short_name, DEFAULT_PRICING.get(short_name, DEFAULT_PRICING["sonnet"]))

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a single API call."""
        pricing = self.get_pricing(model)
        input_cost = (input_tokens / 1_000_000) * pricing.input
        output_cost = (output_tokens / 1_000_000) * pricing.output
        return input_cost + output_cost

    def add_usage(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Add usage from an API call.

        Returns the cost of this call.
        """
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        # Update totals
        self.total_cost += cost
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.api_calls += 1

        # Update per-model tracking
        if model not in self.cost_by_model:
            self.cost_by_model[model] = 0.0
            self.tokens_by_model[model] = {"input": 0, "output": 0}

        self.cost_by_model[model] += cost
        self.tokens_by_model[model]["input"] += input_tokens
        self.tokens_by_model[model]["output"] += output_tokens

        # Check thresholds
        self._check_thresholds()

        return cost

    def _check_thresholds(self) -> None:
        """Check and trigger threshold callbacks."""
        if self.total_cost >= self.config.warn and not self.warning_acknowledged:
            self.warning_acknowledged = True
            if self.on_warning:
                self.on_warning(self.total_cost)

        if self.total_cost >= self.config.alert and not self.alert_acknowledged:
            self.alert_acknowledged = True
            if self.on_alert:
                self.on_alert(self.total_cost)

    @property
    def threshold_level(self) -> ThresholdLevel:
        """Get current threshold level."""
        if self.total_cost >= self.config.max:
            return ThresholdLevel.STOP
        elif self.total_cost >= self.config.alert:
            return ThresholdLevel.ALERT
        elif self.total_cost >= self.config.warn:
            return ThresholdLevel.WARNING
        return ThresholdLevel.OK

    @property
    def should_stop(self) -> bool:
        """Check if we should stop execution."""
        return self.total_cost >= self.config.max

    @property
    def remaining_budget(self) -> float:
        """Get remaining budget before max threshold."""
        return max(0, self.config.max - self.total_cost)

    def reset_alerts(self) -> None:
        """Reset alert acknowledgments (for resume with new budget)."""
        self.warning_acknowledged = False
        self.alert_acknowledged = False

    def set_initial_cost(self, cost: float) -> None:
        """Set initial cost when resuming from checkpoint."""
        self.total_cost = cost
        self._check_thresholds()

    def get_summary(self) -> dict:
        """Get cost summary."""
        return {
            "total_cost": round(self.total_cost, 4),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            "api_calls": self.api_calls,
            "threshold_level": self.threshold_level.value,
            "remaining_budget": round(self.remaining_budget, 4),
            "cost_by_model": {k: round(v, 4) for k, v in self.cost_by_model.items()},
        }

    def format_status(self) -> str:
        """Format status for display."""
        level = self.threshold_level
        icons = {
            ThresholdLevel.OK: "✓",
            ThresholdLevel.WARNING: "⚠️",
            ThresholdLevel.ALERT: "🟠",
            ThresholdLevel.STOP: "🛑",
        }

        lines = [
            f"{icons[level]} Cost: ${self.total_cost:.2f} / ${self.config.max:.2f}",
            f"   Tokens: {self.input_tokens + self.output_tokens:,} ({self.api_calls} calls)",
        ]

        if self.cost_by_model:
            lines.append("   By model:")
            for model, cost in sorted(self.cost_by_model.items()):
                lines.append(f"     {model}: ${cost:.2f}")

        return "\n".join(lines)
