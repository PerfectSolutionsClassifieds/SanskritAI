from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Rule Set

Provides the canonical reusable DerivationRuleSet for the
Morphological Derivation Kernel.

This initial default rule set is intentionally empty. Concrete
derivation rules can be added incrementally later without
changing the strategy or resolver APIs.

Version
-------
v1.0.0
"""

from SanskritAI.domain.derivation.derivation_rule_set import DerivationRuleSet


def default_derivation_rule_set() -> DerivationRuleSet:
    """
    Returns the canonical derivation rule bundle.

    The initial bundle is empty and serves as the stable
    default configuration for the Morphological Derivation
    kernel.
    """
    return DerivationRuleSet()
