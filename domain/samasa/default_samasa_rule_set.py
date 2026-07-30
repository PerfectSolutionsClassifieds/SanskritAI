from __future__ import annotations

"""
SanskritAI
==========

Default Samasa Rule Set

Provides the canonical reusable SamasaRuleSet for the Samasa
Kernel.

This default rule set bundles the growing family of Samasa
rules in a stable Paninian-inspired order.

Version
-------
v1.2.0
"""

from SanskritAI.domain.samasa.avyayibhava_rule import AvyayibhavaRule
from SanskritAI.domain.samasa.bahuvrihi_rule import BahuvrihiRule
from SanskritAI.domain.samasa.dvigu_rule import DviguRule
from SanskritAI.domain.samasa.dvandva_rule import DvandvaRule
from SanskritAI.domain.samasa.karmadharaya_rule import KarmadharayaRule
from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet
from SanskritAI.domain.samasa.tatpurusha_rule import TatpurushaRule


DEFAULT_SAMASA_RULES: tuple[SamasaRule, ...] = (
    TatpurushaRule(),
    KarmadharayaRule(),
    DvandvaRule(),
    BahuvrihiRule(),
    AvyayibhavaRule(),
    DviguRule(),
)


def default_samasa_rule_set() -> SamasaRuleSet:
    """
    Returns the canonical Samasa rule bundle.
    """
    return SamasaRuleSet(
        rules=DEFAULT_SAMASA_RULES,
    )
