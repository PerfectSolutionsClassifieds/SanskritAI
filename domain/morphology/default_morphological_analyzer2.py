from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Analyzer

Canonical rule-based morphological analyzer.

This implementation wires a MorphologicalRuleSet containing the
canonical nominal and verbal rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.morphological_analyzer import (
    MorphologicalAnalyzer,
)
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)
from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)
from SanskritAI.domain.morphology.nominal_morphological_rule import (
    NominalMorphologicalRule,
)
from SanskritAI.domain.morphology.verbal_morphological_rule import (
    VerbalMorphologicalRule,
)


@dataclass(frozen=True, slots=True)
class DefaultMorphologicalAnalyzer(
    MorphologicalAnalyzer,
):
    """
    Default rule-based morphological analyzer.

    The default rule set contains:
        - NominalMorphologicalRule
        - VerbalMorphologicalRule
    """

    rule_set: MorphologicalRuleSet = field(
        default_factory=lambda: MorphologicalRuleSet(
            rules=(
                NominalMorphologicalRule(),
                VerbalMorphologicalRule(),
            ),
        ),
    )

    @property
    def display_name(self) -> str:
        return "Default Morphological Analyzer"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Rule-based morphological analyzer using the "
            "canonical nominal and verbal rules."
        )

    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Analyzes the supplied word form using the configured rule set.
        """
        return self.rule_set.apply(word_form)
