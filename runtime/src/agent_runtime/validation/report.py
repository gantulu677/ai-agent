"""Validation report data structures and serialization."""
from dataclasses import asdict, dataclass
from enum import StrEnum
import json
from pathlib import Path


class Severity(StrEnum):
    CRITICAL = "Critical"
    WARNING = "Warning"
    INFO = "Info"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    path: str | None = None
    agent_id: str | None = None


@dataclass(slots=True)
class ValidationReport:
    issues: list[ValidationIssue]

    @property
    def has_critical(self) -> bool:
        return any(issue.severity == Severity.CRITICAL for issue in self.issues)

    def to_dict(self) -> dict:
        return {
            "valid": not self.has_critical,
            "issues": [
                {**asdict(issue), "severity": issue.severity.value}
                for issue in self.issues
            ],
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        lines = [
            "# Validation Report", "",
            f"**Status:** {'Invalid' if self.has_critical else 'No critical errors'}", "",
            "| Severity | Code | Agent | Path | Message |",
            "|---|---|---|---|---|",
        ]
        for item in self.issues:
            cells = [item.severity.value, item.code, item.agent_id or "-", item.path or "-", item.message]
            lines.append("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in cells) + " |")
        if not self.issues:
            lines.append("| Info | NO_ISSUES | - | - | No validation issues found. |")
        return "\n".join(lines) + "\n"

    def write(self, directory: Path) -> tuple[Path, Path]:
        directory.mkdir(parents=True, exist_ok=True)
        json_path = directory / "validation-report.json"
        markdown_path = directory / "validation-report.md"
        json_path.write_text(self.to_json() + "\n", encoding="utf-8")
        markdown_path.write_text(self.to_markdown(), encoding="utf-8")
        return json_path, markdown_path
