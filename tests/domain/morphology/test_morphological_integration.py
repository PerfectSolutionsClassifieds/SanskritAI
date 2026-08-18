from __future__ import annotations

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

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


class TestMorphologicalIntegration:

    def test_canonical_repository_exposes_morphology_service(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert isinstance(
            service,
            DefaultMorphologicalService,
        )

    def test_morphology_service_uses_canonical_repository(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert isinstance(
            service.repository,
            DefaultMorphologicalRepository,
        )

    def test_morphology_service_uses_repository_analyzer(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert isinstance(
            service.analyzer,
            DefaultMorphologicalAnalyzer,
        )

        assert (
            service.analyzer
            is service.repository.analyzer
        )

    def test_morphology_service_uses_repository_rule_set(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert (
            service.rule_set
            is service.repository.rule_set
        )

    def test_morphology_service_uses_canonical_resolution_kernel(
        self,
    ):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert isinstance(
            service.resolution_kernel,
            DefaultMorphologicalResolutionKernel,
        )

    def test_resolution_kernel_uses_same_repository(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert (
            service.resolution_kernel.repository
            is service.repository
        )

    def test_repository_count_is_consistent(self):
        repository = CanonicalKnowledgeRepository()

        service = repository.services.morphology

        assert service.count == service.repository.count
        assert service.count == len(service.rule_set)
