from __future__ import annotations

"""
SanskritAI
==========

Paragraph

Canonical paragraph within a Verse.

A Paragraph groups one or more Line objects and provides a
structural container for textual content. It may represent:

    • verse text
    • prose
    • translation
    • commentary
    • critical apparatus

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterator

from SanskritAI.common.identifiers.paragraph_id import (
    ParagraphId,
)

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.corpus.models.paragraph_metadata import (
    ParagraphMetadata,
)

if TYPE_CHECKING:
    from SanskritAI.corpus.models.line import Line


@dataclass(slots=True)
class Paragraph(
    ContainerNode[
        ParagraphId,
        ParagraphMetadata,
    ]
):
    """
    Canonical paragraph node.
    """

    id: ParagraphId

    metadata: ParagraphMetadata = field(
        default_factory=ParagraphMetadata
    )

    lines: list["Line"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Line Management
    # ---------------------------------------------------------

    def add_line(
        self,
        line: "Line",
    ) -> None:
        """
        Add a line to the paragraph.
        """

        self._add_to_collection(
            self.lines,
            line,
        )

    # ---------------------------------------------------------

    def remove_line(
        self,
        line: "Line",
    ) -> None:
        """
        Remove a line from the paragraph.
        """

        self._remove_from_collection(
            self.lines,
            line,
        )

    # ---------------------------------------------------------

    def clear_lines(
        self,
    ) -> None:
        """
        Remove all lines.
        """

        self._clear_collection(
            self.lines,
        )

    # ---------------------------------------------------------
    # Collection Helpers
    # ---------------------------------------------------------

    @property
    def line_count(self) -> int:
        """
        Number of lines contained in this paragraph.
        """

        return self._collection_size(
            self.lines,
        )

    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.line_count

    # ---------------------------------------------------------

    def __iter__(self) -> Iterator["Line"]:
        return self._collection_iter(
            self.lines,
        )

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> "Line":
        return self._collection_get(
            self.lines,
            index,
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the paragraph.
        """

        data = super().to_dict()

        data["lines"] = [

            line.to_dict()

            for line in self.lines

        ]

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"Paragraph("

            f"number={self.metadata.paragraph_number}, "

            f"lines={self.line_count})"

        )
