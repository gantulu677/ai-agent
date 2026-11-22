"""Load and order an agent's instruction files."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent_runtime.cache.manager import FileCache
from agent_runtime.discovery.instructions import discover_instructions
from agent_runtime.ordering.instructions import order_instructions
from agent_runtime.parsers.instructions import ParsedInstruction, parse_instruction


@dataclass(frozen=True, slots=True)
class LoadedInstruction:
    source: str
    category: str
    format: str
    content: Any
    metadata: dict[str, Any]


def load_instructions(
    agent_directory: Path,
    configured_categories: list[str] | None = None,
    cache: FileCache | None = None,
) -> list[LoadedInstruction]:
    candidates = discover_instructions(agent_directory)
    ordered = order_instructions(candidates, configured_categories)
    loaded = []
    for item in ordered:
        parsed: ParsedInstruction = cache.get_or_load(item.path, parse_instruction) if cache else parse_instruction(item.path)
        loaded.append(LoadedInstruction(item.relative_path, item.category, parsed.format, parsed.content, parsed.metadata))
    return loaded
