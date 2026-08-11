from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Canonical-ID navigation façade for the Reader Domain.

ReaderNavigator coordinates navigation between the
ReaderPosition model, ReaderPositionFactory, and
ReaderRepository.

Design
------

ReaderNavigator
      │
      ├── ReaderPositionFactory
      │       └── constructs immutable positions
      │
      └── ReaderRepository
              ├── resolves objects
              └── performs next/previous navigation

The navigator deliberately contains no positional-index
logic.

Canonical identifiers are the only navigation coordinates.

Version
-------
v2.3.0
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


@dataclass(
    slots=True,
)
class ReaderNavigator(
    Displayable,
):
    """
    Canonical Reader navigation façade.
    """

    repository: ReaderRepository

    position_factory: ReaderPositionFactory = (
        ReaderPositionFactory()
    )

    # =========================================================
    # Display
    # =========================================================

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
            "Canonical-ID navigation façade for the Reader Domain."
        )

    # =========================================================
    # Retrieval
    # =========================================================

    def get_document(
        self,
        document_id,
    ):
        """
        Retrieve a document by canonical identifier.
        """

        return self.repository.get_document(
            document_id,
        )

    # ---------------------------------------------------------

    def get_chapter(
        self,
        chapter_id,
    ):
        """
        Retrieve a chapter by canonical identifier.
        """

        return self.repository.get_chapter(
            chapter_id,
        )

    # ---------------------------------------------------------

    def get_sloka(
        self,
        sloka_id,
    ):
        """
        Retrieve a śloka by canonical identifier.
        """

        return self.repository.get_sloka(
            sloka_id,
        )

    # ---------------------------------------------------------

    def get_word(
        self,
        word_id,
    ):
        """
        Retrieve a word by canonical identifier.
        """

        return self.repository.get_word(
            word_id,
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

        The repository remains responsible for determining
        which chapter follows the supplied chapter.
        """

        if position.chapter_id is None:
            raise ValueError(
                "A chapter_id is required for chapter navigation."
            )

        chapter = self.repository.next_chapter(
            position.chapter_id,
        )

        if chapter is None:
            return None

        return self.position_factory.chapter(
            purana_id=position.purana_id,
            chapter_id=self._identifier(
                chapter,
            ),
        )

    # ---------------------------------------------------------

    def previous_chapter(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous chapter.
        """

        if position.chapter_id is None:
            raise ValueError(
                "A chapter_id is required for chapter navigation."
            )

        chapter = self.repository.previous_chapter(
            position.chapter_id,
        )

        if chapter is None:
            return None

        return self.position_factory.chapter(
            purana_id=position.purana_id,
            chapter_id=self._identifier(
                chapter,
            ),
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

        if position.sloka_id is None:
            raise ValueError(
                "A sloka_id is required for śloka navigation."
            )

        sloka = self.repository.next_sloka(
            position.sloka_id,
        )

        if sloka is None:
            return None

        return self.position_factory.sloka(
            purana_id=position.purana_id,
            chapter_id=self._require_parent_id(
                position.chapter_id,
                "chapter_id",
            ),
            sloka_id=self._identifier(
                sloka,
            ),
        )

    # ---------------------------------------------------------

    def previous_sloka(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous śloka.
        """

        if position.sloka_id is None:
            raise ValueError(
                "A sloka_id is required for śloka navigation."
            )

        sloka = self.repository.previous_sloka(
            position.sloka_id,
        )

        if sloka is None:
            return None

        return self.position_factory.sloka(
            purana_id=position.purana_id,
            chapter_id=self._require_parent_id(
                position.chapter_id,
                "chapter_id",
            ),
            sloka_id=self._identifier(
                sloka,
            ),
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

        if position.word_id is None:
            raise ValueError(
                "A word_id is required for word navigation."
            )

        word = self.repository.next_word(
            position.word_id,
        )

        if word is None:
            return None

        return self.position_factory.word(
            purana_id=position.purana_id,
            chapter_id=self._require_parent_id(
                position.chapter_id,
                "chapter_id",
            ),
            sloka_id=self._require_parent_id(
                position.sloka_id,
                "sloka_id",
            ),
            word_id=self._identifier(
                word,
            ),
        )

    # ---------------------------------------------------------

    def previous_word(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Return the position of the previous word.
        """

        if position.word_id is None:
            raise ValueError(
                "A word_id is required for word navigation."
            )

        word = self.repository.previous_word(
            position.word_id,
        )

        if word is None:
            return None

        return self.position_factory.word(
            purana_id=position.purana_id,
            chapter_id=self._require_parent_id(
                position.chapter_id,
                "chapter_id",
            ),
            sloka_id=self._require_parent_id(
                position.sloka_id,
                "sloka_id",
            ),
            word_id=self._identifier(
                word,
            ),
        )

    # =========================================================
    # Position Construction
    # =========================================================

    def chapter_position(
        self,
        *,
        purana_id,
        chapter_id,
    ) -> ReaderPosition:
        """
        Construct an immutable chapter position.
        """

        return self.position_factory.chapter(
            purana_id=purana_id,
            chapter_id=chapter_id,
        )

    # ---------------------------------------------------------

    def sloka_position(
        self,
        *,
        purana_id,
        chapter_id,
        sloka_id,
    ) -> ReaderPosition:
        """
        Construct an immutable śloka position.
        """

        return self.position_factory.sloka(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
        )

    # ---------------------------------------------------------

    def word_position(
        self,
        *,
        purana_id,
        chapter_id,
        sloka_id,
        word_id,
    ) -> ReaderPosition:
        """
        Construct an immutable word position.
        """

        return self.position_factory.word(
            purana_id=purana_id,
            chapter_id=chapter_id,
            sloka_id=sloka_id,
            word_id=word_id,
        )

    # =========================================================
    # Generic Position Navigation
    # =========================================================

    def next(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate one step forward according to the position
        depth.
        """

        if position.is_word:
            return self.next_word(
                position,
            )

        if position.is_sloka:
            return self.next_sloka(
                position,
            )

        if position.is_chapter:
            return self.next_chapter(
                position,
            )

        raise ValueError(
            "A ReaderPosition must identify at least "
            "a chapter, śloka, or word."
        )

    # ---------------------------------------------------------

    def previous(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition | None:
        """
        Navigate one step backward according to the position
        depth.
        """

        if position.is_word:
            return self.previous_word(
                position,
            )

        if position.is_sloka:
            return self.previous_sloka(
                position,
            )

        if position.is_chapter:
            return self.previous_chapter(
                position,
            )

        raise ValueError(
            "A ReaderPosition must identify at least "
            "a chapter, śloka, or word."
        )

    # =========================================================
    # Internal Identifier Extraction
    # =========================================================

    @staticmethod
    def _identifier(
        value,
    ):
        """
        Extract a canonical identifier from a repository
        result.

        Supports canonical corpus nodes exposing either:

            .id

        or

            .identifier

        This keeps the navigator tolerant of the current
        Corpus Domain naming conventions.
        """

        if hasattr(
            value,
            "id",
        ):
            return value.id

        if hasattr(
            value,
            "identifier",
        ):
            return value.identifier

        raise TypeError(
            "Repository navigation result does not expose "
            "a canonical id or identifier."
        )

    # ---------------------------------------------------------

    @staticmethod
    def _require_parent_id(
        value,
        name: str,
    ):
        """
        Require a parent identifier when constructing a
        descendant ReaderPosition.
        """

        if value is None:
            raise ValueError(
                f"{name} is required to construct "
                "a descendant ReaderPosition."
            )

        return value

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:

        return self.display_text
