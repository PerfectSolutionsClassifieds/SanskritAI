from __future__ import annotations

"""
SanskritAI
==========

AI Request

Provider-neutral immutable inference request.
"""

from dataclasses import dataclass, field

from SanskritAI.ai.ai_model import AIModel
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIRequest(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable AI inference request.
    """

    model: AIModel

    prompt: str

    parameters: frozenset[tuple[str, object]] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        return self.model.identifier

    @property
    def display_name(self) -> str:
        return "AI Request"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.model.display_name

    def parameter(
        self,
        name: str,
        default=None,
    ):
        params = dict(self.parameters)
        return params.get(name, default)

    def __str__(self) -> str:
        return self.display_text
