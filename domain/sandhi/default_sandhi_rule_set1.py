from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Rule Set

Provides the canonical reusable SandhiRuleSet for the Sandhi
Kernel.

This initial default rule set is intentionally empty. Concrete
Paninian Sandhi rules can be added incrementally later without
changing the strategy or resolver APIs.

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


def default_sandhi_rule_set() -> SandhiRuleSet:
    """
    Returns the canonical Sandhi rule bundle.

    The initial bundle is empty and serves as the stable
    default configuration for the Sandhi kernel.
    """
    return SandhiRuleSet()
