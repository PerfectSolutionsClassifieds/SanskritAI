
from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Pipeline

Purpose
-------
Concrete implementation of the canonical acquisition pipeline
for the Monier–Williams Sanskrit-English Dictionary.

Architecture
------------

AbstractLexicalPipeline
        │
        ▼
MonierWilliamsPipeline
        │
        ├── MonierWilliamsConnector
        ├── MonierWilliamsParser
        ├── MonierWilliamsTransformer
        ├── CanonicalLexicalRepository
        └── MonierWilliamsManifest

Lifecycle
---------

connect()
    ↓
fetch()
    ↓
parse()
    ↓
transform()
    ↓
validate()
    ↓
persist()
    ↓
build_manifest()
    ↓
report()

Version
-------
2.0.0
"""

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)

from SanskritAI.acquisition.knowledge.manifests.monier_williams_manifest import (
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

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        canonical_records,
    ):
        """
        Monier–Williams specific validation hook.

        The current implementation deliberately preserves
        the canonical records unchanged.

        Resource-specific validation rules can be introduced
        here later without changing the abstract pipeline
        lifecycle.
        """

        return canonical_records

    # ---------------------------------------------------------
    # Manifest
    # ---------------------------------------------------------

    def build_manifest(
        self,
        persisted_objects,
    ) -> MonierWilliamsManifest:
        """
        Builds the Monier–Williams resource manifest.

        The manifest records the result of the current
        pipeline execution without introducing acquisition
        or persistence responsibilities into the manifest.
        """

        return MonierWilliamsManifest(
            total_records=len(persisted_objects),
            imported_records=len(persisted_objects),
            skipped_records=0,
            failed_records=0,
            source_name="Monier-Williams",
            version="1.0.0",
        )
