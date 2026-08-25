
from unittest.mock import Mock

from SanskritAI.domain.lexical.default_lexical_repository import (
    DefaultLexicalRepository,
)


def make_repository():
    return Mock()


def test_get_entry_delegates():
    canonical = make_repository()
    expected = object()

    canonical.get_entry.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.get_entry("राम") is expected
    canonical.get_entry.assert_called_once_with("राम")


def test_find_entries_by_lemma_delegates():
    canonical = make_repository()
    canonical.find_entries_by_lemma.return_value = ("entry",)

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.find_entries_by_lemma("राम") == ("entry",)


def test_find_entries_by_word_form_delegates():
    canonical = make_repository()
    canonical.find_entries_by_word_form.return_value = ("entry",)

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.find_entries_by_word_form("रामः") == (
        "entry",
    )


def test_find_senses_delegates():
    canonical = make_repository()
    canonical.find_senses.return_value = ("sense",)

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.find_senses("राम") == ("sense",)


def test_search_delegates():
    canonical = make_repository()
    canonical.search.return_value = ("entry",)

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.search("राम") == ("entry",)


def test_all_entries_delegates():
    canonical = make_repository()
    canonical.all_entries.return_value = ("entry",)

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.all_entries() == ("entry",)


def test_count_uses_canonical_repository_count():
    canonical = make_repository()
    canonical.lexical_entry_count = 123

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.count == 123


def test_display_contract():
    repository = DefaultLexicalRepository(
        repository=make_repository(),
    )

    assert repository.display_name == "Default Lexical Repository"
    assert repository.display_text == "Default Lexical Repository"
