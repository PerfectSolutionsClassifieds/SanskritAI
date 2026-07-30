from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Rule Set

Provides the canonical reusable SemanticRuleSet for the
Semantic Kernel.

Version
-------
v1.1.0
"""

from SanskritAI.domain.semantic.semantic_rule import (
    MeaningHintRule,
    SemanticRule,
    UpstreamSemanticRule,
)
from SanskritAI.domain.semantic.semantic_rule_set import SemanticRuleSet
from SanskritAI.domain.semantic.semantic_upstream_rules import (
    DerivationSemanticFrameRule,
    GrammarSemanticFrameRule,
    SamasaSemanticFrameRule,
    VakyaSemanticFrameRule,
)


DEFAULT_SEMANTIC_RULES: tuple[SemanticRule, ...] = (
    VakyaSemanticFrameRule(),
    DerivationSemanticFrameRule(),
    SamasaSemanticFrameRule(),
    GrammarSemanticFrameRule(),
    UpstreamSemanticRule(),
    MeaningHintRule(),
)


def default_semantic_rule_set() -> SemanticRuleSet:
    """
    Returns the canonical semantic rule bundle.
    """
    return SemanticRuleSet(
        rules=DEFAULT_SEMANTIC_RULES,
    )
