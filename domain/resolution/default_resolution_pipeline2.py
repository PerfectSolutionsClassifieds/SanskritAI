from __future__ import annotations

"""
SanskritAI
==========

Default Resolution Pipeline

Constructs the canonical SanskritAI linguistic
resolution pipeline.

The pipeline wires together the canonical resolution stages
in dependency order.

Pipeline
--------

Lexical
    ↓
Morphology
    ↓
Sandhi
    ↓
Samasa
    ↓
Semantic

Future stages
-------------

Pragmatics
Commentarial Reasoning
Knowledge Graph
AI Reasoning

may be inserted without modifying ResolutionPipeline itself.

Relationship
------------

CanonicalKnowledgeRepository
            │
            ▼
DefaultResolutionPipeline
            │
            ▼
ResolutionPipeline
            │
            ▼
ResolutionStage(s)

Version
-------
v3.0.0
"""

from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)

from SanskritAI.domain.resolution.lexical_resolution_stage import (
    LexicalResolutionStage,
)

from SanskritAI.domain.resolution.morphology_resolution_stage import (
    MorphologyResolutionStage,
)

# from SanskritAI.domain.resolution.plane_coordinate_geometry import (
#     ResolutionPipeline,
# )

from SanskritAI.domain.resolution.resolution_pipeline import (
    ResolutionPipeline,
)

from SanskritAI.domain.resolution.samasa_resolution_stage import (
    SamasaResolutionStage,
)

from SanskritAI.domain.resolution.sandhi_resolution_stage import (
    SandhiResolutionStage,
)

from SanskritAI.domain.resolution.semantic_resolution_stage import (
    SemanticResolutionStage,
)


def default_resolution_pipeline(
    repository: CanonicalKnowledgeRepository,
) -> ResolutionPipeline:
    """
    Constructs the canonical SanskritAI
    linguistic resolution pipeline.

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
            LexicalResolutionStage(
                service=repository.lexical_service,
            ),

            MorphologyResolutionStage(
                service=repository.morphological_service,
            ),

            SandhiResolutionStage(
                service=repository.sandhi_service,
            ),

            SamasaResolutionStage(
                service=repository.samasa_service,
            ),

            SemanticResolutionStage(
                service=repository.semantic_service,
            ),
        ),
    )
