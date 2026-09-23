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
v0.3.1
"""

from typing import Iterable, Self

from SanskritAI.common.identifiers.line_id import (
    LineId,
)

from SanskritAI.corpus.builders.child_node_builder import (
    ChildNodeBuilder,
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

    The builder exposes only metadata fields that are part of
    the canonical LineMetadata model.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Line:
        """
        Create a fresh canonical Line instance.
        """

        return Line(
            identifier=LineId.generate(),
            metadata=LineMetadata(),
        )

    # ---------------------------------------------------------
    # Line Identification
    # ---------------------------------------------------------

    def with_line_number(
        self,
        number: int,
    ) -> Self:
        """
        Set the canonical line number.
        """

        self._instance.metadata.line_number = number

        return self

    # ---------------------------------------------------------

    def with_sequence_number(
        self,
        number: int,
    ) -> Self:
        """
        Compatibility alias for line-number terminology.

        The canonical representation is ``line_number``.
        """

        return self.with_line_number(number)

    # ---------------------------------------------------------
    # Visual / Layout Information
    # ---------------------------------------------------------

    def with_visual_line_number(
        self,
        number: int | None,
    ) -> Self:
        """
        Set the source/display visual line number.
        """

        self._instance.metadata.visual_line_number = number

        return self

    # ---------------------------------------------------------

    def with_indentation(
        self,
        level: int,
    ) -> Self:
        """
        Set the indentation level of the line.
        """

        self._instance.metadata.indentation_level = level

        return self

    # ---------------------------------------------------------
    # Metrical Information
    # ---------------------------------------------------------

    def with_pada_number(
        self,
        number: int | None,
    ) -> Self:
        """
        Set the metrical pāda number.
        """

        self._instance.metadata.pada_number = number

        return self

    # ---------------------------------------------------------
    # Line Characteristics
    # ---------------------------------------------------------

    def as_continuation(
        self,
        value: bool = True,
    ) -> Self:
        """
        Mark the line as a continuation line.
        """

        self._instance.metadata.is_continuation = value

        return self

    # ---------------------------------------------------------

    def as_refrain(
        self,
        value: bool = True,
    ) -> Self:
        """
        Mark the line as a refrain.
        """

        self._instance.metadata.is_refrain = value

        return self

    # ---------------------------------------------------------

    def as_fragment(
        self,
        value: bool = True,
    ) -> Self:
        """
        Mark the line as a fragment.
        """

        self._instance.metadata.is_fragment = value

        return self

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    def with_language(
        self,
        language: str,
    ) -> Self:
        """
        Set the language of the line.
        """

        self._instance.metadata.language = language

        return self

    # ---------------------------------------------------------

    def with_language_variant(
        self,
        language: str,
    ) -> Self:
        """
        Compatibility alias.

        The canonical LineMetadata field is ``language``.
        """

        return self.with_language(language)

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

        return cls().from_instance(line)
