from __future__ import annotations

"""
SanskritAI
==========

Reader Position Factory

Centralized construction of immutable ReaderPosition objects.

Version
-------
v2.2.0
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
    ):

        if value is None:
            raise ValueError(
                f"{name} must not be None."
            )

        if not str(value).strip():
            raise ValueError(
                f"{name} must not be empty."
            )

        return str(value)

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
