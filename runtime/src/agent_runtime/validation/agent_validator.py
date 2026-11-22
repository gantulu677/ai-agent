"""Convenience entry point for repository validation."""
from pathlib import Path
from agent_runtime.validation.engine import ValidationEngine


def validate_repository(repository_root: Path):
    return ValidationEngine(repository_root).validate()
