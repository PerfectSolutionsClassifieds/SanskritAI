
from __future__ import annotations

from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)

from SanskritAI.domain.sandhi.default_sandhi_rule_set import (
    default_sandhi_rule_set,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


def test_default_repository_can_be_constructed():

    repository = DefaultSandhiRepository()

    assert repository is not None


def test_default_repository_implements_repository_contract():

    repository = DefaultSandhiRepository()

    assert isinstance(
        repository,
        SandhiRepository,
    )


def test_default_repository_has_rule_set():

    repository = DefaultSandhiRepository()

    assert isinstance(
        repository.rule_set,
        SandhiRuleSet,
    )


def test_default_repository_is_empty_by_default():

    repository = DefaultSandhiRepository()

    assert len(repository.rule_set) == 0


def test_default_repository_all_returns_rule_set():

    repository = DefaultSandhiRepository()

    result = repository.all()

    assert isinstance(
        result,
        SandhiRuleSet,
    )


def test_default_repository_all_returns_repository_rule_set():

    repository = DefaultSandhiRepository()

    assert repository.all() is repository.rule_set


def test_default_repository_count_is_zero_by_default():

    repository = DefaultSandhiRepository()

    assert repository.count == 0


def test_default_repository_contains_missing_rule_returns_false():

    repository = DefaultSandhiRepository()

    assert not repository.contains(
        "NON_EXISTENT_SANDHI_RULE",
    )


def test_default_repository_get_missing_rule_returns_none():

    repository = DefaultSandhiRepository()

    result = repository.get(
        "NON_EXISTENT_SANDHI_RULE",
    )

    assert result is None


def test_default_repository_search_returns_rule_set():

    repository = DefaultSandhiRepository()

    result = repository.search(
        "sandhi",
    )

    assert isinstance(
        result,
        SandhiRuleSet,
    )


def test_default_repository_search_is_empty_for_empty_repository():

    repository = DefaultSandhiRepository()

    result = repository.search(
        "sandhi",
    )

    assert len(result) == 0


def test_default_repository_search_missing_query_returns_empty_set():

    repository = DefaultSandhiRepository()

    result = repository.search(
        "NO_SUCH_SANDHI_RULE",
    )

    assert isinstance(
        result,
        SandhiRuleSet,
    )

    assert len(result) == 0


def test_default_repository_display_name():

    repository = DefaultSandhiRepository()

    assert repository.display_name == (
        "Default Sandhi Repository"
    )


def test_default_repository_display_text():

    repository = DefaultSandhiRepository()

    assert repository.display_text == (
        repository.display_name
    )


def test_default_repository_display_description():

    repository = DefaultSandhiRepository()

    assert repository.display_description == (
        "Default in-memory repository of canonical "
        "Sandhi rules."
    )


def test_default_repository_has_dataclass_representation():

    repository = DefaultSandhiRepository()

    representation = repr(repository)

    assert representation.startswith(
        "DefaultSandhiRepository("
    )

    assert "rule_set=" in representation


def test_default_repository_instances_are_distinct():

    first = DefaultSandhiRepository()
    second = DefaultSandhiRepository()

    assert first is not second
    assert first.rule_set is not second.rule_set


def test_default_repository_is_immutable():

    repository = DefaultSandhiRepository()

    replacement = SandhiRuleSet(
        rules=(),
    )

    try:
        repository.rule_set = replacement
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DefaultSandhiRepository must be immutable."
        )


def test_default_repository_accepts_explicit_rule_set():

    rule_set = default_sandhi_rule_set()

    repository = DefaultSandhiRepository(
        rule_set=rule_set,
    )

    assert repository.rule_set is rule_set
    assert repository.count == len(rule_set)
    assert repository.count > 0


