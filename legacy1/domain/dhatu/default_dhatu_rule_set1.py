from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Rule Set

Provides the canonical reusable DhatuRuleSet for the Dhatu
Kernel.

This initial default rule set is intentionally empty. Concrete
root-analysis rules can be added incrementally later without
changing the strategy or resolver APIs.

Version
-------
v1.0.0
"""

from SanskritAI.domain.dhatu.dhatu_rule_set import DhatuRuleSet


def default_dhatu_rule_set() -> DhatuRuleSet:
    """
    Returns the canonical Dhatu rule bundle.

    The initial bundle is empty and serves as the stable
    default configuration for the Dhatu kernel.
    """
    return DhatuRuleSet()
