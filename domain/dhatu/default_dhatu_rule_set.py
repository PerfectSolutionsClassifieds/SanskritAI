from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Rule Set

Provides the canonical reusable DhatuRuleSet for the Dhatu
Kernel.

This default rule set bundles the first concrete Dhatu rules:

- KnownDhatuRule
- GanaMatchRule

Version
-------
v1.1.0
"""

from SanskritAI.domain.dhatu.dhatu_rule import DhatuRule
from SanskritAI.domain.dhatu.dhatu_rule_set import DhatuRuleSet
from SanskritAI.domain.dhatu.gana_match_rule import GanaMatchRule
from SanskritAI.domain.dhatu.known_dhatu_rule import KnownDhatuRule


DEFAULT_DHATU_RULES: tuple[DhatuRule, ...] = (
    KnownDhatuRule(),
    GanaMatchRule(),
)


def default_dhatu_rule_set() -> DhatuRuleSet:
    """
    Returns the canonical Dhatu rule bundle.
    """
    return DhatuRuleSet(
        rules=DEFAULT_DHATU_RULES,
    )
