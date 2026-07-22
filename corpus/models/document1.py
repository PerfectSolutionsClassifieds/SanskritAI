from __future__ import annotations

"""
SanskritAI
==========

Document

Canonical document within a corpus.

A Document represents a logical subdivision of a Corpus.

Examples
--------
• Parva
• Samhita
• Kanda
• Mandala
• Book
• Volume
• Part

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator

from SanskritAI.common.identifiers.document_id import (
    DocumentId,
)

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.corpus.models.document_metadata import (
    DocumentMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.section import Section


@dataclass(slots=True)
class Document(
    ContainerNode[
        DocumentId,
        DocumentMetadata,
    ]
):
    """
    Canonical document.
    """

    id: DocumentId

    metadata: DocumentMetadata = field(
        default_factory=DocumentMetadata
    )

    sections: list["Section"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Section Management
    # ---------------------------------------------------------

    def add_section(
        self,
        section: "Section",
    ) -> None:
        """
        Add a section to the document.
        """

        self._add_to_collection(
            self.sections,
            section,
        )

    # ---------------------------------------------------------

    def remove_section(
        self,
        section: "Section",
    ) -> None:
        """
        Remove a section from the document.
        """

        self._remove_from_collection(
            self.sections,
            section,
        )

    # ---------------------------------------------------------

    def clear_sections(
        self,
    ) -> None:
        """
        Remove every section.
        """

        self._clear_collection(
            self.sections,
        )

    # ---------------------------------------------------------
    # Collection Helpers
    # ---------------------------------------------------------

    @property
    def section_count(
        self,
    ) -> int:

        return self._collection_size(
            self.sections,
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.section_count

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator["Section"]:

        return self._collection_iter(
            self.sections,
        )

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> "Section":

        return self._collection_get(
            self.sections,
            index,
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

        return data

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"Document("

            f"title={self.title!r}, "

            f"sections={self.section_count})"

        )
