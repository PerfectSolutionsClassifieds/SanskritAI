from __future__ import annotations

"""
SanskritAI
==========

Line Builder

Builder for constructing canonical Line objects.

Version
-------
v0.1.0
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
    Builder for Line objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Line:

        return Line(
            id=LineId.generate(),
            metadata=LineMetadata(),
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def with_line_number(
        self,
        number: int,
    ) -> Self:

        self._instance.metadata.line_number = number

        return self

    # ---------------------------------------------------------

    def with_visual_line_number(
        self,
        number: int | None,
    ) -> Self:

        self._instance.metadata.visual_line_number = number

        return self

    # ---------------------------------------------------------

    def with_pada_number(
        self,
        number: int | None,
    ) -> Self:

        self._instance.metadata.pada_number = number

        return self

    # ---------------------------------------------------------

    def with_indentation(
        self,
        level: int,
    ) -> Self:

        self._instance.metadata.indentation_level = level

        return self

    # ---------------------------------------------------------

    def as_continuation(
        self,
        value: bool = True,
    ) -> Self:

        self._instance.metadata.is_continuation = value

        return self

    # ---------------------------------------------------------
    # Tokens
    # ---------------------------------------------------------

    def add_token(
        self,
        token: Token,
    ) -> Self:

        return self._add_child(
            token,
            self._instance.add_token,
        )

    # ---------------------------------------------------------

    def add_tokens(
        self,
        tokens: Iterable[Token],
    ) -> Self:

        return self._add_children(
            tokens,
            self._instance.add_token,
        )

    # ---------------------------------------------------------

    @classmethod
    def from_line(
        cls,
        line: Line,
    ) -> "LineBuilder":

        return cls().from_instance(line)
