from __future__ import annotations

"""
SanskritAI
==========

Reader Engine

Application-facing façade for the Reader Domain.

Architecture
------------

ReaderEngine
    │
    ├── ReaderRepository
    │       └── resolves canonical Reader views
    │
    └── ReaderNavigator
            └── performs canonical-ID navigation

The ReaderEngine does not implement navigation logic itself.
It delegates navigation to ReaderNavigator and object resolution
to ReaderRepository.

This keeps the Reader Domain cleanly separated from the
underlying Corpus implementation.

Version
-------
v3.2.0
"""

from dataclasses import dataclass

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_repository import (
    ReaderRepository,
)

from SanskritAI.domain.reader.reader_navigator import (
    ReaderNavigator,
)

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


@dataclass(slots=True)
class ReaderEngine:
    """
    Reader Domain façade.

    Responsibilities
    ----------------
    • resolve Reader objects through ReaderRepository
    • navigate through ReaderNavigator
    • expose a simple API to the Application/UI layer

    The engine deliberately contains no Corpus traversal logic.
    """

    repository: ReaderRepository

    navigator: ReaderNavigator

    # =========================================================
    # Document
    # =========================================================

    def document(
        self,
        document_id: str | None = None,
    ) -> ReaderDocument:
        """
        Resolve the ReaderDocument.
        """

        return self.repository.get_document(
            document_id,
        )

    # =========================================================
    # Chapter
    # =========================================================

    def chapter(
        self,
        chapter_id: str,
    ) -> ChapterView:
        """
        Resolve a chapter by canonical identifier.
        """

        return self.repository.get_chapter(
            chapter_id,
        )

    # ---------------------------------------------------------

    def next_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the next chapter.
        """

        return self.navigator.next_chapter(
            position,
        )

    # ---------------------------------------------------------

    def previous_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the previous chapter.
        """

        return self.navigator.previous_chapter(
            position,
        )

    # =========================================================
    # Śloka
    # =========================================================

    def sloka(
        self,
        sloka_id: str,
    ) -> SlokaView:
        """
        Resolve a śloka by canonical identifier.
        """

        return self.repository.get_sloka(
            sloka_id,
        )

    # ---------------------------------------------------------

    def next_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the next śloka.
        """

        return self.navigator.next_sloka(
            position,
        )

    # ---------------------------------------------------------

    def previous_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the previous śloka.
        """

        return self.navigator.previous_sloka(
            position,
        )

    # =========================================================
    # Word
    # =========================================================

    def word(
        self,
        word_id: str,
    ) -> WordView:
        """
        Resolve a word by canonical identifier.
        """

        return self.repository.get_word(
            word_id,
        )

    # ---------------------------------------------------------

    def next_word(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the next word.
        """

        return self.navigator.next_word(
            position,
        )

    # ---------------------------------------------------------

    def previous_word(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate to the previous word.
        """

        return self.navigator.previous_word(
            position,
        )

    # =========================================================
    # Generic Position Resolution
    # =========================================================

    def resolve(
        self,
        position: ReaderPosition,
    ) -> (
        ChapterView
        | SlokaView
        | WordView
    ):
        """
        Resolve the Reader object represented by a position.

        Resolution precedence is delegated to the repository
        implementation where appropriate.
        """

        resolver = getattr(
            self.repository,
            "resolve_position",
            None,
        )

        if callable(resolver):
            return resolver(
                position,
            )

        if position.word_id is not None:
            return self.word(
                position.word_id,
            )

        if position.sloka_id is not None:
            return self.sloka(
                position.sloka_id,
            )

        return self.chapter(
            position.chapter_id,
        )

    # =========================================================
    # Combined Navigation Helpers
    # =========================================================

    def move_next(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Move to the next object at the level represented by
        the current ReaderPosition.

        Priority:

            word
              ↓
            sloka
              ↓
            chapter
        """

        if position.word_id is not None:
            return self.next_word(
                position,
            )

        if position.sloka_id is not None:
            return self.next_sloka(
                position,
            )

        return self.next_chapter(
            position,
        )

    # ---------------------------------------------------------

    def move_previous(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Move to the previous object at the level represented by
        the current ReaderPosition.
        """

        if position.word_id is not None:
            return self.previous_word(
                position,
            )

        if position.sloka_id is not None:
            return self.previous_sloka(
                position,
            )

        return self.previous_chapter(
            position,
        )
