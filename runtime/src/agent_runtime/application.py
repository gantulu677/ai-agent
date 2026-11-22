"""Application-level information for the initial runtime CLI."""

from dataclasses import dataclass

from agent_runtime import __version__


@dataclass(frozen=True, slots=True)
class RuntimeInfo:
    name: str
    version: str
    implementation_phase: str
    implemented_capabilities: tuple[str, ...]


class RuntimeApplication:
    """Expose runtime metadata without starting agent discovery or execution."""

    def get_info(self) -> RuntimeInfo:
        return RuntimeInfo(
            name="AI Agent Runtime",
            version=__version__,
            implementation_phase="Phase 1 - Runtime Foundation",
            implemented_capabilities=(
                "Python package foundation",
                "Agent and skill configuration data models",
                "Basic command-line interface",
            ),
        )
