
from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Pipeline

Concrete implementation of the canonical lexical
acquisition pipeline for the Monier–Williams resource.
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)

from SanskritAI.acquisition.knowledge.monier_williams_manifest import (
    MonierWilliamsManifest,
)

from SanskritAI.acquisition.knowledge.parsers.monier_williams_parser import (
    MonierWilliamsParser,
)

from SanskritAI.acquisition.knowledge.pipelines.abstract_lexical_pipeline import (
    AbstractLexicalPipeline,
)

from SanskritAI.acquisition.knowledge.repositories.canonical_lexical_repository import (
    CanonicalLexicalRepository,
)

from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    MonierWilliamsTransformer,
)


@dataclass(slots=True)
class MonierWilliamsPipeline(
    AbstractLexicalPipeline,
):
    """
    Canonical Monier–Williams acquisition pipeline.
    """

    connector: MonierWilliamsConnector = (
        MonierWilliamsConnector()
    )

    parser: MonierWilliamsParser = (
        MonierWilliamsParser()
    )

    transformer: MonierWilliamsTransformer = (
        MonierWilliamsTransformer()
    )

    repository: CanonicalLexicalRepository = (
        CanonicalLexicalRepository()
    )

    def validate(
        self,
        canonical_records,
    ):
        """
        Monier–Williams specific validation hook.

        Current implementation preserves records unchanged.
        """

        return canonical_records

    def build_manifest(
        self,
        persisted_objects,
    ) -> MonierWilliamsManifest:
        """
        Builds the Monier–Williams manifest.
        """

        return MonierWilliamsManifest(
            total_records=len(persisted_objects),
            imported_records=len(persisted_objects),
            skipped_records=0,
            failed_records=0,
            source_name="Monier-Williams",
            version="1.0.0",
        )
