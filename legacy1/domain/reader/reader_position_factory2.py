from __future__ import annotations

"""
SanskritAI
==========

Reader Position Factory

Centralized construction of immutable ReaderPosition objects.

The Reader Domain uses canonical identifiers rather than
array/list indices for navigation.

Canonical hierarchy
-------------------

Purāṇa
    ↓
Document
    ↓
Chapter
    ↓
Śloka
    ↓
Word

The factory provides the canonical construction points for:

    • chapter positions
    • śloka positions
    • word positions

Design Principle
----------------

ReaderPositionFactory is intentionally small.

It does NOT:

    • retrieve corpus objects
    • perform navigation
    • inspect repository internals
    • calculate array indices
    • resolve linguistic information

Those responsibilities belong to the ReaderRepository,
ReaderNavigator, and Resolution layers respectively.

Version
-------
v2.1.0
"""

from dataclasses import dataclass

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderPositionFactory:
    """
    Canonical factory for ReaderPosition objects.
    """

    # =========================================================
    # Chapter Position
    # =========================================================

    @staticmethod
    def chapter(
        *,
        purana_id,
        chapter_id,
    ) -> ReaderPosition:
        """
        Create a ReaderPosition representing a chapter.

        Parameters
        ----------
        purana_id:
            Canonical identifier of the Purāṇa/corpus.

        chapter_id:
            Canonical identifier of the chapter.

        Returns
        -------
        ReaderPosition
            Immutable chapter-level reader position.
        """

        return ReaderPosition(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=None,
            word_id=None,
        )

    # =========================================================
    # Śloka Position
    # =========================================================

    @staticmethod
    def sloka(
        *,
        purana_id,
        chapter_id,
        sloka_id,
    ) -> ReaderPosition:
        """
        Create a ReaderPosition representing a śloka.

        The parent chapter identifier is retained so that the
        resulting position remains self-describing.
        """

        return ReaderPosition(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=None,
        )

    # =========================================================
    # Word Position
    # =========================================================

    @staticmethod
    def word(
        *,
        purana_id,
        chapter_id,
        sloka_id,
        word_id,
    ) -> ReaderPosition:
        """
        Create a ReaderPosition representing a word.

        The complete canonical ancestry is retained:

            Purāṇa
                → Chapter
                    → Śloka
                        → Word
        """

        return ReaderPosition(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word_id,
        )
