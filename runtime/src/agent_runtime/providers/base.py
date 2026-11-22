"""Provider protocol for pluggable LLM backends."""
from typing import Protocol, Any


class LLMProvider(Protocol):
    async def generate(self, *, messages: list[dict[str, str]], model: str | None = None, **options: Any) -> str:
        """Generate a response from a sequence of role/content messages."""
        ...
