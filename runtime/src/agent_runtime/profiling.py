"""Lightweight timing helpers for measuring runtime stages."""
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Iterator


@dataclass(frozen=True, slots=True)
class TimingResult:
    operation: str
    elapsed_seconds: float


@contextmanager
def measure(operation: str, sink=None) -> Iterator[dict[str, float]]:
    """Measure a synchronous block; optionally send the result to sink(result)."""
    started = perf_counter()
    result: dict[str, float] = {}
    try:
        yield result
    finally:
        timing = TimingResult(operation, perf_counter() - started)
        result["elapsed_seconds"] = timing.elapsed_seconds
        if sink is not None:
            sink(timing)
