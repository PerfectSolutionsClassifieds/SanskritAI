from __future__ import annotations

"""
SanskritAI
==========

Section

Represents a canonical section within a document.

Examples
--------

Mahabharata
    └── Adi Parva
            └── Sambhava Parva

Rigveda
    └── Mandala
            └── Sukta

Ramayana
    └── Kanda
            └── Sarga

A Section is a container of Verses.

Version
-------
v0.3.0
"""

from typing import TYPE_CHECKING

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)
from SanskritAI.corpus.models.section_metadata import (
    SectionMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.verse import Verse


class Section(
    ContainerNode[
        str,
        SectionMetadata,
        "Verse",
    ]
):
    """
    Canonical section.

    A Section belongs to a Document and contains one or more
    Verses.
    """

    def __init__(
        self,
        identifier: str,
        metadata: SectionMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def verses(self):
        """
        Alias for children.
        """

        return self.children

    # ---------------------------------------------------------

    def add_verse(
        self,
        verse: "Verse",
    ) -> None:
        """
        Add a verse.
        """

        self.add_child(verse)

    # ---------------------------------------------------------

    def remove_verse(
        self,
        verse: "Verse",
    ) -> None:
        """
        Remove a verse.
        """

        self.remove_child(verse)

    # ---------------------------------------------------------

    @property
    def verse_count(
        self,
    ) -> int:
        """
        Number of verses.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_verse(
        self,
    ) -> "Verse | None":
        """
        Return the first verse.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_verse(
        self,
    ) -> "Verse | None":
        """
        Return the last verse.
        """

        return self.last_child
