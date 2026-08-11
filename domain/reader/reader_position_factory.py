from __future__ import annotations

"""
SanskritAI
==========

Reader Position Factory

Centralized construction of immutable ReaderPosition objects.

All ReaderPosition creation should pass through this factory
when constructing navigation positions from domain identifiers.

Version
-------
v2.3.0
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
    Factory for canonical ReaderPosition objects.
    """

    # =========================================================
    # Normalization
    # =========================================================

    @staticmethod
    def _require_id(
        value,
        name: str,
    ) -> str:
        """
        Validate and normalize an identifier.
        """

        if value is None:
            raise ValueError(
                f"{name} must not be None."
            )

        normalized = str(value).strip()

        if not normalized:
            raise ValueError(
                f"{name} must not be empty."
            )

        return normalized

    # =========================================================
    # Purāṇa
    # =========================================================

    @classmethod
    def purana(
        cls,
        *,
        purana_id,
    ) -> ReaderPosition:
        """
        Construct a purāṇa-level position.
        """

        return ReaderPosition(
            purana_id=cls._require_id(
                purana_id,
                "purana_id",
            ),
        )

    # =========================================================
    # Chapter
    # =========================================================

    @classmethod
    def chapter(
        cls,
        *,
        purana_id,
        chapter_id,
    ) -> ReaderPosition:
        """
        Construct a chapter-level position.
        """

        return ReaderPosition(
            purana_id=cls._require_id(
                purana_id,
                "purana_id",
            ),
            chapter_id=cls._require_id(
                chapter_id,
                "chapter_id",
            ),
        )

    # =========================================================
    # Śloka
    # =========================================================

    @classmethod
    def sloka(
        cls,
        *,
        purana_id,
        chapter_id,
        sloka_id,
    ) -> ReaderPosition:
        """
        Construct a śloka-level position.
        """

        return ReaderPosition(
            purana_id=cls._require_id(
                purana_id,
                "purana_id",
            ),
            chapter_id=cls._require_id(
                chapter_id,
                "chapter_id",
            ),
            sloka_id=cls._require_id(
                sloka_id,
                "sloka_id",
            ),
        )

    # =========================================================
    # Word
    # =========================================================

    @classmethod
    def word(
        cls,
        *,
        purana_id,
        chapter_id,
        sloka_id,
        word_id,
    ) -> ReaderPosition:
        """
        Construct a word-level position.
        """

        return ReaderPosition(
            purana_id=cls._require_id(
                purana_id,
                "purana_id",
            ),
            chapter_id=cls._require_id(
                chapter_id,
                "chapter_id",
            ),
            sloka_id=cls._require_id(
                sloka_id,
                "sloka_id",
            ),
            word_id=cls._require_id(
                word_id,
                "word_id",
            ),
        )
