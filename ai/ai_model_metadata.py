from __future__ import annotations

"""
SanskritAI
==========

AI Model Metadata

Defines the immutable descriptive metadata of an AI model.

AIModelMetadata describes *what* an AI model is rather than
*how* it is executed.

Execution, inference, configuration, and provider-specific
behavior belong to higher layers.

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

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AIModelMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing an AI model.
    """

    identifier: str

    name: str

    provider: str

    family: str = ""

    version: str = ""

    description: str = ""

    capabilities: frozenset[str] = field(
        default_factory=frozenset,
    )

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        if self.version:
            return f"{self.name} ({self.version})"
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_family(self) -> bool:
        return bool(self.family)

    @property
    def has_version(self) -> bool:
        return bool(self.version)

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
        Determines whether the model advertises the supplied
        capability.
        """
        return capability in self.capabilities

    def __str__(self) -> str:
        return self.display_text
