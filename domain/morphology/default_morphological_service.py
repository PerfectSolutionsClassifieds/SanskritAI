from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Service

Default implementation of the MorphologicalService.

Acts as the canonical façade over the Morphology Kernel.

Relationship
------------

MorphologicalService
        │
        ▼
DefaultMorphologicalService
        │
        ▼
DefaultMorphologicalRepository
        │
        ├── categories
        ├── rule set
        └── analyzer

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.lexical.word_form import WordForm

from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)

from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)

from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)

from SanskritAI.domain.morphology.morphological_service import (
    MorphologicalService,
)


@dataclass(slots=True)
class DefaultMorphologicalService(
    MorphologicalService,
):
    """
    Canonical MorphologicalService implementation.
    """

    repository: DefaultMorphologicalRepository = field(
        default_factory=DefaultMorphologicalRepository,
    )

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Delegates analysis to the canonical analyzer.
        """
        return (
            self.repository
            .morphological_analyzer
            .analyze(word_form)
        )

    # ---------------------------------------------------------
    # Categories
    # ---------------------------------------------------------

    @property
    def nominal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.nominal_categories

    @property
    def verbal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.verbal_categories

    @property
    def all_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return self.repository.all_categories

    # ---------------------------------------------------------
    # Rule Set
    # ---------------------------------------------------------

    @property
    def rule_set(
        self,
    ) -> MorphologicalRuleSet:
        return self.repository.morphological_rule_set

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Morphological Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical façade over the Morphology Kernel."
        )
