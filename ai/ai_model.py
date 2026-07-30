from __future__ import annotations

"""
SanskritAI
==========

AI Model

Defines an immutable AI model.

AIModel represents a concrete language model and owns only
its semantic identity and metadata.

Execution, inference, networking, authentication, and model
hosting belong to AIProvider.

Architecture
------------

AIModelMetadata
        │
        ▼
AIModel
        │
        ▼
AIProvider

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.ai.ai_model_metadata import AIModelMetadata
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIModel(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable AI model.
    """

    metadata: AIModelMetadata

    @property
    def identifier(self) -> str:
        return self.metadata.identifier

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    @property
    def provider(self) -> str:
        return self.metadata.provider

    @property
    def family(self) -> str:
        return self.metadata.family

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def capabilities(self) -> frozenset[str]:
        return self.metadata.capabilities

    @property
    def capability_count(self) -> int:
        return self.metadata.capability_count

    @property
    def has_capabilities(self) -> bool:
        return self.metadata.has_capabilities

    def supports(
        self,
        capability: str,
    ) -> bool:
        """
        Determines whether the model advertises the supplied
        capability.
        """
        return self.metadata.supports(capability)

    def __str__(self) -> str:
        return self.display_text
