from __future__ import annotations

"""
SanskritAI
==========

Lifecycle

Defines the immutable lifecycle of a runtime component.

A Lifecycle encapsulates runtime state semantics but owns
no executable behavior.

Architecture
------------

RuntimeState
      │
      ▼
Lifecycle
      │
      ▼
Component

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.runtime_state import RuntimeState
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Lifecycle(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable lifecycle description.
    """

    state: RuntimeState = RuntimeState.CREATED

    @property
    def identifier(self) -> str:
        return self.state.identifier

    @property
    def display_name(self) -> str:
        return self.state.display_name

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            f"Lifecycle currently in "
            f"{self.state.display_name} state."
        )

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the lifecycle is active.
        """
        return self.state.is_active

    @property
    def is_terminal(self) -> bool:
        """
        Indicates whether the lifecycle has reached
        a terminal state.
        """
        return self.state.is_terminal

    def transition_to(
        self,
        state: RuntimeState,
    ) -> "Lifecycle":
        """
        Returns a new lifecycle in the supplied state.
        """
        return Lifecycle(state=state)

    def __str__(self) -> str:
        return self.display_text
