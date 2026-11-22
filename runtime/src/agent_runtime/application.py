"""Application services for discovery, validation, and runtime info."""
from dataclasses import dataclass
from pathlib import Path

from agent_runtime import __version__
from agent_runtime.discovery.agents import discover_agents
from agent_runtime.loaders.agent_loader import LoadedAgent, load_agent
from agent_runtime.validation.engine import ValidationEngine
from agent_runtime.validation.report import Severity


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

    def load_valid_agents(self) -> tuple[LoadedAgent, ...]:
        """Load only agents without Critical findings; isolate malformed agents."""
        import logging

        logger = logging.getLogger("agent_runtime.application")
        report = self.validate()
        rejected_ids = {
            issue.agent_id
            for issue in report.issues
            if issue.severity == Severity.CRITICAL and issue.agent_id
        }
        rejected_directories = set()
        for issue in report.issues:
            if issue.severity != Severity.CRITICAL or not issue.path:
                continue
            parts = Path(issue.path).parts
            if len(parts) >= 2 and parts[0] == "agents":
                rejected_directories.add(parts[1])

        loaded: list[LoadedAgent] = []
        for candidate in self.discover():
            if candidate.directory.name in rejected_directories:
                continue
            try:
                agent = load_agent(candidate.directory)
                if agent.config.id in rejected_ids:
                    continue
                loaded.append(agent)
            except Exception:
                logger.exception("Agent loading failed; continuing with other agents: %s", candidate.directory)
        return tuple(loaded)
