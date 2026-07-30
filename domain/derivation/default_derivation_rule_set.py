from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Rule Set

Provides the canonical reusable DerivationRuleSet for the
Morphological Derivation Kernel.

This updated bundle adds a sandhi-aware derivation rule in
addition to the baseline concatenation and hint-based rules.

Version
-------
v1.2.0
"""

from SanskritAI.domain.derivation.derivation_rule import (
    DerivationRule,
)
from SanskritAI.domain.derivation.derivation_rule_set import (
    DerivationRuleSet,
)
from SanskritAI.domain.derivation.dhatu_pratyaya_concat_rule import (
    DhatuPratyayaConcatRule,
)
from SanskritAI.domain.derivation.dhatu_pratyaya_sandhi_rule import (
    DhatuPratyayaSandhiRule,
)
from SanskritAI.domain.derivation.hint_based_derivation_rule import (
    HintBasedDerivationRule,
)


DEFAULT_DERIVATION_RULES: tuple[DerivationRule, ...] = (
    DhatuPratyayaSandhiRule(),
    DhatuPratyayaConcatRule(),
    HintBasedDerivationRule(),
)


def default_derivation_rule_set() -> DerivationRuleSet:
    """
    Returns the canonical derivation rule bundle.
    """
    return DerivationRuleSet(
        rules=DEFAULT_DERIVATION_RULES,
    )
