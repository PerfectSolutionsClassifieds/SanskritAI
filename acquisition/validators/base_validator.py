
from __future__ import annotations

"""
SanskritAI
==========

Base Validator

Defines the abstract interface implemented by every acquisition
validator.

Concrete implementations include:

    • ChecksumValidator
    • FileValidator

Future implementations may include:

    • ArchiveValidator
    • EncodingValidator
    • LicenseValidator
    • XMLValidator
    • TEIValidator
    • OCRQualityValidator

A validator is responsible ONLY for verifying acquired
resources.

It does NOT perform:

    • downloading
    • archive extraction
    • unicode normalization
    • parsing
    • importing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from pathlib import Path

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult


class BaseValidator(ABC):
    """
    Abstract base class for acquisition validators.
    """

    def __init__(self) -> None:
        self._name = self.__class__.__name__

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Human-readable validator name.
        """
        return self._name

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @abstractmethod
    def supports(
        self,
        manifest: AcquisitionManifest,
    ) -> bool:
        """
        Returns True if this validator can validate the supplied
        acquisition manifest.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        manifest: AcquisitionManifest,
        result: AcquisitionResult,
    ) -> AcquisitionResult:
        """
        Validates an acquisition result.

        Implementations should update and return the supplied
        AcquisitionResult.

        Parameters
        ----------
        manifest:
            Acquisition configuration.

        result:
            Result produced by the downloader.

        Returns
        -------
        AcquisitionResult
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Protected Helpers
    # ------------------------------------------------------------------

    def require_downloads(
        self,
        result: AcquisitionResult,
    ) -> list[Path]:
        """
        Returns the downloaded files.

        Raises
        ------
        ValueError
            If no downloaded files are present.
        """
        if not result.downloaded_files:
            raise ValueError(
                "AcquisitionResult contains no downloaded files."
            )

        return result.downloaded_files

    def require_file(
        self,
        path: Path,
    ) -> None:
        """
        Ensures the supplied path exists and is a regular file.

        Raises
        ------
        FileNotFoundError
        IsADirectoryError
        """
        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise IsADirectoryError(path)

    def add_warning(
        self,
        result: AcquisitionResult,
        message: str,
    ) -> None:
        """
        Adds a validation warning.
        """
        result.add_warning(message)

    def add_error(
        self,
        result: AcquisitionResult,
        message: str,
    ) -> None:
        """
        Adds a validation error.
        """
        result.add_error(message)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
