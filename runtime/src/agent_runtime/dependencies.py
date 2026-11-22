"""Inspect declared external skill dependencies without installing or executing them."""
from dataclasses import dataclass
from importlib.util import find_spec
from typing import Any


@dataclass(frozen=True, slots=True)
class DependencyStatus:
    name: str
    declared_type: str
    available: bool | None
    detail: str


def inspect_dependencies(dependencies: Any) -> list[DependencyStatus]:
    if dependencies is None:
        return []
    if not isinstance(dependencies, list):
        return [DependencyStatus("dependencies", "unknown", None, "Dependency declaration is not an array; no installation attempted.")]
    results = []
    for item in dependencies:
        if isinstance(item, str):
            results.append(DependencyStatus(item, "package", find_spec(item) is not None, "Checked import availability only."))
        elif isinstance(item, dict):
            name = str(item.get("name", "unnamed"))
            kind = str(item.get("type", "external"))
            available = find_spec(name) is not None if kind == "python" and name.isidentifier() else None
            results.append(DependencyStatus(name, kind, available, "Inspected declaration; no installation or network access attempted."))
        else:
            results.append(DependencyStatus("invalid-entry", "unknown", None, "Unsupported dependency declaration entry."))
    return results
