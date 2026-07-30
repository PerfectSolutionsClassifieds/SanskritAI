from __future__ import annotations

"""
SanskritAI
==========

Morphological Rule

Defines the abstract foundation for rule-based Sanskrit
morphological analysis.

A MorphologicalRule evaluates a WordForm and may produce one
or more MorphologicalAnalysis objects.

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


class MorphologicalRule(
    ABC,
    Displayable,
):
    """
    Abstract morphological rule.
    """

    @property
    def identifier(self) -> str:
        return self.__class__.__name__

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract morphological rule."

    @abstractmethod
    def applies_to(
        self,
        word_form: WordForm,
    ) -> bool:
        """
        Determines whether this rule applies to the supplied
        word form.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Applies this rule to the supplied word form and returns
        candidate analyses.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text
