from __future__ import annotations
"""SanskritAI
==========
Reader Controller Integration Tests
Verifies:
Corpus → DefaultReaderRepository → ReaderNavigator → ReaderEngine
→ ReaderSession → ReaderController
"""
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
from SanskritAI.domain.reader.reader_controller import ReaderController
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.default_reader_repository import DefaultReaderRepository
from SanskritAI.domain.reader.reader_navigator import ReaderNavigator
from SanskritAI.domain.reader.reader_position import ReaderPosition
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
    line = Line(identifier=identifier, metadata=LineMetadata())
    for token in tokens:
        line.add_token(token)
    return line
def _paragraph(identifier: str, *lines: Line) -> Paragraph:
    paragraph = Paragraph(identifier=identifier, metadata=ParagraphMetadata())
    for line in lines:
        paragraph.add_line(line)
    return paragraph
def _verse(identifier: str, *paragraphs: Paragraph) -> Verse:
    verse = Verse(identifier=identifier, metadata=VerseMetadata())
    for paragraph in paragraphs:
        verse.add_paragraph(paragraph)
    return verse
def _section(identifier: str, *verses: Verse) -> Section:
    section = Section(identifier=identifier, metadata=SectionMetadata())
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
    chapter_1 = _section("chapter-1", sloka_1, sloka_2)
    chapter_2 = _section("chapter-2", sloka_3)
    document = _document("document-1", chapter_1, chapter_2)
    corpus = Corpus(
        id="corpus-1",
        metadata=CorpusMetadata(title="Test Purāṇa"),
    )
    corpus.add_document(document)
    return corpus
@pytest.fixture
def repository(corpus) -> DefaultReaderRepository:
    return DefaultReaderRepository(corpus=corpus)
@pytest.fixture
def navigator(repository) -> ReaderNavigator:
    return ReaderNavigator(repository=repository)
@pytest.fixture
def engine(repository, navigator) -> ReaderEngine:
    return ReaderEngine(
        repository=repository,
        navigator=navigator,
    )
@pytest.fixture
def controller(engine) -> ReaderController:
    return ReaderController.open(
        engine,
        ReaderPosition(
            purana_id="corpus-1",
            chapter_id="chapter-1",
            sloka_id="sloka-1",
            word_id="word-1",
        ),
    )
def test_controller_opens_at_requested_position(controller):
    assert controller.has_position is True
    assert controller.current_position is not None
    assert controller.current_position.identifier == "word-1"
def test_controller_exposes_engine(controller, engine):
    assert controller.engine is engine
def test_controller_resolves_document(controller):
    document = controller.document()
    assert document.identifier == "document-1"
def test_controller_resolves_chapter(controller):
    chapter = controller.chapter("chapter-1")
    assert chapter.identifier == "chapter-1"
def test_controller_resolves_sloka(controller):
    sloka = controller.sloka("sloka-1")
    assert sloka.identifier == "sloka-1"
def test_controller_resolves_word(controller):
    word = controller.word("word-1")
    assert word.identifier == "word-1"
def test_controller_resolves_current_position(controller):
    resolved = controller.resolve_position(
        controller.current_position,
    )
    assert resolved.identifier == "word-1"
def test_controller_next_moves_to_next_word(controller):
    result = controller.next()
    assert result is not None
    assert result.identifier == "word-2"
    assert controller.current_position is result
def test_controller_previous_moves_to_previous_word(controller):
    controller.next()
    result = controller.previous()
    assert result is not None
    assert result.identifier == "word-1"
    assert controller.current_position is result
def test_controller_moves_across_sloka_boundary(controller):
    controller.next()
    result = controller.next()
    assert result is not None
    assert result.identifier == "word-3"
    assert controller.current_position is result
def test_controller_moves_across_chapter_boundary(controller):
    controller.next()
    controller.next()
    controller.next()
    result = controller.next()
    assert result is not None
    assert result.identifier == "word-5"
    assert controller.current_position is result
def test_controller_back_restores_previous_position(controller):
    first = controller.current_position
    controller.next()
    assert controller.back() is first
    assert controller.current_position is first
def test_controller_forward_restores_forward_position(controller):
    controller.next()
    next_position = controller.current_position
    controller.back()
    assert controller.forward() is next_position
    assert controller.current_position is next_position
def test_controller_clear_history_preserves_position(controller):
    controller.next()
    position = controller.current_position
    controller.clear_history()
    assert controller.current_position is position
    assert controller.can_go_back is False
def test_controller_set_position_establishes_new_root(controller):
    position = ReaderPosition(
        purana_id="corpus-1",
        chapter_id="chapter-2",
    )
    result = controller.set_position(position)
    assert result is position
    assert controller.current_position is position
    assert controller.history_count == 1
    assert controller.can_go_back is False
def test_controller_set_position_none_clears_position(controller):
    assert controller.set_position(None) is None
    assert controller.current_position is None
    assert controller.has_position is False
def test_controller_failed_navigation_preserves_position(controller):
    controller.set_position(
        ReaderPosition(
            purana_id="corpus-1",
            chapter_id="chapter-2",
        )
    )
    before = controller.current_position
    assert controller.next() is None
    assert controller.current_position is before
def test_controller_history_count_tracks_structural_navigation(controller):
    assert controller.history_count == 1
    controller.next()
    controller.next()
    assert controller.history_count == 3
def test_controller_immutable_move_next_does_not_mutate_controller(controller):
    before = controller.current_position
    new_session = controller.move_next()
    assert new_session is not None
    assert new_session.current_position is not before
    assert controller.current_position is before
def test_controller_immutable_move_previous_does_not_mutate_controller(controller):
    controller.next()
    before = controller.current_position
    new_session = controller.move_previous()
    assert new_session is not None
    assert new_session.current_position is not before
    assert controller.current_position is before
def test_controller_display_state(controller):
    assert controller.display_name == "Reader Controller"
    assert controller.display_text == str(controller.current_position)
    assert controller.display_description
