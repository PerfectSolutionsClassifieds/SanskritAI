from __future__ import annotations

"""
SanskritAI
==========

Default Resolution Pipeline

Constructs the canonical SanskritAI linguistic
resolution pipeline.

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

Future stages can be inserted without modifying the
ResolutionPipeline implementation.

Version
-------
v2.0.0
"""

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


def default_resolution_pipeline(
    repository: CanonicalKnowledgeRepository,
) -> ResolutionPipeline:
    """
    Builds the canonical SanskritAI resolution pipeline.

    Parameters
    ----------
    repository

        CanonicalKnowledgeRepository

    Returns
    -------
    ResolutionPipeline
    """

    return ResolutionPipeline(
        stages=(
            ResolutionStage(
                name="Lexical",
                service=repository.lexical_service,
            ),

            ResolutionStage(
                name="Morphology",
                service=repository.morphological_service,
            ),

            ResolutionStage(
                name="Sandhi",
                service=repository.sandhi_service,
            ),

            ResolutionStage(
                name="Samasa",
                service=repository.samasa_service,
            ),

            ResolutionStage(
                name="Semantic",
                service=repository.semantic_service,
            ),
        ),
    )
