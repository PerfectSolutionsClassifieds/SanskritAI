from __future__ import annotations

"""
SanskritAI
==========

Verse Metadata

Metadata describing a canonical textual unit.

A Verse represents the primary textual unit within a canonical
document.

Examples
--------
• Śloka
• Mantra
• Ṛc
• Sūtra
• Stanza

Version
-------
v0.2.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.corpus.enums.meter import Meter
from SanskritAI.corpus.enums.verse_type import VerseType

from SanskritAI.corpus.models.base_node_metadata import (
    BaseNodeMetadata,
)


@dataclass(slots=True)
class VerseMetadata(BaseNodeMetadata):
    """
    Metadata describing a canonical verse.
    """

    # ---------------------------------------------------------
    # Canonical Identification
    # ---------------------------------------------------------

    verse_number: str = ""

    canonical_number: str = ""

    verse_type: VerseType = VerseType.UNKNOWN

    # ---------------------------------------------------------
    # Literary Information
    # ---------------------------------------------------------

    meter: Meter = Meter.UNKNOWN

    language_variant: str = ""

    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------

    start_page: int | None = None

    end_page: int | None = None

    # ---------------------------------------------------------
    # Optional Media
    # ---------------------------------------------------------

    audio_reference: str = ""

    image_reference: str = ""

    # ---------------------------------------------------------

    @property
    def page_count(self) -> int | None:

        if (
            self.start_page is None
            or self.end_page is None
        ):
            return None

        return self.end_page - self.start_page + 1

    # ---------------------------------------------------------

    @property
    def has_page_range(self) -> bool:

        return (
            self.start_page is not None
            and self.end_page is not None
        )

    # ---------------------------------------------------------

    @property
    def has_audio(self) -> bool:

        return bool(self.audio_reference)

    # ---------------------------------------------------------

    @property
    def has_image(self) -> bool:

        return bool(self.image_reference)

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize metadata.
        """

        data = super().to_dict()

        data.update(

            {

                "verse_number":
                    self.verse_number,

                "canonical_number":
                    self.canonical_number,

                "verse_type":
                    self.verse_type.value,

                "meter":
                    self.meter.value,

                "language_variant":
                    self.language_variant,

                "start_page":
                    self.start_page,

                "end_page":
                    self.end_page,

                "page_count":
                    self.page_count,

                "audio_reference":
                    self.audio_reference,

                "image_reference":
                    self.image_reference,

            }

        )

        return data

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"VerseMetadata("

            f"verse={self.verse_number!r}, "

            f"type={self.verse_type.value!r}, "

            f"meter={self.meter.value!r})"

        )
