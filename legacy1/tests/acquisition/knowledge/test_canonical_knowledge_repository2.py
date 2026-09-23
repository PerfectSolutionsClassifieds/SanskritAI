
from __future__ import annotations

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


def test_registry_is_constructed() -> None:
    repository = CanonicalKnowledgeRepository()

    assert isinstance(
        repository.registry,
        KnowledgeServiceRegistry,
    )


def test_services_returns_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.services is repository.registry


# ============================================================
# Repository Composition
# ============================================================


def test_all_canonical_repositories_are_constructed() -> None:
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


def test_canonical_services_are_constructed() -> None:
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
# Registry Repository Wiring
# ============================================================


def test_registry_uses_same_repository_instances() -> None:
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


def test_registry_uses_same_service_instances() -> None:
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
# Service → Repository Wiring
# ============================================================


def test_lexical_service_uses_canonical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical_service.repository is (
        repository.lexical_repository
    )


def test_morphological_service_uses_canonical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.morphological_service.repository is (
        repository.morphological_repository
    )


def test_sandhi_service_uses_canonical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.sandhi_service.repository is (
        repository.sandhi_repository
    )


def test_samasa_service_uses_canonical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.samasa_service.repository is (
        repository.samasa_repository
    )


def test_semantic_service_uses_canonical_repository() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.semantic_service.repository is (
        repository.semantic_repository
    )


# ============================================================
# Registry Convenience Service Aliases
# ============================================================


def test_lexical_alias_returns_lexical_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.lexical is (
        repository.registry.lexical_service
    )


def test_dhatu_alias_returns_dhatu_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.dhatu is (
        repository.registry.dhatu_service
    )


def test_morphology_alias_returns_morphological_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.morphology is (
        repository.registry.morphological_service
    )


def test_sandhi_alias_returns_sandhi_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.sandhi is (
        repository.registry.sandhi_service
    )


def test_samasa_alias_returns_samasa_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.samasa is (
        repository.registry.samasa_service
    )


def test_semantic_alias_returns_semantic_service() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.semantic is (
        repository.registry.semantic_service
    )


# ============================================================
# CanonicalKnowledgeRepository Convenience Properties
# ============================================================


def test_lexical_property_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.lexical is repository.registry.lexical


def test_dhatu_property_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.dhatu is repository.registry.dhatu


def test_morphology_property_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.morphology is repository.registry.morphology


def test_sandhi_property_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.sandhi is repository.registry.sandhi


def test_samasa_property_delegates_to_registry() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.samasa is repository.registry.samasa


def test_semantic_property_delegates_to_registry() -> None:
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
# Registry Cardinality
# ============================================================


def test_registry_has_six_repositories() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.repository_count == 6


def test_registry_has_six_services() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.service_count == 6


def test_registry_has_twelve_components() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.registry.component_count == 12


def test_canonical_repository_has_twelve_components() -> None:
    repository = CanonicalKnowledgeRepository()

    assert repository.component_count == 12
    assert len(repository) == 12


# ============================================================
# Repository Identity
# ============================================================


def test_repository_instances_are_distinct() -> None:
    repository = CanonicalKnowledgeRepository()

    repositories = (
        repository.lexical_repository,
        repository.dhatu_repository,
        repository.morphological_repository,
        repository.sandhi_repository,
        repository.samasa_repository,
        repository.semantic_repository,
    )

    assert len({id(item) for item in repositories}) == 6


# ============================================================
# Service Identity
# ============================================================


def test_constructed_services_are_distinct() -> None:
    repository = CanonicalKnowledgeRepository()

    services = (
        repository.lexical_service,
        repository.morphological_service,
        repository.sandhi_service,
        repository.samasa_service,
        repository.semantic_service,
    )

    assert len({id(item) for item in services}) == 5
    
