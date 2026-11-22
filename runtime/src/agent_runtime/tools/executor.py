"""Tool registry; discovered skill scripts are never executed implicitly."""
import asyncio
import inspect
from collections.abc import Callable
from typing import Any


class ToolExecutor:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        if not name or name in self._tools:
            raise ValueError(f"Tool name is empty or already registered: {name!r}")
        self._tools[name] = function

    async def execute(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool is not registered: {name}")
        function = self._tools[name]
        if inspect.iscoroutinefunction(function):
            return await function(**kwargs)
        result = await asyncio.to_thread(function, **kwargs)
        return await result if inspect.isawaitable(result) else result
