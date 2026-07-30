from __future__ import annotations

"""
SanskritAI
==========

Knowledge Graph Context

Defines the canonical context for graph construction.

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
class KnowledgeGraphContext(
    ValueObject,
    Immutable,
    Displayable,
):
    identifier: str

    subject: Any

    source: str = ""

    language: str = "Sanskrit"

    script: str = "Devanagari"

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Knowledge Graph Context"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return "Canonical context for knowledge graph construction."

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return self.display_text
