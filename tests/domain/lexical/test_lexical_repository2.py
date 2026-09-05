from __future__ import annotations

import pytest

from SanskritAI.domain.lexical.lexical_repository import LexicalRepository


class ConcreteLexicalRepository(LexicalRepository):
    """Minimal concrete implementation for testing the abstract contract."""

    def get_entry(self, headword: str):
        return None

    def find_entries_by_lemma(self, lemma: str):
        return ()

    def find_entries_by_word_form(self, word_form: str):
        return ()

    def find_senses(self, headword: str):
        return ()

    def search(self, query: str):
        return ()

    def all_entries(self):
        return ()

    @property
    def count(self) -> int:
        return 0


def test_lexical_repository_is_abstract():
    with pytest.raises(TypeError):
        LexicalRepository(repository=None)


def test_concrete_repository_can_implement_contract():
    underlying = object()

    repository = ConcreteLexicalRepository(
        repository=underlying,
    )

    assert repository.repository is underlying


def test_repository_exposes_identity_lookup_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.get_entry("राम") is None


def test_repository_exposes_lemma_lookup_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.find_entries_by_lemma("राम") == ()


def test_repository_exposes_word_form_lookup_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.find_entries_by_word_form("रामः") == ()


def test_repository_exposes_sense_lookup_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.find_senses("राम") == ()


def test_repository_exposes_search_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.search("राम") == ()


def test_repository_exposes_enumeration_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.all_entries() == ()


def test_repository_exposes_count_contract():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.count == 0


def test_repository_display_name_defaults_to_class_name():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.display_name == "ConcreteLexicalRepository"


def test_repository_display_text_defaults_to_display_name():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.display_text == repository.display_name


def test_repository_display_description_identifies_canonical_adapter():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.display_description == (
        "Adapter over the Canonical Knowledge Repository."
    )


def test_repository_display_description_is_non_empty():
    repository = ConcreteLexicalRepository(
        repository=object(),
    )

    assert repository.display_description.strip()


def test_repository_has_all_required_abstract_methods():
    abstract_methods = {
        "get_entry",
        "find_entries_by_lemma",
        "find_entries_by_word_form",
        "find_senses",
        "search",
        "all_entries",
        "count",
    }

    assert abstract_methods.issubset(
        ConcreteLexicalRepository.__dict__
        | {
            name
            for name in dir(ConcreteLexicalRepository)
            if name in abstract_methods
        }
    )
