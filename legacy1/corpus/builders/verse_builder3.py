
from __future__ import annotations

"""
SanskritAI
==========

Verse Builder

Builder for constructing canonical Verse objects.

Version
-------
v0.3.0
"""

from typing import Iterable, Self

from SanskritAI.common.identifiers.verse_id import (
    VerseId,
)

from SanskritAI.corpus.builders.child_node_builder import (
    ChildNodeBuilder,
)

from SanskritAI.corpus.enums.meter import (
    Meter,
)

from SanskritAI.corpus.enums.verse_type import (
    VerseType,
)

from SanskritAI.corpus.models.paragraph import (
    Paragraph,
)

from SanskritAI.corpus.models.verse import (
    Verse,
)

from SanskritAI.corpus.models.verse_metadata import (
    VerseMetadata,
)


class VerseBuilder(
    ChildNodeBuilder[
        Verse,
        VerseMetadata,
        Paragraph,
    ]
):
    """
    Builder for canonical Verse objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Verse:
        """
        Create a fresh canonical Verse instance.

        The canonical Verse model uses `identifier`
        rather than `id`.
        """

        return Verse(
            identifier=VerseId.generate(),
            metadata=VerseMetadata(),
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate a Verse.

        A Verse is not a titled node. Therefore the generic
        NodeBuilder title validation must not be applied here.

        Structural validation remains delegated to the canonical
        Verse model / child-node infrastructure where applicable.
        """

        return None

    # ---------------------------------------------------------
    # Verse Metadata
    # ---------------------------------------------------------

    def with_verse_number(
        self,
        number: str,
    ) -> Self:
        """
        Set the verse number.
        """

        self._instance.metadata.verse_number = number
        return self

    # ---------------------------------------------------------

    def with_verse_type(
        self,
        verse_type: VerseType,
    ) -> Self:
        """
        Set the verse type.
        """

        self._instance.metadata.verse_type = verse_type
        return self

    # ---------------------------------------------------------

    def with_meter(
        self,
        meter: Meter,
    ) -> Self:
        """
        Set the canonical meter.
        """

        self._instance.metadata.meter = meter
        return self

    # ---------------------------------------------------------

    def with_meter_name(
        self,
        meter_name: str,
    ) -> Self:
        """
        Set the meter name.

        The current canonical VerseMetadata does not expose
        a `meter_name` field. The method is retained as part
        of the builder API for compatibility with the existing
        builder tests, but the value is intentionally not
        written as an ad-hoc metadata attribute.

        The canonical Meter field remains the authoritative
        representation.
        """

        return self

    # ---------------------------------------------------------
    # Paragraphs
    # ---------------------------------------------------------

    def add_paragraph(
        self,
        paragraph: Paragraph,
    ) -> Self:
        """
        Add a single Paragraph.
        """

        return self._add_child(
            paragraph,
            self._instance.add_paragraph,
        )

    # ---------------------------------------------------------

    def add_paragraphs(
        self,
        paragraphs: Iterable[Paragraph],
    ) -> Self:
        """
        Add multiple Paragraphs.
        """

        return self._add_children(
            paragraphs,
            self._instance.add_paragraph,
        )

    # ---------------------------------------------------------
    # Factory From Existing Instance
    # ---------------------------------------------------------

    @classmethod
    def from_verse(
        cls,
        verse: Verse,
    ) -> "VerseBuilder":
        """
        Create a VerseBuilder from an existing Verse.
        """

        return cls().from_instance(
            verse,
        )
