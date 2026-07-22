
from __future__ import annotations

"""
SanskritAI
==========

Internet Archive Provider

Acquisition provider for Internet Archive resources.

The InternetArchiveProvider is responsible for orchestrating the
acquisition of Sanskrit resources hosted on archive.org while
delegating all repository-specific communication to an
InternetArchiveRepositoryClient.

Typical Resources
-----------------
* Scanned Sanskrit books
* OCR text files
* PDF editions
* DjVu files
* JP2 image collections
* MARC/XML metadata
* EPUB editions

Responsibilities
----------------
* Resource discovery
* Download orchestration
* AcquisitionResult creation
* Provider health reporting

The provider intentionally does NOT perform

    * OCR
    * Metadata extraction
    * Normalization
    * Importing
    * PDF parsing

Those belong to later stages of the SanskritAI pipeline.

Version
-------
v0.7.0
"""

from pathlib import Path
from typing import Iterable

from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)
from SanskritAI.acquisition.providers.acquisition_request import (
    AcquisitionRequest,
)
from SanskritAI.acquisition.providers.acquisition_response import (
    AcquisitionResponse,
)
from SanskritAI.acquisition.repositories.base_repository_client import (
    BaseRepositoryClient,
)


class InternetArchiveProvider(BaseProvider):
    """
    Acquisition provider for Internet Archive.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        repository: BaseRepositoryClient,
    ) -> None:

        super().__init__(repository)

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:

        return "internet_archive"

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:

        return "Internet Archive Provider"

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(
        self,
        request: AcquisitionRequest,
    ) -> Iterable:
        """
        Discover archive resources.
        """

        return self.repository.discover(
            request
        )

    # ---------------------------------------------------------
    # Acquisition
    # ---------------------------------------------------------

    def acquire(
        self,
        request: AcquisitionRequest,
    ) -> AcquisitionResponse:
        """
        Acquire resources from Internet Archive.
        """

        response = AcquisitionResponse(
            provider_name=self.display_name,
        )

        resources = self.discover(
            request
        )

        for resource in resources:

            try:

                destination = self.repository.download(
                    resource,
                    destination=request.destination,
                )

                response.add_download(
                    Path(destination)
                )

            except Exception as exc:

                response.error(
                    str(exc)
                )

        response.finish()

        return response

    # ---------------------------------------------------------
    # Supported Formats
    # ---------------------------------------------------------

    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """
        Common file formats available
        from Internet Archive.
        """

        return (

            ".pdf",

            ".djvu",

            ".txt",

            ".xml",

            ".tei",

            ".tei.xml",

            ".epub",

            ".zip",

            ".gz",

            ".jpg",

            ".jpeg",

            ".jp2",

            ".png",

            ".tif",

            ".tiff",

            ".json",

            ".csv",

        )

    # ---------------------------------------------------------

    def supports_extension(
        self,
        extension: str,
    ) -> bool:

        return (

            extension.lower()

            in self.supported_extensions()

        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict:

        return {

            "identifier":
                self.identifier,

            "display_name":
                self.display_name,

            "repository":
                self.repository.identifier,

            "supports_discovery":
                True,

            "supports_download":
                True,

            "supports_metadata":
                True,

            "supports_scanned_books":
                True,

            "supports_ocr_text":
                True,

            "supports_images":
                True,

            "source":
                "Internet Archive",

        }

    # ---------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Verify repository availability.
        """

        try:

            return self.repository.ping()

        except Exception:

            return False

    # ---------------------------------------------------------

    def preferred_formats(
        self,
    ) -> tuple[str, ...]:
        """
        SanskritAI preference order when
        multiple downloadable formats exist.
        """

        return (

            ".txt",

            ".tei.xml",

            ".tei",

            ".xml",

            ".pdf",

            ".epub",

            ".djvu",

            ".jp2",

        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"repository={self.repository.identifier!r})"

        )
