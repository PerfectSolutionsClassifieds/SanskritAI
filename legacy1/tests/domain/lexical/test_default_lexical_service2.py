
from unittest.mock import Mock

from SanskritAI.domain.lexical.default_lexical_service import (
    DefaultLexicalService,
)
from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)


def test_default_service_is_lexical_service():
    service = DefaultLexicalService(
        repository=Mock(),
    )

    assert isinstance(
        service,
        LexicalService,
    )


def test_display_contract():
    service = DefaultLexicalService(
        repository=Mock(),
    )

    assert service.display_name == "Default Lexical Service"
    assert service.display_text == "Default Lexical Service"

    assert (
        service.display_description
        == "Canonical lexical resolution service."
    )


def test_default_service_inherits_repository():
    repository = Mock()

    service = DefaultLexicalService(
        repository=repository,
    )

    assert service.repository is repository


def test_default_service_inherits_lookup_operations():
    repository = Mock()

    repository.get_entry.return_value = "entry"

    service = DefaultLexicalService(
        repository=repository,
    )

    assert service.get_entry("राम") == "entry"

    repository.get_entry.assert_called_once_with(
        "राम",
    )


def test_string_representation():
    service = DefaultLexicalService(
        repository=Mock(),
    )

    assert str(service) == "Default Lexical Service"
