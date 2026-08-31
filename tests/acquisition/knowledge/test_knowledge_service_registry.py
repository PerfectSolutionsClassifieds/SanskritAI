
from types import SimpleNamespace

import pytest

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)


# =========================================================
# Test Fixtures / Helpers
# =========================================================

def make_components():
    """Create isolated stand-ins for all registry components."""

    repositories = {
        "lexical": SimpleNamespace(name="lexical_repository"),
        "dhatu": SimpleNamespace(name="dhatu_repository"),
        "morphological": SimpleNamespace(name="morphological_repository"),
        "sandhi": SimpleNamespace(name="sandhi_repository"),
        "samasa": SimpleNamespace(name="samasa_repository"),
        "semantic": SimpleNamespace(name="semantic_repository"),
    }

    services = {
        "lexical": SimpleNamespace(name="lexical_service"),
        "dhatu": SimpleNamespace(name="dhatu_service"),
        "morphological": SimpleNamespace(name="morphological_service"),
        "sandhi": SimpleNamespace(name="sandhi_service"),
        "samasa": SimpleNamespace(name="samasa_service"),
        "semantic": SimpleNamespace(name="semantic_service"),
    }

    return repositories, services


def make_registry():
    """Construct a KnowledgeServiceRegistry with isolated test doubles."""

    repositories, services = make_components()

    registry = KnowledgeServiceRegistry(
        lexical_repository=repositories["lexical"],
        dhatu_repository=repositories["dhatu"],
        morphological_repository=repositories["morphological"],
        sandhi_repository=repositories["sandhi"],
        samasa_repository=repositories["samasa"],
        semantic_repository=repositories["semantic"],
        lexical_service=services["lexical"],
        dhatu_service=services["dhatu"],
        morphological_service=services["morphological"],
        sandhi_service=services["sandhi"],
        samasa_service=services["samasa"],
        semantic_service=services["semantic"],
    )

    return registry, repositories, services


# =========================================================
# Construction
# =========================================================

def test_registry_can_be_constructed():
    registry, _, _ = make_registry()

    assert isinstance(registry, KnowledgeServiceRegistry)


def test_registry_preserves_repository_references():
    registry, repositories, _ = make_registry()

    assert registry.lexical_repository is repositories["lexical"]
    assert registry.dhatu_repository is repositories["dhatu"]
    assert registry.morphological_repository is repositories["morphological"]
    assert registry.sandhi_repository is repositories["sandhi"]
    assert registry.samasa_repository is repositories["samasa"]
    assert registry.semantic_repository is repositories["semantic"]


def test_registry_preserves_service_references():
    registry, _, services = make_registry()

    assert registry.lexical_service is services["lexical"]
    assert registry.dhatu_service is services["dhatu"]
    assert registry.morphological_service is services["morphological"]
    assert registry.sandhi_service is services["sandhi"]
    assert registry.samasa_service is services["samasa"]
    assert registry.semantic_service is services["semantic"]


# =========================================================
# Component Counts
# =========================================================

def test_repository_count_is_six():
    registry, _, _ = make_registry()

    assert registry.repository_count == 6


def test_service_count_is_six():
    registry, _, _ = make_registry()

    assert registry.service_count == 6


def test_component_count_is_twelve():
    registry, _, _ = make_registry()

    assert registry.component_count == 12


def test_len_returns_total_component_count():
    registry, _, _ = make_registry()

    assert len(registry) == 12
    assert len(registry) == registry.component_count


# =========================================================
# Convenience Aliases
# =========================================================

def test_lexical_alias_points_to_lexical_service():
    registry, _, services = make_registry()

    assert registry.lexical is services["lexical"]
    assert registry.lexical is registry.lexical_service


def test_dhatu_alias_points_to_dhatu_service():
    registry, _, services = make_registry()

    assert registry.dhatu is services["dhatu"]
    assert registry.dhatu is registry.dhatu_service


def test_morphology_alias_points_to_morphological_service():
    registry, _, services = make_registry()

    assert registry.morphology is services["morphological"]
    assert registry.morphology is registry.morphological_service


def test_sandhi_alias_points_to_sandhi_service():
    registry, _, services = make_registry()

    assert registry.sandhi is services["sandhi"]
    assert registry.sandhi is registry.sandhi_service


def test_samasa_alias_points_to_samasa_service():
    registry, _, services = make_registry()

    assert registry.samasa is services["samasa"]
    assert registry.samasa is registry.samasa_service


def test_semantic_alias_points_to_semantic_service():
    registry, _, services = make_registry()

    assert registry.semantic is services["semantic"]
    assert registry.semantic is registry.semantic_service


# =========================================================
# Immutability
# =========================================================

def test_registry_is_frozen():
    registry, _, _ = make_registry()

    with pytest.raises(AttributeError):
        registry.lexical_service = SimpleNamespace(
            name="replacement_service",
        )


# =========================================================
# Registry Structure
# =========================================================

def test_registry_contains_six_repository_fields():
    registry, _, _ = make_registry()

    repository_fields = (
        registry.lexical_repository,
        registry.dhatu_repository,
        registry.morphological_repository,
        registry.sandhi_repository,
        registry.samasa_repository,
        registry.semantic_repository,
    )

    assert len(repository_fields) == registry.repository_count


def test_registry_contains_six_service_fields():
    registry, _, _ = make_registry()

    service_fields = (
        registry.lexical_service,
        registry.dhatu_service,
        registry.morphological_service,
        registry.sandhi_service,
        registry.samasa_service,
        registry.semantic_service,
    )

    assert len(service_fields) == registry.service_count


# =========================================================
# Combined Contract
# =========================================================

def test_registry_exposes_all_canonical_services():
    registry, _, services = make_registry()

    assert registry.lexical is services["lexical"]
    assert registry.dhatu is services["dhatu"]
    assert registry.morphology is services["morphological"]
    assert registry.sandhi is services["sandhi"]
    assert registry.samasa is services["samasa"]
    assert registry.semantic is services["semantic"]


def test_registry_component_count_equals_repository_plus_services():
    registry, _, _ = make_registry()

    assert (
        registry.component_count
        == registry.repository_count + registry.service_count
    )
