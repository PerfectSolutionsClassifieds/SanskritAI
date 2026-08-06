from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Analyzer

Canonical implementation of the MorphologicalAnalyzer.

Purpose
-------
Produces candidate MorphologicalAnalysis objects using the
configured MorphologicalRuleSet.

The analyzer performs grammatical analysis only.

It deliberately does NOT perform:

    • lexical lookup

    • dhātu resolution

    • repository access

    • candidate ranking

    • ambiguity resolution

Those responsibilities belong to the Morphological Resolution
Strategy and Morphological Resolution Kernel.

Architecture
------------

MorphologicalResolutionKernel
        │
        ▼
MorphologicalResolutionStrategy
        │
        ▼
DefaultMorphologicalAnalyzer
        │
        ▼
MorphologicalRuleSet
        │
        ▼
MorphologicalRule
        │
        ▼
MorphologicalAnalysisCollection

Version
-------
v2.0.0
"""

from dataclasses import dataclass
from dataclasses import field

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


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultMorphologicalAnalyzer(
    MorphologicalAnalyzer,
):
    """
    Canonical rule-based morphology analyzer.

    This analyzer simply applies the configured rule set and
    returns every candidate analysis.
    """

    rule_set: MorphologicalRuleSet = field(
        default_factory=default_morphological_rule_set,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Default Morphological Analyzer"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Canonical rule-based analyzer using the "
            "configured MorphologicalRuleSet."
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @property
    def rules(
        self,
    ) -> MorphologicalRuleSet:

        return self.rule_set

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Produces candidate analyses for the supplied word form.
        """

        return self.rule_set.apply(
            word_form,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
