from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Provides canonical navigation through a ReaderDocument.

Responsibilities
----------------

• navigate chapters

• navigate ślokas

• navigate words

The navigator owns no linguistic logic.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.reader.reader_document import (
    ReaderDocument,
)

from SanskritAI.domain.reader.chapter_view import (
    ChapterView,
)

from SanskritAI.domain.reader.sloka_view import (
    SlokaView,
)

from SanskritAI.domain.reader.word_view import (
    WordView,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderNavigator(
    Displayable,
):
    """
    Canonical navigation engine.
    """

    document: ReaderDocument

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Reader Navigator"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical navigation engine for ReaderDocument."
        )

    # ---------------------------------------------------------
    # Chapters
    # ---------------------------------------------------------

    @property
    def chapters(
        self,
    ) -> tuple[ChapterView, ...]:
        return self.document.chapters

    def chapter(
        self,
        index: int,
    ) -> ChapterView:
        return self.chapters[index]

    # ---------------------------------------------------------
    # Ślokas
    # ---------------------------------------------------------

    def sloka(
        self,
        chapter_index: int,
        sloka_index: int,
    ) -> SlokaView:
        return self.chapter(
            chapter_index,
        ).slokas[sloka_index]

    # ---------------------------------------------------------
    # Words
    # ---------------------------------------------------------

    def word(
        self,
        chapter_index: int,
        sloka_index: int,
        word_index: int,
    ) -> WordView:
        return self.sloka(
            chapter_index,
            sloka_index,
        ).words[word_index]

    # ---------------------------------------------------------
    # Counts
    # ---------------------------------------------------------

    @property
    def chapter_count(self) -> int:
        return len(self.chapters)

    def sloka_count(
        self,
        chapter_index: int,
    ) -> int:
        return len(
            self.chapter(chapter_index).slokas
        )

    def word_count(
        self,
        chapter_index: int,
        sloka_index: int,
    ) -> int:
        return len(
            self.sloka(
                chapter_index,
                sloka_index,
            ).words
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
