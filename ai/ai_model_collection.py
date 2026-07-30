from __future__ import annotations

"""
SanskritAI
==========

AI Model Collection

Immutable collection of AIModel objects.

Architecture
------------

AIModel
    │
    ▼
AIModelCollection
    │
    ▼
AIProvider
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.ai.ai_model import AIModel
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIModelCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of AI models.
    """

    models: frozenset[AIModel] = field(
        default_factory=frozenset,
    )

    @property
    def display_name(self) -> str:
        return "AI Models"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return f"{len(self.models)} model(s)"

    @property
    def size(self) -> int:
        return len(self.models)

    @property
    def is_empty(self) -> bool:
        return len(self.models) == 0

    def contains(
        self,
        model: AIModel,
    ) -> bool:
        return model in self.models

    def add(
        self,
        model: AIModel,
    ) -> "AIModelCollection":
        return AIModelCollection(
            models=self.models | {model},
        )

    def __iter__(self) -> Iterator[AIModel]:
        return iter(self.models)

    def __len__(self) -> int:
        return len(self.models)

    def __str__(self) -> str:
        return self.display_text
