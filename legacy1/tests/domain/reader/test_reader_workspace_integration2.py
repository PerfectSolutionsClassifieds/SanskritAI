from __future__ import annotations

import pytest

from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse_metadata import VerseMetadata
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.token_metadata import TokenMetadata

from SanskritAI.domain.reader.default_reader_repository import (
    DefaultReaderRepository,
)
from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_navigator import ReaderNavigator
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import (
    ReaderSelectionContext,
)
from SanskritAI.domain.reader.reader_workspace import ReaderWorkspace


def _token(identifier: str, text: str, position: int) -> Token:
    return Token(
        identifier=identifier,
        metadata=TokenMetadata(
            identifier=identifier,
            token_index=position,
            normalized_text=text,
        ),
    )


def _line(identifier: str, *tokens: Token) -> Line:
    line = Line(
        identifier=identifier,
        metadata=LineMetadata(),
    )
    for token in tokens:
        line.add_token(token)
    return line


def _paragraph(identifier: str, *lines: Line) -> Paragraph:
    paragraph = Paragraph(
        identifier=identifier,
        metadata=ParagraphMetadata(),
    )
    for line in lines:
        paragraph.add_line(line)
    return paragraph


def _verse(identifier: str, *paragraphs: Paragraph) -> Verse:
    verse = Verse(
        identifier=identifier,
        metadata=VerseMetadata(),
    )
    for paragraph in paragraphs:
        verse.add_paragraph(paragraph)
    return verse


def _section(identifier: str, *verses: Verse) -> Section:
    section = Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )
    for verse in verses:
        section.add_verse(verse)
    return section


def _document(identifier: str, *sections: Section) -> Document:
    document = Document(
        identifier=identifier,
        metadata=DocumentMetadata(title=identifier),
    )
    for section in sections:
        document.add_section(section)
    return document


@pytest.fixture
def corpus() -> Corpus:
    sloka_1 = _verse(
        "sloka-1",
        _paragraph(
            "paragraph-1",
            _line(
                "line-1",
                _token("word-1", "धर्मः", 1),
                _token("word-2", "रक्षति", 2),
            ),
        ),
    )
    sloka_2 = _verse(
        "sloka-2",
        _paragraph(
            "paragraph-2",
            _line(
                "line-2",
                _token("word-3", "धर्मः", 1),
                _token("word-4", "सर्वदा", 2),
            ),
        ),
    )
    sloka_3 = _verse(
        "sloka-3",
        _paragraph(
            "paragraph-3",
            _line(
                "line-3",
                _token("word-5", "सत्यं", 1),
                _token("word-6", "वद", 2),
            ),
        ),
    )

    chapter_1 = _section(
        "chapter-1",
        sloka_1,
        sloka_2,
    )
    chapter_2 = _section(
        "chapter-2",
        sloka_3,
    )

    document = _document(
        "document-1",
        chapter_1,
        chapter_2,
    )

    corpus = Corpus(
        id="corpus-1",
        metadata=CorpusMetadata(
            title="Test Purāṇa",
        ),
    )
    corpus.add_document(document)

    return corpus


@pytest.fixture
def repository(corpus) -> DefaultReaderRepository:
    return DefaultReaderRepository(
        corpus=corpus,
    )


@pytest.fixture
def navigator(repository) -> ReaderNavigator:
    return ReaderNavigator(
        repository=repository,
    )


@pytest.fixture
def engine(repository, navigator) -> ReaderEngine:
    return ReaderEngine(
        repository=repository,
        navigator=navigator,
    )


@pytest.fixture
def position() -> ReaderPosition:
    return ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )


@pytest.fixture
def workspace(
    engine,
    position,
) -> ReaderWorkspace:
    return ReaderWorkspace.open(
        engine,
        position,
    )


def test_workspace_open_integrates_with_reader_controller(
    workspace,
    engine,
    position,
):
    assert isinstance(workspace, ReaderWorkspace)
    assert isinstance(workspace.controller, ReaderController)
    assert workspace.engine is engine
    assert workspace.position == position


def test_workspace_exposes_active_reader_session(workspace, engine):
    assert workspace.session is workspace.controller.session
    assert workspace.engine is workspace.session.engine
    assert workspace.engine is engine


def test_workspace_exposes_resolved_reader_state(
    workspace,
    position,
):
    assert workspace.has_position is True
    assert workspace.current_position == position
    assert workspace.selection is not None
    assert isinstance(
        workspace.selection,
        ReaderSelectionContext,
    )


def test_workspace_selection_tracks_session_position(
    workspace,
):
    initial_position = workspace.current_position
    initial_selection = workspace.selection

    workspace.controller.next()

    assert workspace.current_position is workspace.session.current_position
    assert workspace.current_position != initial_position
    assert workspace.selection is not initial_selection
    assert workspace.selection.position is workspace.current_position


def test_workspace_preserves_controller_navigation_semantics(
    workspace,
    position,
):
    assert workspace.current_position == position

    result = workspace.controller.next()

    assert result is not None
    assert result.identifier == "word-2"
    assert workspace.current_position is workspace.controller.current_position
    assert workspace.current_position.identifier == "word-2"

    result = workspace.controller.previous()

    assert result is not None
    assert result.identifier == "word-1"
    assert workspace.current_position is workspace.controller.current_position
    assert workspace.current_position.identifier == "word-1"


def test_workspace_preserves_browser_history_semantics(
    workspace,
    position,
):
    initial_position = workspace.current_position

    workspace.controller.next()

    next_position = workspace.current_position

    assert next_position is not None
    assert next_position != initial_position
    assert workspace.can_go_back is True

    workspace.controller.back()

    assert workspace.current_position == initial_position

    assert workspace.can_go_forward is True

    workspace.controller.forward()

    assert workspace.current_position == next_position


def test_workspace_state_remains_controller_owned(
    workspace,
):
    assert workspace.position is workspace.controller.current_position
    assert workspace.result is workspace.controller.current_result
    assert workspace.has_position == workspace.controller.has_position
    assert workspace.has_result == workspace.controller.has_result
    assert workspace.succeeded == workspace.controller.succeeded
    assert workspace.can_go_back == workspace.controller.can_go_back
    assert workspace.can_go_forward == workspace.controller.can_go_forward
