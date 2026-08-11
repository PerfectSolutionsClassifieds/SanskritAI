from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Thin navigation service for the Reader Domain.

The ReaderNavigator delegates ordering and object retrieval to
ReaderRepository and uses ReaderPositionFactory to construct
new immutable ReaderPosition objects.

Canonical navigation hierarchy
------------------------------

ReaderPosition
    purana_id
        chapter_id
            sloka_id
                word_id

The Navigator does not store positional indices.

Version
-------
v3.1.1
"""

from dataclasses import dataclass, field

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_position_factory import (
    ReaderPositionFactory,
)

from SanskritAI.domain.reader.reader_repository import (
    ReaderRepository,
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
class ReaderNavigator:
    """
    Navigate the Reader Domain using canonical identifiers.

    Responsibilities
    ----------------
    • chapter navigation
    • śloka navigation
    • word navigation
    • immutable position construction
    • delegation to ReaderRepository

    The Navigator does not know how the underlying Corpus is
    stored or ordered.

    ``position_factory`` remains injectable for testing or future
    alternative position-construction policies, but normal callers
    may construct the navigator with only a repository.
    """

    repository: ReaderRepository

    position_factory: ReaderPositionFactory = field(
        default_factory=ReaderPositionFactory,
    )

    # =========================================================
    # Chapter Navigation
    # =========================================================

    def next_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the next chapter.
        """

        chapter_id = self._require_chapter_id(
            position,
        )

        chapter = self.repository.next_chapter(
            chapter_id,
        )

        if chapter is None:
            return None

        return self._chapter_position(
            chapter,
            position,
        )

    # ---------------------------------------------------------

    def previous_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous chapter.
        """

        chapter_id = self._require_chapter_id(
            position,
        )

        chapter = self.repository.previous_chapter(
            chapter_id,
        )

        if chapter is None:
            return None

        return self._chapter_position(
            chapter,
            position,
        )

    # =========================================================
    # Śloka Navigation
    # =========================================================

    def next_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the next śloka.
        """

        sloka_id = self._require_sloka_id(
            position,
        )

        sloka = self.repository.next_sloka(
            sloka_id,
        )

        if sloka is None:
            return None

        return self._sloka_position(
            sloka,
            position,
        )

    # ---------------------------------------------------------

    def previous_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous śloka.
        """

        sloka_id = self._require_sloka_id(
            position,
        )

        sloka = self.repository.previous_sloka(
            sloka_id,
        )

        if sloka is None:
            return None

        return self._sloka_position(
            sloka,
            position,
        )

    # =========================================================
    # Word Navigation
    # =========================================================

    def next_word(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the next word.
        """

        word_id = self._require_word_id(
            position,
        )

        word = self.repository.next_word(
            word_id,
        )

        if word is None:
            return None

        return self._word_position(
            word,
            position,
        )

    # ---------------------------------------------------------

    def previous_word(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous word.
        """

        word_id = self._require_word_id(
            position,
        )

        word = self.repository.previous_word(
            word_id,
        )

        if word is None:
            return None

        return self._word_position(
            word,
            position,
        )

    # =========================================================
    # Position Construction
    # =========================================================

    def _chapter_position(
        self,
        chapter: ChapterView,
        current: ReaderPosition,
    ) -> ReaderPosition:
        """
        Construct a new chapter position using the canonical
        ReaderPositionFactory contract.
        """

        return self.position_factory.chapter(
            purana_id=current.purana_id,
            chapter_id=chapter.identifier,
        )

    # ---------------------------------------------------------

    def _sloka_position(
        self,
        sloka: SlokaView,
        current: ReaderPosition,
    ) -> ReaderPosition:
        """
        Construct a new śloka position using the canonical
        hierarchy carried by SlokaView.
        """

        sloka_position = sloka.position

        chapter_id = (
            sloka_position.chapter_id
            or current.chapter_id
        )

        if chapter_id is None:
            raise ValueError(
                "Unable to determine chapter_id for sloka navigation."
            )

        return self.position_factory.sloka(
            purana_id=current.purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka.identifier,
        )

    # ---------------------------------------------------------

    def _word_position(
        self,
        word: WordView,
        current: ReaderPosition,
    ) -> ReaderPosition:
        """
        Construct a new word position using the canonical
        structural context carried by WordView.
        """

        word_position = word.position

        chapter_id = (
            word_position.chapter_id
            or current.chapter_id
        )

        sloka_id = (
            word_position.sloka_id
            or current.sloka_id
        )

        if chapter_id is None:
            raise ValueError(
                "Unable to determine chapter_id for word navigation."
            )

        if sloka_id is None:
            raise ValueError(
                "Unable to determine sloka_id for word navigation."
            )

        return self.position_factory.word(
            purana_id=current.purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word.identifier,
        )

    # =========================================================
    # Position Validation
    # =========================================================

    @staticmethod
    def _require_chapter_id(
        position: ReaderPosition,
    ) -> str:
        """
        Require a chapter identifier.
        """

        chapter_id = position.chapter_id

        if chapter_id is None:
            raise ValueError(
                "ReaderPosition does not contain a chapter_id."
            )

        return str(
            chapter_id,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _require_sloka_id(
        position: ReaderPosition,
    ) -> str:
        """
        Require a śloka identifier.
        """

        sloka_id = position.sloka_id

        if sloka_id is None:
            raise ValueError(
                "ReaderPosition does not contain a sloka_id."
            )

        return str(
            sloka_id,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _require_word_id(
        position: ReaderPosition,
    ) -> str:
        """
        Require a word identifier.
        """

        word_id = position.word_id

        if word_id is None:
            raise ValueError(
                "ReaderPosition does not contain a word_id."
            )

        return str(
            word_id,
        )
