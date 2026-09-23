from __future__ import annotations

"""
SanskritAI
==========

Default Samasa Rule Set

Provides the canonical reusable SamasaRuleSet for the Samasa
Kernel.

This initial default rule set is intentionally empty. Concrete
compound rules can be added incrementally later without
changing the strategy or resolver APIs.

Version
-------
v1.0.0
"""

from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet


def default_samasa_rule_set1() -> SamasaRuleSet:
    """
    Returns the canonical Samasa rule bundle.

    The initial bundle is empty and serves as the stable
    default configuration for the Samasa kernel.
    """
    return SamasaRuleSet()
