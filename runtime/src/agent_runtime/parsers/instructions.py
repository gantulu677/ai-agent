"""Parse supported instruction formats into content and metadata."""
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class ParsedInstruction:
    content: Any
    metadata: dict[str, Any]
    format: str


def parse_instruction(path: Path) -> ParsedInstruction:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".md":
        metadata: dict[str, Any] = {}
        body = text
        match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, flags=re.DOTALL)
        if match:
            parsed = yaml.safe_load(match.group(1)) or {}
            if not isinstance(parsed, dict):
                raise ValueError("Markdown frontmatter must be a YAML object")
            metadata = parsed
            body = text[match.end():]
        return ParsedInstruction(body, metadata, "markdown")
    if suffix == ".txt":
        return ParsedInstruction(text, {}, "text")
    if suffix == ".json":
        return ParsedInstruction(json.loads(text), {}, "json")
    if suffix == ".yaml":
        return ParsedInstruction(yaml.safe_load(text), {}, "yaml")
    raise ValueError(f"Unsupported instruction format: {suffix}")
