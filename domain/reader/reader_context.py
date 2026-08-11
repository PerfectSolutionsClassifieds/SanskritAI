from __future__ import annotations

"""
SanskritAI
==========

Reader Context

Defines the immutable context supplied to the Reader Engine.

The ReaderContext is the highest-level orchestration context in
SanskritAI. It represents a reader's request to analyze one
linguistic unit (word, sentence, śloka, paragraph, etc.) while
carrying sufficient contextual information for downstream
resolution.

Unlike ResolutionContext, which is consumed by individual
linguistic kernels, ReaderContext represents the complete
reading session.

Hierarchy
---------

ReaderEngine
      │
      ▼
ReaderContext
      │
      ▼
ResolutionPipeline
      │
      ▼
ResolutionContext
      │
      ▼
Lexical
Morphology
Sandhi
Samasa
Semantic

Future Extensions
-----------------

• chapter context

• previous śloka

• next śloka

• commentary selection

• translation preference

• preferred lexicon

• user profile

• AI reasoning preferences

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
class ReaderContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Reader Engine context.
    """

    identifier: str

    subject: Any

    language: str = "sa"

    script: str = "Devanagari"

    source: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Context"

    @property
    def display_text(self) -> str:
        return str(self.subject)

    @property
    def display_description(self) -> str:
        return (
            "Immutable reader context supplied to the "
            "Reader Engine."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_source(self) -> bool:
        return bool(self.source)

    @property
    def has_language(self) -> bool:
        return bool(self.language)

    @property
    def has_script(self) -> bool:
        return bool(self.script)

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves metadata.

        Returns
        -------
        default

            if the key does not exist.
        """

        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
