from __future__ import annotations

"""
SanskritAI
==========

AI Response

Provider-neutral immutable inference response.
"""

from dataclasses import dataclass

from SanskritAI.ai.ai_request import AIRequest
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIResponse(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable AI response.
    """

    request: AIRequest

    content: str

    succeeded: bool

    message: str = ""

    @property
    def identifier(self) -> str:
        return self.request.identifier

    @property
    def display_name(self) -> str:
        return "AI Response"

    @property
    def display_text(self) -> str:
        status = "Succeeded" if self.succeeded else "Failed"
        return f"AI Response [{status}]"

    @property
    def display_description(self) -> str:
        return self.message

    @property
    def model(self):
        return self.request.model

    @property
    def prompt(self) -> str:
        return self.request.prompt

    @property
    def is_success(self) -> bool:
        return self.succeeded

    @property
    def is_failure(self) -> bool:
        return not self.succeeded

    def __str__(self) -> str:
        return self.display_text
