"""Apply category and per-file instruction ordering rules."""
from pathlib import Path
import re
from typing import Iterable

from agent_runtime.discovery.instructions import InstructionCandidate
from agent_runtime.parsers.instructions import parse_instruction

_NUMERIC_PREFIX = re.compile(r"^(\\d+)")
DEFAULT_CATEGORY_ORDER = ("core", "behavior", "workflow", "response")


def category_order(categories: Iterable[str], configured: list[str] | None = None) -> list[str]:
    preferred = list(configured) if configured is not None else list(DEFAULT_CATEGORY_ORDER)
    present = set(categories)
    ordered = [name for name in preferred if name in present]
    ordered.extend(sorted(present.difference(ordered)))
    return ordered


def _file_key(candidate: InstructionCandidate) -> tuple:
    parsed = parse_instruction(candidate.path)
    priority = parsed.metadata.get("priority") if parsed.format == "markdown" else None
    if priority is not None and (isinstance(priority, bool) or not isinstance(priority, int) or priority < 1):
        raise ValueError(f"Invalid priority in {candidate.relative_path}: expected a positive integer")
    match = _NUMERIC_PREFIX.match(candidate.path.name)
    numeric = int(match.group(1)) if match else None
    primary = priority if priority is not None else numeric if numeric is not None else float("inf")
    tie_numeric = numeric if numeric is not None else float("inf")
    return (primary, tie_numeric, candidate.relative_path)


def order_instructions(candidates: list[InstructionCandidate], configured_categories: list[str] | None = None) -> list[InstructionCandidate]:
    categories = category_order((item.category for item in candidates), configured_categories)
    by_category = {name: [] for name in categories}
    for item in candidates:
        by_category[item.category].append(item)
    result = []
    for category in categories:
        result.extend(sorted(by_category[category], key=_file_key))
    return result
