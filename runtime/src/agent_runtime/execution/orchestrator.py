"""Async orchestration over an injected LLM provider."""
import asyncio
import json
import logging
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
                content = instruction.content
                if isinstance(content, str):
                    system_content = content
                else:
                    system_content = json.dumps(content, ensure_ascii=False, indent=2)
                if system_content.strip():
                    session.add_message("system", f"[{instruction.source}]\n{system_content}")
        session.add_message("user", user_input)
        response = await self.provider.generate(messages=list(session.history), model=model)
        session.add_message("assistant", response)
        return response

    async def run_many(
        self,
        tasks: Sequence[tuple[AgentContext, AgentSession, str]],
        *,
        model: str | None = None,
    ) -> list[str | BaseException]:
        """Run independent sessions concurrently and return failures per task."""
        results = await asyncio.gather(
            *(self.run(context, session, prompt, model=model) for context, session, prompt in tasks),
            return_exceptions=True,
        )
        logger = logging.getLogger("agent_runtime.execution")
        for (context, _session, _prompt), result in zip(tasks, results):
            if isinstance(result, BaseException):
                logger.error(
                    "Agent execution failed; other agents remain isolated: %s",
                    context.agent.config.id,
                    exc_info=(type(result), result, result.__traceback__),
                )
        return list(results)
