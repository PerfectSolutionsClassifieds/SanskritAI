
from __future__ import annotations

"""
SanskritAI
==========

Base Downloader

Defines the abstract interface implemented by every acquisition
downloader.

Concrete implementations include:

    • HTTPDownloader
    • LocalFileImporter

Future implementations may include:

    • GitDownloader
    • FTPDownloader
    • S3Downloader
    • GoogleDriveDownloader

A downloader is responsible ONLY for obtaining source files.

It does NOT perform:

    • corpus parsing
    • validation
    • unicode normalization
    • database importing

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from abc import ABC, abstractmethod
from pathlib import Path
import shutil

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.models.acquisition_result import AcquisitionResult


class BaseDownloader(ABC):
    """
    Abstract base class for all downloaders.
    """

    def __init__(self) -> None:
        self._name = self.__class__.__name__

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Human-readable downloader name.
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
        Returns True if this downloader can process the manifest.
        """
        raise NotImplementedError

    @abstractmethod
    def download(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        """
        Executes the acquisition operation.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Protected Helpers
    # ------------------------------------------------------------------

    def prepare_directory(
        self,
        directory: Path,
    ) -> None:
        """
        Creates the destination directory if necessary.
        """
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def validate_destination(
        self,
        directory: Path,
    ) -> None:
        """
        Ensures the destination directory is writable.
        """
        if directory.exists() and not directory.is_dir():
            raise NotADirectoryError(directory)

        self.prepare_directory(directory)

    def destination_file(
        self,
        manifest: AcquisitionManifest,
        filename: str,
    ) -> Path:
        """
        Returns the full destination path for a downloaded file.
        """
        if manifest.destination_directory is None:
            raise ValueError(
                "Manifest.destination_directory is not configured."
            )

        self.validate_destination(
            manifest.destination_directory,
        )

        return manifest.destination_directory / filename

    def remove_existing(
        self,
        path: Path,
        overwrite: bool,
    ) -> None:
        """
        Removes an existing file if overwrite is enabled.
        """
        if not path.exists():
            return

        if not overwrite:
            raise FileExistsError(path)

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    def finalize_result(
        self,
        result: AcquisitionResult,
    ) -> AcquisitionResult:
        """
        Marks the acquisition result as complete.
        """
        result.finalize()
        return result

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
