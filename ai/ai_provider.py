from __future__ import annotations

"""
SanskritAI
==========

AI Provider

Represents an immutable AI provider.

Owns metadata and the collection of models.

Networking, authentication and inference are implemented
by provider-specific infrastructure.
"""

from dataclasses import dataclass

from SanskritAI.ai.ai_model_collection import AIModelCollection
from SanskritAI.ai.ai_provider_metadata import AIProviderMetadata
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIProvider(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable AI provider.
    """

    metadata: AIProviderMetadata

    models: AIModelCollection

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
    def organization(self) -> str:
        return self.metadata.organization

    @property
    def website(self) -> str:
        return self.metadata.website

    @property
    def capability_count(self) -> int:
        return self.metadata.capability_count

    @property
    def model_count(self) -> int:
        return self.models.size

    def supports(
        self,
        capability: str,
    ) -> bool:
        return self.metadata.supports(capability)

    def __str__(self) -> str:
        return self.display_text
