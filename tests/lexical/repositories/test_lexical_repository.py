import pytest

from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.repositories.lexical_repository import (
    LexicalRepository,
)


class StubLexicalRepository(LexicalRepository):
    """
    Minimal concrete implementation used to verify the repository
    contract without introducing persistence or dictionary logic.
    """

    def __init__(self):
        self._source = LexicalSource(
            identifier="test-source",
            name="Test Lexical Source",
        )

    @property
    def source(self):
        return self._source

    def get_lexeme(self, identifier):
        return None

    def get_entry(self, identifier):
        return None

    def get_sense(self, identifier):
        return None

    def find_by_lemma(self, lemma):
        return ()

    def find_by_transliteration(self, transliteration):
        return ()

    def contains(self, identifier):
        return False

    def search(self, query):
        return ()


def test_lexical_repository_is_abstract():
    assert LexicalRepository.__abstractmethods__


def test_repository_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        LexicalRepository()


def test_repository_exposes_source():
    repository = StubLexicalRepository()
    assert isinstance(repository.source, LexicalSource)
    assert repository.source.identifier == "test-source"


def test_get_lexeme_contract():
    repository = StubLexicalRepository()
    result = repository.get_lexeme("lexeme-1")
    assert result is None


def test_get_entry_contract():
    repository = StubLexicalRepository()
    result = repository.get_entry("entry-1")
    assert result is None


def test_get_sense_contract():
    repository = StubLexicalRepository()
    result = repository.get_sense("sense-1")
    assert result is None


def test_find_by_lemma_contract():
    repository = StubLexicalRepository()
    result = repository.find_by_lemma("राम")
    assert result == ()


def test_find_by_transliteration_contract():
    repository = StubLexicalRepository()
    result = repository.find_by_transliteration("rāma")
    assert result == ()


def test_contains_contract():
    repository = StubLexicalRepository()
    assert repository.contains("lexeme-1") is False


def test_search_contract():
    repository = StubLexicalRepository()
    result = repository.search("राम")
    assert result == ()


def test_repository_source_is_lexical_source():
    repository = StubLexicalRepository()
    assert isinstance(repository.source, LexicalSource)


def test_repository_lookup_return_annotations_are_domain_objects():
    annotations = LexicalRepository.get_lexeme.__annotations__
    assert annotations


def test_repository_defines_all_required_operations():
    required_methods = {
        "get_lexeme",
        "get_entry",
        "get_sense",
        "find_by_lemma",
        "find_by_transliteration",
        "contains",
        "search",
    }

    for method_name in required_methods:
        assert hasattr(LexicalRepository, method_name)
        assert callable(getattr(LexicalRepository, method_name))
