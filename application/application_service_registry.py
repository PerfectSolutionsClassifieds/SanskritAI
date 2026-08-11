from __future__ import annotations

"""
SanskritAI
==========

Application Service Registry

Top-level composition root for the SanskritAI platform.

This registry owns and wires together every major subsystem.

Architecture
------------

ApplicationServiceRegistry
│
├── KnowledgeServiceRegistry
├── ReaderServiceRegistry
├── ResolutionPipeline
└── ReaderEngine

Future extensions

├── AIRAGEngine
├── CommentaryEngine
├── SearchEngine
├── AnnotationEngine
├── TranslationEngine
└── WebApplication

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.acquisition.knowledge.knowledge_service_registry import (
    KnowledgeServiceRegistry,
)

from SanskritAI.domain.reader.reader_service_registry import (
    ReaderServiceRegistry,
)

from SanskritAI.domain.resolution.default_resolution_pipeline import (
    default_resolution_pipeline,
)

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.corpus.models.corpus import (
    Corpus,
)


@dataclass(slots=True)
class ApplicationServiceRegistry:
    """
    Global composition root.

    Every application entry point should construct exactly one
    ApplicationServiceRegistry instance.
    """

    corpus: Corpus

    knowledge: KnowledgeServiceRegistry = field(
        default_factory=KnowledgeServiceRegistry,
    )

    reader: ReaderServiceRegistry = field(init=False)

    resolution_pipeline = field(init=False)

    reader_engine = field(init=False)

    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.reader = ReaderServiceRegistry(
            corpus=self.corpus,
        )

        self.resolution_pipeline = (
            default_resolution_pipeline(
                self.knowledge,
            )
        )

        self.reader_engine = ReaderEngine(
            repository=self.reader.repository,
            navigator=self.reader.navigator,
            pipeline=self.resolution_pipeline,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def engine(
        self,
    ) -> ReaderEngine:
        """
        Primary Reader API.
        """
        return self.reader_engine

    @property
    def pipeline(
        self,
    ):
        return self.resolution_pipeline
