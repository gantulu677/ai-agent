"""Small internal data models used by the runtime foundation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


def _required_string(data: Mapping[str, Any], field_name: str) -> str:
    value = data.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{field_name}' must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class AgentConfig:
    """Parsed agent configuration with extension fields preserved."""

    id: str
    version: str
    extra_fields: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AgentConfig":
        known_fields = {"id", "version"}
        return cls(
            id=_required_string(data, "id"),
            version=_required_string(data, "version"),
            extra_fields={key: value for key, value in data.items() if key not in known_fields},
        )


@dataclass(frozen=True, slots=True)
class SkillConfig:
    """Parsed skill configuration with extension fields preserved."""

    id: str
    name: str
    description: str
    version: str
    extra_fields: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SkillConfig":
        known_fields = {"id", "name", "description", "version"}
        return cls(
            id=_required_string(data, "id"),
            name=_required_string(data, "name"),
            description=_required_string(data, "description"),
            version=_required_string(data, "version"),
            extra_fields={key: value for key, value in data.items() if key not in known_fields},
        )
