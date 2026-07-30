from __future__ import annotations

"""
Canonical Sandhi Rule Bundle

The ordering follows increasing specificity.

1. Svara Sandhi
2. Vyanjana Sandhi
3. Visarga Transformations
4. Visarga Allophones

Version
-------
v1.4.0
"""

from SanskritAI.domain.sandhi.guna_sandhi_rule import (
    GunaSandhiRule,
)
from SanskritAI.domain.sandhi.jastva_rule import (
    JastvaRule,
)
from SanskritAI.domain.sandhi.jihvamuliya_rule import (
    JihvamuliyaRule,
)
from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)
from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)
from SanskritAI.domain.sandhi.savarna_dirgha_rule import (
    SavarnaDirghaRule,
)
from SanskritAI.domain.sandhi.upadhmaniya_rule import (
    UpadhmaniyaRule,
)
from SanskritAI.domain.sandhi.visarga_to_r_rule import (
    VisargaToRRule,
)
from SanskritAI.domain.sandhi.visarga_to_s_rule import (
    VisargaToSRule,
)
from SanskritAI.domain.sandhi.vrddhi_sandhi_rule import (
    VrddhiSandhiRule,
)


DEFAULT_SANDHI_RULES: tuple[
    SandhiRule,
    ...
] = (

    # -----------------------------------------
    # Svara Sandhi
    # -----------------------------------------

    SavarnaDirghaRule(),
    GunaSandhiRule(),
    VrddhiSandhiRule(),

    # -----------------------------------------
    # Vyanjana Sandhi
    # -----------------------------------------

    JastvaRule(),

    # -----------------------------------------
    # Visarga Transformation
    # -----------------------------------------

    VisargaToSRule(),
    VisargaToRRule(),

    # -----------------------------------------
    # Visarga Allophones
    # -----------------------------------------

    JihvamuliyaRule(),
    UpadhmaniyaRule(),

)


def default_sandhi_rule_set() -> SandhiRuleSet:

    return SandhiRuleSet(
        rules=DEFAULT_SANDHI_RULES,
    )
