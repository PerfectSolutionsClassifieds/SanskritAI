from __future__ import annotations

"""
SanskritAI
==========

Document Builder

Builder for constructing canonical Document objects.

Version
-------
v0.2.0
"""

from typing import Self

from SanskritAI.common.identifiers.document_id import (
    DocumentId,
)

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)

from SanskritAI.corpus.models.document import (
    Document,
)

from SanskritAI.corpus.models.document_metadata import (
    DocumentMetadata,
)

from SanskritAI.corpus.models.section import (
    Section,
)


class DocumentBuilder(
    NodeBuilder[
        Document,
        DocumentMetadata,
    ]
):
    """
    Builder for Document objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Document:

        return Document(
            id=DocumentId.generate(),
            metadata=DocumentMetadata(),
        )

    # ---------------------------------------------------------
    # Document-specific Metadata
    # ---------------------------------------------------------

    def with_document_type(
        self,
        document_type: str,
    ) -> Self:

        self._instance.metadata.document_type = document_type

        return self

    # ---------------------------------------------------------

    def with_page_range(
        self,
        start_page: int | None,
        end_page: int | None,
    ) -> Self:

        self._instance.metadata.start_page = start_page
        self._instance.metadata.end_page = end_page

        return self

    # ---------------------------------------------------------

    def with_publisher(
        self,
        publisher: str,
    ) -> Self:

        self._instance.metadata.publisher = publisher

        return self

    # ---------------------------------------------------------

    def with_edition(
        self,
        edition: str,
    ) -> Self:

        self._instance.metadata.edition = edition

        return self

    # ---------------------------------------------------------

    def with_publication_year(
        self,
        year: str,
    ) -> Self:

        self._instance.metadata.publication_year = year

        return self

    # ---------------------------------------------------------
    # Contributors
    # ---------------------------------------------------------

    def add_author(
        self,
        author: str,
    ) -> Self:

        self._instance.metadata.authors.append(author)

        return self

    # ---------------------------------------------------------

    def add_editor(
        self,
        editor: str,
    ) -> Self:

        self._instance.metadata.editors.append(editor)

        return self

    # ---------------------------------------------------------

    def add_translator(
        self,
        translator: str,
    ) -> Self:

        self._instance.metadata.translators.append(
            translator
        )

        return self

    # ---------------------------------------------------------
    # Sections
    # ---------------------------------------------------------

    def add_section(
        self,
        section: Section,
    ) -> Self:

        self._instance.add_section(section)

        return self

    # ---------------------------------------------------------

    def add_sections(
        self,
        sections: list[Section],
    ) -> Self:

        for section in sections:

            self._instance.add_section(section)

        return self

    # ---------------------------------------------------------

    @classmethod
    def from_document(
        cls,
        document: Document,
    ) -> "DocumentBuilder":

        return cls().from_instance(document)
