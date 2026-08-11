from __future__ import annotations

"""
SanskritAI
==========

Reader Navigator

Canonical-ID navigation façade for the Reader Domain.

The navigator intentionally delegates navigation to
ReaderRepository.

Current repository contract
---------------------------

    get_document(document_id)

    get_chapter(chapter_id)
    get_sloka(sloka_id)
    get_word(word_id)

    next_chapter(chapter_id)
    previous_chapter(chapter_id)

    next_sloka(sloka_id)
    previous_sloka(sloka_id)

    next_word(word_id)
    previous_word(word_id)

Design Principle
----------------

ReaderNavigator owns navigation semantics at the Reader
Domain level, while ReaderRepository owns retrieval and
navigation against the underlying corpus projection.

The navigator does NOT:

    • use array indices
    • inspect Corpus internals
    • reconstruct repository objects
    • assume repository methods that are not part of the
      ReaderRepository contract

Canonical identifiers are therefore the only navigation
coordinates exposed by this class.

Version
-------
v2.3.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import (
    Displayable,
)

from SanskritAI.domain.reader.reader_repository import (
    ReaderRepository,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(
    slots=True,
)
class ReaderNavigator(
    Displayable,
):
    """
    Canonical-ID navigation façade.

    ReaderNavigator is deliberately thin.

    It delegates all actual retrieval/navigation to the
    ReaderRepository.
    """

    repository: ReaderRepository

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
    # Document
    # =========================================================

    def get_document(
        self,
        document_id,
    ):
        """
        Resolve a Reader document by canonical identifier.
        """

        return self.repository.get_document(
            document_id,
        )

    # =========================================================
    # Chapter
    # =========================================================

    def get_chapter(
        self,
        chapter_id,
    ):
        """
        Resolve a chapter by canonical identifier.
        """

        return self.repository.get_chapter(
            chapter_id,
        )

    # ---------------------------------------------------------

    def next_chapter(
        self,
        chapter_id,
    ):
        """
        Navigate to the chapter following chapter_id.
        """

        return self.repository.next_chapter(
            chapter_id,
        )

    # ---------------------------------------------------------

    def previous_chapter(
        self,
        chapter_id,
    ):
        """
        Navigate to the chapter preceding chapter_id.
        """

        return self.repository.previous_chapter(
            chapter_id,
        )

    # =========================================================
    # Śloka
    # =========================================================

    def get_sloka(
        self,
        sloka_id,
    ):
        """
        Resolve a śloka by canonical identifier.
        """

        return self.repository.get_sloka(
            sloka_id,
        )

    # ---------------------------------------------------------

    def next_sloka(
        self,
        sloka_id,
    ):
        """
        Navigate to the śloka following sloka_id.
        """

        return self.repository.next_sloka(
            sloka_id,
        )

    # ---------------------------------------------------------

    def previous_sloka(
        self,
        sloka_id,
    ):
        """
        Navigate to the śloka preceding sloka_id.
        """

        return self.repository.previous_sloka(
            sloka_id,
        )

    # =========================================================
    # Word
    # =========================================================

    def get_word(
        self,
        word_id,
    ):
        """
        Resolve a word by canonical identifier.
        """

        return self.repository.get_word(
            word_id,
        )

    # ---------------------------------------------------------

    def next_word(
        self,
        word_id,
    ):
        """
        Navigate to the word following word_id.
        """

        return self.repository.next_word(
            word_id,
        )

    # ---------------------------------------------------------

    def previous_word(
        self,
        word_id,
    ):
        """
        Navigate to the word preceding word_id.
        """

        return self.repository.previous_word(
            word_id,
        )

    # =========================================================
    # Position Helpers
    # =========================================================

    def chapter_id_from_position(
        self,
        position: ReaderPosition,
    ):
        """
        Extract the canonical chapter identifier from a
        ReaderPosition.

        This helper keeps callers independent of the concrete
        ReaderPosition implementation.
        """

        return position.chapter_id

    # ---------------------------------------------------------

    def sloka_id_from_position(
        self,
        position: ReaderPosition,
    ):
        """
        Extract the canonical śloka identifier.
        """

        return position.sloka_id

    # ---------------------------------------------------------

    def word_id_from_position(
        self,
        position: ReaderPosition,
    ):
        """
        Extract the canonical word identifier.
        """

        return position.word_id

    # =========================================================
    # Position-Based Navigation
    # =========================================================

    def next_from_position(
        self,
        position: ReaderPosition,
    ):
        """
        Navigate forward from a ReaderPosition.

        The navigation level is determined by the deepest
        canonical identifier available in the position.

        Word position
            → next word

        Śloka position
            → next śloka

        Chapter position
            → next chapter
        """

        if position.word_id is not None:

            return self.next_word(
                position.word_id,
            )

        if position.sloka_id is not None:

            return self.next_sloka(
                position.sloka_id,
            )

        if position.chapter_id is not None:

            return self.next_chapter(
                position.chapter_id,
            )

        raise ValueError(
            "ReaderPosition does not contain a navigable "
            "chapter_id, sloka_id, or word_id."
        )

    # ---------------------------------------------------------

    def previous_from_position(
        self,
        position: ReaderPosition,
    ):
        """
        Navigate backward from a ReaderPosition.

        The navigation level is determined by the deepest
        canonical identifier available in the position.
        """

        if position.word_id is not None:

            return self.previous_word(
                position.word_id,
            )

        if position.sloka_id is not None:

            return self.previous_sloka(
                position.sloka_id,
            )

        if position.chapter_id is not None:

            return self.previous_chapter(
                position.chapter_id,
            )

        raise ValueError(
            "ReaderPosition does not contain a navigable "
            "chapter_id, sloka_id, or word_id."
        )

    # =========================================================
    # Convenience Aliases
    # =========================================================

    def chapter(
        self,
        chapter_id,
    ):
        """
        Short alias for get_chapter().
        """

        return self.get_chapter(
            chapter_id,
        )

    # ---------------------------------------------------------

    def sloka(
        self,
        sloka_id,
    ):
        """
        Short alias for get_sloka().
        """

        return self.get_sloka(
            sloka_id,
        )

    # ---------------------------------------------------------

    def word(
        self,
        word_id,
    ):
        """
        Short alias for get_word().
        """

        return self.get_word(
            word_id,
        )

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:

        return self.display_text
