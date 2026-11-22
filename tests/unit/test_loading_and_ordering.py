from pathlib import Path

from agent_runtime.discovery.instructions import discover_instructions
from agent_runtime.loaders.instruction_loader import load_instructions
from agent_runtime.ordering.instructions import category_order, order_instructions
from agent_runtime.parsers.instructions import parse_instruction


def test_frontmatter_priority_overrides_numeric_prefix(tmp_path: Path):
    root = tmp_path / "instructions" / "core"
    root.mkdir(parents=True)
    (root / "99-later.md").write_text("---\npriority: 1\n---\nfirst")
    (root / "20-earlier.md").write_text("second")
    ordered = order_instructions(discover_instructions(tmp_path))
    assert [x.path.name for x in ordered] == ["99-later.md", "20-earlier.md"]


def test_equal_priority_uses_numeric_prefix_then_path(tmp_path: Path):
    root = tmp_path / "instructions" / "core"
    root.mkdir(parents=True)
    (root / "20-b.md").write_text("---\npriority: 3\n---\nb")
    (root / "10-a.md").write_text("---\npriority: 3\n---\na")
    ordered = order_instructions(discover_instructions(tmp_path))
    assert [x.path.name for x in ordered] == ["10-a.md", "20-b.md"]


def test_category_extras_are_sorted_after_configured():
    assert category_order(["zeta", "response", "core", "alpha"]) == ["core", "response", "alpha", "zeta"]


def test_json_instruction_parses_as_structured_data(tmp_path: Path):
    path = tmp_path / "policy.json"
    path.write_text('{"enabled": true}')
    parsed = parse_instruction(path)
    assert parsed.content == {"enabled": True}
    assert parsed.format == "json"


def test_loader_preserves_source_and_metadata(tmp_path: Path):
    root = tmp_path / "instructions" / "core"
    root.mkdir(parents=True)
    (root / "rule.md").write_text("---\npriority: 2\n---\nKeep safe.")
    loaded = load_instructions(tmp_path)
    assert loaded[0].source == "core/rule.md"
    assert loaded[0].metadata["priority"] == 2
