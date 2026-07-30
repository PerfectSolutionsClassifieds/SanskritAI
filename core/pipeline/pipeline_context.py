from __future__ import annotations

"""
SanskritAI
==========

Core Pipeline Context

Defines the generic immutable context supplied to every
Pipeline execution.

Unlike the domain-specific pipeline contexts (for example,
DerivationPipelineContext), this class contains only
pipeline-level execution metadata and therefore can be reused
by every kernel within SanskritAI.

Hierarchy
---------

PipelineContext
        │
        ▼
Pipeline
        │
        ▼
PipelineResult

Domain-specific contexts should inherit from this class.

Examples
--------

DerivationPipelineContext

SemanticPipelineContext

VakyaPipelineContext

ChandasPipelineContext

AlankaraPipelineContext

KnowledgeGraphPipelineContext

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PipelineContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Generic immutable execution context for every pipeline.
    """

    identifier: str

    subject: Any = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    source: str = "Unknown"

    language: str = "Sanskrit"

    script: str = "Devanagari"

    user_data: dict[str, Any] = field(
        default_factory=dict,
    )

    # -----------------------------------------------------
    # Display
    # -----------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Context"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Generic immutable execution context for a "
            "Pipeline."
        )

    # -----------------------------------------------------
    # Metadata helpers
    # -----------------------------------------------------

    @property
    def has_subject(self) -> bool:
        return self.subject is not None

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    @property
    def metadata_count(self) -> int:
        return len(self.metadata)

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Returns a metadata value.
        """
        return self.metadata.get(
            key,
            default,
        )

    def has(
        self,
        key: str,
    ) -> bool:
        """
        Returns True if metadata contains the key.
        """
        return key in self.metadata

    def __str__(self) -> str:
        return self.display_text
