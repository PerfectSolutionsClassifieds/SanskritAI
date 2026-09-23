from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Analyzer

Canonical morphological analyzer placeholder.

This implementation is intentionally minimal and can later be
extended with rule-based, dictionary-based, and hybrid parsing
strategies.

Version
-------
v1.0.0
"""

from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.morphological_analyzer import (
    MorphologicalAnalyzer,
)
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)


class DefaultMorphologicalAnalyzer(
    MorphologicalAnalyzer,
):
    """
    Default morphological analyzer.

    Currently returns an empty collection and can later be
    expanded with heuristic or rule-based analysis.
    """

    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Analyzes the supplied word form.

        The current default implementation is intentionally
        conservative and returns no analyses until the rule
        engine is introduced.
        """
        return MorphologicalAnalysisCollection()
