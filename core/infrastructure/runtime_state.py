from __future__ import annotations

"""
SanskritAI
==========

Runtime State

Defines the canonical lifecycle states of runtime infrastructure
components.

RuntimeState is intentionally generic and reusable across the
Infrastructure kernel.

Typical users include:

- RuntimeEnvironment
- LifecycleManager
- PluginManager
- ResourceLoader
- EventBus
- Pipeline
- Cache
- InfrastructureService

Architecture
------------

RuntimeState
      │
      ▼
RuntimeContext
      │
      ▼
RuntimeEnvironment

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class RuntimeState(Enum):
    """
    Canonical runtime lifecycle states.
    """

    CREATED = "created"

    INITIALIZED = "initialized"

    STARTING = "starting"

    RUNNING = "running"

    PAUSED = "paused"

    STOPPING = "stopping"

    STOPPED = "stopped"

    FAILED = "failed"

    DISPOSED = "disposed"

    @property
    def identifier(self) -> str:
        """
        Canonical identifier.
        """
        return self.value

    @property
    def display_name(self) -> str:
        """
        Human-readable runtime state.
        """
        return self.value.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        """
        Canonical display representation.
        """
        return self.display_name

    @property
    def display_description(self) -> str:
        """
        Brief description.
        """
        return (
            f"{self.display_name} runtime state."
        )

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the runtime is operational.
        """
        return self in (
            RuntimeState.STARTING,
            RuntimeState.RUNNING,
            RuntimeState.PAUSED,
        )

    @property
    def is_terminal(self) -> bool:
        """
        Indicates whether the state is terminal.
        """
        return self in (
            RuntimeState.STOPPED,
            RuntimeState.FAILED,
            RuntimeState.DISPOSED,
        )

    def __str__(self) -> str:
        return self.display_name
