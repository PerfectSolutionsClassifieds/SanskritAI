from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Manifest

Purpose
-------
Defines the canonical metadata contract for every lexical
knowledge resource integrated into SanskritAI.

Concrete implementations include

    • MonierWilliamsManifest
    • ApteManifest
    • AmarakoshaManifest
    • ShabdakalpadrumaManifest
    • VacaspatyamManifest
    • DhatupathaManifest
    • GanapathaManifest
    • UnadiManifest

The manifest contains only descriptive metadata.
It performs no acquisition, parsing, transformation,
or persistence.

Version
-------
1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class AbstractLexicalManifest(ABC):
    """
    Canonical metadata contract for lexical resources.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    resource_name: str

    short_name: str

    version: str

    # ---------------------------------------------------------
    # Source
    # ---------------------------------------------------------

    provider: str

    source_url: str | None = None

    download_url: str | None = None

    homepage: str | None = None

    # ---------------------------------------------------------
    # Resource Characteristics
    # ---------------------------------------------------------

    language: str = "sa"

    script: str = "Devanagari"

    transliteration_scheme: str | None = None

    # ---------------------------------------------------------
    # Local Acquisition
    # ---------------------------------------------------------

    local_directory: Path | None = None

    source_filename: str | None = None

    encoding: str = "utf-8"

    checksum: str | None = None

    # ---------------------------------------------------------
    # Publication
    # ---------------------------------------------------------

    edition: str | None = None

    publication_year: int | None = None

    license_name: str | None = None

    attribution: str | None = None

    copyright_notice: str | None = None

    # ---------------------------------------------------------
    # Optional Metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] | None = None

    # ---------------------------------------------------------
    # Required Behaviour
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def identifier(
        self,
    ) -> str:
        """
        Stable identifier for the lexical resource.

        Examples

            MW
            APTE
            AMARAKOSHA
            SHABDKALPA
        """
        raise NotImplementedError

    @abstractmethod
    def summary(
        self,
    ) -> dict:
        """
        Returns manifest diagnostics.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        """
        Human-readable display name.
        """
        return self.resource_name

    @property
    def has_download(
        self,
    ) -> bool:
        """
        Returns True if a download URL exists.
        """
        return self.download_url is not None

    @property
    def has_local_copy(
        self,
    ) -> bool:
        """
        Returns True if a local directory is configured.
        """
        return self.local_directory is not None

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(identifier='{self.identifier}', "
            f"version='{self.version}')"
        )
