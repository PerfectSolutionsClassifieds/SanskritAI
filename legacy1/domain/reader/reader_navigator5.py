from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Thin navigation service for the Reader Domain.

The ReaderNavigator does not navigate the underlying Corpus
hierarchy directly.

Instead:

    ReaderPosition
          |
          v
    ReaderNavigator
          |
          v
    ReaderRepository
          |
          v
    ChapterView / SlokaView / WordView
          |
          v
    ReaderPositionFactory
          |
          v
    next ReaderPosition

Navigation is therefore based entirely on canonical identifiers.

No positional indices are stored or exposed by this class.

Version
-------
v3.0.0
"""

from dataclasses import dataclass

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

    The Navigator owns cursor movement, while the repository
    owns corpus ordering and object retrieval.

    Responsibilities
    ----------------

    • navigate chapters

    • navigate ślokas

    • navigate words

    • preserve ReaderPosition immutability

    • delegate ordering decisions to ReaderRepository

    • construct new positions through ReaderPositionFactory

    Non-responsibilities
    -------------------

    • corpus traversal

    • linguistic analysis

    • lexical resolution

    • morphology

    • sandhi

    • samāsa

    • semantic analysis

    • commentary

    • AI reasoning
    """

    repository: ReaderRepository

    position_factory: ReaderPositionFactory

    # =========================================================
    # Chapter Navigation
    # =========================================================

    def next_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Move to the next chapter.

        The repository determines the canonical ordering.

        Parameters
        ----------
        position:
            Current ReaderPosition.

        Returns
        -------
        ReaderPosition | None
            Position of the next chapter, or None when the
            current chapter is the final chapter.
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
        Move to the previous chapter.

        Returns None when the current chapter is the first
        chapter.
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
        Move to the next śloka.

        The repository determines the canonical ordering.
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
        Move to the previous śloka.
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
        Move to the next word/token.

        The repository determines the canonical traversal
        order across the Reader projection.
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
        Move to the previous word/token.
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
        Construct a new immutable chapter position.

        Corpus and Purāṇa identity are preserved from the current
        cursor while the canonical chapter identifier comes from
        the repository result.
        """

        return self.position_factory.chapter(
            corpus_id=current.corpus_id,
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
        Construct a new immutable śloka position.

        Chapter identity is taken from the returned SlokaView
        whenever its position provides it; otherwise the current
        chapter context is preserved.
        """

        chapter_id = (
            sloka.position.chapter_id
            or current.chapter_id
        )

        return self.position_factory.sloka(
            corpus_id=current.corpus_id,
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
        Construct a new immutable word position.

        The returned WordView carries the canonical structural
        context of the word. That context is preferred over
        reconstructing it from indices.
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

        return self.position_factory.word(
            corpus_id=current.corpus_id,
            purana_id=current.purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word.identifier,
        )

    # =========================================================
    # Validation
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
