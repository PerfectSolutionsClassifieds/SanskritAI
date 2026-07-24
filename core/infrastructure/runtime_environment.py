from __future__ import annotations

"""
SanskritAI
==========

Runtime Environment

Defines the immutable execution environment for SanskritAI.

Architecture
------------

RuntimeContext
        │
Lifecycle
        │
        ▼
RuntimeEnvironment

Version
-------
v0.7.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.infrastructure.lifecycle import Lifecycle
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
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

    lifecycle: Lifecycle = field(
        default_factory=Lifecycle,
    )

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
            f"({self.lifecycle.display_name})"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable runtime execution environment."
        )

    @property
    def is_running(self) -> bool:
        return self.lifecycle.is_active

    @property
    def is_terminal(self) -> bool:
        return self.lifecycle.is_terminal

    def transition_to(
        self,
        state,
    ) -> "RuntimeEnvironment":
        """
        Returns a new environment with the supplied
        lifecycle state.
        """
        return RuntimeEnvironment(
            context=self.context,
            lifecycle=self.lifecycle.transition_to(state),
        )

    def __str__(self) -> str:
        return self.display_text
