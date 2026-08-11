from __future__ import annotations

"""
SanskritAI
==========

Reader Position Factory

Constructs canonical ReaderPosition objects.

This factory centralizes creation of immutable navigation
positions so every subsystem (Reader, AI, RAG, Search,
Bookmarks, Commentary, Cross References) uses the same
canonical identifiers.

Version
-------
v1.0.0
"""

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


class ReaderPositionFactory:
    """
    Factory for canonical ReaderPosition objects.
    """

    @staticmethod
    def chapter(
        *,
        corpus_id: str,
        purana_id: str,
        chapter_id: str,
    ) -> ReaderPosition:
        """
        Creates a chapter position.
        """

        return ReaderPosition(
            corpus_id=corpus_id,
            purana_id=purana_id,
            chapter_id=chapter_id,
        )

    @staticmethod
    def sloka(
        *,
        corpus_id: str,
        purana_id: str,
        chapter_id: str,
        sloka_id: str,
    ) -> ReaderPosition:
        """
        Creates a śloka position.
        """

        return ReaderPosition(
            corpus_id=corpus_id,
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
        )

    @staticmethod
    def word(
        *,
        corpus_id: str,
        purana_id: str,
        chapter_id: str,
        sloka_id: str,
        word_id: str,
    ) -> ReaderPosition:
        """
        Creates a word position.
        """

        return ReaderPosition(
            corpus_id=corpus_id,
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word_id,
        )
