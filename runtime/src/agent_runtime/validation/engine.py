"""Repository and per-agent validation engine."""
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator

from agent_runtime.discovery.agents import discover_agents
from agent_runtime.discovery.instructions import discover_instructions
from agent_runtime.discovery.skills import discover_skills
from agent_runtime.models import AgentConfig, SkillConfig
from agent_runtime.ordering.instructions import order_instructions
from agent_runtime.parsers.instructions import parse_instruction
from agent_runtime.validation.report import Severity, ValidationIssue, ValidationReport

_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ValidationEngine:
    def __init__(self, repository_root: Path):
        self.root = repository_root.resolve()
        self.issues: list[ValidationIssue] = []

    def _add(self, severity: Severity, code: str, message: str, path: Path | None = None, agent_id: str | None = None) -> None:
        relative = path.relative_to(self.root).as_posix() if path else None
        self.issues.append(ValidationIssue(severity, code, message, relative, agent_id))

    def _load_json(self, path: Path, agent_id: str | None = None) -> dict[str, Any] | None:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("JSON root must be an object")
            return value
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            self._add(Severity.CRITICAL, "INVALID_JSON", str(exc), path, agent_id)
            return None

    def _schema_check(self, data: dict, schema_name: str, path: Path, agent_id: str | None) -> None:
        schema_path = self.root / "schemas" / schema_name
        if not schema_path.is_file():
            self._add(Severity.CRITICAL, "SCHEMA_MISSING", f"Schema not found: {schema_name}", schema_path, agent_id)
            return
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
            for error in errors:
                self._add(Severity.CRITICAL, "SCHEMA_VALIDATION", error.message, path, agent_id)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            self._add(Severity.CRITICAL, "INVALID_SCHEMA", str(exc), schema_path, agent_id)

    def validate(self) -> ValidationReport:
        self.issues = []
        candidates = discover_agents(self.root)
        if not candidates:
            self._add(Severity.INFO, "NO_AGENTS", "No agent directories with agent.json were discovered.")
        seen_agents: dict[str, Path] = {}
        for candidate in candidates:
            raw = self._load_json(candidate.config_path)
            if raw is None:
                continue
            self._schema_check(raw, "agent.schema.json", candidate.config_path, None)
            try:
                config = AgentConfig.from_mapping(raw)
            except ValueError as exc:
                self._add(Severity.CRITICAL, "AGENT_CONFIG_INVALID", str(exc), candidate.config_path)
                continue
            agent_id = config.id
            if not _ID_PATTERN.fullmatch(agent_id):
                self._add(Severity.CRITICAL, "INVALID_AGENT_ID", "Agent ID must use lowercase kebab-case.", candidate.config_path, agent_id)
            if agent_id in seen_agents:
                self._add(Severity.CRITICAL, "DUPLICATE_AGENT_ID", f"Agent ID duplicates {seen_agents[agent_id].as_posix()}.", candidate.config_path, agent_id)
            else:
                seen_agents[agent_id] = candidate.directory

            configured_categories = raw.get("instruction_category_order")
            if configured_categories is not None and (
                not isinstance(configured_categories, list)
                or not all(isinstance(value, str) for value in configured_categories)
            ):
                self._add(Severity.CRITICAL, "INVALID_CATEGORY_ORDER", "instruction_category_order must be an array of strings.", candidate.config_path, agent_id)
                configured_categories = None

            instruction_candidates = discover_instructions(candidate.directory)
            for instruction in instruction_candidates:
                try:
                    parsed = parse_instruction(instruction.path)
                    if parsed.format == "markdown" and "priority" in parsed.metadata:
                        priority = parsed.metadata["priority"]
                        if isinstance(priority, bool) or not isinstance(priority, int) or priority < 1:
                            raise ValueError("priority must be a positive integer")
                except Exception as exc:
                    self._add(Severity.CRITICAL, "INSTRUCTION_PARSE_ERROR", str(exc), instruction.path, agent_id)
            try:
                order_instructions(instruction_candidates, configured_categories)
            except Exception as exc:
                self._add(Severity.CRITICAL, "INSTRUCTION_ORDER_ERROR", str(exc), candidate.directory / "instructions", agent_id)

            seen_skills: set[str] = set()
            for skill in discover_skills(candidate.directory):
                skill_raw = self._load_json(skill.config_path, agent_id) if skill.config_path.is_file() else None
                if not skill.config_path.is_file():
                    self._add(Severity.CRITICAL, "SKILL_CONFIG_MISSING", "skill.json is required.", skill.config_path, agent_id)
                if not skill.instruction_path.is_file():
                    self._add(Severity.CRITICAL, "SKILL_INSTRUCTIONS_MISSING", "SKILL.md is required.", skill.instruction_path, agent_id)
                if skill_raw is None:
                    continue
                self._schema_check(skill_raw, "skill.schema.json", skill.config_path, agent_id)
                try:
                    skill_config = SkillConfig.from_mapping(skill_raw)
                except ValueError as exc:
                    self._add(Severity.CRITICAL, "SKILL_CONFIG_INVALID", str(exc), skill.config_path, agent_id)
                    continue
                if not _ID_PATTERN.fullmatch(skill_config.id):
                    self._add(Severity.CRITICAL, "INVALID_SKILL_ID", "Skill ID must use lowercase kebab-case.", skill.config_path, agent_id)
                if skill_config.id in seen_skills:
                    self._add(Severity.CRITICAL, "DUPLICATE_SKILL_ID", "Skill ID must be unique within its owning agent.", skill.config_path, agent_id)
                seen_skills.add(skill_config.id)
        return ValidationReport(self.issues)
