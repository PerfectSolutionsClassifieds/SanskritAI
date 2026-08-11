from __future__ import annotations

"""
SanskritAI
==========

Reader Result

Immutable aggregate of the linguistic knowledge resolved for a
ReaderPosition.

ReaderResult is the bridge between the Reader Domain and the
Resolution Domain.

Hierarchy
---------

ReaderPosition
      │
      ▼
ReaderResult
      │
      ├── LexicalResolutionResult
      ├── MorphologicalResolutionResult
      ├── SandhiResolutionResult
      ├── SamasaResolutionResult
      └── SemanticResolutionResult

Future Extensions
-----------------

• pragmatics
• commentary
• cross references
• canonical sources
• translation
• metadata

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable aggregate of Reader-level linguistic results.
    """

    identifier: str

    position: ReaderPosition

    subject: Any

    lexical_result: Any = None

    morphology_result: Any = None

    sandhi_result: Any = None

    samasa_result: Any = None

    semantic_result: Any = None

    pragmatics: Any = None

    commentary: Any = None

    cross_references: tuple[Any, ...] = field(
        default_factory=tuple,
    )

    canonical_sources: tuple[Any, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Result"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return (
            "Immutable aggregate of linguistic knowledge "
            "resolved for a Reader position."
        )

    # ---------------------------------------------------------
    # Resolution Availability
    # ---------------------------------------------------------

    @property
    def lexical_available(self) -> bool:
        return self.lexical_result is not None

    @property
    def morphology_available(self) -> bool:
        return self.morphology_result is not None

    @property
    def sandhi_available(self) -> bool:
        return self.sandhi_result is not None

    @property
    def samasa_available(self) -> bool:
        return self.samasa_result is not None

    @property
    def semantic_available(self) -> bool:
        return self.semantic_result is not None

    @property
    def pragmatics_available(self) -> bool:
        return self.pragmatics is not None

    @property
    def commentary_available(self) -> bool:
        return self.commentary is not None

    # ---------------------------------------------------------
    # Completion
    # ---------------------------------------------------------

    @property
    def completed_stage_count(self) -> int:
        return sum(
            (
                self.lexical_available,
                self.morphology_available,
                self.sandhi_available,
                self.samasa_available,
                self.semantic_available,
                self.pragmatics_available,
                self.commentary_available,
            )
        )

    @property
    def total_stage_count(self) -> int:
        return 7

    @property
    def completion_ratio(self) -> float:
        return (
            self.completed_stage_count
            / self.total_stage_count
        )

    @property
    def is_complete(self) -> bool:
        return (
            self.completed_stage_count
            == self.total_stage_count
        )

    # ---------------------------------------------------------
    # Cross References
    # ---------------------------------------------------------

    @property
    def has_cross_references(self) -> bool:
        return bool(self.cross_references)

    @property
    def cross_reference_count(self) -> int:
        return len(
            self.cross_references
        )

    # ---------------------------------------------------------
    # Canonical Sources
    # ---------------------------------------------------------

    @property
    def has_canonical_sources(self) -> bool:
        return bool(self.canonical_sources)

    @property
    def canonical_source_count(self) -> int:
        return len(
            self.canonical_sources
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
