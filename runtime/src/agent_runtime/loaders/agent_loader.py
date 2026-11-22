"""Load an agent's configuration and instructions."""
import json
from pathlib import Path

from agent_runtime.loaders.instruction_loader import LoadedInstruction, load_instructions
from agent_runtime.models import AgentConfig


@dataclass(frozen=True, slots=True)
class LoadedAgent:
    config: AgentConfig
    directory: Path
    instructions: tuple[LoadedInstruction, ...]


def load_agent(agent_directory: Path) -> LoadedAgent:
    config_path = agent_directory / "agent.json"
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("agent.json root must be an object")
    config = AgentConfig.from_mapping(raw)
    configured = raw.get("instruction_category_order")
    if configured is not None and (not isinstance(configured, list) or not all(isinstance(x, str) for x in configured)):
        raise ValueError("instruction_category_order must be an array of strings")
    return LoadedAgent(config, agent_directory, tuple(load_instructions(agent_directory, configured)))
