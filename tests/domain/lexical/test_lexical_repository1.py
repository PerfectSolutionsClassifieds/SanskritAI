
import pytest

from SanskritAI.domain.lexical.lexical_repository import (
    LexicalRepository,
)


def test_lexical_repository_is_abstract():
    with pytest.raises(TypeError):
        LexicalRepository(repository=None)


def test_concrete_repository_can_implement_contract():

    class TestRepository(LexicalRepository):

        def get_entry(self, headword):
            return None

        def find_entries_by_lemma(self, lemma):
            return ()

        def find_entries_by_word_form(self, word_form):
            return ()

        def find_senses(self, headword):
            return ()

        def search(self, query):
            return ()

        def all_entries(self):
            return ()

        @property
        def count(self):
            return 0

    repository = TestRepository(
        repository=object(),
    )

    assert repository.repository is not None
    assert repository.count == 0
    assert repository.all_entries() == ()
    assert repository.search("राम") == ()


def test_repository_display_contract():

    class TestRepository(LexicalRepository):

        def get_entry(self, headword):
            return None

        def find_entries_by_lemma(self, lemma):
            return ()

        def find_entries_by_word_form(self, word_form):
            return ()

        def find_senses(self, headword):
            return ()

        def search(self, query):
            return ()

        def all_entries(self):
            return ()

        @property
        def count(self):
            return 0

    repository = TestRepository(
        repository=object(),
    )

    assert repository.display_name == "TestRepository"
    assert repository.display_text == "TestRepository"
    assert "Canonical Knowledge Repository" in (
        repository.display_description
    )
