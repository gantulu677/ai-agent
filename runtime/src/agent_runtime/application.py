"""Application services for discovery, validation, and runtime info."""
from dataclasses import dataclass
from pathlib import Path

from agent_runtime import __version__
from agent_runtime.discovery.agents import discover_agents
from agent_runtime.validation.engine import ValidationEngine


@dataclass(frozen=True, slots=True)
class RuntimeInfo:
    name: str
    version: str
    implementation_phase: str
    implemented_capabilities: tuple[str, ...]


class RuntimeApplication:
    def __init__(self, repository_root: Path | None = None):
        self.repository_root = (repository_root or Path.cwd()).resolve()

    def get_info(self) -> RuntimeInfo:
        return RuntimeInfo(
            name="AI Agent Runtime", version=__version__,
            implementation_phase="Phases 1-6 implementation baseline",
            implemented_capabilities=(
                "Automatic agent, skill, and instruction discovery",
                "Per-agent and repository configuration validation",
                "Markdown, TXT, JSON, and YAML instruction parsing",
                "Deterministic category and file ordering",
                "On-demand skill loading and dependency inspection",
                "Async LLM provider and explicit tool execution interfaces",
                "Isolated agent contexts, sessions, caching, and logging",
                "JSON and Markdown validation reports",
            ),
        )

    def discover(self):
        return discover_agents(self.repository_root)

    def validate(self):
        return ValidationEngine(self.repository_root).validate()
