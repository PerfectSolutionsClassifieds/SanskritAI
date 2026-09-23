
from __future__ import annotations

"""
SanskritAI
==========

Line Builder

Builder for constructing canonical Line objects.

A Line is a structural/content node belonging to a Paragraph.
It is not a titled node.

Version
-------
v0.3.0
"""

from typing import Self

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


class LineBuilder(
    ChildNodeBuilder[
        Line,
        LineMetadata,
        str,
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
    # Validation
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate a Line.

        A Line is a structural/content node and does not
        require a title. Therefore generic NodeBuilder title
        validation must not be applied.
        """

        return None

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
