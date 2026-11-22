"""Discover agents in direct child directories of agents/."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AgentCandidate:
    directory: Path
    config_path: Path


def discover_agents(repository_root: Path) -> list[AgentCandidate]:
    agents_root = repository_root / "agents"
    if not agents_root.is_dir():
        return []
    found = []
    for directory in sorted(agents_root.iterdir(), key=lambda p: p.name):
        if directory.is_symlink() or not directory.is_dir() or directory.name.startswith("."):
            continue
        config_path = directory / "agent.json"
        if config_path.is_file() and not config_path.is_symlink():
            found.append(AgentCandidate(directory=directory, config_path=config_path))
    return found
