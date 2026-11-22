"""Discover supported instruction files recursively within category folders."""
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".json", ".yaml", ".txt"}


@dataclass(frozen=True, slots=True)
class InstructionCandidate:
    path: Path
    relative_path: str
    category: str


def discover_instructions(agent_directory: Path) -> list[InstructionCandidate]:
    root = agent_directory / "instructions"
    if not root.is_dir():
        return []
    found = []
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if len(relative.parts) < 2:
            continue
        found.append(InstructionCandidate(path, relative.as_posix(), relative.parts[0]))
    return sorted(found, key=lambda item: item.relative_path)
