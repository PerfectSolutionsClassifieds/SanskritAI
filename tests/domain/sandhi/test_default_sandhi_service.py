
from __future__ import annotations

from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)

from SanskritAI.domain.sandhi.default_sandhi_service import (
    DefaultSandhiService,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


def test_default_service_can_be_constructed():

    service = DefaultSandhiService()

    assert service is not None


def test_default_service_uses_default_repository():

    service = DefaultSandhiService()

    assert isinstance(
        service.repository,
        DefaultSandhiRepository,
    )


def test_default_service_accepts_explicit_repository():

    repository = DefaultSandhiRepository()

    service = DefaultSandhiService(
        _repository=repository,
    )

    assert service.repository is repository


def test_default_service_display_name():

    service = DefaultSandhiService()

    assert service.display_name == (
        "Default Sandhi Service"
    )


def test_default_service_display_text():

    service = DefaultSandhiService()

    assert service.display_text == (
        service.display_name
    )


def test_default_service_display_description():

    service = DefaultSandhiService()

    assert service.display_description == (
        "Default service providing access to canonical "
        "Sandhi rules."
    )


def test_default_service_get_rule_delegates_to_repository():

    service = DefaultSandhiService()

    first_rule = next(
        iter(service.repository.all()),
    )

    result = service.get_rule(
        first_rule.identifier,
    )

    assert result is first_rule


def test_default_service_get_missing_rule_returns_none():

    service = DefaultSandhiService()

    result = service.get_rule(
        "NON_EXISTENT_SANDHI_RULE",
    )

    assert result is None


def test_default_service_search_rules_delegates_to_repository():

    service = DefaultSandhiService()

    result = service.search_rules(
        "sandhi",
    )

    assert isinstance(
        result,
        SandhiRuleSet,
    )


def test_default_service_all_rules_delegates_to_repository():

    service = DefaultSandhiService()

    result = service.all_rules()

    assert result is service.repository.all()


def test_default_service_rule_count_delegates_to_repository():

    service = DefaultSandhiService()

    assert service.rule_count == (
        service.repository.count
    )


def test_default_service_repository_is_read_only():

    service = DefaultSandhiService()

    try:
        service.repository = DefaultSandhiRepository()
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DefaultSandhiService must be immutable."
        )


def test_default_service_is_slot_based():

    service = DefaultSandhiService()

    assert not hasattr(
        service,
        "__dict__",
    )


def test_default_service_string_representation():

    service = DefaultSandhiService()

    assert str(service) == service.display_text
