
from __future__ import annotations

import pytest

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)
from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)
from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


class ConcreteSandhiRule(SandhiRule):
    """Minimal concrete rule for repository tests."""

    def __init__(
        self,
        identifier: str,
    ) -> None:
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    def applies_to(
        self,
        context,
    ) -> bool:
        return True

    def apply(
        self,
        context,
    ) -> tuple[str, ...]:
        return ()


class InMemorySandhiRepository(
    SandhiRepository,
):
    """Minimal repository implementation for contract testing."""

    def __init__(
        self,
        rules: tuple[SandhiRule, ...] = (),
    ) -> None:
        self._rules = rules

    def get(
        self,
        identifier: str,
    ) -> SandhiRule | None:

        for rule in self._rules:
            if rule.identifier == identifier:
                return rule

        return None

    def contains(
        self,
        identifier: str,
    ) -> bool:

        return self.get(identifier) is not None

    def search(
        self,
        query: str,
    ) -> SandhiRuleSet:

        query = query.lower()

        matches = tuple(
            rule
            for rule in self._rules
            if query in rule.identifier.lower()
        )

        return SandhiRuleSet(
            rules=matches,
        )

    def all(
        self,
    ) -> SandhiRuleSet:

        return SandhiRuleSet(
            rules=self._rules,
        )

    @property
    def count(
        self,
    ) -> int:

        return len(self._rules)


def make_repository() -> InMemorySandhiRepository:
    return InMemorySandhiRepository(
        rules=(
            ConcreteSandhiRule("s1"),
            ConcreteSandhiRule("s2"),
            ConcreteSandhiRule("vowel-sandhi"),
        ),
    )


def test_sandhi_repository_is_abstract():

    assert getattr(
        SandhiRepository,
        "__abstractmethods__",
    ) == {
        "get",
        "contains",
        "search",
        "all",
        "count",
    }


def test_sandhi_repository_cannot_be_instantiated():

    with pytest.raises(TypeError):
        SandhiRepository()


def test_concrete_repository_is_sandhi_repository():

    repository = make_repository()

    assert isinstance(
        repository,
        SandhiRepository,
    )


def test_repository_is_displayable():

    repository = make_repository()

    assert repository.is_displayable is True


def test_repository_display_name_defaults_to_class_name():

    repository = make_repository()

    assert (
        repository.display_name
        == "InMemorySandhiRepository"
    )


def test_repository_display_text_delegates_to_display_name():

    repository = make_repository()

    assert (
        repository.display_text
        == repository.display_name
    )


def test_repository_display_description_is_canonical():

    repository = make_repository()

    assert (
        repository.display_description
        == "Abstract repository for canonical Sandhi rules."
    )


def test_repository_to_display_string_returns_display_text():

    repository = make_repository()

    assert (
        repository.to_display_string()
        == repository.display_text
    )


def test_get_returns_rule_by_identifier():

    repository = make_repository()

    rule = repository.get("s1")

    assert rule is not None
    assert rule.identifier == "s1"


def test_get_returns_none_for_unknown_identifier():

    repository = make_repository()

    assert repository.get("unknown") is None


def test_contains_returns_true_for_existing_rule():

    repository = make_repository()

    assert repository.contains("s2") is True


def test_contains_returns_false_for_unknown_rule():

    repository = make_repository()

    assert repository.contains("unknown") is False


def test_search_returns_matching_rule_set():

    repository = make_repository()

    result = repository.search("vowel")

    assert isinstance(
        result,
        SandhiRuleSet,
    )

    assert result.count == 1
    assert result[0].identifier == "vowel-sandhi"


def test_search_is_case_insensitive():

    repository = make_repository()

    result = repository.search("VOWEL")

    assert result.count == 1
    assert result[0].identifier == "vowel-sandhi"


def test_search_returns_empty_rule_set_when_no_match():

    repository = make_repository()

    result = repository.search("unknown")

    assert isinstance(
        result,
        SandhiRuleSet,
    )

    assert result.is_empty is True


def test_all_returns_complete_rule_set():

    repository = make_repository()

    result = repository.all()

    assert isinstance(
        result,
        SandhiRuleSet,
    )

    assert result.count == 3


def test_all_preserves_repository_order():

    repository = make_repository()

    result = repository.all()

    assert tuple(
        rule.identifier
        for rule in result
    ) == (
        "s1",
        "s2",
        "vowel-sandhi",
    )


def test_count_returns_total_rule_count():

    repository = make_repository()

    assert repository.count == 3


def test_empty_repository_contract():

    repository = InMemorySandhiRepository()

    assert repository.count == 0
    assert repository.all().is_empty is True
    assert repository.search("anything").is_empty is True
    assert repository.get("s1") is None
    assert repository.contains("s1") is False


def test_repository_string_representation():

    repository = make_repository()

    assert str(repository) == (
        "InMemorySandhiRepository"
    )
