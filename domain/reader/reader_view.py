from __future__ import annotations

"""
SanskritAI
==========

Reader View

Abstract immutable base class for every Reader-facing object.

ReaderView is the canonical presentation-layer value object
that bridges the Corpus Domain and the Reader Domain.

Hierarchy
---------

ReaderView
    │
    ├── ReaderDocument
    ├── ChapterView
    ├── SlokaView
    └── WordView

Responsibilities
----------------

• Canonical identifier

• Canonical ReaderPosition

• Display metadata

• Immutable reader object

ReaderView intentionally contains no linguistic analysis.

Analysis is delegated to the Resolution Kernel.

Version
-------
v1.0.0
"""

from abc import ABC
from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import (
    ValueObject,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderView(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Abstract immutable Reader object.
    """

    identifier: str

    position: ReaderPosition

    title: str = ""

    metadata: dict[str, Any] | None = None

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        """
        Subclasses should override when appropriate.
        """
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        """
        Human-readable label.
        """
        return self.title or self.identifier

    @property
    def display_description(self) -> str:
        """
        Generic description.
        """
        return (
            "Immutable Reader Domain object."
        )

    # ---------------------------------------------------------
    # Position helpers
    # ---------------------------------------------------------

    @property
    def corpus_id(self) -> str:
        return self.position.corpus_id

    @property
    def purana_id(self) -> str:
        return self.position.purana_id

    @property
    def chapter_id(self) -> str:
        return self.position.chapter_id

    @property
    def sloka_id(self) -> str | None:
        return self.position.sloka_id

    @property
    def word_id(self) -> str | None:
        return self.position.word_id

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
        """
        Retrieves metadata value.
        """

        if self.metadata is None:
            return default

        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
