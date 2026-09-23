from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Analyzer

Canonical rule-based morphological analyzer.

This implementation reuses the canonical MorphologicalRuleSet
via the default_morphological_rule_set helper so future analyzers
can share the same rule bundle without repeating the wiring.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.default_morphological_rule_set import (
    default_morphological_rule_set,
)
from SanskritAI.domain.morphology.morphological_analyzer import (
    MorphologicalAnalyzer,
)
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)
from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)


@dataclass(frozen=True, slots=True)
class DefaultMorphologicalAnalyzer(
    MorphologicalAnalyzer,
):
    """
    Default rule-based morphological analyzer.
    """

    rule_set: MorphologicalRuleSet = field(
        default_factory=default_morphological_rule_set,
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
