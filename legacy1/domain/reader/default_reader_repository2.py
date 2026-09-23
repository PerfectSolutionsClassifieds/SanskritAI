from __future__ import annotations

"""
SanskritAI
==========

Default Reader Repository

Concrete Reader repository backed by the canonical Corpus Domain.

Corpus → Reader mapping
-----------------------

Corpus
    └── Document
         └── Section
              └── Verse
                   └── Paragraph
                        └── Line
                             └── Token

Reader projection
-----------------

Corpus
    Document       → ReaderDocument
    Section        → ChapterView
    Verse          → SlokaView
    Token          → WordView

The Reader Domain is a projection of the canonical Corpus Domain.
It does not duplicate or replace the Corpus hierarchy.

Version
-------
v2.1.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.corpus.models.corpus import (
    Corpus,
)

from SanskritAI.corpus.models.document import (
    Document,
)

from SanskritAI.corpus.models.section import (
    Section,
)

from SanskritAI.corpus.models.verse import (
    Verse,
)

from SanskritAI.corpus.models.token import (
    Token,
)

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

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass(slots=True)
class DefaultReaderRepository(
    ReaderRepository,
):
    """
    Default Reader repository backed by a canonical Corpus.

    Responsibilities
    ----------------

    • project Corpus objects into Reader views

    • preserve canonical Corpus ordering

    • provide canonical-ID lookup

    • resolve ReaderPosition objects

    • expose ReaderDocument as the Reader aggregate root

    This repository performs no linguistic analysis.

    Linguistic analysis belongs to the Resolution Kernel.
    """

    corpus: Corpus

    _document: ReaderDocument | None = field(
        init=False,
        default=None,
    )

    _chapters: dict[
        str,
        ChapterView,
    ] = field(
        init=False,
        default_factory=dict,
    )

    _slokas: dict[
        str,
        SlokaView,
    ] = field(
        init=False,
        default_factory=dict,
    )

    _words: dict[
        str,
        WordView,
    ] = field(
        init=False,
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
        self._build_reader_document()

    # ---------------------------------------------------------
    # Reader Document
    # ---------------------------------------------------------

    @property
    def document(
        self,
    ) -> ReaderDocument:
        """
        Immutable Reader aggregate root.
        """

        if self._document is None:
            raise RuntimeError(
                "Reader document has not been initialized."
            )

        return self._document

    # ---------------------------------------------------------

    def get_document(
        self,
        document_id: str | None = None,
    ) -> ReaderDocument:
        """
        Return the ReaderDocument.

        The current ReaderDocument represents the complete
        Corpus projection.

        When document_id is supplied, it is validated against
        the canonical Corpus documents.
        """

        if document_id is None:
            return self.document

        for document in self.corpus.documents:

            if str(document.identifier) == str(
                document_id,
            ):
                return self.document

        raise KeyError(
            f"Unknown document '{document_id}'."
        )

    # ---------------------------------------------------------
    # Chapters
    # ---------------------------------------------------------

    def get_chapter(
        self,
        chapter_id: str,
    ) -> ChapterView:
        """
        Return a ChapterView by canonical identifier.
        """

        key = str(chapter_id)

        try:
            return self._chapters[key]

        except KeyError as exc:

            raise KeyError(
                f"Unknown chapter '{chapter_id}'."
            ) from exc

    # ---------------------------------------------------------

    def get_chapters(
        self,
    ) -> tuple[
        ChapterView,
        ...
    ]:
        """
        Return all chapters in canonical Corpus order.
        """

        return self.document.chapters

    # ---------------------------------------------------------

    def get_chapter_slokas(
        self,
        chapter_id: str,
    ) -> tuple[
        SlokaView,
        ...
    ]:
        """
        Return all ślokas belonging to a chapter.
        """

        return self.get_chapter(
            chapter_id,
        ).slokas

    # ---------------------------------------------------------
    # Ślokas
    # ---------------------------------------------------------

    def get_sloka(
        self,
        sloka_id: str,
    ) -> SlokaView:
        """
        Return a SlokaView by canonical identifier.
        """

        key = str(sloka_id)

        try:
            return self._slokas[key]

        except KeyError as exc:

            raise KeyError(
                f"Unknown śloka '{sloka_id}'."
            ) from exc

    # ---------------------------------------------------------

    def get_slokas(
        self,
    ) -> tuple[
        SlokaView,
        ...
    ]:
        """
        Return every śloka in canonical Corpus order.
        """

        return tuple(
            self._slokas.values()
        )

    # ---------------------------------------------------------

    def get_sloka_words(
        self,
        sloka_id: str,
    ) -> tuple[
        WordView,
        ...
    ]:
        """
        Return every Token projected as a WordView.

        Punctuation is intentionally retained. The Reader
        projection represents the complete structural text.

        Callers interested only in lexical words should filter
        using the underlying Corpus token classification or
        WordView metadata.
        """

        return self.get_sloka(
            sloka_id,
        ).words

    # ---------------------------------------------------------
    # Words
    # ---------------------------------------------------------

    def get_word(
        self,
        word_id: str,
    ) -> WordView:
        """
        Return a WordView by canonical identifier.
        """

        key = str(word_id)

        try:
            return self._words[key]

        except KeyError as exc:

            raise KeyError(
                f"Unknown word '{word_id}'."
            ) from exc

    # ---------------------------------------------------------

    def get_words(
        self,
    ) -> tuple[
        WordView,
        ...
    ]:
        """
        Return all Reader words/tokens in canonical order.
        """

        return tuple(
            self._words.values()
        )

    # ---------------------------------------------------------
    # Position Resolution
    # ---------------------------------------------------------

    def resolve_position(
        self,
        position: ReaderPosition,
    ):
        """
        Resolve a canonical ReaderPosition.

        Resolution precedence:

            word_id
                ↓
            sloka_id
                ↓
            chapter_id
        """

        if position.word_id is not None:

            return self.get_word(
                position.word_id,
            )

        if position.sloka_id is not None:

            return self.get_sloka(
                position.sloka_id,
            )

        return self.get_chapter(
            position.chapter_id,
        )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def _build_reader_document(
        self,
    ) -> None:
        """
        Build the immutable Reader hierarchy from Corpus data.

        Corpus ordering is preserved exactly.
        """

        chapters: list[
            ChapterView
        ] = []

        for document in self.corpus.documents:

            for section in document.sections:

                chapter = self._build_chapter(
                    document=document,
                    section=section,
                )

                chapters.append(
                    chapter,
                )

        if not chapters:

            raise ValueError(
                "Corpus contains no sections for Reader projection."
            )

        first_chapter = chapters[0]

        position = ReaderPosition(
            corpus_id=str(
                self.corpus.id,
            ),
            purana_id=self._purana_identifier(),
            chapter_id=first_chapter.identifier,
            sloka_id=None,
            word_id=None,
        )

        self._document = ReaderDocument(
            identifier=str(
                self.corpus.id,
            ),
            position=position,
            title=self._corpus_title(),
            metadata=self._metadata_dict(
                self.corpus,
            ),
            chapters=tuple(
                chapters,
            ),
        )

    # ---------------------------------------------------------

    def _build_chapter(
        self,
        document: Document,
        section: Section,
    ) -> ChapterView:
        """
        Project one Corpus Section into ChapterView.
        """

        chapter_id = str(
            section.identifier,
        )

        slokas: list[
            SlokaView
        ] = []

        for verse in section.verses:

            sloka = self._build_sloka(
                document=document,
                section=section,
                verse=verse,
            )

            slokas.append(
                sloka,
            )

        position = ReaderPosition(
            corpus_id=str(
                self.corpus.id,
            ),
            purana_id=self._purana_identifier(),
            chapter_id=chapter_id,
            sloka_id=None,
            word_id=None,
        )

        chapter = ChapterView(
            identifier=chapter_id,
            position=position,
            title=self._title_from_metadata(
                section.metadata,
                fallback=chapter_id,
            ),
            metadata=self._metadata_dict(
                section,
            ),
            slokas=tuple(
                slokas,
            ),
        )

        self._chapters[
            chapter_id
        ] = chapter

        return chapter

    # ---------------------------------------------------------

    def _build_sloka(
        self,
        document: Document,
        section: Section,
        verse: Verse,
    ) -> SlokaView:
        """
        Project one Corpus Verse into SlokaView.
        """

        sloka_id = str(
            verse.identifier,
        )

        words = self._extract_words(
            document=document,
            section=section,
            verse=verse,
        )

        position = ReaderPosition(
            corpus_id=str(
                self.corpus.id,
            ),
            purana_id=self._purana_identifier(),
            chapter_id=str(
                section.identifier,
            ),
            sloka_id=sloka_id,
            word_id=None,
        )

        sloka = SlokaView(
            identifier=sloka_id,
            position=position,
            title=sloka_id,
            metadata=self._metadata_dict(
                verse,
            ),
            words=tuple(
                words,
            ),
            sloka_text=self._verse_text(
                verse,
            ),
            translation="",
        )

        self._slokas[
            sloka_id
        ] = sloka

        return sloka

    # ---------------------------------------------------------

    def _extract_words(
        self,
        document: Document,
        section: Section,
        verse: Verse,
    ) -> list[
        WordView
    ]:
        """
        Traverse:

            Verse
              ↓
            Paragraph
              ↓
            Line
              ↓
            Token

        using the canonical Corpus convenience aliases.
        """

        words: list[
            WordView
        ] = []

        for paragraph in verse.paragraphs:

            for line in paragraph.lines:

                for token in line.tokens:

                    word = self._build_word(
                        document=document,
                        section=section,
                        verse=verse,
                        token=token,
                    )

                    words.append(
                        word,
                    )

        return words

    # ---------------------------------------------------------

    def _build_word(
        self,
        document: Document,
        section: Section,
        verse: Verse,
        token: Token,
    ) -> WordView:
        """
        Project one Corpus Token into WordView.
        """

        word_id = str(
            token.identifier,
        )

        position = ReaderPosition(
            corpus_id=str(
                self.corpus.id,
            ),
            purana_id=self._purana_identifier(),
            chapter_id=str(
                section.identifier,
            ),
            sloka_id=str(
                verse.identifier,
            ),
            word_id=word_id,
        )

        word = WordView(
            identifier=word_id,
            position=position,
            title=token.text,
            metadata=self._metadata_dict(
                token,
            ),
            surface=token.text,
            transliteration="",
            normalized=token.normalized_text,
        )

        self._words[
            word_id
        ] = word

        return word

    # ---------------------------------------------------------
    # Corpus Helpers
    # ---------------------------------------------------------

    def _purana_identifier(
        self,
    ) -> str:
        """
        Resolve the canonical Purāṇa identifier.

        Corpus metadata may eventually expose purana_id
        explicitly. Until then the Corpus identifier is the
        canonical fallback.
        """

        metadata = getattr(
            self.corpus,
            "metadata",
            None,
        )

        purana_id = getattr(
            metadata,
            "purana_id",
            None,
        )

        if purana_id is not None:
            return str(
                purana_id,
            )

        return str(
            self.corpus.id,
        )

    # ---------------------------------------------------------

    def _corpus_title(
        self,
    ) -> str:
        return self._title_from_metadata(
            getattr(
                self.corpus,
                "metadata",
                None,
            ),
            fallback=str(
                self.corpus.id,
            ),
        )

    # ---------------------------------------------------------

    @staticmethod
    def _title_from_metadata(
        metadata: Any,
        fallback: str,
    ) -> str:
        """
        Extract a human-readable title from metadata.
        """

        if metadata is None:
            return fallback

        title = getattr(
            metadata,
            "title",
            None,
        )

        if title:
            return str(title)

        name = getattr(
            metadata,
            "name",
            None,
        )

        if name:
            return str(name)

        return fallback

    # ---------------------------------------------------------

    @staticmethod
    def _metadata_dict(
        node: Any,
    ) -> dict[str, Any] | None:
        """
        Convert a Corpus object's metadata to a dictionary.
        """

        metadata = getattr(
            node,
            "metadata",
            None,
        )

        if metadata is None:
            return None

        to_dict = getattr(
            metadata,
            "to_dict",
            None,
        )

        if callable(to_dict):
            return to_dict()

        return None

    # ---------------------------------------------------------

    @property
    def chapter_count(
        self,
    ) -> int:
        return self.document.chapter_count

    @property
    def sloka_count(
        self,
    ) -> int:
        return len(
            self._slokas,
        )

    @property
    def word_count(
        self,
    ) -> int:
        return len(
            self._words,
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        return self.chapter_count
