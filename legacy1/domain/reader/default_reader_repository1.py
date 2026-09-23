from __future__ import annotations

"""
SanskritAI
==========

Default Reader Repository

Default implementation of ReaderRepository backed by the
canonical Corpus model.

At the current architectural stage this class acts as the
bridge between the Reader Domain and the Corpus Domain.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.corpus.models.corpus import Corpus

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
    frozen=True,
    slots=True,
)
class DefaultReaderRepository(
    ReaderRepository,
):
    """
    Default corpus-backed implementation.

    NOTE
    ----
    The navigation methods currently act as placeholders until
    the canonical Corpus Registry / indexing subsystem is
    connected.
    """

    corpus: Corpus

    # ---------------------------------------------------------
    # Documents
    # ---------------------------------------------------------

    def get_document(
        self,
        document_id: str,
    ) -> ReaderDocument:
        raise NotImplementedError(
            "Document lookup will be connected to the "
            "Corpus Registry."
        )

    # ---------------------------------------------------------

    def get_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView:
        raise NotImplementedError

    # ---------------------------------------------------------

    def get_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView:
        raise NotImplementedError

    # ---------------------------------------------------------

    def get_word(
        self,
        word_id: str,
    ) -> WordView:
        raise NotImplementedError

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def next_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView | None:
        raise NotImplementedError

    def previous_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView | None:
        raise NotImplementedError

    def next_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView | None:
        raise NotImplementedError

    def previous_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView | None:
        raise NotImplementedError

    def next_word(
        self,
        word_id: str,
    ) -> WordView | None:
        raise NotImplementedError

    def previous_word(
        self,
        word_id: str,
    ) -> WordView | None:
        raise NotImplementedError
