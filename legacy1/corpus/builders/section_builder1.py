from __future__ import annotations

"""
SanskritAI
==========

Section Builder

Builder for constructing canonical Section objects.

Version
-------
v0.2.0
"""

from typing import Self

from SanskritAI.common.identifiers.section_id import (
    SectionId,
)

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)

from SanskritAI.corpus.models.section import (
    Section,
)

from SanskritAI.corpus.models.section_metadata import (
    SectionMetadata,
)

from SanskritAI.corpus.models.verse import (
    Verse,
)


class SectionBuilder(
    NodeBuilder[
        Section,
        SectionMetadata,
    ]
):
    """
    Builder for Section objects.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Section:

        return Section(
            id=SectionId.generate(),
            metadata=SectionMetadata(),
        )

    # ---------------------------------------------------------
    # Section-specific Metadata
    # ---------------------------------------------------------

    def with_section_type(
        self,
        section_type: str,
    ) -> Self:

        self._instance.metadata.section_type = section_type

        return self

    # ---------------------------------------------------------

    def with_section_number(
        self,
        number: str,
    ) -> Self:

        self._instance.metadata.section_number = number

        return self

    # ---------------------------------------------------------
    # Child Sections
    # ---------------------------------------------------------

    def add_section(
        self,
        section: Section,
    ) -> Self:

        self._instance.add_section(section)

        return self

    # ---------------------------------------------------------

    def add_sections(
        self,
        sections: list[Section],
    ) -> Self:

        for section in sections:

            self._instance.add_section(section)

        return self

    # ---------------------------------------------------------
    # Verses
    # ---------------------------------------------------------

    def add_verse(
        self,
        verse: Verse,
    ) -> Self:

        self._instance.add_verse(verse)

        return self

    # ---------------------------------------------------------

    def add_verses(
        self,
        verses: list[Verse],
    ) -> Self:

        for verse in verses:

            self._instance.add_verse(verse)

        return self

    # ---------------------------------------------------------

    @classmethod
    def from_section(
        cls,
        section: Section,
    ) -> "SectionBuilder":

        return cls().from_instance(section)
