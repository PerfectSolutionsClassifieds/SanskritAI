from __future__ import annotations

"""
SanskritAI
==========

Default Resolution Pipeline

Constructs the canonical SanskritAI linguistic resolution
pipeline.

Pipeline Order
--------------

Lexical
    ↓
Morphology
    ↓
Sandhi
    ↓
Samasa
    ↓
Semantic

Future contributors may be inserted without modifying the
ResolutionPipeline or ResolutionStage implementations.

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

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


def default_resolution_pipeline(
    services: KnowledgeServiceRegistry,
) -> ResolutionPipeline:
    """
    Builds the canonical SanskritAI linguistic resolution
    pipeline.

    Parameters
    ----------
    services

        KnowledgeServiceRegistry containing every linguistic
        contributor.

    Returns
    -------
    ResolutionPipeline
    """

    return ResolutionPipeline(
        stages=(
            ResolutionStage(
                contributor=services.lexical_service,
            ),
            ResolutionStage(
                contributor=services.morphological_service,
            ),
            ResolutionStage(
                contributor=services.sandhi_service,
            ),
            ResolutionStage(
                contributor=services.samasa_service,
            ),
            ResolutionStage(
                contributor=services.semantic_service,
            ),
        ),
    )
