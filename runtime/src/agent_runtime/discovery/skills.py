"""Discover skill directories directly below each agent's skills/ folder."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SkillCandidate:
    directory: Path
    config_path: Path
    instruction_path: Path


def discover_skills(agent_directory: Path) -> list[SkillCandidate]:
    root = agent_directory / "skills"
    if not root.is_dir():
        return []
    found = []
    for directory in sorted(root.iterdir(), key=lambda p: p.name):
        if directory.is_symlink() or not directory.is_dir() or directory.name.startswith("."):
            continue
        config = directory / "skill.json"
        instruction = directory / "SKILL.md"
        # Include partial structures so validation can report missing required files.
        if config.exists() or instruction.exists():
            found.append(SkillCandidate(directory, config, instruction))
    return found
