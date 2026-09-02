
from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Connector

Purpose
-------
Concrete acquisition connector for the Monier–Williams
Sanskrit-English Dictionary.

The connector provides the Monier–Williams-specific
implementation of AbstractLexicalConnector.

Canonical acquisition lifecycle
--------------------------------

    discover()
        ↓
    acquire()
        ↓
    parse()
        ↓
    transform()
        ↓
    validate()
        ↓
    publish()

Pipeline compatibility
----------------------

AbstractLexicalConnector uses:

    discover()
    acquire()

AbstractLexicalPipeline currently uses:

    connect()
    fetch()

This connector therefore provides ``connect()`` and ``fetch()``
as compatibility adapters while retaining the canonical
AbstractLexicalConnector lifecycle.

Important
---------
This initial implementation deliberately does NOT perform
network downloading or dictionary-specific parsing.

Those responsibilities remain delegated to:

    MonierWilliamsParser
    MonierWilliamsTransformer
    repository / persistence layer

Version
-------
1.0.0
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.knowledge.connectors.abstract_lexical_connector import (
    AbstractLexicalConnector,
)


@dataclass(slots=True)
class MonierWilliamsConnector(AbstractLexicalConnector):
    """
    Concrete connector for the Monier–Williams lexical source.
    """

    source_name: str = "Monier-Williams"

    source_version: str = "unknown"

    resource: Path | None = None

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    def connect(
        self,
    ) -> None:
        """
        Establishes the connection to the configured resource.

        For the initial local-resource implementation there is
        no external connection to establish.

        If a resource has been configured, verify that it exists.
        """

        if self.resource is not None and not self.resource.exists():
            raise FileNotFoundError(
                f"Monier-Williams resource not found: "
                f"{self.resource}"
            )

    # ---------------------------------------------------------
    # Fetch
    # ---------------------------------------------------------

    def fetch(
        self,
    ) -> Path:
        """
        Returns the configured Monier–Williams resource.

        This method is the pipeline-facing adapter for the
        canonical ``acquire()`` lifecycle.
        """

        if self.resource is None:
            raise ValueError(
                "No Monier-Williams resource has been configured."
            )

        return self.acquire(
            self.resource.parent,
        )

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
    ) -> dict[str, Any]:
        """
        Discovers the configured Monier–Williams resource.
        """

        return {
            "source_name": self.source_name,
            "source_version": self.source_version,
            "resource": (
                str(self.resource)
                if self.resource is not None
                else None
            ),
            "available": (
                self.resource is not None
                and self.resource.exists()
            ),
        }

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    def acquire(
        self,
        destination: Path,
    ) -> Path:
        """
        Acquires the configured Monier–Williams resource.

        Initial implementation
        ----------------------

        The resource is expected to already exist locally.

        No network download is performed at this stage.
        """

        if self.resource is None:
            raise ValueError(
                "No Monier-Williams resource has been configured."
            )

        if not self.resource.exists():
            raise FileNotFoundError(
                f"Monier-Williams resource not found: "
                f"{self.resource}"
            )

        return self.resource

    # ---------------------------------------------------------
    # Parsing
    # ---------------------------------------------------------

    def parse(
        self,
        source: Path,
    ) -> Any:
        """
        Parsing is delegated to MonierWilliamsParser.

        The connector deliberately does not contain parsing
        logic.
        """

        from SanskritAI.acquisition.knowledge.parsers.monier_williams_parser import (
            MonierWilliamsParser,
        )

        parser = MonierWilliamsParser(
            source_name=self.source_name,
            source_version=self.source_version,
        )

        return parser.parse(
            source,
        )

    # ---------------------------------------------------------
    # Transformation
    # ---------------------------------------------------------

    def transform(
        self,
        parsed: Any,
    ) -> Any:
        """
        Transformation is delegated to
        MonierWilliamsTransformer.
        """

        from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
            MonierWilliamsTransformer,
        )

        transformer = MonierWilliamsTransformer(
            resource_name=self.source_name,
            resource_version=self.source_version,
        )

        return tuple(
            transformer.transform(entry)
            for entry in parsed
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        transformed: Any,
    ) -> Any:
        """
        Initial validation hook.

        The canonical records are returned unchanged until
        resource-specific validation rules are introduced.
        """

        return transformed

    # ---------------------------------------------------------
    # Publishing
    # ---------------------------------------------------------

    def publish(
        self,
        transformed: Any,
    ) -> Any:
        """
        Initial publishing hook.

        Persistence remains the responsibility of the
        CanonicalLexicalRepository when the connector is used
        through MonierWilliamsPipeline.

        Therefore this method currently returns the transformed
        records unchanged.
        """

        return transformed

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Returns connector metadata.
        """

        summary = super().summary()

        summary.update(
            {
                "resource": (
                    str(self.resource)
                    if self.resource is not None
                    else None
                ),
            }
        )

        return summary

    # ---------------------------------------------------------
    # String Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return (
            "MonierWilliamsConnector("
            f"source='{self.source_name}', "
            f"version='{self.source_version}')"
        )
