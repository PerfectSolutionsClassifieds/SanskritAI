import pytest

from SanskritAI.lexical.models.dictionary_entry import DictionaryEntry
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.dictionary_sense import DictionarySense
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata
from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.repositories.in_memory_lexical_repository import (
    InMemoryLexicalRepository,
)


@pytest.fixture
def source():
    return LexicalSource(
        identifier="test-source",
        name="Test Lexical Source",
    )


@pytest.fixture
def repository(source):
    return InMemoryLexicalRepository(source=source)


@pytest.fixture
def lexeme():
    return Lexeme(
        identifier="lexeme-1",
        metadata=LexemeMetadata(
            lemma="राम",
            transliteration="rāma",
            description="A lexical form.",
        ),
    )


@pytest.fixture
def entry():
    return DictionaryEntry(
        identifier="entry-1",
        source="test-source",
        metadata=DictionaryEntryMetadata(
            lemma="राम",
            transliteration="rāma",
            description="Dictionary entry.",
        ),
    )


@pytest.fixture
def sense():
    return DictionarySense(
        identifier="sense-1",
        metadata=DictionarySenseMetadata(
            definition="a name of Viṣṇu",
            short_definition="Viṣṇu",
            gloss="Rama",
        ),
    )


def test_repository_requires_lexical_source():
    with pytest.raises(TypeError, match="LexicalSource"):
        InMemoryLexicalRepository(source="invalid")


def test_repository_exposes_source(repository, source):
    assert repository.source is source


def test_repository_starts_empty(repository):
    assert repository.count == 0
    assert repository.lexeme_count == 0
    assert repository.entry_count == 0
    assert repository.sense_count == 0


def test_add_registers_lexeme(repository, lexeme):
    repository.add(lexeme)

    assert repository.get_lexeme("lexeme-1") is lexeme
    assert repository.contains("lexeme-1")
    assert repository.lexeme_count == 1


def test_add_registers_dictionary_entry(repository, entry):
    repository.add(entry)

    assert repository.get_entry("entry-1") is entry
    assert repository.contains("entry-1")
    assert repository.entry_count == 1


def test_add_registers_dictionary_sense(repository, sense):
    repository.add(sense)

    assert repository.get_sense("sense-1") is sense
    assert repository.contains("sense-1")
    assert repository.sense_count == 1


def test_add_rejects_unknown_object(repository):
    with pytest.raises(
        TypeError,
        match="Lexeme, DictionaryEntry, or DictionarySense",
    ):
        repository.add(object())


def test_add_many_registers_all_objects(
    repository,
    lexeme,
    entry,
    sense,
):
    repository.add_many([lexeme, entry, sense])

    assert repository.count == 3
    assert repository.get_lexeme("lexeme-1") is lexeme
    assert repository.get_entry("entry-1") is entry
    assert repository.get_sense("sense-1") is sense


def test_lookup_returns_none_for_unknown_identifier(repository):
    assert repository.get_lexeme("missing") is None
    assert repository.get_entry("missing") is None
    assert repository.get_sense("missing") is None


def test_identifier_is_normalized_to_string(repository, lexeme):
    repository.add(lexeme)

    assert repository.get_lexeme(lexeme.id) is lexeme
    assert repository.contains(lexeme.id)


def test_find_by_lemma_returns_matching_lexeme(
    repository,
    lexeme,
):
    repository.add(lexeme)

    result = repository.find_by_lemma("राम")

    assert result == (lexeme,)


def test_find_by_lemma_returns_matching_entry(
    repository,
    entry,
):
    repository.add(entry)

    result = repository.find_by_lemma("राम")

    assert result == (entry,)


def test_find_by_lemma_returns_both_matching_objects(
    repository,
    lexeme,
    entry,
):
    repository.add_many([lexeme, entry])

    result = repository.find_by_lemma("राम")

    assert result == (lexeme, entry)


def test_find_by_lemma_returns_empty_tuple_when_missing(
    repository,
):
    assert repository.find_by_lemma("अज्ञात") == ()


def test_find_by_transliteration_returns_matching_objects(
    repository,
    lexeme,
    entry,
):
    repository.add_many([lexeme, entry])

    result = repository.find_by_transliteration("rāma")

    assert result == (lexeme, entry)


def test_find_by_transliteration_returns_empty_tuple_when_missing(
    repository,
):
    assert repository.find_by_transliteration("unknown") == ()


def test_contains_checks_all_lexical_object_types(
    repository,
    lexeme,
    entry,
    sense,
):
    repository.add_many([lexeme, entry, sense])

    assert repository.contains("lexeme-1")
    assert repository.contains("entry-1")
    assert repository.contains("sense-1")
    assert not repository.contains("missing")


def test_general_search_finds_lexeme(
    repository,
    lexeme,
):
    repository.add(lexeme)

    result = repository.search("राम")

    assert result == (lexeme,)


def test_general_search_finds_entry(
    repository,
    entry,
):
    repository.add(entry)

    result = repository.search("rāma")

    assert result == (entry,)


def test_general_search_finds_sense(
    repository,
    sense,
):
    repository.add(sense)

    result = repository.search("Viṣṇu")

    assert result == (sense,)


def test_general_search_finds_by_identifier(
    repository,
    lexeme,
):
    repository.add(lexeme)

    result = repository.search("lexeme-1")

    assert result == (lexeme,)


def test_general_search_returns_empty_tuple_when_missing(
    repository,
):
    assert repository.search("not-present") == ()


def test_counts_track_registered_objects(
    repository,
    lexeme,
    entry,
    sense,
):
    repository.add_many([lexeme, entry, sense])

    assert repository.lexeme_count == 1
    assert repository.entry_count == 1
    assert repository.sense_count == 1
    assert repository.count == 3


def test_readding_same_identifier_replaces_object(
    repository,
    lexeme,
):
    replacement = Lexeme(
        identifier="lexeme-1",
        metadata=LexemeMetadata(
            lemma="रामः",
        ),
    )

    repository.add(lexeme)
    repository.add(replacement)

    assert repository.get_lexeme("lexeme-1") is replacement
    assert repository.lexeme_count == 1


def test_clear_removes_all_objects(
    repository,
    lexeme,
    entry,
    sense,
):
    repository.add_many([lexeme, entry, sense])

    repository.clear()

    assert repository.count == 0
    assert repository.lexeme_count == 0
    assert repository.entry_count == 0
    assert repository.sense_count == 0
    assert repository.contains("lexeme-1") is False
    assert repository.contains("entry-1") is False
    assert repository.contains("sense-1") is False
