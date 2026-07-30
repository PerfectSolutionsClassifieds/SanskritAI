from __future__ import annotations

"""
SanskritAI
==========

Reasoning Context

Defines the immutable runtime context supplied to a
Reasoner.

ReasoningContext aggregates all information required for
reasoning while remaining completely immutable.

A Reasoner should never reason directly over a Prompt or
Conversation alone. Instead, it receives a fully prepared
ReasoningContext.

Architecture
------------

Conversation
      │
      ▼
ReasoningContext
      │
      ▼
Reasoner

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from SanskritAI.ai.conversation import Conversation
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ReasoningContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable reasoning context.

    A ReasoningContext encapsulates everything required by a
    reasoning engine to perform one reasoning session.
    """

    runtime: RuntimeContext

    conversation: Conversation

    reasoning_id: UUID = field(
        default_factory=uuid4,
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def identifier(self) -> str:
        return str(self.reasoning_id)

    @property
    def display_name(self) -> str:
        return "Reasoning Context"

    @property
    def display_text(self) -> str:
        return (
            f"{self.conversation.display_name}"
            " Reasoning"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable reasoning session."
        )

    @property
    def prompt_count(self) -> int:
        return self.conversation.prompt_count

    @property
    def is_empty(self) -> bool:
        return self.conversation.is_empty

    @property
    def configuration(self):
        return self.runtime.configuration

    @property
    def services(self):
        return self.runtime.services

    @property
    def plugins(self):
        return self.runtime.plugins

    @property
    def resources(self):
        return self.runtime.resources

    @property
    def events(self):
        return self.runtime.events

    def __str__(self) -> str:
        return self.display_text
