"""Inspect external skill dependencies without installing or executing them."""
from dataclasses import dataclass
from importlib.util import find_spec
from typing import Any

_SUPPORTED_TYPES = {"package", "python", "tool", "api", "resource"}


@dataclass(frozen=True, slots=True)
class DependencyStatus:
    name: str
    declared_type: str
    available: bool | None
    detail: str
    valid: bool = True


def _package_available(name: str) -> bool | None:
    # Distribution names and import names are not always identical.
    # Only probe simple import identifiers; never import or install a package.
    if not name.isidentifier():
        return None
    try:
        return find_spec(name) is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


def inspect_dependencies(dependencies: Any) -> list[DependencyStatus]:
    """Inspect a flexible list of package/tool/API/resource declarations.

    Accepted entries are package-name strings or objects with non-empty
    name and a type in package/python/tool/api/resource. Extra keys are
    retained by the skill configuration and are intentionally allowed.
    """
    if dependencies is None:
        return []
    if not isinstance(dependencies, list):
        return [DependencyStatus(
            "dependencies", "invalid", None,
            "Dependency declaration must be an array; no installation attempted.",
            valid=False,
        )]

    results: list[DependencyStatus] = []
    for item in dependencies:
        if isinstance(item, str) and item.strip():
            available = _package_available(item)
            detail = (
                "Package is available in this Python environment; no installation attempted."
                if available is True else
                "Package is not available in this Python environment; no installation attempted."
                if available is False else
                "Package declaration recorded; import availability was not probed."
            )
            results.append(DependencyStatus(item, "package", available, detail))
            continue

        if isinstance(item, dict):
            name = item.get("name")
            kind = item.get("type")
            valid = (
                isinstance(name, str) and bool(name.strip())
                and isinstance(kind, str) and kind.lower() in _SUPPORTED_TYPES
            )
            if not valid:
                results.append(DependencyStatus(
                    str(name or "invalid-entry"), str(kind or "invalid"), None,
                    "Dependency object requires a non-empty name and supported type "
                    "(package, python, tool, api, resource).",
                    valid=False,
                ))
                continue
            name = name.strip()
            kind = kind.lower()
            available = _package_available(name) if kind in {"package", "python"} else None
            detail = (
                "Package is available in this Python environment; no installation attempted."
                if available is True else
                "Package is not available in this Python environment; no installation attempted."
                if available is False else
                f"{kind} dependency declaration recorded; external availability is not resolved."
            )
            results.append(DependencyStatus(name, kind, available, detail))
            continue

        results.append(DependencyStatus(
            "invalid-entry", "invalid", None,
            "Dependency entry must be a non-empty package string or a typed object.",
            valid=False,
        ))
    return results
