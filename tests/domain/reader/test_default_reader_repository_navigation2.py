from __future__ import annotations
"""
SanskritAI
==========
DefaultReaderRepository Navigation and Projection Tests
Verifies canonical Reader projection, lookup, ordering, navigation,
position resolution, statistics, and boundary/error contracts.
"""
import pytest
from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata
from SanskritAI.domain.reader.default_reader_repository import DefaultReaderRepository
from SanskritAI.domain.reader.reader_position import ReaderPosition

def _build_corpus():
    corpus = Corpus(id="purana-1", metadata=CorpusMetadata(title="Test Purana"))
    document = Document(identifier="document-1", metadata=DocumentMetadata())
    for chapter_number in range(1, 4):
        section = Section(identifier=f"chapter-{chapter_number}", metadata=SectionMetadata())
        for sloka_number in range(1, 4):
            verse_id = f"chapter-{chapter_number}-sloka-{sloka_number}"
            verse = Verse(identifier=verse_id, metadata=VerseMetadata())
            paragraph = Paragraph(identifier=f"{verse_id}-paragraph-1", metadata=ParagraphMetadata())
            line = Line(identifier=f"{verse_id}-line-1", metadata=LineMetadata())
            for word_number, text in enumerate(("धर्मः", "शाश्वतः"), start=1):
                token = Token(
                    identifier=f"{verse_id}-word-{word_number}",
                    metadata=TokenMetadata(
                        text=text,
                        normalized_text=text,
                        position=word_number,
                    ),
                )
                line.add_token(token)
            paragraph.add_line(line)
            verse.add_paragraph(paragraph)
            section.add_verse(verse)
        document.add_section(section)
    corpus.add_document(document)
    return corpus

@pytest.fixture
def repository():
    return DefaultReaderRepository(corpus=_build_corpus())

# =============================================================
# Document
# =============================================================

def test_document_property_returns_reader_document(repository):
    document = repository.document
    assert document.identifier == "purana-1"
    assert document.title == "Test Purana"
    assert document.chapter_count == 3

def test_get_document_without_id_returns_document(repository):
    assert repository.get_document() is repository.document

def test_get_document_with_valid_id_returns_document(repository):
    assert repository.get_document("document-1") is repository.document

def test_get_document_normalizes_identifier_to_string(repository):
    assert repository.get_document(document_id="document-1") is repository.document

def test_get_document_unknown_id_raises_key_error(repository):
    with pytest.raises(KeyError, match="Unknown document"):
        repository.get_document("document-does-not-exist")

# =============================================================
# Chapter Lookup and Projection
# =============================================================

def test_get_chapters_preserves_corpus_order(repository):
    assert [chapter.identifier for chapter in repository.get_chapters()] == [
        "chapter-1", "chapter-2", "chapter-3"
    ]

def test_get_chapter_returns_expected_view(repository):
    chapter = repository.get_chapter("chapter-2")
    assert chapter.identifier == "chapter-2"
    assert len(chapter.slokas) == 3

def test_get_chapter_accepts_identifier_convertible_to_string(repository):
    assert repository.get_chapter(str("chapter-1")).identifier == "chapter-1"

def test_get_chapter_unknown_id_raises_key_error(repository):
    with pytest.raises(KeyError, match="Unknown chapter"):
        repository.get_chapter("chapter-does-not-exist")

def test_get_chapter_slokas_returns_chapter_slokas(repository):
    result = repository.get_chapter_slokas("chapter-2")
    assert [sloka.identifier for sloka in result] == [
        "chapter-2-sloka-1",
        "chapter-2-sloka-2",
        "chapter-2-sloka-3",
    ]

def test_chapter_count_is_three(repository):
    assert repository.chapter_count == 3

def test_len_returns_chapter_count(repository):
    assert len(repository) == repository.chapter_count == 3

# =============================================================
# Chapter Navigation
# =============================================================

def test_next_chapter(repository):
    result = repository.next_chapter("chapter-1")
    assert result is not None
    assert result.identifier == "chapter-2"

def test_previous_chapter(repository):
    result = repository.previous_chapter("chapter-2")
    assert result is not None
    assert result.identifier == "chapter-1"

def test_first_chapter_has_no_previous(repository):
    assert repository.previous_chapter("chapter-1") is None

