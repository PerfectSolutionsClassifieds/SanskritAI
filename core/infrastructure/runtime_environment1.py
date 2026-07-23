from __future__ import annotations

"""
SanskritAI
==========

Runtime Environment

Defines the immutable execution environment for SanskritAI.

A RuntimeEnvironment combines the shared RuntimeContext with
the current RuntimeState.

Architecture
------------

RuntimeContext
        │
RuntimeState
        │
        ▼
RuntimeEnvironment

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.infrastructure.runtime_state import RuntimeState
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class RuntimeEnvironment(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime environment.
    """

    context: RuntimeContext

    state: RuntimeState = RuntimeState.CREATED

    @property
    def identifier(self) -> str:
        return "runtime_environment"

    @property
    def display_name(self) -> str:
        return "Runtime Environment"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"({self.state.display_name})"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable runtime execution environment."
        )

    @property
    def is_running(self) -> bool:
        """
        Indicates whether the environment is active.
        """
        return self.state.is_active

    @property
    def is_terminal(self) -> bool:
        """
        Indicates whether the environment has reached
        a terminal state.
        """
        return self.state.is_terminal

    def __str__(self) -> str:
        return self.display_text
