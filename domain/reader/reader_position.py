from __future__ import annotations

"""
SanskritAI
==========

Reader Position

Immutable canonical navigation cursor for the Reader Domain.

A ReaderPosition identifies a location in the corpus using
canonical identifiers rather than positional indices.

Hierarchy
---------

Purāṇa
    └── Chapter
          └── Śloka
                └── Word

A position may represent:

    • purāṇa level
    • chapter level
    • śloka level
    • word level

The ``identifier`` property provides the active identifier for
the current level and acts as a compatibility alias for
``canonical_id``.

Version
-------
v2.3.0
"""

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ReaderPosition:
    """
    Immutable canonical Reader position.
    """

    purana_id: str

    chapter_id: str | None = None

    sloka_id: str | None = None

    word_id: str | None = None

    # =========================================================
    # Validation
    # =========================================================

    def __post_init__(self) -> None:
        """
        Validate the hierarchical identifier structure.
        """

        if not self.purana_id:
            raise ValueError(
                "purana_id must not be empty."
            )

        if (
            self.sloka_id is not None
            and self.chapter_id is None
        ):
            raise ValueError(
                "sloka_id requires chapter_id."
            )

        if (
            self.word_id is not None
            and self.sloka_id is None
        ):
            raise ValueError(
                "word_id requires sloka_id."
            )

    # =========================================================
    # Level
    # =========================================================

    @property
    def level(
        self,
    ) -> str:
        """
        Return the deepest level represented by this position.
        """

        if self.word_id is not None:
            return "word"

        if self.sloka_id is not None:
            return "sloka"

        if self.chapter_id is not None:
            return "chapter"

        return "purana"

    # =========================================================
    # Convenience Predicates
    # =========================================================

    @property
    def is_purana(
        self,
    ) -> bool:
        """
        Return True if this position is at purāṇa level.
        """

        return self.level == "purana"

    # ---------------------------------------------------------

    @property
    def is_chapter(
        self,
    ) -> bool:
        """
        Return True if this position is at chapter level.
        """

        return self.level == "chapter"

    # ---------------------------------------------------------

    @property
    def is_sloka(
        self,
    ) -> bool:
        """
        Return True if this position is at śloka level.
        """

        return self.level == "sloka"

    # ---------------------------------------------------------

    @property
    def is_word(
        self,
    ) -> bool:
        """
        Return True if this position is at word level.
        """

        return self.level == "word"

    # =========================================================
    # Canonical Identity
    # =========================================================

    @property
    def canonical_id(
        self,
    ) -> str:
        """
        Return the identifier of the deepest active level.
        """

        if self.word_id is not None:
            return self.word_id

        if self.sloka_id is not None:
            return self.sloka_id

        if self.chapter_id is not None:
            return self.chapter_id

        return self.purana_id

    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        """
        Return the active identifier for this position.

        This is a compatibility and convenience alias for
        ``canonical_id``.

        Examples
        --------
        chapter position:
            identifier == chapter_id

        śloka position:
            identifier == sloka_id

        word position:
            identifier == word_id
        """

        return self.canonical_id

    # =========================================================
    # Parent Positions
    # =========================================================

    @property
    def chapter_position(
        self,
    ) -> "ReaderPosition":
        """
        Return the chapter-level position.
        """

        if self.chapter_id is None:
            raise ValueError(
                "Position does not identify a chapter."
            )

        return ReaderPosition(
            purana_id=self.purana_id,
            chapter_id=self.chapter_id,
        )

    # ---------------------------------------------------------

    @property
    def sloka_position(
        self,
    ) -> "ReaderPosition":
        """
        Return the śloka-level position.
        """

        if self.sloka_id is None:
            raise ValueError(
                "Position does not identify a śloka."
            )

        return ReaderPosition(
            purana_id=self.purana_id,
            chapter_id=self.chapter_id,
            sloka_id=self.sloka_id,
        )

    # ---------------------------------------------------------

    @property
    def word_position(
        self,
    ) -> "ReaderPosition":
        """
        Return the word-level position.
        """

        if self.word_id is None:
            raise ValueError(
                "Position does not identify a word."
            )

        return ReaderPosition(
            purana_id=self.purana_id,
            chapter_id=self.chapter_id,
            sloka_id=self.sloka_id,
            word_id=self.word_id,
        )

    # =========================================================
    # Serialization
    # =========================================================

    def to_dict(
        self,
    ) -> dict[str, str | None]:
        """
        Serialize the canonical position.
        """

        return {
            "purana_id": self.purana_id,
            "chapter_id": self.chapter_id,
            "sloka_id": self.sloka_id,
            "word_id": self.word_id,
            "level": self.level,
            "canonical_id": self.canonical_id,
            "identifier": self.identifier,
        }

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:
        """
        Return the canonical identifier.
        """

        return self.canonical_id

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Return a developer-friendly representation.
        """

        return (
            "ReaderPosition("
            f"purana_id={self.purana_id!r}, "
            f"chapter_id={self.chapter_id!r}, "
            f"sloka_id={self.sloka_id!r}, "
            f"word_id={self.word_id!r})"
        )
