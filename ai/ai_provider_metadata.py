from __future__ import annotations

"""
SanskritAI
==========

AI Provider Metadata

Defines the immutable descriptive metadata of an AI provider.

An AIProviderMetadata describes the provider organization,
independent of any runtime implementation or networking.

Execution, authentication, inference, and model hosting
belong to AIProvider.

Architecture
------------

AIProviderMetadata
        │
        ▼
AIProvider

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIProviderMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing an AI provider.
    """

    identifier: str

    name: str

    organization: str = ""

    website: str = ""

    description: str = ""

    capabilities: frozenset[str] = field(
        default_factory=frozenset,
    )

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_organization(self) -> bool:
        return bool(self.organization)

    @property
    def has_website(self) -> bool:
        return bool(self.website)

    @property
    def capability_count(self) -> int:
        return len(self.capabilities)

    @property
    def has_capabilities(self) -> bool:
        return bool(self.capabilities)

    def supports(
        self,
        capability: str,
    ) -> bool:
        """
        Determines whether this provider advertises the supplied
        capability.
        """
        return capability in self.capabilities

    def __str__(self) -> str:
        return self.display_text
