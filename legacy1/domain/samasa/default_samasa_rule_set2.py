from __future__ import annotations

"""
SanskritAI
==========

Default Samasa Rule Set

Provides the canonical reusable SamasaRuleSet for the Samasa
Kernel.

This default rule set bundles the first concrete Samasa rules:

• TatpurushaRule
• KarmadharayaRule
• DvandvaRule

The default Samasa strategy uses this bundle automatically.

Version
-------
v1.1.0
"""

from SanskritAI.domain.samasa.dvandva_rule import DvandvaRule
from SanskritAI.domain.samasa.karmadharaya_rule import KarmadharayaRule
from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet
from SanskritAI.domain.samasa.tatpurusha_rule import TatpurushaRule


DEFAULT_SAMASA_RULES: tuple[SamasaRule, ...] = (
    TatpurushaRule(),
    KarmadharayaRule(),
    DvandvaRule(),
)


def default_samasa_rule_set() -> SamasaRuleSet:
    """
    Returns the canonical Samasa rule bundle.
    """
    return SamasaRuleSet(
        rules=DEFAULT_SAMASA_RULES,
    )
