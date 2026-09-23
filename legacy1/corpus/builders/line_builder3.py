from __future__ import annotations

"""
SanskritAI
==========

Line Builder

Builder for constructing canonical Line objects.

A Line represents an ordered textual unit within a Paragraph.

Hierarchy
---------
Corpus
    Document
        Section
            Verse
                Paragraph
                    Line
                        Token

Version
-------
v0.3.0
"""

from typing import Iterable, Self

from SanskritAI.common.identifiers.line_id import (
    LineId,
)

from SanskritAI.corpus.builders.child_node_builder import (
    ChildNodeBuilder,
)

from SanskritAI.corpus.enums.line_type import (
    LineType,
)

from SanskritAI.corpus.models.line import (
    Line,
)

from SanskritAI.corpus.models.line_metadata import (
    LineMetadata,
)

from SanskritAI.corpus.models.token import (
    Token,
)


class LineBuilder(
    ChildNodeBuilder[
        Line,
        LineMetadata,
        Token,
    ]
):
    """
    Builder for canonical Line objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Line:
        """
        Create a fresh canonical Line instance.

        The canonical Line model uses `identifier`
        rather than `id`.
        """

        return Line(
            identifier=LineId.generate(),
            metadata=LineMetadata(),
        )

    # ---------------------------------------------------------
    # Line Metadata
    # ---------------------------------------------------------

    def with_line_number(
        self,
        number: int,
    ) -> Self:
        """
        Set the canonical line number.

        `line_number` is the semantic builder API used by
        the corpus builder layer.
        """

        self._instance.metadata.line_number = number

        return self

    # ---------------------------------------------------------

    def with_sequence_number(
        self,
        number: int,
    ) -> Self:
        """
        Compatibility alias for sequence-number terminology.

        The canonical representation is `line_number`.
        """

        return self.with_line_number(number)

    # ---------------------------------------------------------

    def with_line_type(
        self,
        line_type: LineType,
    ) -> Self:
        """
        Set the line type.
        """

        self._instance.metadata.line_type = line_type

        return self

    # ---------------------------------------------------------

    def with_language_variant(
        self,
        language: str,
    ) -> Self:
        """
        Set the language variant.
        """

        self._instance.metadata.language_variant = language

        return self

    # ---------------------------------------------------------
    # Tokens
    # ---------------------------------------------------------

    def add_token(
        self,
        token: Token,
    ) -> Self:
        """
        Add a single Token.
        """

        return self._add_child(
            token,
            self._instance.add_token,
        )

    # ---------------------------------------------------------

    def add_tokens(
        self,
        tokens: Iterable[Token],
    ) -> Self:
        """
        Add multiple Tokens while preserving order.
        """

        return self._add_children(
            tokens,
            self._instance.add_token,
        )

    # ---------------------------------------------------------
    # Factory From Existing Instance
    # ---------------------------------------------------------

    @classmethod
    def from_line(
        cls,
        line: Line,
    ) -> "LineBuilder":
        """
        Create a LineBuilder from an existing Line.
        """

        return cls().from_instance(
            line,
        )
