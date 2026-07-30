from __future__ import annotations

"""
SanskritAI
==========

Default Alankara Rule Set

Provides the canonical reusable AlankaraRuleSet.

Version
-------
v1.0.0
"""

from SanskritAI.domain.alankara.alankara_rule import (
    AlankaraRule,
    AnuprasaRule,
    RupakaRule,
    ShleshaRule,
    UpamaRule,
    YamakaRule,
)
from SanskritAI.domain.alankara.alankara_rule_set import AlankaraRuleSet


DEFAULT_ALANKARA_RULES: tuple[AlankaraRule, ...] = (
    UpamaRule(),
    RupakaRule(),
    AnuprasaRule(),
    YamakaRule(),
    ShleshaRule(),
)


def default_alankara_rule_set() -> AlankaraRuleSet:
    """
    Returns the canonical Alankara rule bundle.
    """
    return AlankaraRuleSet(
        rules=DEFAULT_ALANKARA_RULES,
    )
