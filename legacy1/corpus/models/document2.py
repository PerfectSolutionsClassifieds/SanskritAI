from __future__ import annotations

"""
SanskritAI
==========

Document

Represents a canonical document within a corpus.

Examples
--------

Mahabharata
    └── Adi Parva

Rigveda
    └── Mandala 1

Ramayana
    └── Bala Kanda

A Document is a container of Sections.

Version
-------
v0.3.0
"""

from typing import TYPE_CHECKING

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)
from SanskritAI.corpus.models.document_metadata import (
    DocumentMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.section import Section


class Document(
    ContainerNode[
        str,
        DocumentMetadata,
        "Section",
    ]
):
    """
    Canonical document.
    """

    def __init__(
        self,
        identifier: str,
        metadata: DocumentMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def sections(self):
        """
        Alias for children.
        """

        return self.children

    # ---------------------------------------------------------

    def add_section(
        self,
        section: "Section",
    ) -> None:
        """
        Add a section.
        """

        self.add_child(section)

    # ---------------------------------------------------------

    def remove_section(
        self,
        section: "Section",
    ) -> None:
        """
        Remove a section.
        """

        self.remove_child(section)

    # ---------------------------------------------------------

    @property
    def section_count(
        self,
    ) -> int:
        """
        Number of sections.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_section(
        self,
    ) -> "Section | None":
        """
        First section.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_section(
        self,
    ) -> "Section | None":
        """
        Last section.
        """

        return self.last_child
