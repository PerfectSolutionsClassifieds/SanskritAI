from __future__ import annotations

"""
SanskritAI
==========

Verse

Canonical textual unit within the SanskritAI Corpus Model.

A Verse represents the primary textual unit contained within a
Section.

Examples
--------
• Śloka
• Mantra
• Ṛc
• Sūtra
• Stanza

A Verse contains one or more Paragraph objects, allowing the same
model to represent poetry, prose, translations, commentaries and
parallel editions.

Version
-------
v0.2.0
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator

from SanskritAI.common.identifiers.verse_id import VerseId

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.corpus.models.verse_metadata import (
    VerseMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.paragraph import Paragraph


@dataclass(slots=True)
class Verse(
    ContainerNode[
        VerseId,
        VerseMetadata,
    ]
):
    """
    Canonical Verse node.
    """

    id: VerseId

    metadata: VerseMetadata = field(
        default_factory=VerseMetadata
    )

    paragraphs: list["Paragraph"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Paragraph Management
    # ---------------------------------------------------------

    def add_paragraph(
        self,
        paragraph: "Paragraph",
    ) -> None:
        """
        Add a paragraph to the verse.
        """

        self._add_to_collection(
            self.paragraphs,
            paragraph,
        )

    # ---------------------------------------------------------

    def remove_paragraph(
        self,
        paragraph: "Paragraph",
    ) -> None:
        """
        Remove a paragraph from the verse.
        """

        self._remove_from_collection(
            self.paragraphs,
            paragraph,
        )

    # ---------------------------------------------------------

    def clear_paragraphs(
        self,
    ) -> None:
        """
        Remove all paragraphs.
        """

        self._clear_collection(
            self.paragraphs,
        )

    # ---------------------------------------------------------
    # Collection Helpers
    # ---------------------------------------------------------

    @property
    def paragraph_count(self) -> int:
        """
        Number of paragraphs in the verse.
        """

        return self._collection_size(
            self.paragraphs,
        )

    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.paragraph_count

    # ---------------------------------------------------------

    def __iter__(self) -> Iterator["Paragraph"]:
        return self._collection_iter(
            self.paragraphs,
        )

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> "Paragraph":
        return self._collection_get(
            self.paragraphs,
            index,
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the verse.
        """

        data = super().to_dict()

        data["paragraphs"] = [

            paragraph.to_dict()

            for paragraph in self.paragraphs

        ]

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Verse("

            f"number={self.metadata.verse_number!r}, "

            f"type={self.metadata.verse_type.value!r}, "

            f"paragraphs={self.paragraph_count})"

        )
