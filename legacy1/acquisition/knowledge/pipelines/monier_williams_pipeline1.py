from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Knowledge Acquisition Pipeline

Purpose
-------
Executes the complete acquisition lifecycle for the
Monier–Williams Sanskrit Dictionary.

Pipeline
--------

Manifest
    │
    ▼
Connector
    │
    ▼
Parser
    │
    ▼
Transformer
    │
    ▼
Canonical Repository

Responsibilities
----------------

• Own the complete acquisition workflow.
• Coordinate the participating components.
• Never perform parsing.
• Never perform transformation.
• Never perform repository logic.
• Produce a populated CanonicalLexicalRepository.

Version
-------
1.0.0
"""

from dataclasses import dataclass, field
from pathlib import Path

from SanskritAI.acquisition.knowledge.monier_williams_manifest import (
    MonierWilliamsManifest,
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


@dataclass(slots=True)
class MonierWilliamsPipeline:
    """
    Canonical acquisition pipeline for Monier–Williams.
    """

    manifest: MonierWilliamsManifest = field(
        default_factory=MonierWilliamsManifest,
    )

    connector: MonierWilliamsConnector = field(
        default_factory=MonierWilliamsConnector,
    )

    parser: MonierWilliamsParser = field(
        default_factory=MonierWilliamsParser,
    )

    transformer: MonierWilliamsTransformer = field(
        default_factory=MonierWilliamsTransformer,
    )

    repository: CanonicalLexicalRepository = field(
        default_factory=CanonicalLexicalRepository,
    )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        destination: Path,
    ) -> CanonicalLexicalRepository:
        """
        Executes the complete acquisition workflow.

        Manifest
            ↓
        Connector
            ↓
        Parser
            ↓
        Transformer
            ↓
        Repository
        """

        # ---------------------------------------------
        # Discover source
        # ---------------------------------------------

        self.connector.discover()

        # ---------------------------------------------
        # Acquire source
        # ---------------------------------------------

        source = self.connector.acquire(
            destination,
        )

        # ---------------------------------------------
        # Parse
        # ---------------------------------------------

        raw_entries = self.parser.parse(
            source,
        )

        # ---------------------------------------------
        # Transform
        # ---------------------------------------------

        canonical_records = self.transformer.transform_all(
            raw_entries,
        )

        # ---------------------------------------------
        # Populate repository
        # ---------------------------------------------

        self.repository.add_all(
            canonical_records,
        )

        return self.repository

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Pipeline diagnostics.
        """

        return {

            "pipeline": self.__class__.__name__,

            "manifest": self.manifest.summary(),

            "connector": self.connector.summary(),

            "parser": self.parser.summary(),

            "transformer": self.transformer.summary(),

            "repository": self.repository.summary(),

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def resource_name(
        self,
    ) -> str:

        return self.manifest.resource_name

    @property
    def identifier(
        self,
    ) -> str:

        return self.manifest.identifier

    def __str__(
        self,
    ) -> str:

        return (
            "MonierWilliamsPipeline("
            f"{self.identifier})"
        )
