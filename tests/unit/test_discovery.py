from pathlib import Path

from agent_runtime.discovery.agents import discover_agents
from agent_runtime.discovery.instructions import discover_instructions
from agent_runtime.discovery.skills import discover_skills


def test_agent_discovery_only_directories_with_agent_json(tmp_path: Path):
    (tmp_path / "agents" / "alpha").mkdir(parents=True)
    (tmp_path / "agents" / "alpha" / "agent.json").write_text('{"id":"alpha","version":"1"}')
    (tmp_path / "agents" / "nested").mkdir()
    (tmp_path / "agents" / "nested" / "child").mkdir()
    (tmp_path / "agents" / "nested" / "child" / "agent.json").write_text("{}")
    assert [x.directory.name for x in discover_agents(tmp_path)] == ["alpha"]


def test_skill_discovery_is_not_recursive(tmp_path: Path):
    root = tmp_path / "skills"
    (root / "one").mkdir(parents=True)
    (root / "one" / "skill.json").write_text("{}")
    (root / "nested" / "two").mkdir(parents=True)
    (root / "nested" / "two" / "skill.json").write_text("{}")
    assert [x.directory.name for x in discover_skills(tmp_path)] == ["one"]


def test_instruction_discovery_is_recursive_and_filters_extensions(tmp_path: Path):
    root = tmp_path / "instructions" / "core" / "nested"
    root.mkdir(parents=True)
    (root / "10-rule.md").write_text("rule")
    (root / "data.json").write_text("{}")
    (root / "skip.py").write_text("pass")
    found = discover_instructions(tmp_path)
    assert [x.path.name for x in found] == ["10-rule.md", "data.json"]
