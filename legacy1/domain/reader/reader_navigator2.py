from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Canonical-ID navigation service for the Reader Domain.

Purpose
-------

ReaderNavigator provides navigation through the Reader projection
without exposing positional array indices.

Navigation is based entirely on canonical identifiers:

    purana_id
        ↓
    chapter_id
        ↓
    sloka_id
        ↓
    word_id

The navigator operates on ReaderRepository rather than directly
on the Corpus Domain.

Architecture
------------

Reader UI
    │
    ▼
ReaderNavigator
    │
    ▼
ReaderRepository
    │
    ▼
ReaderDocument
    │
    ├── ChapterView
    │       └── SlokaView
    │               └── WordView
    │
    ▼
Canonical Corpus

Design Principle
----------------

Navigation semantics belong to the Reader Domain.

The repository knows how to retrieve objects.

The navigator knows how to move between them.

The ReaderEngine knows how to analyze them.

The ResolutionPipeline knows how to enrich them.

Version
-------
v2.2.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import (
    Displayable,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_position_factory import (
    ReaderPositionFactory,
)

from SanskritAI.domain.reader.reader_repository import (
    ReaderRepository,
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


@dataclass(
    slots=True,
)
class ReaderNavigator(
    Displayable,
):
    """
    Canonical-ID navigation over the Reader Repository.

    No array indices are exposed by this class.

    Examples
    --------

    First chapter::

        navigator.first_chapter()

    Next chapter::

        navigator.next_chapter(position)

    First śloka::

        navigator.first_sloka(chapter_id)

    Next śloka::

        navigator.next_sloka(position)

    First word::

        navigator.first_word(sloka_id)

    Next word::

        navigator.next_word(position)
    """

    repository: ReaderRepository

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Reader Navigator"

    # ---------------------------------------------------------

    @property
    def display_text(
        self,
    ) -> str:
        return self.display_name

    # ---------------------------------------------------------

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Canonical-ID navigation service for the Reader Domain."
        )

    # =========================================================
    # Document
    # =========================================================

    @property
    def document(
        self,
    ) -> ReaderDocument:
        """
        Return the Reader aggregate root.
        """

        return self.repository.get_document()

    # =========================================================
    # Chapters
    # =========================================================

    def chapters(
        self,
    ) -> tuple[
        ChapterView,
        ...
    ]:
        """
        Return all chapters in canonical corpus order.
        """

        return self.repository.get_chapters()

    # ---------------------------------------------------------

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

    def first_chapter(
        self,
    ) -> ChapterView | None:
        """
        Return the first chapter.
        """

        chapters = self.chapters()

        if not chapters:
            return None

        return chapters[0]

    # ---------------------------------------------------------

    def last_chapter(
        self,
    ) -> ChapterView | None:
        """
        Return the last chapter.
        """

        chapters = self.chapters()

        if not chapters:
            return None

        return chapters[-1]

    # ---------------------------------------------------------

    def next_chapter(
        self,
        position: ReaderPosition,
    ) -> ChapterView | None:
        """
        Return the chapter following the current chapter.

        Navigation is performed using the canonical chapter ID
        contained in ReaderPosition.

        Returns None when the current chapter is the final
        chapter.
        """

        chapters = self.chapters()

        if not chapters:
            return None

        current_id = position.chapter_id

        for index, chapter in enumerate(
            chapters,
        ):

            if chapter.identifier != current_id:
                continue

            if index + 1 >= len(chapters):
                return None

            return chapters[
                index + 1
            ]

        raise KeyError(
            f"Unknown chapter '{current_id}'."
        )

    # ---------------------------------------------------------

    def previous_chapter(
        self,
        position: ReaderPosition,
    ) -> ChapterView | None:
        """
        Return the chapter preceding the current chapter.

        Returns None when the current chapter is the first
        chapter.
        """

        chapters = self.chapters()

        if not chapters:
            return None

        current_id = position.chapter_id

        for index, chapter in enumerate(
            chapters,
        ):

            if chapter.identifier != current_id:
                continue

            if index == 0:
                return None

            return chapters[
                index - 1
            ]

        raise KeyError(
            f"Unknown chapter '{current_id}'."
        )

    # =========================================================
    # Ślokas
    # =========================================================

    def slokas(
        self,
        chapter_id: str,
    ) -> tuple[
        SlokaView,
        ...
    ]:
        """
        Return all ślokas belonging to a chapter.
        """

        return self.repository.get_chapter_slokas(
            chapter_id,
        )

    # ---------------------------------------------------------

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

    def first_sloka(
        self,
        chapter_id: str,
    ) -> SlokaView | None:
        """
        Return the first śloka of a chapter.
        """

        slokas = self.slokas(
            chapter_id,
        )

        if not slokas:
            return None

        return slokas[0]

    # ---------------------------------------------------------

    def last_sloka(
        self,
        chapter_id: str,
    ) -> SlokaView | None:
        """
        Return the final śloka of a chapter.
        """

        slokas = self.slokas(
            chapter_id,
        )

        if not slokas:
            return None

        return slokas[-1]

    # ---------------------------------------------------------

    def next_sloka(
        self,
        position: ReaderPosition,
    ) -> SlokaView | None:
        """
        Return the śloka following the current śloka.

        The current position must contain sloka_id.
        """

        sloka_id = position.sloka_id

        if sloka_id is None:
            raise ValueError(
                "next_sloka() requires a sloka-level position."
            )

        chapter_id = position.chapter_id

        slokas = self.slokas(
            chapter_id,
        )

        for index, sloka in enumerate(
            slokas,
        ):

            if sloka.identifier != sloka_id:
                continue

            if index + 1 >= len(slokas):
                return None

            return slokas[
                index + 1
            ]

        raise KeyError(
            f"Unknown śloka '{sloka_id}'."
        )

    # ---------------------------------------------------------

    def previous_sloka(
        self,
        position: ReaderPosition,
    ) -> SlokaView | None:
        """
        Return the śloka preceding the current śloka.
        """

        sloka_id = position.sloka_id

        if sloka_id is None:
            raise ValueError(
                "previous_sloka() requires a sloka-level position."
            )

        chapter_id = position.chapter_id

        slokas = self.slokas(
            chapter_id,
        )

        for index, sloka in enumerate(
            slokas,
        ):

            if sloka.identifier != sloka_id:
                continue

            if index == 0:
                return None

            return slokas[
                index - 1
            ]

        raise KeyError(
            f"Unknown śloka '{sloka_id}'."
        )

    # =========================================================
    # Words
    # =========================================================

    def words(
        self,
        sloka_id: str,
    ) -> tuple[
        WordView,
        ...
    ]:
        """
        Return all tokens/words belonging to a śloka.
        """

        return self.repository.get_sloka_words(
            sloka_id,
        )

    # ---------------------------------------------------------

    def word(
        self,
        word_id: str,
    ) -> WordView:
        """
        Resolve a word/token by canonical identifier.
        """

        return self.repository.get_word(
            word_id,
        )

    # ---------------------------------------------------------

    def first_word(
        self,
        sloka_id: str,
    ) -> WordView | None:
        """
        Return the first word/token of a śloka.
        """

        words = self.words(
            sloka_id,
        )

        if not words:
            return None

        return words[0]

    # ---------------------------------------------------------

    def last_word(
        self,
        sloka_id: str,
    ) -> WordView | None:
        """
        Return the final word/token of a śloka.
        """

        words = self.words(
            sloka_id,
        )

        if not words:
            return None

        return words[-1]

    # ---------------------------------------------------------

    def next_word(
        self,
        position: ReaderPosition,
    ) -> WordView | None:
        """
        Return the word/token following the current word.
        """

        word_id = position.word_id

        if word_id is None:
            raise ValueError(
                "next_word() requires a word-level position."
            )

        sloka_id = position.sloka_id

        if sloka_id is None:
            raise ValueError(
                "A word position must contain sloka_id."
            )

        words = self.words(
            sloka_id,
        )

        for index, word in enumerate(
            words,
        ):

            if word.identifier != word_id:
                continue

            if index + 1 >= len(words):
                return None

            return words[
                index + 1
            ]

        raise KeyError(
            f"Unknown word '{word_id}'."
        )

    # ---------------------------------------------------------

    def previous_word(
        self,
        position: ReaderPosition,
    ) -> WordView | None:
        """
        Return the word/token preceding the current word.
        """

        word_id = position.word_id

        if word_id is None:
            raise ValueError(
                "previous_word() requires a word-level position."
            )

        sloka_id = position.sloka_id

        if sloka_id is None:
            raise ValueError(
                "A word position must contain sloka_id."
            )

        words = self.words(
            sloka_id,
        )

        for index, word in enumerate(
            words,
        ):

            if word.identifier != word_id:
                continue

            if index == 0:
                return None

            return words[
                index - 1
            ]

        raise KeyError(
            f"Unknown word '{word_id}'."
        )

    # =========================================================
    # Position Creation
    # =========================================================

    def chapter_position(
        self,
        chapter_id: str,
    ) -> ReaderPosition:
        """
        Construct a canonical chapter-level position.
        """

        chapter = self.chapter(
            chapter_id,
        )

        return ReaderPositionFactory.chapter(
            purana_id=chapter.position.purana_id,
            chapter_id=chapter.identifier,
            corpus_id=chapter.position.corpus_id,
        )

    # ---------------------------------------------------------

    def sloka_position(
        self,
        sloka_id: str,
    ) -> ReaderPosition:
        """
        Construct a canonical śloka-level position.
        """

        sloka = self.sloka(
            sloka_id,
        )

        return ReaderPositionFactory.sloka(
            purana_id=sloka.position.purana_id,
            chapter_id=sloka.position.chapter_id,
            sloka_id=sloka.identifier,
            corpus_id=sloka.position.corpus_id,
        )

    # ---------------------------------------------------------

    def word_position(
        self,
        word_id: str,
    ) -> ReaderPosition:
        """
        Construct a canonical word-level position.
        """

        word = self.word(
            word_id,
        )

        return ReaderPositionFactory.word(
            purana_id=word.position.purana_id,
            chapter_id=word.position.chapter_id,
            sloka_id=word.position.sloka_id,
            word_id=word.identifier,
            corpus_id=word.position.corpus_id,
        )

    # =========================================================
    # Relative Position Navigation
    # =========================================================

    def next_position(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Move one logical navigation unit forward.

        Rules
        -----

        Word
            → next word

        Last word of śloka
            → first word of next śloka

        Last śloka of chapter
            → first śloka of next chapter

        Last chapter
            → None

        This method returns a canonical ReaderPosition rather
        than a ReaderView object.
        """

        # -----------------------------------------------------
        # Word-level navigation
        # -----------------------------------------------------

        if position.word_id is not None:

            next_word = self.next_word(
                position,
            )

            if next_word is not None:
                return next_word.position

            # End of current śloka.
            sloka = self.sloka(
                position.sloka_id,
            )

            next_sloka = self.next_sloka(
                position,
            )

            if next_sloka is not None:
                first_word = self.first_word(
                    next_sloka.identifier,
                )

                if first_word is not None:
                    return first_word.position

            # Continue at chapter level.
            next_chapter = self.next_chapter(
                position,
            )

            if next_chapter is None:
                return None

            next_sloka = self.first_sloka(
                next_chapter.identifier,
            )

            if next_sloka is None:
                return next_chapter.position

            first_word = self.first_word(
                next_sloka.identifier,
            )

            if first_word is not None:
                return first_word.position

            return next_sloka.position

        # -----------------------------------------------------
        # Śloka-level navigation
        # -----------------------------------------------------

        if position.sloka_id is not None:

            next_sloka = self.next_sloka(
                position,
            )

            if next_sloka is not None:
                return next_sloka.position

            next_chapter = self.next_chapter(
                position,
            )

            if next_chapter is None:
                return None

            next_sloka = self.first_sloka(
                next_chapter.identifier,
            )

            if next_sloka is None:
                return next_chapter.position

            return next_sloka.position

        # -----------------------------------------------------
        # Chapter-level navigation
        # -----------------------------------------------------

        next_chapter = self.next_chapter(
            position,
        )

        if next_chapter is None:
            return None

        return next_chapter.position

    # ---------------------------------------------------------

    def previous_position(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Move one logical navigation unit backward.

        This is the inverse of next_position().
        """

        # -----------------------------------------------------
        # Word-level navigation
        # -----------------------------------------------------

        if position.word_id is not None:

            previous_word = self.previous_word(
                position,
            )

            if previous_word is not None:
                return previous_word.position

            # First word of current śloka.
            previous_sloka = self.previous_sloka(
                position,
            )

            if previous_sloka is not None:

                last_word = self.last_word(
                    previous_sloka.identifier,
                )

                if last_word is not None:
                    return last_word.position

                return previous_sloka.position

            # First śloka of current chapter.
            previous_chapter = self.previous_chapter(
                position,
            )

            if previous_chapter is None:
                return None

            previous_sloka = self.last_sloka(
                previous_chapter.identifier,
            )

            if previous_sloka is None:
                return previous_chapter.position

            last_word = self.last_word(
                previous_sloka.identifier,
            )

            if last_word is not None:
                return last_word.position

            return previous_sloka.position

        # -----------------------------------------------------
        # Śloka-level navigation
        # -----------------------------------------------------

        if position.sloka_id is not None:

            previous_sloka = self.previous_sloka(
                position,
            )

            if previous_sloka is not None:
                return previous_sloka.position

            previous_chapter = self.previous_chapter(
                position,
            )

            if previous_chapter is None:
                return None

            previous_sloka = self.last_sloka(
                previous_chapter.identifier,
            )

            if previous_sloka is None:
                return previous_chapter.position

            return previous_sloka.position

        # -----------------------------------------------------
        # Chapter-level navigation
        # -----------------------------------------------------

        previous_chapter = self.previous_chapter(
            position,
        )

        if previous_chapter is None:
            return None

        return previous_chapter.position

    # =========================================================
    # Counts
    # =========================================================

    def chapter_count(
        self,
    ) -> int:
        """
        Return total chapter count.
        """

        return len(
            self.chapters(),
        )

    # ---------------------------------------------------------

    def sloka_count(
        self,
        chapter_id: str,
    ) -> int:
        """
        Return śloka count for a chapter.
        """

        return len(
            self.slokas(
                chapter_id,
            ),
        )

    # ---------------------------------------------------------

    def word_count(
        self,
        sloka_id: str,
    ) -> int:
        """
        Return token/word count for a śloka.
        """

        return len(
            self.words(
                sloka_id,
            ),
        )

    # =========================================================
    # Position Validation
    # =========================================================

    def contains(
        self,
        position: ReaderPosition,
    ) -> bool:
        """
        Determine whether a canonical ReaderPosition resolves
        successfully.

        No index arithmetic is used.
        """

        try:

            self.repository.resolve_position(
                position,
            )

            return True

        except (
            KeyError,
            ValueError,
        ):

            return False

    # ---------------------------------------------------------

    def resolve(
        self,
        position: ReaderPosition,
    ):
        """
        Resolve a ReaderPosition through the repository.
        """

        return self.repository.resolve_position(
            position,
        )

    # =========================================================
    # Diagnostics
    # =========================================================

    def summary(
        self,
    ) -> dict[str, int]:
        """
        Return navigation statistics.
        """

        return {
            "chapters": self.chapter_count(),
            "slokas": sum(
                self.sloka_count(
                    chapter.identifier,
                )
                for chapter in self.chapters()
            ),
            "words": sum(
                self.word_count(
                    sloka.identifier,
                )
                for sloka in self.slokas_all()
            ),
        }

    # ---------------------------------------------------------

    def slokas_all(
        self,
    ) -> tuple[
        SlokaView,
        ...
    ]:
        """
        Return every śloka across every chapter.
        """

        result: list[
            SlokaView
        ] = []

        for chapter in self.chapters():

            result.extend(
                self.slokas(
                    chapter.identifier,
                ),
            )

        return tuple(
            result,
        )

    # =========================================================
    # Python Protocol
    # =========================================================

    def __len__(
        self,
    ) -> int:
        return self.chapter_count()

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return (
            "ReaderNavigator("
            f"chapters={self.chapter_count()}, "
            f"slokas={len(self.slokas_all())}"
            ")"
        )
