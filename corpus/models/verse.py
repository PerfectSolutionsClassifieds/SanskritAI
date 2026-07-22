from __future__ import annotations

"""
SanskritAI
==========

Verse

Represents a canonical verse within a section.

A Verse is the principal linguistic unit of the SanskritAI
Canonical Corpus Model.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

Future linguistic layers such as meter analysis,
padaccheda, morphology, syntax, semantics, commentaries,
translations, and AI annotations are expected to attach
primarily to Verse objects.

Version
-------
v0.3.0
"""

from typing import TYPE_CHECKING

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)
from SanskritAI.corpus.models.verse_metadata import (
    VerseMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.paragraph import Paragraph


class Verse(
    ContainerNode[
        str,
        VerseMetadata,
        "Paragraph",
    ]
):
    """
    Canonical verse.
    """

    def __init__(
        self,
        identifier: str,
        metadata: VerseMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def paragraphs(self):
        """
        Alias for child paragraphs.
        """

        return self.children

    # ---------------------------------------------------------

    def add_paragraph(
        self,
        paragraph: "Paragraph",
    ) -> None:
        """
        Add a paragraph.
        """

        self.add_child(paragraph)

    # ---------------------------------------------------------

    def remove_paragraph(
        self,
        paragraph: "Paragraph",
    ) -> None:
        """
        Remove a paragraph.
        """

        self.remove_child(paragraph)

    # ---------------------------------------------------------

    @property
    def paragraph_count(
        self,
    ) -> int:
        """
        Number of paragraphs.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_paragraph(
        self,
    ) -> "Paragraph | None":
        """
        First paragraph.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_paragraph(
        self,
    ) -> "Paragraph | None":
        """
        Last paragraph.
        """

        return self.last_child

    # ---------------------------------------------------------
    # Linguistic convenience
    # ---------------------------------------------------------

    @property
    def verse_type(self):
        """
        Alias for the verse type stored in metadata.
        """

        return self.metadata.verse_type

    # ---------------------------------------------------------

    @property
    def meter(self):
        """
        Alias for the metrical classification stored in metadata.
        """

        return self.metadata.meter

    # ---------------------------------------------------------

    @property
    def language(self):
        """
        Alias for the language stored in metadata.
        """

        return self.metadata.language
