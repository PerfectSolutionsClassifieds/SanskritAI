from __future__ import annotations

"""
SanskritAI
==========

Section Metadata

Metadata describing a hierarchical section within a document.

Examples
--------
• Parva
• Samhita
• Mandala
• Kanda
• Skandha
• Book
• Part
• Chapter
• Adhyaya
• Sukta

This class inherits all common node metadata from
BaseNodeMetadata.

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
class SectionMetadata(BaseNodeMetadata):
    """
    Metadata describing a Section.
    """

    # ---------------------------------------------------------
    # Section-specific information
    # ---------------------------------------------------------

    section_type: str = ""

    numbering_scheme: str = ""

    start_page: int | None = None

    end_page: int | None = None

    # ---------------------------------------------------------

    @property
    def page_count(self) -> int | None:
        """
        Total page count if page range is known.
        """

        if (
            self.start_page is None
            or self.end_page is None
        ):
            return None

        return self.end_page - self.start_page + 1

    # ---------------------------------------------------------

    @property
    def has_page_range(self) -> bool:
        """
        Returns True if page range is known.
        """

        return (
            self.start_page is not None
            and self.end_page is not None
        )

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = super().to_dict()

        data.update(

            {

                "section_type":
                    self.section_type,

                "numbering_scheme":
                    self.numbering_scheme,

                "start_page":
                    self.start_page,

                "end_page":
                    self.end_page,

                "page_count":
                    self.page_count,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"SectionMetadata("

            f"title={self.title!r}, "

            f"type={self.section_type!r}, "

            f"level={self.hierarchy_level})"

        )
