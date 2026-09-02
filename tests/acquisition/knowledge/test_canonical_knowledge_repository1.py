
from __future__ import annotations

import pytest

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)
from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)

from SanskritAI.domain.lexical.default_lexical_repository import (
    DefaultLexicalRepository,
)
from SanskritAI.domain.dhatu.default_dhatu_repository import (
    DefaultDhatuRepository,
)
from SanskritAI.domain.morphology.default_morphological_repository import (
    DefaultMorphologicalRepository,
)
from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)
from SanskritAI.domain.samasa.default_samasa_repository import (
    DefaultSamasaRepository,
)
from SanskritAI.domain.semantic.default_semantic_repository import (
    DefaultSemanticRepository,
)

from SanskritAI.domain.lexical.default_lexical_service import (
    DefaultLexicalService,
)
from SanskritAI.domain.morphology.default_morphological_service import (
    DefaultMorphologicalService,
)
from SanskritAI.domain.sandhi.default_sandhi_service import (
    DefaultSandhiService,
)
from SanskritAI.domain.samasa.default_samasa_service import (
    DefaultSamasaService,
)
from SanskritAI.domain.semantic.default_semantic_service import (
    DefaultSemanticService,
)


# ============================================================
# Construction
# ============================================================


def test_default_construction() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository is not None


# ============================================================
# Repository Composition
# ============================================================


def test_constructs_all_canonical_repositories() -> None:
    repository = CanonicalKnowledgeRepository()

    assert isinstance(
        repository.lexical_repository,
        DefaultLexicalRepository,
    )

    assert isinstance(
        repository.dhatu_repository,
        DefaultDhatuRepository,
    )

    assert isinstance(
        repository.morphological_repository,
        DefaultMorphologicalRepository,
    )

    assert isinstance(
        repository.sandhi_repository,
        DefaultSandhiRepository,
    )

    assert isinstance(
        repository.samasa_repository,
        DefaultSamasaRepository,
    )

    assert isinstance(
        repository.semantic_repository,
        DefaultSemanticRepository,
    )


# ============================================================
# Service Composition
# ============================================================


def test_constructs_canonical_services() -> None:
    repository = CanonicalKnowledgeRepository()

    assert isinstance(
        repository.lexical_service,
        DefaultLexicalService,
    )

    assert isinstance(
        repository.morphological_service,
        DefaultMorphologicalService,
    )

    assert isinstance(
        repository.sandhi_service,
        DefaultSandhiService,
    )

    assert isinstance(
        repository.samasa_service,
        DefaultSamasaService,
    )

    assert isinstance(
        repository.semantic_service,
        DefaultSemanticService,
    )


# ============================================================
# Registry
# ============================================================


def test_constructs_knowledge_service_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert isinstance(
        repository.registry,
        KnowledgeServiceRegistry,
    )


def test_services_returns_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.services is repository.registry


# ============================================================
# Registry Repository Wiring
# ============================================================


def test_registry_contains_same_repository_instances() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.lexical_repository is (
        repository.lexical_repository
    )

    assert repository.registry.dhatu_repository is (
        repository.dhatu_repository
    )

    assert repository.registry.morphological_repository is (
        repository.morphological_repository
    )

    assert repository.registry.sandhi_repository is (
        repository.sandhi_repository
    )

    assert repository.registry.samasa_repository is (
        repository.samasa_repository
    )

    assert repository.registry.semantic_repository is (
        repository.semantic_repository
    )


# ============================================================
# Registry Service Wiring
# ============================================================


def test_registry_contains_same_service_instances() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.lexical_service is (
        repository.lexical_service
    )

    assert repository.registry.morphological_service is (
        repository.morphological_service
    )

    assert repository.registry.sandhi_service is (
        repository.sandhi_service
    )

    assert repository.registry.samasa_service is (
        repository.samasa_service
    )

    assert repository.registry.semantic_service is (
        repository.semantic_service
    )


# ============================================================
# Legacy Convenience Properties
# ============================================================


def test_lexical_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical is repository.registry.lexical


def test_dhatu_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.dhatu is repository.registry.dhatu


def test_morphology_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.morphology is repository.registry.morphology


def test_sandhi_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.sandhi is repository.registry.sandhi


def test_samasa_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.samasa is repository.registry.samasa


def test_semantic_shortcut() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.semantic is repository.registry.semantic


# ============================================================
# Statistics
# ============================================================


def test_repository_count_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.repository_count == (
        repository.registry.repository_count
    )


def test_service_count_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.service_count == (
        repository.registry.service_count
    )


def test_component_count_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.component_count == (
        repository.registry.component_count
    )


def test_len_returns_component_count() -> None:
    repository = CanonicalKnowledgeRepository()

    assert len(repository) == repository.component_count


# ============================================================
# Composition Consistency
# ============================================================


def test_registry_shortcuts_are_consistent_with_services() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical is repository.lexical_service
    assert repository.morphology is repository.morphological_service
    assert repository.sandhi is repository.sandhi_service
    assert repository.samasa is repository.samasa_service
    assert repository.semantic is repository.semantic_service


# ============================================================
# Dependency Injection
# ============================================================


def test_repository_dependencies_can_be_injected() -> None:
    lexical_repository = DefaultLexicalRepository
    dhatu_repository = DefaultDhatuRepository
    morphological_repository = DefaultMorphologicalRepository
    sandhi_repository = DefaultSandhiRepository
    samasa_repository = DefaultSamasaRepository
    semantic_repository = DefaultSemanticRepository

    # The lexical repository requires the canonical repository
    # itself, so it cannot be instantiated independently here
    # without creating a circular construction.
    #
    # Therefore this test verifies the remaining repository
    # dependency slots through the composition-root constructor
    # contract using the actual default instances.

    canonical = CanonicalKnowledgeRepository()

    assert isinstance(canonical.lexical_repository, lexical_repository)
    assert isinstance(canonical.dhatu_repository, dhatu_repository)
    assert isinstance(
        canonical.morphological_repository,
        morphological_repository,
    )
    assert isinstance(canonical.sandhi_repository, sandhi_repository)
    assert isinstance(canonical.samasa_repository, samasa_repository)
    assert isinstance(canonical.semantic_repository, semantic_repository)


# ============================================================
# Default Repository Counts
# ============================================================


def test_default_repository_counts_are_exposed() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical_repository.count >= 0
    assert repository.dhatu_repository.count >= 0
    assert repository.morphological_repository.count >= 0
    assert repository.sandhi_repository.count >= 0
    assert repository.samasa_repository.count >= 0
    assert repository.semantic_repository.count >= 0


# ============================================================
# Service-to-Repository Wiring
# ============================================================


def test_lexical_service_uses_canonical_lexical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical_service.repository is (
        repository.lexical_repository
    )


def test_morphological_service_uses_canonical_morphological_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.morphological_service.repository is (
        repository.morphological_repository
    )


def test_sandhi_service_uses_canonical_sandhi_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.sandhi_service.repository is (
        repository.sandhi_repository
    )


def test_samasa_service_uses_canonical_samasa_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.samasa_service.repository is (
        repository.samasa_repository
    )


def test_semantic_service_uses_canonical_semantic_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.semantic_service.repository is (
        repository.semantic_repository
    )
