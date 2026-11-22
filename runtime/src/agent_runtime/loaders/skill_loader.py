"""Load skill metadata and markdown instructions on demand."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from agent_runtime.models import SkillConfig


@dataclass(frozen=True, slots=True)
class LoadedSkill:
    config: SkillConfig
    instructions: str
    directory: Path
    resources: tuple[Path, ...]
    dependencies: Any


def load_skill(skill_directory: Path) -> LoadedSkill:
    config_path, instruction_path = skill_directory / "skill.json", skill_directory / "SKILL.md"
    if not config_path.is_file() or not instruction_path.is_file():
        raise FileNotFoundError("A skill requires both skill.json and SKILL.md")
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("skill.json root must be an object")
    config = SkillConfig.from_mapping(raw)
    resources = tuple(sorted(
        (path for path in skill_directory.iterdir() if path.is_dir() and not path.is_symlink()),
        key=lambda path: path.name,
    ))
    return LoadedSkill(config, instruction_path.read_text(encoding="utf-8"), skill_directory, resources, raw.get("dependencies"))
