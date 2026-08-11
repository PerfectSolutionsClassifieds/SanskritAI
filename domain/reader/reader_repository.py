from __future__ import annotations

"""
SanskritAI
==========

Reader Repository

Defines the domain contract used by the Reader Layer for
navigating the canonical Sanskrit corpus.

The ReaderRepository deliberately hides the underlying corpus
implementation (JSON, in-memory objects, PostgreSQL, etc.) and
returns Reader-facing view objects.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

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


class ReaderRepository(ABC):
    """
    Domain abstraction for corpus navigation.
    """

    # ---------------------------------------------------------
    # Documents
    # ---------------------------------------------------------

    @abstractmethod
    def get_document(
        self,
        document_id: str,
    ) -> ReaderDocument:
        """
        Returns a reader document.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Chapters
    # ---------------------------------------------------------

    @abstractmethod
    def get_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView:
        """
        Returns a chapter view.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Ślokas
    # ---------------------------------------------------------

    @abstractmethod
    def get_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView:
        """
        Returns a śloka view.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Words
    # ---------------------------------------------------------

    @abstractmethod
    def get_word(
        self,
        word_id: str,
    ) -> WordView:
        """
        Returns a word view.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    @abstractmethod
    def next_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView | None:
        raise NotImplementedError

    @abstractmethod
    def previous_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView | None:
        raise NotImplementedError

    @abstractmethod
    def next_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView | None:
        raise NotImplementedError

    @abstractmethod
    def previous_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView | None:
        raise NotImplementedError

    @abstractmethod
    def next_word(
        self,
        word_id: str,
    ) -> WordView | None:
        raise NotImplementedError

    @abstractmethod
    def previous_word(
        self,
        word_id: str,
    ) -> WordView | None:
        raise NotImplementedError
