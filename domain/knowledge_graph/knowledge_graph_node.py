from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Node

Represents one node in the Knowledge Graph layer.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class KnowledgeGraphNode(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable knowledge graph node.
    """

    identifier: str

    label: str

    node_type: str = ""

    description: str = ""

    payload: dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    @property
    def display_name(self) -> str:
        return self.label

    @property
    def display_text(self) -> str:
        return self.label

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_payload(self) -> bool:
        return bool(self.payload)

    def __str__(self) -> str:
        return self.display_text