def test_last_chapter_has_no_next(repository):
    assert repository.next_chapter("chapter-3") is None

def test_chapter_navigation_preserves_projection_order(repository):
    assert repository.next_chapter("chapter-1").identifier == "chapter-2"
    assert repository.next_chapter("chapter-2").identifier == "chapter-3"
    assert repository.previous_chapter("chapter-3").identifier == "chapter-2"
    assert repository.previous_chapter("chapter-2").identifier == "chapter-1"

# =============================================================
# Śloka Lookup and Projection
# =============================================================

def test_get_slokas_preserves_complete_corpus_order(repository):
    assert [sloka.identifier for sloka in repository.get_slokas()] == [
        "chapter-1-sloka-1",
        "chapter-1-sloka-2",
        "chapter-1-sloka-3",
        "chapter-2-sloka-1",
        "chapter-2-sloka-2",
        "chapter-2-sloka-3",
        "chapter-3-sloka-1",
        "chapter-3-sloka-2",
        "chapter-3-sloka-3",
    ]

def test_get_sloka_returns_expected_view(repository):
    sloka = repository.get_sloka("chapter-2-sloka-2")
    assert sloka.identifier == "chapter-2-sloka-2"
    assert sloka.position.chapter_id == "chapter-2"
    assert sloka.position.sloka_id == "chapter-2-sloka-2"

def test_get_sloka_unknown_id_raises_key_error(repository):
    with pytest.raises(KeyError, match="Unknown śloka"):
        repository.get_sloka("sloka-does-not-exist")

def test_sloka_count_is_nine(repository):
    assert repository.sloka_count == 9

# =============================================================
# Śloka Navigation
# =============================================================

def test_next_sloka(repository):
    result = repository.next_sloka("chapter-1-sloka-1")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-2"

def test_previous_sloka(repository):
    result = repository.previous_sloka("chapter-1-sloka-2")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-1"

def test_first_sloka_has_no_previous(repository):
    assert repository.previous_sloka("chapter-1-sloka-1") is None

def test_last_sloka_has_no_next(repository):
    assert repository.next_sloka("chapter-3-sloka-3") is None

def test_sloka_navigation_crosses_chapter_boundary(repository):
    result = repository.next_sloka("chapter-1-sloka-3")
    assert result is not None
    assert result.identifier == "chapter-2-sloka-1"

def test_sloka_previous_navigation_crosses_chapter_boundary(repository):
    result = repository.previous_sloka("chapter-2-sloka-1")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-3"

# =============================================================
# Word Lookup, Projection and Navigation
# =============================================================

def test_get_words_preserves_token_projection_order(repository):
    words = repository.get_words()
    assert len(words) == 18
    assert words[0].identifier == "chapter-1-sloka-1-word-1"
    assert words[-1].identifier == "chapter-3-sloka-3-word-2"

def test_get_word_returns_expected_view(repository):
    word = repository.get_word("chapter-1-sloka-1-word-1")
    assert word.identifier == "chapter-1-sloka-1-word-1"
    assert word.surface == "धर्मः"
    assert word.normalized == "धर्मः"

def test_get_word_unknown_id_raises_key_error(repository):
    with pytest.raises(KeyError, match="Unknown word"):
        repository.get_word("word-does-not-exist")

def test_word_count_is_eighteen(repository):
    assert repository.word_count == 18

def test_get_sloka_words_returns_projected_words(repository):
    words = repository.get_sloka_words("chapter-2-sloka-2")
    assert [word.identifier for word in words] == [
        "chapter-2-sloka-2-word-1",
        "chapter-2-sloka-2-word-2",
    ]
    assert [word.surface for word in words] == ["धर्मः", "शाश्वतः"]

def test_get_sloka_words_unknown_sloka_raises_key_error(repository):
    with pytest.raises(KeyError, match="Unknown śloka"):
        repository.get_sloka_words("sloka-does-not-exist")

def test_next_word(repository):
    result = repository.next_word("chapter-1-sloka-1-word-1")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-1-word-2"

def test_previous_word(repository):
    result = repository.previous_word("chapter-1-sloka-1-word-2")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-1-word-1"

def test_first_word_has_no_previous(repository):
    assert repository.previous_word("chapter-1-sloka-1-word-1") is None

