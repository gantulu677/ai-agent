"""Small in-memory file cache with stat-based invalidation."""
from pathlib import Path
from typing import Callable, TypeVar, Any

T = TypeVar("T")


class FileCache:
    def __init__(self) -> None:
        self._entries: dict[str, tuple[int, int, Any]] = {}

    def get_or_load(self, path: Path, loader: Callable[[Path], T]) -> T:
        stat = path.stat()
        key = str(path.resolve())
        fingerprint = (stat.st_mtime_ns, stat.st_size)
        cached = self._entries.get(key)
        if cached and cached[:2] == fingerprint:
            return cached[2]
        value = loader(path)
        self._entries[key] = (fingerprint[0], fingerprint[1], value)
        return value

    def clear(self) -> None:
        self._entries.clear()
