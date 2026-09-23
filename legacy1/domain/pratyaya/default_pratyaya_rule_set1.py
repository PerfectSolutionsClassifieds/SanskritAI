from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Rule Set

Provides the canonical reusable PratyayaRuleSet for the
Pratyaya Kernel.

This default rule set bundles the first lightweight Pratyaya
rules:

- KnownPratyayaRule
- AffixHintRule

Version
-------
v1.0.0
"""

from SanskritAI.domain.pratyaya.pratyaya_rule import (
    AffixHintRule,
    KnownPratyayaRule,
    PratyayaRule,
)
from SanskritAI.domain.pratyaya.pratyaya_rule_set import PratyayaRuleSet


DEFAULT_PRATYAYA_RULES: tuple[PratyayaRule, ...] = (
    KnownPratyayaRule(),
    AffixHintRule(),
)


def default_pratyaya_rule_set() -> PratyayaRuleSet:
    """
    Returns the canonical Pratyaya rule bundle.
    """
    return PratyayaRuleSet(
        rules=DEFAULT_PRATYAYA_RULES,
    )