def test_last_word_has_no_next(repository):
    assert repository.next_word("chapter-3-sloka-3-word-2") is None

def test_word_navigation_crosses_sloka_boundary(repository):
    result = repository.next_word("chapter-1-sloka-1-word-2")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-2-word-1"

def test_word_previous_navigation_crosses_sloka_boundary(repository):
    result = repository.previous_word("chapter-1-sloka-2-word-1")
    assert result is not None
    assert result.identifier == "chapter-1-sloka-1-word-2"

# =============================================================
# Invalid IDs
# =============================================================

def test_unknown_chapter_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.next_chapter("chapter-does-not-exist")

def test_unknown_chapter_previous_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.previous_chapter("chapter-does-not-exist")

def test_unknown_sloka_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.next_sloka("sloka-does-not-exist")

def test_unknown_sloka_previous_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.previous_sloka("sloka-does-not-exist")

def test_unknown_word_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.next_word("word-does-not-exist")

def test_unknown_word_previous_raises_key_error(repository):
    with pytest.raises(KeyError):
        repository.previous_word("word-does-not-exist")

# =============================================================
# Position Resolution
# =============================================================

def test_resolve_position_prefers_word_id(repository):
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="chapter-1-sloka-1",
        word_id="chapter-1-sloka-1-word-2",
    )
    result = repository.resolve_position(position)
    assert result.identifier == "chapter-1-sloka-1-word-2"

def test_resolve_position_uses_sloka_when_word_id_absent(repository):
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="chapter-1-sloka-2",
    )
    result = repository.resolve_position(position)
    assert result.identifier == "chapter-1-sloka-2"

def test_resolve_position_uses_chapter_when_only_chapter_id_exists(repository):
    position = ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-2",
    )
    result = repository.resolve_position(position)
    assert result.identifier == "chapter-2"

def test_resolve_position_without_chapter_id_raises_value_error(repository):
    position = ReaderPosition(
        purana_id="purana-1",
    )
    with pytest.raises(ValueError, match="chapter_id"):
        repository.resolve_position(position)

# =============================================================
# Projection and Reader Metadata
# =============================================================

def test_document_position_points_to_first_chapter(repository):
    assert repository.document.position.purana_id == "purana-1"
    assert repository.document.position.chapter_id == "chapter-1"
    assert repository.document.position.sloka_id is None
    assert repository.document.position.word_id is None

def test_projected_chapter_positions_are_canonical(repository):
    chapter = repository.get_chapter("chapter-2")
    assert chapter.position.purana_id == "purana-1"
    assert chapter.position.chapter_id == "chapter-2"
    assert chapter.position.sloka_id is None
    assert chapter.position.word_id is None

def test_projected_sloka_position_contains_parent_chapter(repository):
    sloka = repository.get_sloka("chapter-2-sloka-3")
    assert sloka.position.purana_id == "purana-1"
    assert sloka.position.chapter_id == "chapter-2"
    assert sloka.position.sloka_id == "chapter-2-sloka-3"
    assert sloka.position.word_id is None

def test_projected_word_position_contains_full_hierarchy(repository):
    word = repository.get_word("chapter-2-sloka-3-word-2")
    assert word.position.purana_id == "purana-1"
    assert word.position.chapter_id == "chapter-2"
    assert word.position.sloka_id == "chapter-2-sloka-3"
    assert word.position.word_id == "chapter-2-sloka-3-word-2"

def test_sloka_text_is_reconstructed_from_tokens(repository):
    sloka = repository.get_sloka("chapter-1-sloka-1")
    assert sloka.sloka_text == "धर्मः शाश्वतः"

def test_repository_statistics_are_consistent(repository):
    assert repository.chapter_count == len(repository.get_chapters())
    assert repository.sloka_count == len(repository.get_slokas())
    assert repository.word_count == len(repository.get_words())

# =============================================================
# Construction Errors
# =============================================================

def test_empty_corpus_without_sections_is_rejected():
    corpus = Corpus(id="empty-corpus", metadata=CorpusMetadata())
    document = Document(identifier="document-1", metadata=DocumentMetadata())
    corpus.add_document(document)
    with pytest.raises(ValueError, match="no sections"):
        DefaultReaderRepository(corpus=corpus)
