import asyncio
import json
from pathlib import Path

import pytest

from agent_runtime.dependencies import inspect_dependencies
from agent_runtime.loaders.skill_loader import load_skill
from agent_runtime.models import AgentConfig
from agent_runtime.execution.context import AgentContext
from agent_runtime.execution.session import AgentSession
from agent_runtime.execution.orchestrator import AgentOrchestrator
from agent_runtime.loaders.agent_loader import LoadedAgent
from agent_runtime.tools.executor import ToolExecutor


class RecordingProvider:
    async def generate(self, *, messages, model=None, **options):
        await asyncio.sleep(0)
        return messages[-1]["content"].upper()


def test_skill_loader_loads_metadata_instructions_and_resources(tmp_path: Path):
    skill = tmp_path / "skill"
    (skill / "references").mkdir(parents=True)
    (skill / "skill.json").write_text(json.dumps({
        "id": "demo-skill", "name": "Demo", "description": "Example", "version": "1.0.0",
        "dependencies": [{"name": "requests", "type": "python"}],
    }))
    (skill / "SKILL.md").write_text("Do the task.")
    loaded = load_skill(skill)
    assert loaded.config.id == "demo-skill"
    assert loaded.instructions == "Do the task."
    assert [p.name for p in loaded.resources] == ["references"]


def test_dependency_inspection_never_installs_packages():
    statuses = inspect_dependencies([{"name": "requests", "type": "python"}])
    assert statuses[0].name == "requests"
    assert "no installation" in statuses[0].detail.lower()


def test_tool_executor_rejects_unregistered_tools():
    executor = ToolExecutor()
    with pytest.raises(KeyError):
        asyncio.run(executor.execute("not-registered"))


def test_orchestrator_can_run_independent_sessions_concurrently():
    provider = RecordingProvider()
    orchestrator = AgentOrchestrator(provider)
    contexts = []
    tasks = []
    for agent_id, prompt in [("agent-one", "first"), ("agent-two", "second")]:
        loaded = LoadedAgent(AgentConfig(agent_id, "1.0.0"), Path("."), ())
        context = AgentContext(loaded)
        session = AgentSession(agent_id)
        contexts.append(context)
        tasks.append((context, session, prompt))
    results = asyncio.run(orchestrator.run_many(tasks))
    assert results == ["FIRST", "SECOND"]
    assert tasks[0][1].agent_id != tasks[1][1].agent_id
