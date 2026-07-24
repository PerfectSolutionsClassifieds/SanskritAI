from __future__ import annotations

"""
SanskritAI
==========

Work Metadata

Defines the immutable semantic metadata describing executable
application work.

WorkMetadata is the foundation of the Application Layer.

Every executable unit in SanskritAI—tasks, workflow steps,
pipeline stages, AI operations, dictionary lookups,
grammatical analysis, translation, etc.—shares this metadata.

Architecture
------------

WorkMetadata
      │
      ▼
Work
      │
      ├──────────────┐
      ▼              ▼
Task         WorkflowStep

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.capabilities.capability_set import CapabilitySet
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.version.semantic_version import SemanticVersion
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class WorkMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing executable work.
    """

    identifier: str

    name: str

    version: SemanticVersion

    capabilities: CapabilitySet

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_text
