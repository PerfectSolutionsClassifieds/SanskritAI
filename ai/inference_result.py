from __future__ import annotations

"""
SanskritAI
==========

Inference Result

Defines the immutable outcome of one AI inference session.

Architecture
------------

InferenceContext
      │
      ▼
InferenceResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.ai.ai_response import AIResponse
from SanskritAI.ai.inference_context import InferenceContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class InferenceResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable inference result.
    """

    context: InferenceContext

    response: AIResponse

    succeeded: bool

    message: str = ""

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def request(self):
        return self.context.request

    @property
    def model(self):
        return self.context.model

    @property
    def display_name(self) -> str:
        return (
            f"{self.model.display_name} Result"
        )

    @property
    def display_text(self) -> str:
        status = (
            "Succeeded"
            if self.succeeded
            else "Failed"
        )

        return (
            f"{self.model.display_name}"
            f" [{status}]"
        )

    @property
    def display_description(self) -> str:
        return self.message

    @property
    def is_success(self) -> bool:
        return self.succeeded

    @property
    def is_failure(self) -> bool:
        return not self.succeeded

    @property
    def content(self) -> str:
        return self.response.content

    def __str__(self) -> str:
        return self.display_text
