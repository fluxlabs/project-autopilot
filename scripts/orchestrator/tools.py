"""
Tool implementations for Autopilot API Orchestrator
Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Provides file operations, bash execution, and search tools.
"""

import fnmatch
import os
import re
import subprocess
from pathlib import Path
from typing import Any


class ToolError(Exception):
    """Raised when a tool execution fails."""
    pass


class Tools:
    """Tool implementations matching Claude Code capabilities."""

    def __init__(self, project_dir: str, tools_config: dict, orchestrator_config=None):
        self.project_dir = Path(project_dir).resolve()
        self.config = tools_config
        self.bash_config = self.config.get("bash", {})
        self.orchestrator_config = orchestrator_config

        # Callback for confirmation prompts (set by orchestrator)
        self.on_confirm_request = None

    def get_tool_definitions(self) -> list[dict]:
        """Return tool definitions for the API."""
        return [
            {
                "name": "read_file",
                "description": "Read contents of a file. Returns file content with line numbers.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file (relative to project root)"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Line number to start reading from (1-indexed)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of lines to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file. Creates parent directories if needed.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file (relative to project root)"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "edit_file",
                "description": "Replace a specific string in a file with new content.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file (relative to project root)"
                        },
                        "old_string": {
                            "type": "string",
                            "description": "Exact string to find and replace"
                        },
                        "new_string": {
                            "type": "string",
                            "description": "Replacement string"
                        },
                        "replace_all": {
                            "type": "boolean",
                            "description": "Replace all occurrences (default: false)"
                        }
                    },
                    "required": ["path", "old_string", "new_string"]
                }
            },
            {
                "name": "bash",
                "description": "Execute a bash command. Use for git, npm, tests, etc.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command to execute"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds (default: 120)"
                        }
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "glob",
                "description": "Find files matching a glob pattern.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Glob pattern (e.g., '**/*.ts', 'src/**/*.py')"
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory to search in (default: project root)"
                        }
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "grep",
                "description": "Search file contents using regex.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Regex pattern to search for"
                        },
                        "path": {
                            "type": "string",
                            "description": "File or directory to search"
                        },
                        "glob_filter": {
                            "type": "string",
                            "description": "Only search files matching this glob"
                        },
                        "case_insensitive": {
                            "type": "boolean",
                            "description": "Case insensitive search"
                        }
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "list_dir",
                "description": "List contents of a directory.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path (default: project root)"
                        }
                    }
                }
            },
            {
                "name": "phase_complete",
                "description": "Signal that a phase is complete and verified. Commits all changes with a descriptive message.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "phase_name": {
                            "type": "string",
                            "description": "Name of the completed phase (e.g., 'authentication', 'api-endpoints')"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Brief summary of what was accomplished in this phase"
                        },
                        "files_changed": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of files created or modified"
                        },
                        "tests_passed": {
                            "type": "boolean",
                            "description": "Whether tests were run and passed"
                        },
                        "verification": {
                            "type": "string",
                            "description": "How the phase was verified (e.g., 'unit tests pass', 'manual testing', 'type check passes')"
                        }
                    },
                    "required": ["phase_name", "summary", "verification"]
                }
            },
            {
                "name": "task_complete",
                "description": "Signal that the entire task is complete (all phases done).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Brief summary of what was accomplished"
                        },
                        "next_steps": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Suggested next steps (if any)"
                        }
                    },
                    "required": ["summary"]
                }
            },
            {
                "name": "request_help",
                "description": "Request human intervention when stuck or need clarification.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "What you need help with"
                        },
                        "context": {
                            "type": "string",
                            "description": "Relevant context"
                        },
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Possible options if applicable"
                        }
                    },
                    "required": ["question"]
                }
            }
        ]

    def resolve_path(self, path: str) -> Path:
        """Resolve path relative to project directory."""
        if os.path.isabs(path):
            resolved = Path(path)
        else:
            resolved = self.project_dir / path

        # Security: ensure path is within project
        try:
            resolved.resolve().relative_to(self.project_dir.resolve())
        except ValueError:
            raise ToolError(f"Path '{path}' is outside project directory")

        return resolved

    def execute(self, tool_name: str, tool_input: dict) -> tuple[str, bool]:
        """
        Execute a tool and return (result, is_error).
        """
        try:
            method = getattr(self, f"tool_{tool_name}", None)
            if method is None:
                return f"Unknown tool: {tool_name}", True
            result = method(**tool_input)
            return result, False
        except ToolError as e:
            return str(e), True
        except Exception as e:
            return f"Tool error: {type(e).__name__}: {e}", True

    def tool_read_file(self, path: str, offset: int = 1, limit: int = 2000) -> str:
        """Read file contents with line numbers."""
        file_path = self.resolve_path(path)

        if not file_path.exists():
            raise ToolError(f"File not found: {path}")

        if not file_path.is_file():
            raise ToolError(f"Not a file: {path}")

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            raise ToolError(f"Cannot read file: {e}")

        lines = content.splitlines()
        total_lines = len(lines)

        # Apply offset and limit
        start_idx = max(0, offset - 1)
        end_idx = min(total_lines, start_idx + limit)
        selected_lines = lines[start_idx:end_idx]

        # Format with line numbers
        numbered = []
        for i, line in enumerate(selected_lines, start=start_idx + 1):
            # Truncate very long lines
            if len(line) > 2000:
                line = line[:2000] + "... [truncated]"
            numbered.append(f"{i:6}\t{line}")

        result = "\n".join(numbered)

        if end_idx < total_lines:
            result += f"\n\n[... {total_lines - end_idx} more lines]"

        return result

    def tool_write_file(self, path: str, content: str) -> str:
        """Write content to file."""
        file_path = self.resolve_path(path)

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            file_path.write_text(content, encoding="utf-8")
        except Exception as e:
            raise ToolError(f"Cannot write file: {e}")

        return f"Successfully wrote {len(content)} bytes to {path}"

    def tool_edit_file(
        self, path: str, old_string: str, new_string: str, replace_all: bool = False
    ) -> str:
        """Edit file by replacing string."""
        file_path = self.resolve_path(path)

        if not file_path.exists():
            raise ToolError(f"File not found: {path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ToolError(f"Cannot read file: {e}")

        if old_string not in content:
            raise ToolError(f"String not found in file: {old_string[:100]}...")

        if not replace_all:
            count = content.count(old_string)
            if count > 1:
                raise ToolError(
                    f"String appears {count} times. Use replace_all=true or provide more context."
                )

        if replace_all:
            new_content = content.replace(old_string, new_string)
            count = content.count(old_string)
        else:
            new_content = content.replace(old_string, new_string, 1)
            count = 1

        try:
            file_path.write_text(new_content, encoding="utf-8")
        except Exception as e:
            raise ToolError(f"Cannot write file: {e}")

        return f"Replaced {count} occurrence(s) in {path}"

    def tool_bash(self, command: str, timeout: int = None) -> str:
        """Execute bash command."""
        if timeout is None:
            timeout = self.bash_config.get("timeout", 120)

        # Parse command to get the base command
        parts = command.split()
        if not parts:
            raise ToolError("Empty command")

        base_cmd = parts[0]

        # Handle pipes and chains - check first command
        for separator in ["|", "&&", "||", ";"]:
            if separator in base_cmd:
                base_cmd = base_cmd.split(separator)[0].strip()
                break

        # Security check 1: Blocked commands (always rejected)
        blocked = self.bash_config.get("blocked", [])
        for blocked_cmd in blocked:
            if blocked_cmd in parts:
                raise ToolError(f"Command '{blocked_cmd}' is blocked for security")

        # Security check 2: Allowed commands (whitelist)
        allowed = self.bash_config.get("allowed", [])
        if allowed and base_cmd not in allowed:
            raise ToolError(
                f"Command '{base_cmd}' is not in allowed list. "
                f"Allowed commands: {', '.join(allowed[:10])}..."
            )

        # Security check 3: Commands requiring confirmation
        confirm_list = self.bash_config.get("confirm", [])
        needs_confirm = any(cmd in parts for cmd in confirm_list)

        if needs_confirm:
            if self.on_confirm_request:
                confirmed = self.on_confirm_request(
                    f"Command requires confirmation: {command}\n"
                    f"This command may modify or delete files."
                )
                if not confirmed:
                    raise ToolError(f"Command '{base_cmd}' was not confirmed by user")
            else:
                # No confirmation callback - check config for default behavior
                # Default: block commands requiring confirmation if no callback
                raise ToolError(
                    f"Command '{base_cmd}' requires confirmation but no confirmation handler is set. "
                    f"Command blocked for safety."
                )

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += f"[stderr]\n{result.stderr}"

            if result.returncode != 0:
                output += f"\n[exit code: {result.returncode}]"

            # Truncate very long output
            if len(output) > 30000:
                output = output[:30000] + "\n\n[... output truncated]"

            return output or "[no output]"

        except subprocess.TimeoutExpired:
            raise ToolError(f"Command timed out after {timeout}s")
        except Exception as e:
            raise ToolError(f"Command failed: {e}")

    def tool_glob(self, pattern: str, path: str = None) -> str:
        """Find files matching glob pattern."""
        search_dir = self.resolve_path(path) if path else self.project_dir

        if not search_dir.is_dir():
            raise ToolError(f"Not a directory: {path}")

        matches = []
        for file_path in search_dir.rglob(pattern.lstrip("*/")):
            if file_path.is_file():
                try:
                    rel_path = file_path.relative_to(self.project_dir)
                    matches.append(str(rel_path))
                except ValueError:
                    pass

        if not matches:
            return f"No files matching '{pattern}'"

        # Sort and limit
        matches.sort()
        if len(matches) > 100:
            return "\n".join(matches[:100]) + f"\n\n[... {len(matches) - 100} more files]"

        return "\n".join(matches)

    def tool_grep(
        self,
        pattern: str,
        path: str = None,
        glob_filter: str = None,
        case_insensitive: bool = False,
    ) -> str:
        """Search file contents."""
        search_path = self.resolve_path(path) if path else self.project_dir

        flags = re.IGNORECASE if case_insensitive else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            raise ToolError(f"Invalid regex: {e}")

        results = []
        files_searched = 0

        def search_file(file_path: Path):
            nonlocal files_searched
            files_searched += 1

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                return

            rel_path = file_path.relative_to(self.project_dir)
            for line_num, line in enumerate(content.splitlines(), 1):
                if regex.search(line):
                    results.append(f"{rel_path}:{line_num}: {line[:200]}")
                    if len(results) >= 100:
                        return

        if search_path.is_file():
            search_file(search_path)
        else:
            for file_path in search_path.rglob("*"):
                if len(results) >= 100:
                    break
                if not file_path.is_file():
                    continue
                if glob_filter and not fnmatch.fnmatch(file_path.name, glob_filter):
                    continue
                # Skip binary files and common non-text
                if file_path.suffix in [".pyc", ".so", ".o", ".a", ".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot"]:
                    continue
                search_file(file_path)

        if not results:
            return f"No matches for '{pattern}' in {files_searched} files"

        output = "\n".join(results)
        if len(results) >= 100:
            output += "\n\n[... results limited to 100 matches]"

        return output

    def tool_list_dir(self, path: str = None) -> str:
        """List directory contents."""
        dir_path = self.resolve_path(path) if path else self.project_dir

        if not dir_path.exists():
            raise ToolError(f"Directory not found: {path}")

        if not dir_path.is_dir():
            raise ToolError(f"Not a directory: {path}")

        entries = []
        for entry in sorted(dir_path.iterdir()):
            if entry.name.startswith("."):
                continue  # Skip hidden by default
            if entry.is_dir():
                entries.append(f"{entry.name}/")
            else:
                size = entry.stat().st_size
                entries.append(f"{entry.name} ({size} bytes)")

        return "\n".join(entries) if entries else "[empty directory]"

    def tool_phase_complete(
        self,
        phase_name: str,
        summary: str,
        verification: str = None,
        files_changed: list[str] = None,
        tests_passed: bool = None,
    ) -> str:
        """
        Signal phase completion, verify, and commit changes.

        Commits based on git config options from orchestrator config.
        """
        result_lines = [f"Phase '{phase_name}' completed: {summary}"]

        # Get git config options
        auto_commit = True
        commit_prefix = "feat"
        require_verification = True

        if self.orchestrator_config:
            auto_commit = getattr(self.orchestrator_config, 'git_auto_commit', True)
            commit_prefix = getattr(self.orchestrator_config, 'git_commit_prefix', 'feat')
            require_verification = getattr(self.orchestrator_config, 'git_require_verification', True)

        # Check verification requirement
        if require_verification and not verification:
            result_lines.append("⚠ Verification required but not provided - skipping commit")
            return "\n".join(result_lines)

        if verification:
            result_lines.append(f"Verification: {verification}")

        if tests_passed is not None:
            result_lines.append(f"Tests: {'✓ Passed' if tests_passed else '✗ Failed'}")

        # Skip commit if auto_commit is disabled
        if not auto_commit:
            result_lines.append("\nAuto-commit disabled - changes not committed.")
            return "\n".join(result_lines)

        # Check for uncommitted changes
        try:
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )

            has_changes = bool(status_result.stdout.strip())

            if has_changes:
                # Stage all changes
                subprocess.run(
                    ["git", "add", "-A"],
                    cwd=str(self.project_dir),
                    capture_output=True,
                    timeout=30,
                )

                # Build commit message with configurable prefix
                commit_msg = f"{commit_prefix}({phase_name}): {summary}\n\n"
                if verification:
                    commit_msg += f"Verification: {verification}\n"
                if files_changed:
                    commit_msg += f"\nFiles changed:\n"
                    for f in files_changed[:20]:  # Limit to 20 files in message
                        commit_msg += f"  - {f}\n"
                    if len(files_changed) > 20:
                        commit_msg += f"  ... and {len(files_changed) - 20} more\n"

                # Commit
                commit_result = subprocess.run(
                    ["git", "commit", "-m", commit_msg],
                    cwd=str(self.project_dir),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if commit_result.returncode == 0:
                    result_lines.append(f"\n✓ Committed: {commit_prefix}({phase_name}): {summary}")
                else:
                    result_lines.append(f"\n⚠ Commit failed: {commit_result.stderr}")
            else:
                result_lines.append("\nNo uncommitted changes to commit.")

        except subprocess.TimeoutExpired:
            result_lines.append("\n⚠ Git operation timed out")
        except FileNotFoundError:
            result_lines.append("\n⚠ Git not found - skipping commit")
        except Exception as e:
            result_lines.append(f"\n⚠ Git error: {e}")

        return "\n".join(result_lines)

    def tool_task_complete(self, summary: str, next_steps: list[str] = None) -> str:
        """Signal task completion."""
        result = f"Task completed: {summary}"
        if next_steps:
            result += "\n\nSuggested next steps:\n" + "\n".join(f"- {s}" for s in next_steps)
        return result

    def tool_request_help(
        self, question: str, context: str = None, options: list[str] = None
    ) -> str:
        """Request human help - this pauses execution."""
        result = f"HELP REQUESTED: {question}"
        if context:
            result += f"\n\nContext: {context}"
        if options:
            result += "\n\nOptions:\n" + "\n".join(f"- {o}" for o in options)
        return result
