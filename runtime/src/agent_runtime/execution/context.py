"""Per-agent execution context; state is not shared between agents."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agent_runtime.loaders.agent_loader import LoadedAgent
from agent_runtime.tools.executor import ToolExecutor


@dataclass(slots=True)
class AgentContext:
    agent: LoadedAgent
    tool_executor: ToolExecutor = field(default_factory=ToolExecutor)
    state: dict[str, Any] = field(default_factory=dict)
    working_directory: Path | None = None
