from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Repository

Canonical repository exposing the immutable Morphology Kernel.

Responsibilities
----------------

• provide canonical grammatical categories

• provide grouped category collections

• expose canonical rule set

• expose canonical analyzer

• provide a single integration point for higher layers

This repository performs NO linguistic analysis.

It simply publishes the canonical objects that make up the
Morphology Kernel.

Relationship
------------

CanonicalKnowledgeRepository
            │
            ▼
DefaultMorphologicalRepository
            │
            ├── Vibhakti
            ├── Vacana
            ├── Linga
            ├── Purusha
            ├── Lakara
            ├── Pada
            ├── Prayoga
            │
            ├── NominalMorphologicalRule
            ├── VerbalMorphologicalRule
            │
            ├── MorphologicalRuleSet
            └── DefaultMorphologicalAnalyzer

Version
-------
v2.1.0
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

    The repository owns the canonical MorphologicalRuleSet and
    exposes the canonical analyzer and grammatical categories.

    It performs no linguistic analysis itself.
    """

    rule_set: MorphologicalRuleSet = field(
        default_factory=default_morphological_rule_set,
    )

    analyzer: DefaultMorphologicalAnalyzer = field(
        init=False,
    )

    def __post_init__(self) -> None:
        """
        Construct the canonical analyzer from the repository's
        MorphologicalRuleSet.

        The analyzer accepts `rule_set`, not `kernel`.
        """

        self.analyzer = DefaultMorphologicalAnalyzer(
            rule_set=self.rule_set,
        )

    # =========================================================
    # Statistics
    # =========================================================

    @property
    def count(self) -> int:
        """
        Number of canonical morphological rules exposed by
        this repository.
        """

        return len(self.rule_set)

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
        """
        Canonical nominal grammatical categories.
        """

        return GrammaticalCategoryCollection(
            items=(
                self.vibhakti,
                self.vacana,
                self.linga,
            )
        )

    @property
    def verbal_categories(
        self,
    ) -> GrammaticalCategoryCollection:
        """
        Canonical verbal grammatical categories.
        """

        return GrammaticalCategoryCollection(
            items=(
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
        """
        All canonical grammatical categories.
        """

        return GrammaticalCategoryCollection(
            items=(
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
    # Morphology Kernel
    # =========================================================

    @property
    def morphological_rule_set(
        self,
    ) -> MorphologicalRuleSet:
        """
        Canonical MorphologicalRuleSet.
        """

        return self.rule_set

    @property
    def morphological_analyzer(
        self,
    ) -> DefaultMorphologicalAnalyzer:
        """
        Canonical MorphologicalAnalyzer.
        """

        return self.analyzer
