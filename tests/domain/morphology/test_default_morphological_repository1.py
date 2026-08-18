from __future__ import annotations

import pytest

from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)
from SanskritAI.domain.morphology.default_morphological_analyzer import (
    DefaultMorphologicalAnalyzer,
)
from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)
from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)


class TestDefaultMorphologicalRepository:
    """
    Behavioural tests for the canonical
    DefaultMorphologicalRepository.
    """

    # =========================================================
    # Construction
    # =========================================================

    def test_default_construction(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository,
            DefaultMorphologicalRepository,
        )

    # =========================================================
    # Rule Set
    # =========================================================

    def test_rule_set_is_canonical_type(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.rule_set,
            MorphologicalRuleSet,
        )

    def test_morphological_rule_set_delegates_to_rule_set(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.morphological_rule_set
            is repository.rule_set
        )

    # =========================================================
    # Analyzer
    # =========================================================

    def test_analyzer_is_canonical_type(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.analyzer,
            DefaultMorphologicalAnalyzer,
        )

    def test_morphological_analyzer_delegates_to_analyzer(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.morphological_analyzer
            is repository.analyzer
        )

    def test_analyzer_uses_repository_rule_set(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.analyzer.rule_set
            is repository.rule_set
        )

    # =========================================================
    # Individual Categories
    # =========================================================

    def test_vibhakti_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.vibhakti is not None

    def test_vacana_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.vacana is not None

    def test_linga_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.linga is not None

    def test_purusha_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.purusha is not None

    def test_lakara_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.lakara is not None

    def test_pada_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.pada is not None

    def test_prayoga_is_exposed(self):
        repository = DefaultMorphologicalRepository()

        assert repository.prayoga is not None

    # =========================================================
    # Category Collections
    # =========================================================

    def test_nominal_categories_type(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.nominal_categories,
            GrammaticalCategoryCollection,
        )

    def test_verbal_categories_type(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.verbal_categories,
            GrammaticalCategoryCollection,
        )

    def test_all_categories_type(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.all_categories,
            GrammaticalCategoryCollection,
        )

    # =========================================================
    # Category Collection Cardinality
    # =========================================================

    def test_nominal_categories_count(self):
        repository = DefaultMorphologicalRepository()

        assert repository.nominal_categories.count == 3

    def test_verbal_categories_count(self):
        repository = DefaultMorphologicalRepository()

        assert repository.verbal_categories.count == 4

    def test_all_categories_count(self):
        repository = DefaultMorphologicalRepository()

        assert repository.all_categories.count == 7

    # =========================================================
    # Category Collection Ordering
    # =========================================================

    def test_nominal_category_order(self):
        repository = DefaultMorphologicalRepository()

        actual = tuple(
            category.identifier
            for category in repository.nominal_categories
        )

        expected = (
            repository.vibhakti.identifier,
            repository.vacana.identifier,
            repository.linga.identifier,
        )

        assert actual == expected

    def test_verbal_category_order(self):
        repository = DefaultMorphologicalRepository()

        actual = tuple(
            category.identifier
            for category in repository.verbal_categories
        )

        expected = (
            repository.purusha.identifier,
            repository.lakara.identifier,
            repository.pada.identifier,
            repository.prayoga.identifier,
        )

        assert actual == expected

    def test_all_category_order(self):
        repository = DefaultMorphologicalRepository()

        actual = tuple(
            category.identifier
            for category in repository.all_categories
        )

        expected = (
            repository.vibhakti.identifier,
            repository.vacana.identifier,
            repository.linga.identifier,
            repository.purusha.identifier,
            repository.lakara.identifier,
            repository.pada.identifier,
            repository.prayoga.identifier,
        )

        assert actual == expected

    # =========================================================
    # Repository Structure
    # =========================================================

    def test_repository_exposes_complete_kernel_surface(self):
        repository = DefaultMorphologicalRepository()

        assert repository.rule_set is not None
        assert repository.analyzer is not None

        assert repository.vibhakti is not None
        assert repository.vacana is not None
        assert repository.linga is not None
        assert repository.purusha is not None
        assert repository.lakara is not None
        assert repository.pada is not None
        assert repository.prayoga is not None

        assert repository.nominal_categories is not None
        assert repository.verbal_categories is not None
        assert repository.all_categories is not None
