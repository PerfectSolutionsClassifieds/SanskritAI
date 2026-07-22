from __future__ import annotations

"""
SanskritAI
==========

Paragraph Metadata

Metadata describing a canonical paragraph within a Verse.

A Paragraph groups one or more Line objects and allows the corpus
model to represent poetry, prose, translations, commentaries,
critical apparatus, and parallel editions.

Version
-------
v0.2.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.corpus.enums.paragraph_type import (
    ParagraphType,
)

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True)
class ParagraphMetadata(BaseNodeMetadata):
    """
    Metadata describing a paragraph.
    """

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    paragraph_number: int = 1

    paragraph_type: ParagraphType = (
        ParagraphType.DEFAULT
    )

    # ---------------------------------------------------------
    # Text Classification
    # ---------------------------------------------------------

    language_variant: str = ""

    is_translation: bool = False

    is_commentary: bool = False

    # ---------------------------------------------------------

    @property
    def is_default(self) -> bool:
        """
        True if this is a standard paragraph.
        """

        return (
            self.paragraph_type
            == ParagraphType.DEFAULT
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = super().to_dict()

        data.update(

            {

                "paragraph_number":
                    self.paragraph_number,

                "paragraph_type":
                    self.paragraph_type.value,

                "language_variant":
                    self.language_variant,

                "is_translation":
                    self.is_translation,

                "is_commentary":
                    self.is_commentary,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"ParagraphMetadata("

            f"number={self.paragraph_number}, "

            f"type={self.paragraph_type.value!r})"

        )
