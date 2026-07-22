
from __future__ import annotations

"""
SanskritAI
==========

Base Metadata Extractor

Defines the abstract interface implemented by every metadata
extractor within the Corpus Acquisition Framework.

Metadata extractors analyze corpus resources and derive structured
metadata without modifying the underlying content.

Examples
--------
    • TitleExtractor
    • LanguageExtractor
    • ScriptExtractor
    • CorpusTypeExtractor
    • NumberingExtractor
    • ChapterExtractor

Metadata extractors intentionally do NOT:

    • download resources
    • normalize corpus text
    • import corpus data
    • perform persistence

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from SanskritAI.acquisition.metadata.extraction_result import (
    ExtractionResult,
)


class BaseMetadataExtractor(ABC):
    """
    Abstract base class for all metadata extractors.
    """

    def __init__(self) -> None:

        self._warnings: list[str] = []
        self._errors: list[str] = []

    # ---------------------------------------------------------
    # Primary API
    # ---------------------------------------------------------

    @abstractmethod
    def extract(
        self,
        source: Path | str | bytes,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> ExtractionResult:
        """
        Extract metadata from a corpus resource.

        Parameters
        ----------
        source
            Input resource. May be:

                • Path
                • filename
                • Unicode text
                • raw bytes

        metadata
            Optional metadata produced by previous extractors.

        Returns
        -------
        ExtractionResult
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        source: Path | str | bytes,
    ) -> bool:
        """
        Validate extractor input.

        Subclasses may override.
        """

        if source is None:
            return False

        if isinstance(source, bytes):
            return len(source) > 0

        if isinstance(source, str):
            return len(source.strip()) > 0

        if isinstance(source, Path):
            return source.exists()

        return True

    def extract_if_valid(
        self,
        source: Path | str | bytes,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> ExtractionResult:
        """
        Validate then extract metadata.

        Raises
        ------
        ValueError
            If validation fails.
        """

        if not self.validate(source):
            raise ValueError(
                "Metadata extractor validation failed."
            )

        return self.extract(
            source,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def warnings(self) -> tuple[str, ...]:
        """
        Non-fatal extraction warnings.
        """
        return tuple(self._warnings)

    @property
    def errors(self) -> tuple[str, ...]:
        """
        Extraction errors.
        """
        return tuple(self._errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self._warnings)

    @property
    def has_errors(self) -> bool:
        return bool(self._errors)

    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Record a warning.
        """
        self._warnings.append(message)

    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Record an error.
        """
        self._errors.append(message)

    def clear_diagnostics(self) -> None:
        """
        Clear all diagnostics.
        """
        self._warnings.clear()
        self._errors.clear()

    # ---------------------------------------------------------
    # Optional Metadata
    # ---------------------------------------------------------

    def capabilities(self) -> tuple[str, ...]:
        """
        Returns the metadata fields produced by this extractor.

        Subclasses should override.
        """

        return ()

    def supports(
        self,
        source: Path | str | bytes,
    ) -> bool:
        """
        Returns whether this extractor supports the given input.

        Default implementation returns True.
        """

        return True

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"warnings={len(self._warnings)}, "
            f"errors={len(self._errors)})"
        )
