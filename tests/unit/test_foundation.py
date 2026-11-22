from __future__ import annotations

import pytest

from agent_runtime import __version__
from agent_runtime.cli import main
from agent_runtime.models import AgentConfig, SkillConfig


def test_agent_config_preserves_extension_fields() -> None:
    config = AgentConfig.from_mapping(
        {"id": "sample-agent", "version": "1.0.0", "display_name": "Sample"}
    )
    assert config.id == "sample-agent"
    assert config.version == "1.0.0"
    assert config.extra_fields == {"display_name": "Sample"}


def test_agent_config_requires_non_empty_id() -> None:
    with pytest.raises(ValueError, match="id"):
        AgentConfig.from_mapping({"id": " ", "version": "1.0.0"})


def test_skill_config_reads_required_fields_and_extensions() -> None:
    config = SkillConfig.from_mapping(
        {
            "id": "sample-skill",
            "name": "Sample Skill",
            "description": "A test skill",
            "version": "2.0.0",
            "enabled": True,
        }
    )
    assert config.id == "sample-skill"
    assert config.extra_fields == {"enabled": True}


def test_skill_config_requires_description() -> None:
    with pytest.raises(ValueError, match="description"):
        SkillConfig.from_mapping(
            {"id": "sample-skill", "name": "Sample", "version": "1.0.0"}
        )


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_cli_info(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["info"]) == 0
    output = capsys.readouterr().out
    assert "Phases 1-6" in output
    assert "Automatic agent" in output
