
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


def test_default_repository_has_default_rule_set():

    repository = DefaultSandhiRepository()

    assert isinstance(
        repository.rule_set,
        SandhiRuleSet,
    )


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


def test_default_repository_count_matches_rule_set():

    repository = DefaultSandhiRepository()

    assert repository.count == len(
        repository.rule_set,
    )


def test_default_repository_contains_existing_rule():

    repository = DefaultSandhiRepository()

    first_rule = next(
        iter(repository.rule_set),
    )

    assert repository.contains(
        first_rule.identifier,
    )


def test_default_repository_get_existing_rule():

    repository = DefaultSandhiRepository()

    first_rule = next(
        iter(repository.rule_set),
    )

    result = repository.get(
        first_rule.identifier,
    )

    assert result is first_rule


def test_default_repository_get_missing_rule_returns_none():

    repository = DefaultSandhiRepository()

    result = repository.get(
        "NON_EXISTENT_SANDHI_RULE",
    )

    assert result is None


def test_default_repository_contains_missing_rule_returns_false():

    repository = DefaultSandhiRepository()

    assert not repository.contains(
        "NON_EXISTENT_SANDHI_RULE",
    )


def test_default_repository_search_returns_rule_set():

    repository = DefaultSandhiRepository()

    result = repository.search("sandhi")

    assert isinstance(
        result,
        SandhiRuleSet,
    )


def test_default_repository_search_is_case_insensitive():

    repository = DefaultSandhiRepository()

    lower = repository.search("sandhi")
    upper = repository.search("SANDHI")

    assert tuple(lower) == tuple(upper)


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


def test_default_repository_is_frozen():

    repository = DefaultSandhiRepository()

    try:
        repository.rule_set = default_sandhi_rule_set()
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DefaultSandhiRepository must be immutable."
        )


def test_default_repository_is_slot_based():

    repository = DefaultSandhiRepository()

    assert not hasattr(
        repository,
        "__dict__",
    )


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


def test_default_repository_string_representation():

    repository = DefaultSandhiRepository()

    assert str(repository) == repository.display_text


def test_default_repository_search_matches_identifier():

    repository = DefaultSandhiRepository()

    first_rule = next(
        iter(repository.rule_set),
    )

    query = first_rule.identifier.lower()

    result = repository.search(query)

    assert first_rule in result


def test_default_repository_search_matches_display_text():

    repository = DefaultSandhiRepository()

    first_rule = next(
        iter(repository.rule_set),
    )

    query = first_rule.display_text.lower()

    result = repository.search(query)

    assert first_rule in result
