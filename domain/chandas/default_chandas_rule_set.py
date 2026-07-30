from __future__ import annotations

"""
SanskritAI
==========

Default Chandas Rule Set

Provides the canonical reusable ChandasRuleSet for the Chandas
Kernel.

Version
-------
v1.0.0
"""

from SanskritAI.domain.chandas.chandas_rule import (
    ChandasRule,
    MeterHintRule,
    VerseHeuristicRule,
)
from SanskritAI.domain.chandas.chandas_rule_set import ChandasRuleSet


DEFAULT_CHANDAS_RULES: tuple[ChandasRule, ...] = (
    MeterHintRule(),
    VerseHeuristicRule(),
)


def default_chandas_rule_set() -> ChandasRuleSet:
    """
    Returns the canonical Chandas rule bundle.
    """
    return ChandasRuleSet(
        rules=DEFAULT_CHANDAS_RULES,
    )
