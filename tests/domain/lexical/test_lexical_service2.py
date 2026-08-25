
from unittest.mock import Mock, patch

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)


def make_service():
    return LexicalService(
        repository=Mock(),
    )


def test_display_contract():
    service = make_service()

    assert service.display_name == "Lexical Service"
    assert service.display_text == "Lexical Service"


def test_lookup_engine_uses_service_repository():
    service = make_service()

    engine = service.lookup_engine

    assert engine.repository is service.repository


def test_resolve_delegates_to_lookup_engine():
    service = make_service()

    expected = object()
    context = object()

    with patch.object(
        service.lookup_engine,
        "lookup",
        return_value=expected,
    ) as lookup:

        result = service.resolve(
            context,
        )

    assert result is expected
    lookup.assert_called_once_with(
        context,
    )


def test_get_entry_delegates():
    service = make_service()

    expected = object()

    service.repository.get_entry.return_value = expected

    assert service.get_entry("राम") is expected

    service.repository.get_entry.assert_called_once_with(
        "राम",
    )


def test_lookup_lemma_delegates():
    service = make_service()

    service.repository.find_entries_by_lemma.return_value = (
        "entry",
    )

    assert service.lookup_lemma("राम") == (
        "entry",
    )


def test_lookup_word_form_delegates():
    service = make_service()

    service.repository.find_entries_by_word_form.return_value = (
        "entry",
    )

    assert service.lookup_word_form("रामः") == (
        "entry",
    )


def test_lookup_senses_delegates():
    service = make_service()

    service.repository.find_senses.return_value = (
        "sense",
    )

    assert service.lookup_senses("राम") == (
        "sense",
    )


def test_search_delegates():
    service = make_service()

    service.repository.search.return_value = (
        "entry",
    )

    assert service.search("राम") == (
        "entry",
    )


def test_all_entries_delegates():
    service = make_service()

    service.repository.all_entries.return_value = (
        "entry",
    )

    assert service.all_entries() == (
        "entry",
    )


def test_count_delegates():
    service = make_service()

    service.repository.count = 42

    assert service.count == 42


def test_contribute_adds_lexical_result():
    service = make_service()

    lexical_result = object()
    aggregate = Mock()
    context = object()

    with patch.object(
        service,
        "resolve",
        return_value=lexical_result,
    ):

        aggregate.with_lexical.return_value = "updated"

        result = service.contribute(
            aggregate,
            context,
        )

    assert result == "updated"

    aggregate.with_lexical.assert_called_once_with(
        lexical_result,
    )
