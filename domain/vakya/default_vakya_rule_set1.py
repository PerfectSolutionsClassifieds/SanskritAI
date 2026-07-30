from __future__ import annotations

"""
SanskritAI
==========

Default Vakya Rule Set

Provides the canonical reusable VakyaRuleSet for sentence
analysis.

Version
-------
v1.0.0
"""

from SanskritAI.domain.vakya.vakya_rule import (
    StringSentenceRule,
    UpstreamCompositionRule,
    VakyaRule,
)
from SanskritAI.domain.vakya.vakya_rule_set import VakyaRuleSet


DEFAULT_VAKYA_RULES: tuple[VakyaRule, ...] = (
    UpstreamCompositionRule(),
    StringSentenceRule(),
)


def default_vakya_rule_set() -> VakyaRuleSet:
    """
    Returns the canonical sentence rule bundle.
    """
    return VakyaRuleSet(
        rules=DEFAULT_VAKYA_RULES,
    )
