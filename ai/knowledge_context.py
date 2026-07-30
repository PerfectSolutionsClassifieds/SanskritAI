from __future__ import annotations

"""
SanskritAI
==========

Knowledge Context

Defines the immutable knowledge context supplied to a
reasoning session.

A KnowledgeContext represents the curated knowledge available
to a Reasoner or Agent.

It aggregates immutable memory items without prescribing how
they are retrieved or stored.

Architecture
------------

Memory
    │
    ▼
KnowledgeContext
    │
    ▼
Reasoner
    │
    ▼
Agent

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.ai.memory import Memory
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class KnowledgeContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable knowledge context.

    Represents the curated knowledge supplied to one
    reasoning or agent session.
    """

    memory: Memory

    @property
    def identifier(self) -> str:
        return self.memory.identifier

    @property
    def display_name(self) -> str:
        return "Knowledge Context"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            f"{self.memory.item_count} knowledge item(s)"
        )

    @property
    def item_count(self) -> int:
        return self.memory.item_count

    @property
    def is_empty(self) -> bool:
        return self.memory.is_empty

    @property
    def has_items(self) -> bool:
        return self.memory.has_items

    @property
    def items(self) -> tuple[object, ...]:
        return self.memory.items

    def __iter__(self):
        return iter(self.memory)

    def __len__(self) -> int:
        return len(self.memory)

    def __str__(self) -> str:
        return self.display_text
