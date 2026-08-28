from __future__ import annotations

"""
SanskritAI
==========

Paragraph

Represents a logical paragraph within a Verse.

A Paragraph groups one or more Lines and serves as the bridge
between the canonical corpus hierarchy and the lexical layer.

Hierarchy
---------

Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

Future linguistic processing such as sentence segmentation,
morphological analysis, dependency parsing, translation
alignment, and semantic annotation may begin at the paragraph
level.

Version
-------
v0.3.0
"""

from typing import TYPE_CHECKING

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)
from SanskritAI.corpus.models.paragraph_metadata import (
    ParagraphMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.line import Line


class Paragraph(
    ContainerNode[
        str,
        ParagraphMetadata,
        "Line",
    ]
):
    """
    Canonical paragraph.
    """

    def __init__(
        self,
        identifier: str,
        metadata: ParagraphMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def lines(self):
        """
        Alias for child lines.
        """

        return self.children

    # ---------------------------------------------------------

    def add_line(
        self,
        line: "Line",
    ) -> None:
        """
        Add a line.
        """

        self.add_child(line)

    # ---------------------------------------------------------

    def remove_line(
        self,
        line: "Line",
    ) -> None:
        """
        Remove a line.
        """

        self.remove_child(line)

    # ---------------------------------------------------------

    @property
    def line_count(
        self,
    ) -> int:
        """
        Number of lines.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_line(
        self,
    ) -> "Line | None":
        """
        Return the first line.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_line(
        self,
    ) -> "Line | None":
        """
        Return the last line.
        """

        return self.last_child

    # ---------------------------------------------------------
    # Semantic convenience
    # ---------------------------------------------------------

    @property
    def paragraph_type(self):
        """
        Alias for the paragraph type stored in metadata.
        """

        return self.metadata.paragraph_type

    # ---------------------------------------------------------

    @property
    def language(self):
        """
        Alias for the language stored in metadata.
        """

        return self.metadata.language
