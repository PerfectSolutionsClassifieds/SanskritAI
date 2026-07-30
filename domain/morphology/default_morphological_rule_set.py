from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Rule Set

Provides the canonical reusable MorphologicalRuleSet for the
Morphology Kernel.

Future analyzers can import this helper instead of repeating the
same nominal and verbal rule wiring.

Version
-------
v1.0.0
"""

from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)
from SanskritAI.domain.morphology.nominal_morphological_rule import (
    NominalMorphologicalRule,
)
from SanskritAI.domain.morphology.verbal_morphological_rule import (
    VerbalMorphologicalRule,
)


def default_morphological_rule_set() -> MorphologicalRuleSet:
    """
    Returns the canonical rule bundle for Sanskrit morphology.
    """
    return MorphologicalRuleSet(
        rules=(
            NominalMorphologicalRule(),
            VerbalMorphologicalRule(),
        ),
    )
