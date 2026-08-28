
from __future__ import annotations

"""
SanskritAI
==========

Section Builder

Builder for constructing canonical Section objects.

Version
-------
v0.3.0
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

    A SectionBuilder constructs a Section with:

    - a generated canonical identifier
    - initialized SectionMetadata
    - optional section-specific metadata
    - zero or more child sections
    - zero or more verses

    The builder follows the fluent-builder contract established
    by NodeBuilder.
    """

    # ---------------------------------------------------------
    # Factory
    # ---------------------------------------------------------

    def _create_instance(self) -> Section:
        """
        Create a fresh Section instance.

        Section.__init__() expects the canonical field name
        ``identifier`` rather than ``id``.
        """

        return Section(
            identifier=SectionId.generate(),
            metadata=SectionMetadata(),
        )

    # ---------------------------------------------------------
    # Section-specific Metadata
    # ---------------------------------------------------------

    def with_section_type(
        self,
        section_type: str,
    ) -> Self:
        """
        Set the section type.

        Examples:
            Parva
            Kanda
            Sarga
            Mandala
            Sukta
        """

        self._instance.metadata.section_type = section_type

        return self

    # ---------------------------------------------------------

    def with_section_number(
        self,
        number: str,
    ) -> Self:
        """
        Set the section number.

        The canonical SectionMetadata model is responsible for
        interpreting this value through its numbering scheme.
        """

        self._instance.metadata.section_number = number

        return self

    # ---------------------------------------------------------
    # Child Sections
    # ---------------------------------------------------------

    def add_section(
        self,
        section: Section,
    ) -> Self:
        """
        Add a child section.
        """

        self._instance.add_section(section)

        return self

    # ---------------------------------------------------------

    def add_sections(
        self,
        sections: list[Section],
    ) -> Self:
        """
        Add multiple child sections while preserving order.
        """

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
        """
        Add a verse to the section.
        """

        self._instance.add_verse(verse)

        return self

    # ---------------------------------------------------------

    def add_verses(
        self,
        verses: list[Verse],
    ) -> Self:
        """
        Add multiple verses while preserving order.
        """

        for verse in verses:
            self._instance.add_verse(verse)

        return self

    # ---------------------------------------------------------
    # Copy / Reconstruction
    # ---------------------------------------------------------

    @classmethod
    def from_section(
        cls,
        section: Section,
    ) -> "SectionBuilder":
        """
        Create a SectionBuilder initialized from an existing
        Section.

        NodeBuilder.from_instance() performs the defensive
        copy required by the builder contract.
        """

        return cls().from_instance(section)

