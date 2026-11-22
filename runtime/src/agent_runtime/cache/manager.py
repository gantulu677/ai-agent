"""Small in-memory file cache with stat-based invalidation."""
from pathlib import Path
from typing import Callable, TypeVar, Any

T = TypeVar("T")


class FileCache:
    def __init__(self) -> None:
        self._entries: dict[str, tuple[int, int, int, Any]] = {}

    def get_or_load(self, path: Path, loader: Callable[[Path], T]) -> T:
        stat = path.stat()
        key = str(path.resolve())
        fingerprint = (stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size)
        cached = self._entries.get(key)
        if cached and cached[:3] == fingerprint:
            return cached[3]
        value = loader(path)
        self._entries[key] = (*fingerprint, value)
        return value

    def clear(self) -> None:
        self._entries.clear()
