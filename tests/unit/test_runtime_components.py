import asyncio
from pathlib import Path

from agent_runtime.cache.manager import FileCache
from agent_runtime.execution.context import AgentContext
from agent_runtime.execution.session import AgentSession
from agent_runtime.execution.orchestrator import AgentOrchestrator
from agent_runtime.loaders.agent_loader import LoadedAgent
from agent_runtime.models import AgentConfig
from agent_runtime.tools.executor import ToolExecutor


class FakeProvider:
    async def generate(self, *, messages, model=None, **options):
        return "ok"


def test_file_cache_invalidates_after_file_change(tmp_path: Path):
    path = tmp_path / "x.txt"
    path.write_text("a")
    cache = FileCache()
    assert cache.get_or_load(path, lambda p: p.read_text()) == "a"
    path.write_text("longer")
    assert cache.get_or_load(path, lambda p: p.read_text()) == "longer"


def test_tool_executor_requires_explicit_registration():
    executor = ToolExecutor()
    executor.register("sum", lambda a, b: a + b)
    assert asyncio.run(executor.execute("sum", a=2, b=3)) == 5


def test_orchestrator_uses_isolated_session():
    agent = LoadedAgent(AgentConfig("alpha", "1.0.0"), Path("."), ())
    context = AgentContext(agent)
    session = AgentSession("alpha")
    assert asyncio.run(AgentOrchestrator(FakeProvider()).run(context, session, "hello")) == "ok"
    assert session.history[-1] == {"role": "assistant", "content": "ok"}
