from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Rule Set

Provides the canonical reusable PratyayaRuleSet for the
Pratyaya Kernel.

This updated bundle includes a few concrete rules for the
canonical pratyayas, followed by the generic heuristic rules.

Version
-------
v1.1.0
"""

from SanskritAI.domain.pratyaya.pratyaya_rule import (
    AffixHintRule,
    KnownPratyayaRule,
    PratyayaRule,
)
from SanskritAI.domain.pratyaya.pratyaya_rule_set import PratyayaRuleSet
from SanskritAI.domain.pratyaya.specific_pratyaya_rules import (
    KtaPratyayaRule,
    KtvaPratyayaRule,
    TumunPratyayaRule,
)


DEFAULT_PRATYAYA_RULES: tuple[PratyayaRule, ...] = (
    KtaPratyayaRule(),
    KtvaPratyayaRule(),
    TumunPratyayaRule(),
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
