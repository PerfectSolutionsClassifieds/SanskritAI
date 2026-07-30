from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Rule Set

Provides the canonical reusable SandhiRuleSet for the Sandhi
Kernel.

This default rule set bundles the first concrete Sandhi rules:

• SavarnaDirghaRule
• GunaSandhiRule
• VrddhiSandhiRule
• JastvaRule
• VisargaToSRule

The default Sandhi strategy uses this bundle automatically.

Version
-------
v1.2.0
"""

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)
from SanskritAI.domain.sandhi.guna_sandhi_rule import GunaSandhiRule
from SanskritAI.domain.sandhi.jastva_rule import JastvaRule
from SanskritAI.domain.sandhi.savarna_dirgha_rule import (
    SavarnaDirghaRule,
)
from SanskritAI.domain.sandhi.sandhi_rule_set import SandhiRuleSet
from SanskritAI.domain.sandhi.visarga_to_s_rule import VisargaToSRule
from SanskritAI.domain.sandhi.vrddhi_sandhi_rule import VrddhiSandhiRule


def default_sandhi_rule_set() -> SandhiRuleSet:
    """
    Returns the canonical Sandhi rule bundle.
    """
    return SandhiRuleSet(
        rules=(
            SavarnaDirghaRule(),
            GunaSandhiRule(),
            VrddhiSandhiRule(),
            JastvaRule(),
            VisargaToSRule(),
        ),
    )
