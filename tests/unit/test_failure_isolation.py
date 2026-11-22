import asyncio
from pathlib import Path

from agent_runtime.execution.context import AgentContext
from agent_runtime.execution.orchestrator import AgentOrchestrator
from agent_runtime.execution.session import AgentSession
from agent_runtime.loaders.agent_loader import LoadedAgent
from agent_runtime.models import AgentConfig


class PartlyFailingProvider:
    async def generate(self, *, messages, model=None, **options):
        value = messages[-1]["content"]
        if value == "fail":
            raise RuntimeError("simulated provider failure")
        return "success"


def test_one_agent_failure_does_not_cancel_other_agent_tasks():
    orchestrator = AgentOrchestrator(PartlyFailingProvider())
    tasks = []
    for agent_id, prompt in [("agent-a", "fail"), ("agent-b", "continue")]:
        loaded = LoadedAgent(AgentConfig(agent_id, "1.0.0"), Path("."), ())
        tasks.append((AgentContext(loaded), AgentSession(agent_id), prompt))
    results = asyncio.run(orchestrator.run_many(tasks))
    assert isinstance(results[0], RuntimeError)
    assert results[1] == "success"
