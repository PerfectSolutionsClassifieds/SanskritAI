from __future__ import annotations

from unittest.mock import Mock

import pytest

from SanskritAI.domain.lexical.default_lexical_repository import (
    DefaultLexicalRepository,
)


def make_repository() -> Mock:
    return Mock()


def test_repository_stores_canonical_repository():
    canonical = make_repository()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.repository is canonical


def test_get_entry_delegates():
    canonical = make_repository()
    expected = object()

    canonical.get_entry.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.get_entry("राम")

    assert result is expected
    canonical.get_entry.assert_called_once_with("राम")


def test_get_entry_returns_none_when_canonical_returns_none():
    canonical = make_repository()
    canonical.get_entry.return_value = None

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.get_entry("अज्ञात") is None

    canonical.get_entry.assert_called_once_with("अज्ञात")


def test_find_entries_by_lemma_delegates():
    canonical = make_repository()
    expected = ("entry-1", "entry-2")

    canonical.find_entries_by_lemma.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.find_entries_by_lemma("राम")

    assert result is expected
    canonical.find_entries_by_lemma.assert_called_once_with("राम")


def test_find_entries_by_word_form_delegates():
    canonical = make_repository()
    expected = ("entry",)

    canonical.find_entries_by_word_form.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.find_entries_by_word_form("रामः")

    assert result is expected
    canonical.find_entries_by_word_form.assert_called_once_with("रामः")


def test_find_senses_delegates():
    canonical = make_repository()
    expected = ("sense-1", "sense-2")

    canonical.find_senses.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.find_senses("राम")

    assert result is expected
    canonical.find_senses.assert_called_once_with("राम")


def test_search_delegates():
    canonical = make_repository()
    expected = ("entry-1",)

    canonical.search.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.search("राम")

    assert result is expected
    canonical.search.assert_called_once_with("राम")


def test_all_entries_delegates():
    canonical = make_repository()
    expected = ("entry-1", "entry-2", "entry-3")

    canonical.all_entries.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.all_entries()

    assert result is expected
    canonical.all_entries.assert_called_once_with()


def test_count_uses_canonical_repository_count():
    canonical = make_repository()
    canonical.lexical_entry_count = 123

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.count == 123


def test_count_reflects_current_canonical_repository_count():
    canonical = make_repository()
    canonical.lexical_entry_count = 10

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert repository.count == 10

    canonical.lexical_entry_count = 25

    assert repository.count == 25


def test_add_lexicon_delegates():
    canonical = make_repository()
    lexicon = object()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    repository.add_lexicon(lexicon)

    canonical.add_lexicon.assert_called_once_with(lexicon)


def test_register_lexicon_delegates_through_add_lexicon():
    canonical = make_repository()
    lexicon = object()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    repository.register_lexicon(lexicon)

    canonical.add_lexicon.assert_called_once_with(lexicon)


def test_clear_lexicons_delegates():
    canonical = make_repository()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    repository.clear_lexicons()

    canonical.clear_lexicons.assert_called_once_with()


def test_all_returns_registered_lexicons():
    canonical = make_repository()
    expected = ("lexicon-1", "lexicon-2")

    canonical.all_lexicons.return_value = expected

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    result = repository.all()

    assert result is expected
    canonical.all_lexicons.assert_called_once_with()


def test_display_name():
    repository = DefaultLexicalRepository(
        repository=make_repository(),
    )

    assert repository.display_name == "Default Lexical Repository"


def test_display_text():
    repository = DefaultLexicalRepository(
        repository=make_repository(),
    )

    assert repository.display_text == "Default Lexical Repository"


def test_display_description():
    repository = DefaultLexicalRepository(
        repository=make_repository(),
    )

    assert repository.display_description == (
        "Canonical adapter exposing lexical knowledge."
    )


def test_string_representation_uses_display_text():
    repository = DefaultLexicalRepository(
        repository=make_repository(),
    )

    assert str(repository) == repository.display_text


def test_repository_is_frozen():
    canonical = make_repository()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    with pytest.raises(AttributeError):
        repository.repository = make_repository()


def test_repository_uses_slots():
    assert hasattr(
        DefaultLexicalRepository,
        "__slots__",
    )


def test_repository_does_not_duplicate_lexicon_state():
    canonical = make_repository()

    repository = DefaultLexicalRepository(
        repository=canonical,
    )

    assert "lexicons" not in repository.__slots__
    assert "entries" not in repository.__slots__
    assert "senses" not in repository.__slots__
