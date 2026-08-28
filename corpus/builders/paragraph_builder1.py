from __future__ import annotations

"""
SanskritAI
==========

Paragraph Builder

Builder for constructing canonical Paragraph objects.

Version
-------
v0.1.0
"""

from typing import Iterable, Self

from SanskritAI.common.identifiers.paragraph_id import (
    ParagraphId,
)

from SanskritAI.corpus.builders.child_node_builder import (
    ChildNodeBuilder,
)

from SanskritAI.corpus.enums.paragraph_type import (
    ParagraphType,
)

from SanskritAI.corpus.models.line import (
    Line,
)

from SanskritAI.corpus.models.paragraph import (
    Paragraph,
)

from SanskritAI.corpus.models.paragraph_metadata import (
    ParagraphMetadata,
)


class ParagraphBuilder(
    ChildNodeBuilder[
        Paragraph,
        ParagraphMetadata,
        Line,
    ]
):
    """
    Builder for canonical Paragraph objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Paragraph:

        return Paragraph(
            id=ParagraphId.generate(),
            metadata=ParagraphMetadata(),
        )

    # ---------------------------------------------------------
    # Paragraph Metadata
    # ---------------------------------------------------------

    def with_paragraph_number(
        self,
        number: int,
    ) -> Self:

        self._instance.metadata.paragraph_number = number

        return self

    # ---------------------------------------------------------

    def with_paragraph_type(
        self,
        paragraph_type: ParagraphType,
    ) -> Self:

        self._instance.metadata.paragraph_type = paragraph_type

        return self

    # ---------------------------------------------------------

    def with_language_variant(
        self,
        language: str,
    ) -> Self:

        self._instance.metadata.language_variant = language

        return self

    # ---------------------------------------------------------

    def as_translation(
        self,
        value: bool = True,
    ) -> Self:

        self._instance.metadata.is_translation = value

        return self

    # ---------------------------------------------------------

    def as_commentary(
        self,
        value: bool = True,
    ) -> Self:

        self._instance.metadata.is_commentary = value

        return self

    # ---------------------------------------------------------
    # Lines
    # ---------------------------------------------------------

    def add_line(
        self,
        line: Line,
    ) -> Self:
        """
        Add a Line to this Paragraph.
        """

        return self._add_child(
            line,
            self._instance.add_line,
        )

    # ---------------------------------------------------------

    def add_lines(
        self,
        lines: Iterable[Line],
    ) -> Self:
        """
        Add multiple Lines.
        """

        return self._add_children(
            lines,
            self._instance.add_line,
        )

    # ---------------------------------------------------------

    @classmethod
    def from_paragraph(
        cls,
        paragraph: Paragraph,
    ) -> "ParagraphBuilder":

        return cls().from_instance(
            paragraph,
        )
