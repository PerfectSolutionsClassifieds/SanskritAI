from __future__ import annotations

"""
SanskritAI
==========

Document Metadata

Metadata describing a canonical document within a corpus.

A Document may represent:

    • Parva
    • Samhita
    • Kanda
    • Mandala
    • Book
    • Volume
    • Part

This class inherits all common node metadata from
BaseNodeMetadata and adds document-specific attributes.

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True)
class DocumentMetadata(BaseNodeMetadata):
    """
    Metadata describing a canonical document.
    """

    # ---------------------------------------------------------
    # Document-specific classification
    # ---------------------------------------------------------

    document_type: str = ""

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    start_page: int | None = None

    end_page: int | None = None

    # ---------------------------------------------------------
    # Contributors
    # ---------------------------------------------------------

    # authors: list[str] | None = None

    # editors: list[str] | None = None

    # translators: list[str] | None = None

    authors: list[str] = field(default_factory=list)

    editors: list[str] = field(default_factory=list)

    translators: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Publication
    # ---------------------------------------------------------

    publisher: str = ""

    edition: str = ""

    publication_year: str = ""

    # ---------------------------------------------------------

    @property
    def page_count(self) -> int | None:
        """
        Total page count if page range is known.
        """

        if (
            self.start_page is None
            or self.end_page is None
        ):
            return None

        return self.end_page - self.start_page + 1

    # ---------------------------------------------------------

    @property
    def has_page_range(self) -> bool:
        """
        True if both start and end pages are known.
        """

        return (
            self.start_page is not None
            and self.end_page is not None
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = super().to_dict()

        data.update(

            {

                "document_type":
                    self.document_type,

                "start_page":
                    self.start_page,

                "end_page":
                    self.end_page,

                "page_count":
                    self.page_count,

                "authors":
                    self.authors,

                "editors":
                    self.editors,

                "translators":
                    self.translators,

                "publisher":
                    self.publisher,

                "edition":
                    self.edition,

                "publication_year":
                    self.publication_year,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"DocumentMetadata("

            f"title={self.title!r}, "

            f"type={self.document_type!r}, "

            f"level={self.hierarchy_level})"

        )
