from __future__ import annotations

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.domain.lexical.default_lexical_service import (
    DefaultLexicalService,
)

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.resolution.default_resolution_pipeline import (
    default_resolution_pipeline,
)


class TestLexicalResolutionComposition:

    def test_canonical_repository_constructs_default_lexical_service(self):

        repository = CanonicalKnowledgeRepository()

        assert isinstance(
            repository.lexical_service,
            DefaultLexicalService,
        )

    def test_default_lexical_service_is_registered(self):

        repository = CanonicalKnowledgeRepository()

        assert (
            repository.services.lexical_service
            is repository.lexical_service
        )

    def test_registry_lexical_alias_returns_service(self):

        repository = CanonicalKnowledgeRepository()

        assert (
            repository.services.lexical
            is repository.lexical_service
        )

    def test_lexical_service_is_resolution_contributor(self):

        repository = CanonicalKnowledgeRepository()

        assert isinstance(
            repository.lexical_service,
            LexicalService,
        )

    def test_default_resolution_pipeline_accepts_lexical_service(self):

        repository = CanonicalKnowledgeRepository()

        pipeline = default_resolution_pipeline(
            repository.services,
        )

        assert pipeline.stage_count == 5

        first_stage = pipeline.stages[0]

        assert (
            first_stage.contributor
            is repository.lexical_service
        )

    def test_lexical_service_is_first_pipeline_stage(self):

        repository = CanonicalKnowledgeRepository()

        pipeline = default_resolution_pipeline(
            repository.services,
        )

        assert (
            pipeline.stages[0].contributor.display_name
            == "Default Lexical Service"
        )
