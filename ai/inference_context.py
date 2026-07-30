from __future__ import annotations

"""
SanskritAI
==========

Inference Context

Defines the immutable runtime context for a single AI
inference session.

InferenceContext bridges the declarative AI request and the
runtime inference engine.

Architecture
------------

AIRequest
      │
      ▼
InferenceContext
      │
      ▼
InferenceResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from SanskritAI.ai.ai_request import AIRequest
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class InferenceContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable inference context.
    """

    runtime: RuntimeContext

    request: AIRequest

    inference_id: UUID = field(
        default_factory=uuid4,
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def identifier(self) -> str:
        return str(self.inference_id)

    @property
    def model(self):
        return self.request.model

    @property
    def prompt(self) -> str:
        return self.request.prompt

    @property
    def parameters(self):
        return self.request.parameters

    @property
    def display_name(self) -> str:
        return "Inference Context"

    @property
    def display_text(self) -> str:
        return (
            f"{self.model.display_name}"
            " Inference"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable AI inference session."
        )

    def __str__(self) -> str:
        return self.display_text
