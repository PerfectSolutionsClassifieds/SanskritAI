from __future__ import annotations

"""
SanskritAI
==========

Morphological Analyzer

Defines the abstract morphological analyzer for Sanskrit word forms.

A MorphologicalAnalyzer converts a WordForm into one or more
MorphologicalAnalysis objects.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)


class MorphologicalAnalyzer(
    ABC,
    Displayable,
):
    """
    Abstract morphological analyzer.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract morphological analyzer."

    @abstractmethod
    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Analyzes a word form and returns all candidate analyses.
        """
        raise NotImplementedError
