from __future__ import annotations

"""
SanskritAI
==========

Section

Canonical hierarchical subdivision within a document.

Examples
--------
• Parva
• Kanda
• Skandha
• Mandala
• Adhyaya
• Chapter
• Book
• Part

A Section may contain:

    • nested Sections
    • Verses

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator

from SanskritAI.common.identifiers.section_id import (
    SectionId,
)

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.corpus.models.section_metadata import (
    SectionMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.section import Section
    from SanskritAI.corpus.models.verse import Verse


@dataclass(slots=True)
class Section(
    ContainerNode[
        SectionId,
        SectionMetadata,
    ]
):
    """
    Canonical Section node.
    """

    id: SectionId

    metadata: SectionMetadata = field(
        default_factory=SectionMetadata
    )

    # ---------------------------------------------------------
    # Child Collections
    # ---------------------------------------------------------

    sections: list["Section"] = field(
        default_factory=list
    )

    verses: list["Verse"] = field(
        default_factory=list
    )

    # =========================================================
    # Nested Sections
    # =========================================================

    def add_section(
        self,
        section: "Section",
    ) -> None:

        self._add_to_collection(
            self.sections,
            section,
        )

    # ---------------------------------------------------------

    def remove_section(
        self,
        section: "Section",
    ) -> None:

        self._remove_from_collection(
            self.sections,
            section,
        )

    # ---------------------------------------------------------

    def clear_sections(
        self,
    ) -> None:

        self._clear_collection(
            self.sections,
        )

    # =========================================================
    # Verses
    # =========================================================

    def add_verse(
        self,
        verse: "Verse",
    ) -> None:

        self._add_to_collection(
            self.verses,
            verse,
        )

    # ---------------------------------------------------------

    def remove_verse(
        self,
        verse: "Verse",
    ) -> None:

        self._remove_from_collection(
            self.verses,
            verse,
        )

    # ---------------------------------------------------------

    def clear_verses(
        self,
    ) -> None:

        self._clear_collection(
            self.verses,
        )

    # =========================================================
    # Properties
    # =========================================================

    @property
    def section_count(self) -> int:

        return self._collection_size(
            self.sections,
        )

    # ---------------------------------------------------------

    @property
    def verse_count(self) -> int:

        return self._collection_size(
            self.verses,
        )

    # ---------------------------------------------------------

    @property
    def child_count(self) -> int:

        return (
            self.section_count
            + self.verse_count
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.child_count

    # ---------------------------------------------------------

    def iter_sections(
        self,
    ) -> Iterator["Section"]:

        return self._collection_iter(
            self.sections,
        )

    # ---------------------------------------------------------

    def iter_verses(
        self,
    ) -> Iterator["Verse"]:

        return self._collection_iter(
            self.verses,
        )

    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict:

        data = super().to_dict()

        data["sections"] = [

            section.to_dict()

            for section in self.sections

        ]

        data["verses"] = [

            verse.to_dict()

            for verse in self.verses

        ]

        return data

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"Section("

            f"title={self.title!r}, "

            f"sections={self.section_count}, "

            f"verses={self.verse_count})"

        )
