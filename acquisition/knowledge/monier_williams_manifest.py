from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Manifest

Purpose
-------
Describes the Monier–Williams lexical resource independently
of its acquisition, parsing, or transformation.

The manifest acts as the authoritative metadata definition
for the resource and is consumed by connectors, acquisition
pipelines, repositories, exporters, and diagnostics.

This object is intentionally immutable.

Architecture
------------

Manifest

        ↓

Connector

        ↓

Parser

        ↓

Transformer

        ↓

Canonical Repository

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True,
)
class MonierWilliamsManifest:
    """
    Canonical description of the Monier–Williams resource.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    resource_name: str = "Monier-Williams Sanskrit Dictionary"

    short_name: str = "MW"

    version: str = "unknown"

    edition: str = "Monier Monier-Williams"

    publication_year: int | None = 1899

    # ---------------------------------------------------------
    # Source Information
    # ---------------------------------------------------------

    provider: str = "Monier-Williams"

    source_url: str | None = None

    download_url: str | None = None

    homepage: str | None = None

    # ---------------------------------------------------------
    # Resource Characteristics
    # ---------------------------------------------------------

    language: str = "sa"

    script: str = "Devanagari"

    transliteration_scheme: str = "IAST"

    entry_type: str = "Dictionary"

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    local_directory: Path | None = None

    source_filename: str | None = None

    checksum: str | None = None

    encoding: str = "utf-8"

    # ---------------------------------------------------------
    # Licensing
    # ---------------------------------------------------------

    license_name: str | None = None

    attribution: str | None = None

    copyright_notice: str | None = None

    # ---------------------------------------------------------
    # Parser Configuration
    # ---------------------------------------------------------

    parser_name: str = "MonierWilliamsParser"

    transformer_name: str = "MonierWilliamsTransformer"

    connector_name: str = "MonierWilliamsConnector"

    # ---------------------------------------------------------
    # Optional Metadata
    # ---------------------------------------------------------

    metadata: dict[str, str] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        """
        Stable resource identifier.
        """

        return self.short_name

    def summary(
        self,
    ) -> dict:
        """
        Manifest summary.
        """

        return {

            "identifier": self.identifier,

            "resource": self.resource_name,

            "version": self.version,

            "edition": self.edition,

            "provider": self.provider,

            "language": self.language,

            "script": self.script,

            "parser": self.parser_name,

            "transformer": self.transformer_name,

            "connector": self.connector_name,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "MonierWilliamsManifest("
            f"{self.identifier}, "
            f"version={self.version})"
        )
