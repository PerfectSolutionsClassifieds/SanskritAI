from __future__ import annotations

"""
SanskritAI
==========

Work

Defines the canonical immutable executable unit within the
Application Layer.

A Work represents *what* is intended to be executed, but
contains no execution behavior itself.

Concrete specializations include:

- Task
- WorkflowStep
- PipelineStage
- AI operations
- Dictionary lookup
- Morphological analysis
- Translation

Execution is performed by the Orchestrator.

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

from SanskritAI.application.work_metadata import WorkMetadata
from SanskritAI.core.capabilities.capability_set import CapabilitySet
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Work(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable executable work definition.
    """

    metadata: WorkMetadata

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
    def version(self):
        return self.metadata.version

    @property
    def capabilities(self) -> CapabilitySet:
        return self.metadata.capabilities

    @property
    def capability_count(self) -> int:
        """
        Number of declared capabilities.
        """
        return len(self.capabilities)

    def supports(
        self,
        capability,
    ) -> bool:
        """
        Determines whether this work supports the supplied
        capability.
        """
        return capability in self.capabilities

    def __str__(self) -> str:
        return self.display_text
