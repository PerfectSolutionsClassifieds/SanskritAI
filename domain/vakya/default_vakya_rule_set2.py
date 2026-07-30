from __future__ import annotations

"""
SanskritAI
==========

Default Vakya Rule Set

Provides the canonical reusable VakyaRuleSet for sentence
analysis.

This updated bundle enriches sentence analysis from upstream
kernel outputs before falling back to generic composition or
raw sentence tokenization.

Version
-------
v1.1.0
"""

from SanskritAI.domain.vakya.default_vakya_strategy import DefaultVakyaStrategy
from SanskritAI.domain.vakya.upstream_vakya_rules import (
    DerivationAwareVakyaRule,
    GrammarAwareVakyaRule,
    SamasaAwareVakyaRule,
    SandhiAwareVakyaRule,
)
from SanskritAI.domain.vakya.vakya_rule import (
    StringSentenceRule,
    UpstreamCompositionRule,
    VakyaRule,
)
from SanskritAI.domain.vakya.vakya_rule_set import VakyaRuleSet


DEFAULT_VAKYA_RULES: tuple[VakyaRule, ...] = (
    DerivationAwareVakyaRule(),
    SamasaAwareVakyaRule(),
    SandhiAwareVakyaRule(),
    GrammarAwareVakyaRule(),
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
