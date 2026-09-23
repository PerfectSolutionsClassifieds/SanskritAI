
from __future__ import annotations

"""
SanskritAI
==========

Line Metadata

Metadata describing a canonical line within a paragraph.

A Line groups one or more Token objects.

Depending on the source, a Line may represent:

- a metrical pāda
- a printed line
- a wrapped display line
- a prose line

Version
-------
v0.3.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True)
class LineMetadata(BaseNodeMetadata):
    """
    Metadata describing a canonical line.
    """

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: str = "sanskrit"

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    line_number: int = 1

    # ---------------------------------------------------------
    # Layout Information
    # ---------------------------------------------------------

    visual_line_number: int | None = None

    indentation_level: int = 0

    # ---------------------------------------------------------
    # Metrical Information
    # ---------------------------------------------------------

    pada_number: int | None = None

    # ---------------------------------------------------------
    # Line Characteristics
    # ---------------------------------------------------------

    is_continuation: bool = False

    is_refrain: bool = False

    is_fragment: bool = False

    # ---------------------------------------------------------
    # Derived Properties
    # ---------------------------------------------------------

    @property
    def has_pada(self) -> bool:
        """
        True if this line corresponds to a metrical pāda.
        """
        return self.pada_number is not None

    @property
    def is_indented(self) -> bool:
        """
        True if the line has indentation.
        """
        return self.indentation_level > 0

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.

        Explicit BaseNodeMetadata invocation is used instead of
        zero-argument super() because this class uses
        dataclass(slots=True).
        """
        data = BaseNodeMetadata.to_dict(self)

        data.update(
            {
                "language": self.language,
                "line_number": self.line_number,
                "visual_line_number": self.visual_line_number,
                "indentation_level": self.indentation_level,
                "pada_number": self.pada_number,
                "is_continuation": self.is_continuation,
                "is_refrain": self.is_refrain,
                "is_fragment": self.is_fragment,
            }
        )

        return data

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"LineMetadata("
            f"language={self.language!r}, "
            f"line={self.line_number}, "
            f"pada={self.pada_number}, "
            f"continuation={self.is_continuation})"
        )
