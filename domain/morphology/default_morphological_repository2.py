
from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Repository

Canonical repository exposing the Morphology Kernel components.

Responsibilities
----------------

• provide canonical grammatical categories
• provide grouped category collections
• expose canonical MorphologicalRuleSet
• expose canonical DefaultMorphologicalAnalyzer
• provide a single integration point for higher layers

This repository performs NO linguistic analysis.

Relationship
------------

CanonicalKnowledgeRepository
            │
            ▼
DefaultMorphologicalRepository
            │
            ├── grammatical categories
            ├── MorphologicalRuleSet
            └── DefaultMorphologicalAnalyzer

Version
-------
v3.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.morphology.default_morphological_analyzer import (
    DefaultMorphologicalAnalyzer,
)

from SanskritAI.domain.morphology.default_morphological_rule_set import (
    default_morphological_rule_set,
)

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)

from SanskritAI.domain.morphology.lakara import Lakara
from SanskritAI.domain.morphology.linga import Linga
from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)
from SanskritAI.domain.morphology.pada import Pada
from SanskritAI.domain.morphology.prayoga import Prayoga
from SanskritAI.domain.morphology.purusha import Purusha
from SanskritAI.domain.morphology.vacana import Vacana
from SanskritAI.domain.morphology.vibhakti import Vibhakti


@dataclass(slots=True)
class DefaultMorphologicalRepository:
    """
    Canonical repository for the Morphology Kernel.

    The repository owns the rule-set/analyzer composition.
    It does not perform resolution itself.
    """

    rule_set: MorphologicalRuleSet = field(
        default_factory=default_morphological_rule_set,
    )

    analyzer: DefaultMorphologicalAnalyzer = field(
        init=False,
    )

    def __post_init__(self) -> None:
        """
        Construct the analyzer from the canonical rule set.

        IMPORTANT
        ---------
        DefaultMorphologicalAnalyzer expects `rule_set`,
        not `kernel`.
        """

        self.analyzer = DefaultMorphologicalAnalyzer(
            rule_set=self.rule_set,
        )

    # =========================================================
    # Canonical Categories
    # =========================================================

    @property
    def vibhakti(self) -> Vibhakti:
        return Vibhakti()

    @property
    def vacana(self) -> Vacana:
        return Vacana()

    @property
    def linga(self) -> Linga:
        return Linga()

    @property
    def purusha(self) -> Purusha:
        return Purusha()

    @property
    def lakara(self) -> Lakara:
        return Lakara()

    @property
    def pada(self) -> Pada:
        return Pada()

    @property
    def prayoga(self) -> Prayoga:
        return Prayoga()

    # =========================================================
    # Category Collections
    # =========================================================

    @property
    def nominal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return GrammaticalCategoryCollection(
            categories=(
                self.vibhakti,
                self.vacana,
                self.linga,
            )
        )

    @property
    def verbal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return GrammaticalCategoryCollection(
            categories=(
                self.purusha,
                self.lakara,
                self.pada,
                self.prayoga,
            )
        )

    @property
    def all_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        return GrammaticalCategoryCollection(
            categories=(
                self.vibhakti,
                self.vacana,
                self.linga,
                self.purusha,
                self.lakara,
                self.pada,
                self.prayoga,
            )
        )

    # =========================================================
    # Kernel Components
    # =========================================================

    @property
    def morphological_rule_set(
        self,
    ) -> MorphologicalRuleSet:
        return self.rule_set

    @property
    def morphological_analyzer(
        self,
    ) -> DefaultMorphologicalAnalyzer:
        return self.analyzer

    # =========================================================
    # Statistics
    # =========================================================

    @property
    def count(self) -> int:
        """
        Number of canonical rule definitions.

        This is intentionally delegated to the rule set when
        such a count is available.
        """

        try:
            return len(self.rule_set)
        except TypeError:
            return 0
