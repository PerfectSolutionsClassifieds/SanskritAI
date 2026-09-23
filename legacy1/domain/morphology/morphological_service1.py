from __future__ import annotations

"""
SanskritAI
==========

Morphological Service

Application-facing façade for the Morphology Kernel.

Responsibilities
----------------

• expose morphology analysis

• expose canonical grammatical categories

• expose canonical rule set

• hide repository implementation

The service intentionally contains no grammatical reasoning.
It delegates all work to the MorphologicalRepository and the
configured MorphologicalAnalyzer.

Relationship
------------

CanonicalKnowledgeRepository
            │
            ▼
MorphologicalService
            │
            ▼
MorphologicalRepository
            │
            ▼
DefaultMorphologicalAnalyzer

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.lexical.word_form import WordForm

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)

from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)

from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)


class MorphologicalService(
    ABC,
    Displayable,
):
    """
    Application-facing morphology service.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Application façade for Sanskrit morphology."
        )

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    @abstractmethod
    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Performs canonical morphological analysis.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Categories
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def nominal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        raise NotImplementedError

    @property
    @abstractmethod
    def verbal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        raise NotImplementedError

    @property
    @abstractmethod
    def all_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        raise NotImplementedError

    # ---------------------------------------------------------
    # Rules
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def rule_set(
        self,
    ) -> MorphologicalRuleSet:
        raise NotImplementedError
