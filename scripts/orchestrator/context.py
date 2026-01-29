"""
Context window manager for Autopilot API Orchestrator
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Manages conversation history, token counting, and context optimization.
"""

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenUsage:
    """Track token usage across the session."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0

    def add(self, usage: dict) -> None:
        """Add usage from API response."""
        self.input_tokens += usage.get("input_tokens", 0)
        self.output_tokens += usage.get("output_tokens", 0)
        self.cache_read_tokens += usage.get("cache_read_input_tokens", 0)
        self.cache_creation_tokens += usage.get("cache_creation_input_tokens", 0)

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_creation_tokens": self.cache_creation_tokens,
            "total": self.total,
        }


@dataclass
class ContextManager:
    """
    Manages conversation context with smart windowing.

    Strategies:
    1. Keep system prompt always
    2. Keep recent N turns fully
    3. Summarize older turns
    4. Preserve tool results that are referenced later
    """

    system_prompt: str = ""
    messages: list[dict] = field(default_factory=list)
    max_context_tokens: int = 150000
    checkpoint_threshold: float = 0.6
    summary_threshold: float = 0.8

    # Estimated tokens (rough: 4 chars = 1 token)
    _estimated_tokens: int = 0

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimate. In production, use tiktoken or API."""
        if not text:
            return 0
        return len(text) // 4

    def estimate_message_tokens(self, message: dict) -> int:
        """Estimate tokens for a single message."""
        total = 0
        content = message.get("content", "")

        if isinstance(content, str):
            total += self.estimate_tokens(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        total += self.estimate_tokens(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        total += self.estimate_tokens(json.dumps(block.get("input", {})))
                    elif block.get("type") == "tool_result":
                        total += self.estimate_tokens(str(block.get("content", "")))

        return total

    def update_token_estimate(self) -> int:
        """Recalculate total token estimate."""
        total = self.estimate_tokens(self.system_prompt)
        for msg in self.messages:
            total += self.estimate_message_tokens(msg)
        self._estimated_tokens = total
        return total

    @property
    def context_usage(self) -> float:
        """Return context usage as fraction (0.0 to 1.0)."""
        return self._estimated_tokens / self.max_context_tokens

    @property
    def should_checkpoint(self) -> bool:
        """Check if we should save a checkpoint."""
        return self.context_usage >= self.checkpoint_threshold

    @property
    def should_summarize(self) -> bool:
        """Check if we need to summarize older context."""
        return self.context_usage >= self.summary_threshold

    def add_user_message(self, content: str) -> None:
        """Add a user message."""
        self.messages.append({"role": "user", "content": content})
        self.update_token_estimate()

    def add_assistant_message(self, content: list[dict] | str) -> None:
        """Add an assistant message."""
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        self.messages.append({"role": "assistant", "content": content})
        self.update_token_estimate()

    def add_tool_result(self, tool_use_id: str, result: str, is_error: bool = False) -> None:
        """Add a tool result message."""
        self.messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": result,
                "is_error": is_error,
            }]
        })
        self.update_token_estimate()

    def add_tool_results(self, results: list[dict]) -> None:
        """Add multiple tool results in one message."""
        content = []
        for r in results:
            content.append({
                "type": "tool_result",
                "tool_use_id": r["tool_use_id"],
                "content": r["content"],
                "is_error": r.get("is_error", False),
            })
        self.messages.append({"role": "user", "content": content})
        self.update_token_estimate()

    def get_messages(self) -> list[dict]:
        """Get messages for API call."""
        return self.messages.copy()

    def summarize_old_context(self, summary: str, keep_recent: int = 10) -> None:
        """
        Replace older messages with a summary.

        Args:
            summary: AI-generated summary of older context
            keep_recent: Number of recent message pairs to keep fully
        """
        if len(self.messages) <= keep_recent * 2:
            return

        # Keep system prompt, add summary, keep recent messages
        cutoff = len(self.messages) - (keep_recent * 2)
        old_messages = self.messages[:cutoff]
        recent_messages = self.messages[cutoff:]

        # Create summary message
        summary_msg = {
            "role": "user",
            "content": f"[CONTEXT SUMMARY - {len(old_messages)} previous messages]\n\n{summary}\n\n[END SUMMARY - Recent conversation follows]"
        }

        self.messages = [summary_msg] + recent_messages
        self.update_token_estimate()

    def clear(self) -> None:
        """Clear all messages (keep system prompt)."""
        self.messages = []
        self._estimated_tokens = self.estimate_tokens(self.system_prompt)

    def to_dict(self) -> dict:
        """Export state for checkpointing."""
        return {
            "system_prompt": self.system_prompt,
            "messages": self.messages,
            "estimated_tokens": self._estimated_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict, max_context_tokens: int = 150000) -> "ContextManager":
        """Restore from checkpoint."""
        ctx = cls(
            system_prompt=data.get("system_prompt", ""),
            messages=data.get("messages", []),
            max_context_tokens=max_context_tokens,
        )
        ctx._estimated_tokens = data.get("estimated_tokens", 0)
        ctx.update_token_estimate()  # Recalculate to be safe
        return ctx
