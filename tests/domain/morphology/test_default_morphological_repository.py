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

    # =========================================================
    # Construction
    # =========================================================

    def test_default_construction(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository,
            DefaultMorphologicalRepository,
        )

    def test_rule_set_is_canonical(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.rule_set,
            MorphologicalRuleSet,
        )

    def test_analyzer_is_canonical(self):
        repository = DefaultMorphologicalRepository()

        assert isinstance(
            repository.analyzer,
            DefaultMorphologicalAnalyzer,
        )

    def test_analyzer_uses_repository_rule_set(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.analyzer.rule_set
            is repository.rule_set
        )

    # =========================================================
    # Statistics
    # =========================================================

    def test_count_matches_rule_set(self):
        repository = DefaultMorphologicalRepository()

        assert repository.count == len(repository.rule_set)

    # =========================================================
    # Categories
    # =========================================================

    def test_nominal_categories(self):
        repository = DefaultMorphologicalRepository()

        categories = repository.nominal_categories

        assert isinstance(
            categories,
            GrammaticalCategoryCollection,
        )

        assert categories.count == 3

    def test_verbal_categories(self):
        repository = DefaultMorphologicalRepository()

        categories = repository.verbal_categories

        assert isinstance(
            categories,
            GrammaticalCategoryCollection,
        )

        assert categories.count == 4

    def test_all_categories(self):
        repository = DefaultMorphologicalRepository()

        categories = repository.all_categories

        assert isinstance(
            categories,
            GrammaticalCategoryCollection,
        )

        assert categories.count == 7

    def test_nominal_categories_are_not_empty(self):
        repository = DefaultMorphologicalRepository()

        assert not repository.nominal_categories.is_empty

    def test_verbal_categories_are_not_empty(self):
        repository = DefaultMorphologicalRepository()

        assert not repository.verbal_categories.is_empty

    def test_all_categories_are_not_empty(self):
        repository = DefaultMorphologicalRepository()

        assert not repository.all_categories.is_empty

    # =========================================================
    # Individual Categories
    # =========================================================

    @pytest.mark.parametrize(
        "attribute",
        (
            "vibhakti",
            "vacana",
            "linga",
            "purusha",
            "lakara",
            "pada",
            "prayoga",
        ),
    )
    def test_canonical_category_is_exposed(
        self,
        attribute,
    ):
        repository = DefaultMorphologicalRepository()

        assert getattr(
            repository,
            attribute,
        ) is not None

    # =========================================================
    # Repository Accessors
    # =========================================================

    def test_morphological_rule_set_alias(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.morphological_rule_set
            is repository.rule_set
        )

    def test_morphological_analyzer_alias(self):
        repository = DefaultMorphologicalRepository()

        assert (
            repository.morphological_analyzer
            is repository.analyzer
        )
