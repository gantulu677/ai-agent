"""A single request/response session for an agent."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentSession:
    agent_id: str
    history: list[dict[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        if role not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"Unsupported message role: {role}")
        self.history.append({"role": role, "content": content})
