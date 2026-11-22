"""Async orchestration over an injected LLM provider."""
import asyncio
from collections.abc import Sequence

from agent_runtime.execution.context import AgentContext
from agent_runtime.execution.session import AgentSession
from agent_runtime.providers.base import LLMProvider


class AgentOrchestrator:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, context: AgentContext, session: AgentSession, user_input: str, *, model: str | None = None) -> str:
        if session.agent_id != context.agent.config.id:
            raise ValueError("Session agent ID does not match execution context")
        if not session.history:
            for instruction in context.agent.instructions:
                if isinstance(instruction.content, str) and instruction.content.strip():
                    session.add_message("system", instruction.content)
        session.add_message("user", user_input)
        response = await self.provider.generate(messages=list(session.history), model=model)
        session.add_message("assistant", response)
        return response

    async def run_many(
        self,
        tasks: Sequence[tuple[AgentContext, AgentSession, str]],
        *,
        model: str | None = None,
    ) -> list[str]:
        """Run independent agent sessions concurrently; each retains its own context."""
        return list(await asyncio.gather(*(
            self.run(context, session, prompt, model=model)
            for context, session, prompt in tasks
        )))
