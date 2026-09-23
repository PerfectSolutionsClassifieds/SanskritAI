from __future__ import annotations

import pytest

from SanskritAI.domain.morphology.default_morphological_service import (
    DefaultMorphologicalService,
)
from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)
from SanskritAI.domain.morphology.default_morphological_analyzer import (
    DefaultMorphologicalAnalyzer,
)
from SanskritAI.domain.morphology.default_morphological_resolution_kernel import (
    DefaultMorphologicalResolutionKernel,
)
from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)
from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)


class TestDefaultMorphologicalService:
    """
    Behavioural tests for the canonical
    DefaultMorphologicalService.
    """

    # =========================================================
    # Construction
    # =========================================================

    def test_default_construction(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service,
            DefaultMorphologicalService,
        )

    def test_default_repository_is_canonical_repository(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.repository,
            DefaultMorphologicalRepository,
        )

    def test_repository_is_not_none(self):
        service = DefaultMorphologicalService()

        assert service.repository is not None

    # =========================================================
    # Analyzer
    # =========================================================

    def test_analyzer_is_canonical_analyzer(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.analyzer,
            DefaultMorphologicalAnalyzer,
        )

    def test_analyzer_comes_from_repository(self):
        service = DefaultMorphologicalService()

        assert (
            service.analyzer
            is service.repository.morphological_analyzer
        )

    # =========================================================
    # Rule Set
    # =========================================================

    def test_rule_set_is_morphological_rule_set(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.rule_set,
            MorphologicalRuleSet,
        )

    def test_rule_set_is_repository_rule_set(self):
        service = DefaultMorphologicalService()

        assert (
            service.rule_set
            is service.repository.morphological_rule_set
        )

    # =========================================================
    # Resolution Kernel
    # =========================================================

    def test_resolution_kernel_is_canonical_kernel(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.resolution_kernel,
            DefaultMorphologicalResolutionKernel,
        )

    def test_resolution_kernel_uses_service_repository(self):
        service = DefaultMorphologicalService()

        assert (
            service.resolution_kernel.repository
            is service.repository
        )

    # =========================================================
    # Display
    # =========================================================

    def test_display_name(self):
        service = DefaultMorphologicalService()

        assert (
            service.display_name
            == "Default Morphological Service"
        )

    def test_display_text_matches_display_name(self):
        service = DefaultMorphologicalService()

        assert service.display_text == service.display_name

    def test_string_representation(self):
        service = DefaultMorphologicalService()

        assert str(service) == service.display_text

    # =========================================================
    # Immutability
    # =========================================================

    def test_service_is_frozen(self):
        service = DefaultMorphologicalService()

        with pytest.raises(AttributeError):
            service.repository = None

    # =========================================================
    # Individual Categories
    # =========================================================

    def test_vibhakti_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.vibhakti is not None

    def test_vacana_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.vacana is not None

    def test_linga_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.linga is not None

    def test_purusha_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.purusha is not None

    def test_lakara_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.lakara is not None

    def test_pada_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.pada is not None

    def test_prayoga_is_exposed(self):
        service = DefaultMorphologicalService()

        assert service.prayoga is not None

    # =========================================================
    # Category Collections
    # =========================================================

    def test_nominal_categories_are_exposed(self):
        service = DefaultMorphologicalService()

        assert service.nominal_categories is not None

    def test_verbal_categories_are_exposed(self):
        service = DefaultMorphologicalService()

        assert service.verbal_categories is not None

    def test_all_categories_are_exposed(self):
        service = DefaultMorphologicalService()

        assert service.all_categories is not None

    def test_nominal_categories_are_collection(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.nominal_categories,
            GrammaticalCategoryCollection,
        )

    def test_verbal_categories_are_collection(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.verbal_categories,
            GrammaticalCategoryCollection,
        )

    def test_all_categories_are_collection(self):
        service = DefaultMorphologicalService()

        assert isinstance(
            service.all_categories,
            GrammaticalCategoryCollection,
        )

    # =========================================================
    # Category Collection Cardinality
    # =========================================================

    def test_nominal_categories_count(self):
        service = DefaultMorphologicalService()

        assert service.nominal_categories.count == 3

    def test_verbal_categories_count(self):
        service = DefaultMorphologicalService()

        assert service.verbal_categories.count == 4

    def test_all_categories_count(self):
        service = DefaultMorphologicalService()

        assert service.all_categories.count == 7

    # =========================================================
    # Category Collection Contents
    # =========================================================

    def test_nominal_categories_are_correct(self):
        service = DefaultMorphologicalService()

        categories = service.nominal_categories

        assert categories[0].identifier == (
            service.vibhakti.identifier
        )

        assert categories[1].identifier == (
            service.vacana.identifier
        )

        assert categories[2].identifier == (
            service.linga.identifier
        )

    def test_verbal_categories_are_correct(self):
        service = DefaultMorphologicalService()

        categories = service.verbal_categories

        assert categories[0].identifier == (
            service.purusha.identifier
        )

        assert categories[1].identifier == (
            service.lakara.identifier
        )

        assert categories[2].identifier == (
            service.pada.identifier
        )

        assert categories[3].identifier == (
            service.prayoga.identifier
        )

    def test_all_categories_are_correct(self):
        service = DefaultMorphologicalService()

        categories = service.all_categories

        expected = (
            service.vibhakti.identifier,
            service.vacana.identifier,
            service.linga.identifier,
            service.purusha.identifier,
            service.lakara.identifier,
            service.pada.identifier,
            service.prayoga.identifier,
        )

        actual = tuple(
            category.identifier
            for category in categories
        )

        assert actual == expected

    # =========================================================
    # Category Collection Behaviour
    # =========================================================

    def test_category_collection_is_iterable(self):
        service = DefaultMorphologicalService()

        categories = service.all_categories

        assert len(tuple(categories)) == 7

    def test_category_collection_supports_membership(self):
        service = DefaultMorphologicalService()

        categories = service.all_categories

        assert any(
            category.identifier == service.vibhakti.identifier
            for category in categories
        )

        assert any(
            category.identifier == service.vacana.identifier
            for category in categories
        )

        assert any(
            category.identifier == service.linga.identifier
            for category in categories
        )

    def test_nominal_categories_have_expected_first_and_last(self):
        service = DefaultMorphologicalService()

        categories = service.nominal_categories

        assert (
            categories.first.identifier
            == service.vibhakti.identifier
        )

        assert (
            categories.last.identifier
            == service.linga.identifier
        )

    def test_verbal_categories_have_expected_first_and_last(self):
        service = DefaultMorphologicalService()

        categories = service.verbal_categories

        assert (
            categories.first.identifier
            == service.purusha.identifier
        )

        assert (
            categories.last.identifier
            == service.prayoga.identifier
        )

    # =========================================================
    # Statistics
    # =========================================================

    def test_count_delegates_to_repository(self):
        service = DefaultMorphologicalService()

        assert service.count == service.repository.count

%%writefile -a /content/SanskritAI/tests/domain/morphology/test_default_morphological_service.py

# =========================================================
# Additional Repository Delegation Tests
# =========================================================

def test_repository_count_is_exposed_by_service():
    service = DefaultMorphologicalService()

    assert service.repository.count == len(
        service.repository.rule_set
    )


def test_service_count_matches_rule_set_count():
    service = DefaultMorphologicalService()

    assert service.count == len(
        service.rule_set
    )

