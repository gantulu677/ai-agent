import json
from pathlib import Path

from agent_runtime.validation.engine import ValidationEngine
from agent_runtime.validation.report import Severity, ValidationReport


def make_repo(root: Path):
    (root / "agents" / "alpha").mkdir(parents=True)
    (root / "schemas").mkdir()
    (root / "agents" / "alpha" / "agent.json").write_text(json.dumps({"id": "alpha", "version": "1.0.0"}))
    (root / "schemas" / "agent.schema.json").write_text(json.dumps({"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":["id","version"],"properties":{"id":{"type":"string","minLength":1},"version":{"type":"string","minLength":1}},"additionalProperties":True}))
    (root / "schemas" / "skill.schema.json").write_text(json.dumps({"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":["id","name","description","version"],"properties":{"id":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"version":{"type":"string"}},"additionalProperties":True}))


def test_valid_repository_has_no_critical_issues(tmp_path: Path):
    make_repo(tmp_path)
    report = ValidationEngine(tmp_path).validate()
    assert not report.has_critical


def test_invalid_agent_id_is_critical(tmp_path: Path):
    make_repo(tmp_path)
    path = tmp_path / "agents" / "alpha" / "agent.json"
    path.write_text(json.dumps({"id": "Alpha Name", "version": "1"}))
    report = ValidationEngine(tmp_path).validate()
    assert any(x.code == "INVALID_AGENT_ID" and x.severity == Severity.CRITICAL for x in report.issues)


def test_report_serializes_json_and_markdown():
    report = ValidationReport([])
    assert '"valid": true' in report.to_json()
    assert "# Validation Report" in report.to_markdown()
