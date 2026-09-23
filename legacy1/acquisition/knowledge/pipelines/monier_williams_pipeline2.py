from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Pipeline

Purpose
-------
Concrete implementation of the canonical lexical
acquisition pipeline for the Monier–Williams
Sanskrit-English Dictionary.

Architecture
------------

AbstractLexicalPipeline
            ▲
            │
MonierWilliamsPipeline

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

from SanskritAI.acquisition.knowledge.pipelines.abstract_lexical_pipeline import (
    AbstractLexicalPipeline,
)

from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)

from SanskritAI.acquisition.knowledge.parsers.monier_williams_parser import (
    MonierWilliamsParser,
)

from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    MonierWilliamsTransformer,
)

from SanskritAI.acquisition.knowledge.repositories.canonical_lexical_repository import (
    CanonicalLexicalRepository,
)

from SanskritAI.acquisition.knowledge.manifests.monier_williams_manifest import (
    MonierWilliamsManifest,
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
    # Optional Validation
    # ---------------------------------------------------------

    def validate(
        self,
        canonical_records,
    ):
        """
        Monier–Williams specific validation.

        Additional validators can be inserted here
        later without modifying the acquisition
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

        return MonierWilliamsManifest(

            total_records=len(
                persisted_objects,
            ),

            imported_records=len(
                persisted_objects,
            ),

            skipped_records=0,

            failed_records=0,

            source_name="Monier-Williams",

            version="1.0.0",

        )
