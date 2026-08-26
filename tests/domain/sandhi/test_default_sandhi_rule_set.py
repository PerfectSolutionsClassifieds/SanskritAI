
from __future__ import annotations

from SanskritAI.domain.sandhi.default_sandhi_rule_set import (
    DEFAULT_SANDHI_RULES,
    default_sandhi_rule_set,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)

from SanskritAI.domain.sandhi.savarna_dirgha_rule import (
    SavarnaDirghaRule,
)

from SanskritAI.domain.sandhi.guna_sandhi_rule import (
    GunaSandhiRule,
)

from SanskritAI.domain.sandhi.vrddhi_sandhi_rule import (
    VrddhiSandhiRule,
)

from SanskritAI.domain.sandhi.jastva_rule import (
    JastvaRule,
)

from SanskritAI.domain.sandhi.visarga_to_s_rule import (
    VisargaToSRule,
)

from SanskritAI.domain.sandhi.visarga_to_r_rule import (
    VisargaToRRule,
)

from SanskritAI.domain.sandhi.jihvamuliya_rule import (
    JihvamuliyaRule,
)

from SanskritAI.domain.sandhi.upadhmaniya_rule import (
    UpadhmaniyaRule,
)


def test_default_rule_set_returns_sandhi_rule_set():

    rule_set = default_sandhi_rule_set()

    assert isinstance(
        rule_set,
        SandhiRuleSet,
    )


def test_default_rule_set_contains_expected_number_of_rules():

    rule_set = default_sandhi_rule_set()

    assert len(rule_set) == len(
        DEFAULT_SANDHI_RULES,
    )

    assert len(rule_set) == 8


def test_default_rule_bundle_is_tuple():

    assert isinstance(
        DEFAULT_SANDHI_RULES,
        tuple,
    )


def test_default_rule_bundle_contains_expected_rule_types():

    expected_types = (
        SavarnaDirghaRule,
        GunaSandhiRule,
        VrddhiSandhiRule,
        JastvaRule,
        VisargaToSRule,
        VisargaToRRule,
        JihvamuliyaRule,
        UpadhmaniyaRule,
    )

    assert tuple(
        type(rule)
        for rule in DEFAULT_SANDHI_RULES
    ) == expected_types


def test_default_rule_order_is_preserved():

    rule_set = default_sandhi_rule_set()

    assert tuple(
        type(rule)
        for rule in rule_set
    ) == tuple(
        type(rule)
        for rule in DEFAULT_SANDHI_RULES
    )


def test_default_rule_set_contains_savarna_dirgha():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            SavarnaDirghaRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_contains_guna():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            GunaSandhiRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_contains_vrddhi():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            VrddhiSandhiRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_contains_jastva():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            JastvaRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_contains_visarga_rules():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            VisargaToSRule,
        )
        for rule in rule_set
    )

    assert any(
        isinstance(
            rule,
            VisargaToRRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_contains_visarga_allophones():

    rule_set = default_sandhi_rule_set()

    assert any(
        isinstance(
            rule,
            JihvamuliyaRule,
        )
        for rule in rule_set
    )

    assert any(
        isinstance(
            rule,
            UpadhmaniyaRule,
        )
        for rule in rule_set
    )


def test_default_rule_set_is_recreated_independently():

    first = default_sandhi_rule_set()
    second = default_sandhi_rule_set()

    assert first is not second
    assert tuple(first) == tuple(second)


def test_default_rule_bundle_is_not_empty():

    assert DEFAULT_SANDHI_RULES


def test_default_rule_set_contains_only_sandhi_rules():

    rule_set = default_sandhi_rule_set()

    for rule in rule_set:
        from SanskritAI.domain.sandhi.sandhi_rule import (
            SandhiRule,
        )

        assert isinstance(
            rule,
            SandhiRule,
        )
