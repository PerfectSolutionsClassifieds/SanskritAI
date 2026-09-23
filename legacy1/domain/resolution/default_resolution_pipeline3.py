from __future__ import annotations

"""
SanskritAI
==========

Default Resolution Pipeline

Constructs the canonical linguistic resolution pipeline.

This implementation consumes the KnowledgeServiceRegistry
rather than CanonicalKnowledgeRepository directly.

Architecture
------------

KnowledgeServiceRegistry
            │
            ▼
DefaultResolutionPipeline
            │
            ▼
ResolutionPipeline
            │
            ├── LexicalResolutionStage
            ├── MorphologyResolutionStage
            ├── SandhiResolutionStage
            ├── SamasaResolutionStage
            └── SemanticResolutionStage

Version
-------
v3.0.0
"""

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.lexical_resolution_stage import (
    LexicalResolutionStage,
)

from SanskritAI.domain.resolution.morphology_resolution_stage import (
    MorphologyResolutionStage,
)

from SanskritAI.domain.resolution.sandhi_resolution_stage import (
    SandhiResolutionStage,
)

from SanskritAI.domain.resolution.samasa_resolution_stage import (
    SamasaResolutionStage,
)

from SanskritAI.domain.resolution.semantic_resolution_stage import (
    SemanticResolutionStage,
)


def default_resolution_pipeline(
    services: KnowledgeServiceRegistry,
) -> ResolutionPipeline:
    """
    Builds the canonical SanskritAI Resolution Pipeline.

    Parameters
    ----------
    services

        KnowledgeServiceRegistry

    Returns
    -------
    ResolutionPipeline
    """

    return ResolutionPipeline(
        stages=(
            LexicalResolutionStage(
                service=services.lexical,
            ),

            MorphologyResolutionStage(
                service=services.morphology,
            ),

            SandhiResolutionStage(
                service=services.sandhi,
            ),

            SamasaResolutionStage(
                service=services.samasa,
            ),

            SemanticResolutionStage(
                service=services.semantic,
            ),
        ),
    )
